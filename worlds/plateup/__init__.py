import logging
import math
from collections import Counter

from BaseClasses import ItemClassification, CollectionState
from worlds.AutoWorld import World
from .Items import ITEMS, PlateUpItem
from .Locations import DISH_LOCATIONS, FRANCHISE_LOCATION_DICT, DAY_LOCATION_DICT, EXCLUDED_LOCATIONS
from .Options import PlateUpOptions, Goal
from .Rules import (
    filter_selected_dishes,
    apply_rules,
    restrict_locations_by_progression
)


class PlateUpWorld(World):
    game = "plateup"
    options_dataclass = PlateUpOptions
    options: PlateUpOptions

    # Pre-calculate mappings for items and locations.
    item_name_to_id = {name: data[0] for name, data in ITEMS.items()}
    location_name_to_id = {**FRANCHISE_LOCATION_DICT, **DAY_LOCATION_DICT, **DISH_LOCATIONS}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.excluded_locations = set()

    def generate_location_table(self):
        """Return a planned location table based on the goal and options."""
        goal = self.options.goal.value
        if goal == 0:
            # Franchise goal: include only franchise locations up to the required count.
            required = self.options.franchise_count.value
            max_franchise_id = (required + 1) * 100000
            locs = {
                name: loc
                for name, loc in FRANCHISE_LOCATION_DICT.items()
                if loc < max_franchise_id or name == f"Franchise {required} times"
            }
            return locs
        else:
            required_days = self.options.day_count.value
            max_stars = math.ceil(required_days / 3)
            locs = {}
            for name, loc in DAY_LOCATION_DICT.items():
                if name.startswith("Complete Day "):
                    day = int(name.removeprefix("Complete Day ").strip())
                    if day <= required_days:
                        locs[name] = loc
                elif name.startswith("Complete Star "):
                    star = int(name.removeprefix("Complete Star ").strip())
                    if star <= max_stars:
                        locs[name] = loc
            locs.update(DISH_LOCATIONS)
            return locs

    def validate_ids(self):
        """Ensure that item and location IDs are unique."""
        item_ids = list(self.item_name_to_id.values())
        dupe_items = [item for item, count in Counter(item_ids).items() if count > 1]
        if dupe_items:
            raise Exception(f"Duplicate item IDs found: {dupe_items}")

        loc_ids = list(self.location_name_to_id.values())
        dupe_locs = [loc for loc, count in Counter(loc_ids).items() if count > 1]
        if dupe_locs:
            raise Exception(f"Duplicate location IDs found: {dupe_locs}")

    def create_regions(self):
        """Create regions using the planned location table."""
        from .Regions import create_plateup_regions
        self._location_name_to_id = self.generate_location_table()
        self.validate_ids()
        create_plateup_regions(self)

    def create_item(self, name: str, classification: ItemClassification = ItemClassification.filler) -> PlateUpItem:
        """Create a PlateUp item from the given name."""
        if name in self.item_name_to_id:
            item_id = self.item_name_to_id[name]
        else:
            raise ValueError(f"Item '{name}' not found in ITEMS")
        return PlateUpItem(name, classification, item_id, self.player)

    def create_items(self):
        """Create the initial item pool based on the planned location table."""

        total_locations = len(self.generate_location_table())
        item_pool = []

        # Add progression items.
        item_pool.extend([
            self.create_item("Speed Upgrade Player", classification=ItemClassification.progression)
            for _ in range(5)
        ])

        speed_mode = self.options.appliance_speed_mode.value
        if speed_mode == 0:
            item_pool.extend([
                self.create_item("Speed Upgrade Appliance", classification=ItemClassification.progression)
                for _ in range(5)
            ])
        else:
            for _ in range(5):
                item_pool.extend([
                    self.create_item("Speed Upgrade Cook", classification=ItemClassification.progression),
                    self.create_item("Speed Upgrade Clean", classification=ItemClassification.progression),
                    self.create_item("Speed Upgrade Chop", classification=ItemClassification.progression)
                ])

        if self.options.goal.value == Goal.option_franchise_x_times:
            total_days = 15 * self.options.franchise_count.value
        else:
            total_days = self.options.day_count.value
        lease_count = math.ceil(total_days / 3)
        item_pool.extend([
            self.create_item("Day Lease", classification=ItemClassification.progression)
            for _ in range(lease_count)
        ])

        item_pool.extend([
            self.create_item("Random Customer Card", classification=ItemClassification.trap)
            for _ in range(3)
        ])

        while len(item_pool) < total_locations:
            filler_name = self.get_filler_item_name()
            item_pool.append(self.create_item(filler_name))

        logging.debug(f"[Player {self.multiworld.player_name[self.player]}] Total item pool count: {len(item_pool)}")
        logging.debug(f"[Player {self.multiworld.player_name[self.player]}] Total locations: {total_locations}")
        self.multiworld.itempool.extend(item_pool)

    def set_rules(self):
        """Set progression rules and top-up the item pool based on final locations."""

        filter_selected_dishes(self)
        restrict_locations_by_progression(self)

        from .Locations import DISH_LOCATIONS, PlateUpLocation
        dish_region = next(
            (r for r in self.multiworld.regions if r.name == "Dish Checks" and r.player == self.player),
            None
        )
        if dish_region:
            for loc_name in self.valid_dish_locations:
                if not any(loc.name == loc_name for loc in dish_region.locations):
                    loc_id = DISH_LOCATIONS.get(loc_name)
                    if loc_id:
                        loc = PlateUpLocation(self.player, loc_name, loc_id, parent=dish_region)
                        dish_region.locations.append(loc)

        if self.options.goal.value == Goal.option_franchise_x_times:
            required = self.options.franchise_count.value
            for i in range(required + 1, 11):
                name = f"Franchise {i} times"
                if name in FRANCHISE_LOCATION_DICT:
                    EXCLUDED_LOCATIONS.add(FRANCHISE_LOCATION_DICT[name])

        def plateup_completion(state: CollectionState):
            if self.options.goal.value == Goal.option_franchise_x_times:
                count = self.options.franchise_count.value
                loc_name = f"Franchise {count} times"
            else:
                count = self.options.day_count.value
                loc_name = f"Complete Day {count}"
            return state.can_reach(loc_name, "Location", self.player)

        self.multiworld.completion_condition[self.player] = plateup_completion
        apply_rules(self)

        final_locations = [loc for loc in self.multiworld.get_locations() if loc.player == self.player]
        current_items = [item for item in self.multiworld.itempool if item.player == self.player]
        missing = len(final_locations) - len(current_items)
        if missing > 0:
            logging.debug(f"[Player {self.multiworld.player_name[self.player]}] Item pool is short by {missing} items. Adding filler items.")
            for _ in range(missing):
                filler_name = self.get_filler_item_name()
                self.multiworld.itempool.append(self.create_item(filler_name))

    def fill_slot_data(self):
        """Return slot data for this player."""
        options_dict = self.options.as_dict(
            "goal",
            "franchise_count",
            "day_count",
            "death_link",
            "death_link_behavior",
            "appliance_speed_mode"
        )
        options_dict["items_kept"] = self.options.appliances_kept.value
        options_dict["selected_dishes"] = self.selected_dishes
        return options_dict

    def get_filler_item_name(self):
        """Randomly select a filler item from the available candidates."""
        filler_candidates = [
            name for name, (code, classification) in ITEMS.items()
            if classification == ItemClassification.filler
        ]
        if not filler_candidates:
            raise Exception("No filler items available in ITEMS.")
        return self.random.choice(filler_candidates)