import typing

from .ast import AstGenerator
from .lists import ListInfo
from .parse import JsonParser
from .context import Context
from .util import BASE_ID, RESERVED_ITEM_IDS

from ..types.items import ItemData, SingleItemData
from ..types.locations import LocationData
from ..types.regions import RegionsData
from ..types.world import WorldData

class WorldBuilder:
    ctx: Context
    ast_generator: AstGenerator
    json_parser: JsonParser
    current_location_code: int = BASE_ID

    region_packs: dict[str, RegionsData]

    num_needed_items: dict[str,int]

    def __init__(self, ctx: Context, lists: ListInfo):
        self.ctx = ctx

        self.ast_generator = AstGenerator()
        self.json_parser = JsonParser(self.ctx)

        self.region_packs = {}

        self.num_needed_items = {}

    def __add_location(self, name: str, raw_loc: dict[str, typing.Any], create_event=False):
        num_rewards = 1
        if "reward" in raw_loc:
            if len(raw_loc["reward"]) == 0:
                raise RuntimeError(f"Error while adding location {name}: need one or more rewards (get rid of the entry if there are no rewards)")
            num_rewards = len(raw_loc["reward"])
        
        location_names: list[str] = []

        for idx in range(num_rewards):
            full_name = name
            if num_rewards > 1:
                full_name = full_name + f" - Reward {idx + 1}"

            location_names.append(full_name)

            loc = self.json_parser.parse_location(full_name, raw_loc, self.current_location_code)
            self.current_location_code += 1

            self.locations_dict.append(loc)

        if num_rewards > 1 or create_event:
            prev_loc = self.locations_dict[-1]
            event = LocationData(
                name=f"{name} (Event)",
                code=None,
                region=prev_loc.region,
                cond=prev_loc.cond)
            self.events_dict.append(event)

        if "reward" not in raw_loc or len(raw_loc["reward"]) == 0:
            for mode in raw_loc["region"].keys():
                if not mode in self.num_needed_items:
                    self.num_needed_items[mode] = 1
                else:
                    self.num_needed_items[mode] += 1
            return

        for reward in raw_loc["reward"]:
            item = self.json_parser.parse_reward(reward) 
            key = (item.name, item.amount)
            if key in self.items_dict:
                item = self.items_dict[key]
            else:
                self.items_dict[key] = item

            for mode in raw_loc["region"].keys():
                if not mode in item.quantity:
                    item.quantity[mode] = 1
                else:
                    item.quantity[mode] += 1

    def __add_location_list(self, loc_list: dict[str, dict[str, typing.Any]], create_events=False):
        for name, raw_loc in loc_list.items():
            self.__add_location(name, raw_loc, create_events)

    def build(self) -> WorldData:
        self.__add_location_list(self.ctx.rando_data["chests"])
        self.__add_location_list(self.ctx.rando_data["cutscenes"])
        self.__add_location_list(self.ctx.rando_data["elements"])
        self.__add_location_list(self.ctx.rando_data["quests"], True)

        self.region_packs = self.json_parser.parse_regions_data_list(self.ctx.rando_data["regions"])

        return WorldData(
            region_packs=self.region_packs,
            locations_data=self.locations_dict,
            events_data=self.events_dict,
            num_needed_items=self.num_needed_items,
            items_dict=self.items_dict,
        )
