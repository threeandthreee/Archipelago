from worlds.AutoWorld import World
from BaseClasses import Region
from .items import PseudoregaliaItem, item_table, item_groups
from .locations import PseudoregaliaLocation, location_table
from .regions import region_table
from .options import PseudoregaliaOptions
from .rules_normal import PseudoregaliaNormalRules
from .rules_hard import PseudoregaliaHardRules
from .rules_expert import PseudoregaliaExpertRules
from .rules_lunatic import PseudoregaliaLunaticRules
from typing import Dict, Any
from .constants.difficulties import NORMAL, HARD, EXPERT, LUNATIC
from .constants.versions import FULL_GOLD


class PseudoregaliaWorld(World):
    game = "Pseudoregalia"
    required_client_version = (0, 7, 0)

    item_name_to_id = {name: data.code for name, data in item_table.items() if data.code is not None}
    location_name_to_id = {name: data.code for name, data in location_table.items() if data.code is not None}
    item_name_groups = item_groups

    options_dataclass = PseudoregaliaOptions
    options: PseudoregaliaOptions

    def get_filler_item_name(self) -> str:
        return "Health Piece"

    def create_item(self, name: str) -> PseudoregaliaItem:
        data = item_table[name]
        return PseudoregaliaItem(name, data.classification, data.code, self.player)

    def create_items(self):
        itempool = []
        for item_name, item_data in item_table.items():
            if not item_data.can_create(self.options) or not item_data.code:
                continue
            precollect = item_data.precollect(self.options)
            for _ in range(precollect):
                self.multiworld.push_precollected(self.create_item(item_name))
            itempool += [self.create_item(item_name) for _ in range(precollect, item_data.frequency)]
        total_locations = len(self.multiworld.get_unfilled_locations(self.player))
        itempool += [self.create_filler() for _ in range(total_locations - len(itempool))]
        self.multiworld.itempool += itempool

    def generate_early(self):
        if self.options.logic_level in (EXPERT, LUNATIC):
            # obscure is forced on for expert/lunatic difficulties
            self.options.obscure_logic.value = 1
        if self.options.game_version == FULL_GOLD:
            # zero out options that don't do anything on full gold
            self.options.start_with_map.value = 0
            self.options.randomize_time_trials.value = 0

    def create_regions(self):
        for region_name in region_table.keys():
            self.multiworld.regions.append(Region(region_name, self.player, self.multiworld))

        for loc_name, loc_data in location_table.items():
            if not loc_data.can_create(self.options):
                continue
            region = self.multiworld.get_region(loc_data.region, self.player)
            new_loc = PseudoregaliaLocation(self.player, loc_name, loc_data.code, region)
            region.locations.append(new_loc)
            if loc_data.locked_item:
                new_loc.place_locked_item(self.create_item(loc_data.locked_item))

        for region_name, exit_list in region_table.items():
            region = self.multiworld.get_region(region_name, self.player)
            region.add_exits(exit_list)

    def fill_slot_data(self) -> Dict[str, Any]:
        return {
            "game_version": self.options.game_version.value,
            "logic_level": self.options.logic_level.value,
            "obscure_logic": bool(self.options.obscure_logic),
            "progressive_breaker": bool(self.options.progressive_breaker),
            "progressive_slide": bool(self.options.progressive_slide),
            "split_sun_greaves": bool(self.options.split_sun_greaves),
            "randomize_time_trials": bool(self.options.randomize_time_trials),
        }

    def set_rules(self):
        difficulty = self.options.logic_level
        if difficulty == NORMAL:
            PseudoregaliaNormalRules(self).set_pseudoregalia_rules()
        elif difficulty == HARD:
            PseudoregaliaHardRules(self).set_pseudoregalia_rules()
        elif difficulty == EXPERT:
            PseudoregaliaExpertRules(self).set_pseudoregalia_rules()
        elif difficulty == LUNATIC:
            PseudoregaliaLunaticRules(self).set_pseudoregalia_rules()
