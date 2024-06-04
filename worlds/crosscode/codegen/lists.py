from collections import defaultdict
import typing

from .ast import AstGenerator
from .parse import JsonParser
from .context import Context
from .util import BASE_ID, RESERVED_ITEM_IDS

from ..types.items import ItemData, SingleItemData, ItemPoolEntry, ProgressiveItemChain
from ..types.locations import LocationData
from ..types.condition import Condition


class ListInfo:
    ctx: Context
    ast_generator: AstGenerator
    json_parser: JsonParser
    current_location_code: int

    locations_data: dict[str, LocationData]
    events_data: dict[str, LocationData]

    single_items_dict: dict[str, SingleItemData]
    items_dict: dict[tuple[str, int], ItemData]

    item_pools: dict[str, list[ItemPoolEntry]]

    reward_amounts: dict[str, int]

    variable_definitions: dict[str, dict[str, list[Condition]]]

    progressive_chains: dict[str, ProgressiveItemChain]
    progressive_items: dict[str, ItemData]

    def __init__(self, ctx: Context):
        self.ctx = ctx

        self.ast_generator = AstGenerator()
        self.json_parser = JsonParser(self.ctx)
        self.current_location_code = max(self.ctx.cached_location_ids.values(), default=BASE_ID)
        if self.current_location_code != BASE_ID:
            self.current_location_code += 1

        self.locations_data = {}
        self.events_data = {}

        self.single_items_dict = {}
        self.items_dict = {}

        self.item_pools = {}
        
        self.reward_amounts = {}

        self.ast_generator = AstGenerator()
        self.json_parser = JsonParser(self.ctx)
        self.json_parser.single_items_dict = self.single_items_dict
        self.json_parser.items_dict = self.items_dict

        self.progressive_chains = {}
        self.progressive_items = {}

        self.variable_definitions = defaultdict(dict)

    def build(self):
        self.__add_item_data_list(self.ctx.rando_data["items"])

        file = self.ctx.rando_data

        if "chests" in file: self.__add_location_list(file["chests"])
        if "cutscenes" in file: self.__add_location_list(file["cutscenes"])
        if "elements" in file: self.__add_location_list(file["elements"])
        if "quests" in file: self.__add_location_list(file["quests"], True)

        self.__add_item_pool_list(file["itemPools"])

        # Add any extra items (i.e. elements) that the JSON parser ran into
        self.single_items_dict.update(self.json_parser.single_items_dict)

        for name, data in self.single_items_dict.items():
            if (name, 1) in self.items_dict:
                continue

            self.items_dict[name, 1] = ItemData(data, 1, BASE_ID + RESERVED_ITEM_IDS + data.item_id)

        self.__add_progressive_chains(file["progressiveChains"])

        self.__add_vars(self.ctx.rando_data["vars"])

    def __get_cached_location_id(self, name: str) -> typing.Optional[int]:
        return self.ctx.cached_location_ids.get(name, None)

    def __add_location(self, name: str, raw_loc: dict[str, typing.Any], create_event=False):
        dbentry = self.ctx.database["quests"][raw_loc["questid"]] if "questid" in raw_loc else {}
        rewards = dbentry.get("rewards", {})
        item_rewards = rewards.get("items", [])
        num_rewards = max(1, len(item_rewards))

        found = False

        if name in self.reward_amounts:
            if num_rewards != self.reward_amounts[name]:
                found = True
                num_rewards = 0
                raise RuntimeError(f"Location of name '{name}' already exists with {self.reward_amounts[name]} rewards. Cannot add or overwrite with {num_rewards}.")

        try:
            area = raw_loc["location"]["map"].split('.')[0]
            if area not in self.ctx.rando_data["dungeons"]:
                area = None
        except KeyError or AttributeError:
            area = None

        location_names: list[str] = []

        metadata = raw_loc.get("metadata", None)

        access_info = self.json_parser.parse_location_access_info(raw_loc)

        for idx in range(num_rewards):
            full_name = name
            if num_rewards > 1:
                full_name = full_name + f" - Reward {idx + 1}"

            location_names.append(full_name)

            locid = self.__get_cached_location_id(full_name)

            if locid is None:
                locid = self.current_location_code
                self.current_location_code += 1

            loc = LocationData(
                name=full_name,
                code=locid,
                area=area,
                metadata=metadata,
                access=access_info
            )

            self.locations_data[full_name] = loc

        if not found and (num_rewards > 1 or create_event):
            event_name = f"{name} (Event)"
            event = LocationData(
                name=f"{name} (Event)",
                code=None,
                area=None,
                metadata=metadata,
                access=access_info,
            )
            self.events_data[event_name] = event

    def __add_location_list(self, loc_list: dict[str, dict[str, typing.Any]], create_events=False):
        for name, raw_loc in loc_list.items():
            self.__add_location(name, raw_loc, create_events)

    def __add_item_data(self, name: str, raw_item: dict[str, typing.Any]) -> tuple[SingleItemData, ItemData]:
        single_item, item  = self.json_parser.parse_item_data(name, raw_item)
        self.single_items_dict[name] = single_item
        self.items_dict[name, 1] = item
        return single_item, item

    def __add_item_data_list(self, item_list: dict[str, dict[str, typing.Any]]):
        for name, raw_item in item_list.items():
            self.__add_item_data(name, raw_item)

    def __add_item_pool(self, name: str, raw: list[dict[str, typing.Any]]):
        pool = []
        for data in raw:
            item = self.__add_reward(data["item"])
            pool.append(ItemPoolEntry(
                item=item,
                quantity=data.get("quantity", 1),
                metadata=data.get("metadata", None)
            ))

        self.item_pools[name] = pool

    def __add_item_pool_list(self, raw: dict[str, list[dict[str, typing.Any]]]):
        for name, pool in raw.items():
            self.__add_item_pool(name, pool)

    def __add_reward(self, reward: list) -> ItemData:
        item = self.json_parser.parse_reward(reward)
        key = (item.item.name, item.amount)
        if key in self.items_dict:
            item = self.items_dict[key]
        else:
            self.items_dict[key] = item
        return item

    def __add_progressive_chain(self, name: str, raw: dict[str, typing.Any]):
        chain = self.progressive_chains[name] = self.json_parser.parse_progressive_chain(name, raw)
        raw["reserved"] = True
        _, item = self.__add_item_data(f"Progressive {chain.display_name}", raw)
        self.progressive_items[name] = item

    def __add_progressive_chains(self, raw: dict[str, dict]):
        for name, chain in raw.items():
            self.__add_progressive_chain(name, chain)

    def __add_vars(self, variables: dict[str, dict[str, list[typing.Any]]]):
        for name, values in variables.items():
            for value, conds in values.items():
                self.variable_definitions[name][value] = self.json_parser.parse_condition(conds)
