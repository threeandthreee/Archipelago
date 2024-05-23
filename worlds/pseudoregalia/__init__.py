from worlds.AutoWorld import World
from BaseClasses import Region
from .items import PseudoregaliaItem, item_table, item_frequencies, item_groups
from .locations import PseudoregaliaLocation, location_table
from .regions import region_table
from .options import pseudoregalia_options
from .rules_normal import PseudoregaliaNormalRules
from .rules_hard import PseudoregaliaHardRules
from .rules_expert import PseudoregaliaExpertRules
from .rules_lunatic import PseudoregaliaLunaticRules
from typing import Dict, Any
from .constants.difficulties import NORMAL, HARD, EXPERT, LUNATIC


class PseudoregaliaWorld(World):
    game = "Pseudoregalia"
    required_client_version = (0, 7, 0)

    item_name_to_id = {name: data.code for name, data in item_table.items() if data.code is not None}
    location_name_to_id = {name: data.code for name, data in location_table.items() if data.code is not None}
    locked_locations = {name: data for name, data in location_table.items() if data.locked_item}
    item_name_groups = item_groups

    option_definitions = pseudoregalia_options

    def create_item(self, name: str) -> PseudoregaliaItem:
        data = item_table[name]
        return PseudoregaliaItem(name, data.classification, data.code, self.player)

    def create_items(self):
        for item_name, item_data in item_table.items():
            if (item_name == "Dream Breaker"):
                continue  # Really skrunkled way of just adding the one locked breaker to the pool for now.
            if (item_data.code and item_data.can_create(self.multiworld, self.player)):
                item_count = 1
                if (item_name in item_frequencies):
                    item_count = item_frequencies[item_name]
                for count in range(item_count):
                    self.multiworld.itempool.append(
                        PseudoregaliaItem(item_name, item_data.classification, item_data.code, self.player))

    def create_regions(self):
        for region_name in region_table.keys():
            self.multiworld.regions.append(Region(region_name, self.player, self.multiworld))

        for loc_name, loc_data in location_table.items():
            if not loc_data.can_create(self.multiworld, self.player):
                continue
            region = self.multiworld.get_region(loc_data.region, self.player)
            new_loc = PseudoregaliaLocation(self.player, loc_name, loc_data.code, region)
            if (not loc_data.show_in_spoiler):
                new_loc.show_in_spoiler = False
            region.locations.append(new_loc)

        for region_name, exit_list in region_table.items():
            region = self.multiworld.get_region(region_name, self.player)
            region.add_exits(exit_list)

        # Place locked locations.
        for location_name, location_data in self.locked_locations.items():
            if not location_data.can_create(self.multiworld, self.player):
                continue

            # Doing this really stupidly because breaker's locking will change after logic rework is done
            if location_name == "Dilapidated Dungeon - Dream Breaker":
                if bool(self.multiworld.progressive_breaker[self.player]):
                    locked_item = self.create_item("Progressive Dream Breaker")
                    self.multiworld.get_location(location_name, self.player).place_locked_item(locked_item)
                    continue

            locked_item = self.create_item(location_table[location_name].locked_item)
            self.multiworld.get_location(location_name, self.player).place_locked_item(locked_item)

    def fill_slot_data(self) -> Dict[str, Any]:
        return {"slot_number": self.player,
                "death_link": bool(self.multiworld.death_link[self.player]),
                "logic_level": self.multiworld.logic_level[self.player].value,
                "obscure_logic": bool(self.multiworld.obscure_logic[self.player]),
                "progressive_breaker": bool(self.multiworld.progressive_breaker[self.player]),
                "progressive_slide": bool(self.multiworld.progressive_slide[self.player]),
                "split_sun_greaves": bool(self.multiworld.split_sun_greaves[self.player]), }

    def set_rules(self):
        difficulty = self.multiworld.logic_level[self.player]
        if difficulty == NORMAL:
            PseudoregaliaNormalRules(self).set_pseudoregalia_rules()
        elif difficulty == HARD:
            PseudoregaliaHardRules(self).set_pseudoregalia_rules()
        elif difficulty == EXPERT:
            PseudoregaliaExpertRules(self).set_pseudoregalia_rules()
        elif difficulty == LUNATIC:
            PseudoregaliaLunaticRules(self).set_pseudoregalia_rules()
