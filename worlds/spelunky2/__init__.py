from typing import List, Mapping, Any, Dict

from worlds.AutoWorld import World, WebWorld
from BaseClasses import MultiWorld, Tutorial, ItemClassification, Region

from .Items import Spelunky2Item, item_data_table, filler_items, traps, filler_weights, trap_weights
from .Locations import Spelunky2Location, location_data_table
from .Options import Spelunky2Options
from .Regions import region_data_table
from .Rules import set_common_rules, set_sunken_city_rules, set_cosmic_ocean_rules


class Spelunky2WebWorld(WebWorld):
    theme = "stone"

    setup_en = Tutorial(
        tutorial_name="Setup Guide",
        description="A guide to setting up Spelunky 2",
        language="English",
        file_name="setup_en.md",
        link="setup/en",
        authors=["Eszenn"]
    )
    tutorials = [setup_en]


class Spelunky2World(World):
    """Spelunky 2 is an extremely difficult roguelike 2D platformer. BETTER SUMMARY GOES HERE"""

    game = "Spelunky 2"
    web = Spelunky2WebWorld()
    options = Spelunky2Options
    options_dataclass = Spelunky2Options
    filler_count = 0
    trap_count = 0
    filler_weights = filler_weights

    item_name_to_id = {name: data.code for name, data in item_data_table.items()}
    location_name_to_id = {name: data.address for name, data in location_data_table.items()}

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.trap_weights = trap_weights

    def generate_early(self) -> None:
        pass

    def create_regions(self) -> None:
        exclude_regions = []

        if self.options.goal == 0:
            exclude_regions.append("Sunken City")

        if self.options.goal != 2:
            exclude_regions.append("Cosmic Ocean")

        for region_name in region_data_table.keys():
            if region_name in exclude_regions:
                continue

            region = Region(region_name, self.player, self.multiworld)
            self.multiworld.regions.append(region)

        for region_name, region_data in region_data_table.items():
            if region_name in exclude_regions:
                continue

            region = self.get_region(region_name)
            if region_data.exits is not None:
                for region_exit in region_data.exits:
                    if region_exit in exclude_regions:
                        continue
                    connecting_region = self.get_region(region_exit)
                    region.connect(connecting_region)

            region.add_locations({location_name: self.location_name_to_id[location_name]
                                  for location_name, location_data in location_data_table.items()
                                  if location_data.region == region_name}, Spelunky2Location)

        if self.options.goal == 1:
            goal_region = self.get_region("Sunken City")
        elif self.options.goal == 2:
            goal_region = self.get_region("Cosmic Ocean")
        else:
            goal_region = self.get_region("Neo Babylon")

        goal_location = Spelunky2Location(self.player, "Victory", None, goal_region)
        goal_location.place_locked_item(Spelunky2Item("Victory", ItemClassification.progression, None, self.player))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)
        goal_region.locations.append(goal_location)

        self.filler_count = len(self.multiworld.get_unfilled_locations(self.player))

    def create_item(self, name: str) -> "Spelunky2Item":
        classification = item_data_table[name].classification
        return Spelunky2Item(name, classification, self.item_name_to_id[name], self.player)

    def create_items(self) -> None:
        exclude_items = ["Cosmic Ocean Checkpoint"]

        for key, _ in filler_items.items():
            exclude_items.append(key)

        for key, _ in traps.items():
            exclude_items.append(key)

        spelunky2_item_pool = []

        if self.options.goal == 0:
            exclude_items.append("Arrow of Light")

        if self.options.goal == 2:
            for i in range(int(self.options.goal_level / 10)):
                item = self.create_item("Cosmic Ocean Checkpoint")
                spelunky2_item_pool.append(item)
        else:
            if not self.options.progressive_worlds:
                exclude_items.append("Cosmic Ocean")

        if self.options.progressive_worlds:
            exclude_items.extend(["Jungle", "Volcana", "Olmec's Lair",
                                  "Tide Pool", "Temple", "Ice Caves",
                                  "Neo Babylon", "Sunken City", "Cosmic Ocean"])
        else:
            exclude_items.append("Progressive World Unlock")

        """
        # Shortcuts not implemented yet
        if self.options.progressive_shortcuts:
            exclude_items.extend(["Dwelling Shortcut", "Olmec's Lair Shortcut", "Ice Caves Shortcut"])

        else:
            exclude_items.append("Progressive Shortcut")
        """

        for name, data in item_data_table.items():
            if name not in exclude_items:
                for i in range(data.amount):
                    item = self.create_item(name)
                    spelunky2_item_pool.append(item)
                    self.filler_count -= 1

        if self.options.traps_enabled:
            self.trap_count = int(self.filler_count * (self.options.trap_weight / 100))
            self.filler_count -= self.trap_count

            self.trap_weights["Poison Trap"] = self.options.poison_weight
            self.trap_weights["Curse Trap"] = self.options.curse_weight
            self.trap_weights["Ghost Trap"] = self.options.ghost_weight
            self.trap_weights["Stun Trap"] = self.options.stun_weight
            self.trap_weights["Loose Bombs Trap"] = self.options.bomb_weight
            self.trap_weights["Blindness Trap"] = self.options.blind_weight
            self.trap_weights["Punish Ball Trap"] = self.options.punish_weight

            for i in range(self.trap_count):
                trap = self.create_trap()
                spelunky2_item_pool.append(trap)

        for i in range(self.filler_count):
            filler = self.create_filler()
            spelunky2_item_pool.append(filler)

        self.multiworld.itempool.extend(spelunky2_item_pool)

    def create_filler(self) -> "Spelunky2Item":
        return self.create_item(self.random.choices(list(filler_items.keys()), list(filler_weights.values()))[0])

    def create_trap(self) -> "Spelunky2Item":
        return self.create_item(self.random.choices(list(traps.keys()), list(trap_weights.values()))[0])

    def set_rules(self) -> None:
        set_common_rules(self, self.player)

        if self.options.goal != 0:
            set_sunken_city_rules(self, self.player)

        if self.options.goal == 2:
            set_cosmic_ocean_rules(self, self.player)

    def fill_slot_data(self) -> Mapping[str, Any]:
        slot_data = {
            "goal": self.options.goal.value,
            "progressive_worlds": bool(self.options.progressive_worlds.value),
            "starting_health": self.options.starting_health.value,
            "starting_bombs": self.options.starting_bombs.value,
            "starting_ropes": self.options.starting_ropes.value
        }

        if self.options.goal == 2:
            slot_data["goal_level"] = self.options.goal_level.value

        if self.options.death_link:
            slot_data["death_link"] = True
            slot_data["bypass_ankh"] = bool(self.options.bypass_ankh.value)

        return slot_data
