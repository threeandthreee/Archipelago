import string
import typing

from BaseClasses import ItemClassification

from .context import Context
from .util import BASE_ID, RESERVED_ITEM_IDS, SP_UPGRADE_ID_OFFSET, SP_UPGRADE_NAME, get_item_classification

from ..types.items import ItemData, SingleItemData
from ..types.locations import AccessInfo, Condition
from ..types.regions import RegionConnection, RegionsData
from ..types.condition import ItemCondition, LocationCondition, QuestCondition, RegionCondition, AnyElementCondition, OrCondition, VariableCondition

class JsonParserError(Exception):
    subject: typing.Any
    problem_item: typing.Any
    message: str

    def __init__(self, subject: typing.Any, problem_item: typing.Any, kind: str, message: str):
        self.subject = subject
        self.problem_item = problem_item
        self.message = f"Error parsing {kind}: {message}"
        super().__init__(subject, problem_item, message)

class JsonParser:
    ctx: Context

    single_items_dict: dict[str, SingleItemData]
    items_dict: dict[tuple[str, int], ItemData]

    def __init__(self, ctx: Context):
        self.ctx = ctx
        self.single_items_dict = {}
        self.items_dict = {}

    def parse_condition(self, raw: list[typing.Any]) -> list[Condition]:
        result: list[Condition] = []

        for cond in raw:
            if not isinstance(cond, list):
                raise JsonParserError(raw, cond, "condition", "condition not a list")

            num_args = len(cond) - 1
            if cond[0] == "item":
                if num_args == 1:
                    result.append(ItemCondition(cond[1]))
                elif num_args == 2:
                    result.append(ItemCondition(cond[1], cond[2]))
                else:
                    raise JsonParserError(
                        raw,
                        cond,
                        "item condition",
                        f"expected 1 or 2 argument, not {num_args}"
                    )

            elif cond[0] == "quest":
                if num_args == 1:
                    result.append(QuestCondition(cond[1]))
                else:
                    raise JsonParserError(
                        raw,
                        cond,
                        "quest condition",
                        f"expected 1 argument, not {num_args}"
                    )

            elif cond[0] in ["cutscene", "location"]:
                if num_args == 1:
                    result.append(LocationCondition(cond[1]))
                else:
                    raise JsonParserError(
                        raw,
                        cond,
                        "location condition",
                        f"expected 1 argument, not {num_args}"
                    )

            elif cond[0] == "region":
                if num_args == 2:
                    mode, region = cond[1:]
                    result.append(RegionCondition(mode, region))
                else:
                    raise JsonParserError(
                        raw,
                        cond,
                        "region condition",
                        f"expected 2 arguments, not {num_args}"
                    )
            
            elif cond[0] == "any_element":
                result.append(AnyElementCondition())

            elif cond[0] in ("any", "or"):
                result.append(OrCondition(self.parse_condition(cond[1:])))

            elif cond[0] == "var":
                if num_args == 1:
                    result.append(VariableCondition(cond[1]))
                else:
                    raise JsonParserError(
                        raw,
                        cond,
                        "location condition",
                        f"expected 1 argument, not {num_args}"
                    )

            else:
                raise JsonParserError(raw, cond, "condition", f"unknown type {cond[0]}")

        # Return None if there are no conditions
        return result

    def parse_location_access_info(self, raw: dict[str, typing.Any]) -> AccessInfo:
        region = {}
        if "region" in raw:
            region = raw["region"]

            if not isinstance(region, dict):
                raise JsonParserError(raw, raw["region"], "location", "region must be a dict")

            for region_name in region.values():
                if not isinstance(region_name, str):
                    raise JsonParserError(raw, region_name, "location", "region name must be a string")

        clearance = "Default"
        if "clearance" in raw:
            clearance = raw["clearance"]
            if not isinstance(clearance, str):
                raise JsonParserError(raw, clearance, "location", "clearance must be a string")

        condition = None
        if "condition" in raw:
            condition = self.parse_condition(raw["condition"])

        return AccessInfo(region, condition, clearance)

    def parse_item_data(self, name: str, raw: dict[str, typing.Any]) -> SingleItemData:
        item_id = raw["id"]

        db_entry = self.ctx.item_data[item_id]

        cls = get_item_classification(db_entry)

        if "classification" in raw:
            cls_str = raw["classification"]
            if not hasattr(ItemClassification, cls_str):
                raise JsonParserError(raw, cls_str, "item reward", "invalid classification")
            cls = getattr(ItemClassification, cls_str)

        return SingleItemData(
            name=name,
            item_id=raw["id"],
            classification=cls,
        )

    def parse_item_reward(self, raw: list[typing.Any]) -> ItemData:
        if len(raw) == 1:
            name = raw[0]
            amount = 1
        elif len(raw) == 2:
            name = raw[0]
            amount = raw[1]
        else:
            raise JsonParserError(raw, raw, "item reward", "expected one or two elements")

        try:
            return self.items_dict[name, amount]
        except KeyError:
            pass

        try:
            single_item = self.single_items_dict[name]
        except KeyError:
            if name not in self.ctx.rando_data["items"]:
                raise JsonParserError(raw, name, "item reward", "item does not exist in randomizer data")
            item_overrides = self.ctx.rando_data["items"][name]

            single_item = self.parse_item_data(name, item_overrides)
            self.single_items_dict[name] = single_item

        combo_id = BASE_ID + RESERVED_ITEM_IDS + \
            self.ctx.num_items * (amount - 1) + single_item.item_id

        return ItemData(
            item=single_item,
            amount=amount,
            combo_id=combo_id,
        )

    def parse_element_reward(self, raw: list[typing.Any]) -> ItemData:
        combo_id = BASE_ID

        if len(raw) == 1:
            el = raw[0]
        else:
            raise JsonParserError(raw, raw, "element reward", "expected one string")

        try:
            return self.items_dict[el, 1]
        except KeyError:
            pass

        try:
            single_item = self.single_items_dict[el]
        except KeyError:
            single_item = SingleItemData(el, 0, ItemClassification.progression)
            self.single_items_dict[el] = single_item

        try:
            idx = ["Heat", "Cold", "Shock", "Wave"].index(el)
            combo_id += idx
        except:
            raise RuntimeError("Error adding element: {el} not an element")

        item = ItemData(
            item=single_item,
            amount=1,
            combo_id=combo_id
        )

        self.items_dict[el, 1] = item
        return item

    def parse_sp_reward(self, raw: list[typing.Any]) -> ItemData:
        try:
            return self.items_dict[SP_UPGRADE_NAME, 1]
        except KeyError:
            pass

        try:
            single_item = self.single_items_dict[SP_UPGRADE_NAME]
        except KeyError:
            single_item = SingleItemData(SP_UPGRADE_NAME, 0, ItemClassification.progression)
            self.single_items_dict[SP_UPGRADE_NAME] = single_item

        combo_id = BASE_ID + SP_UPGRADE_ID_OFFSET

        return ItemData(
            item=single_item,
            amount=1,
            combo_id=combo_id,
        )

    def parse_reward(self, raw: list[typing.Any]) -> ItemData:
        kind, *info = raw

        if kind == "item":
            return self.parse_item_reward(info)
        elif kind == "element":
            return self.parse_element_reward(info)
        elif kind == "sp":
            return self.parse_sp_reward(info)
        else:
            raise RuntimeError(f"Error parsing reward {raw}: unrecognized type")

    def parse_region_connection(self, raw: dict[str, typing.Any]) -> RegionConnection:
        if "from" not in raw:
            raise JsonParserError(raw, None, "connection", "region from not found")
        region_from = raw["from"]

        if not isinstance(region_from, str):
            raise JsonParserError(raw, region_from, "connection", "region must be str")

        if "to" not in raw:
            raise JsonParserError(raw, None, "connection", "region to not found")
        region_to = raw["to"]

        if not isinstance(region_to, str):
            raise JsonParserError(raw, region_to, "connection", "region must be str")

        condition = None
        if "condition" in raw:
            condition = self.parse_condition(raw["condition"])

        return RegionConnection(region_from, region_to, condition)

    def parse_regions_data(self, raw: dict[str, typing.Any]) -> RegionsData:
        if "start" not in raw:
            raise JsonParserError(raw, None, "regions data", "must have starting region")
        start = raw["start"]

        if not isinstance(start, str):
            raise JsonParserError(raw, start, "regions data", "starting region must be a string")

        if "goal" not in raw:
            raise JsonParserError(raw, None, "regions data", "must have goal region")
        goal = raw["goal"]

        if not isinstance(goal, str):
            raise JsonParserError(raw, goal, "regions data", "goal region must be a string")

        exclude = []
        if "exclude" in raw:
            exclude = raw["exclude"]
            if not isinstance(exclude, list) or not all([isinstance(region, str) for region in exclude]):
                raise JsonParserError(raw, exclude, "regions data", "excluded regions must be strings")

        if "connections" not in raw:
            raise JsonParserError(raw, None, "regions data", "no connections found")
        raw_connections = raw["connections"]

        if not isinstance(raw_connections, list):
            raise JsonParserError(raw, raw_connections, "regions data", "connection must be list")

        regions_seen: set[str] = set()

        connections = []

        for raw_conn in raw_connections:
            conn = self.parse_region_connection(raw_conn)
            regions_seen.add(conn.region_to)
            regions_seen.add(conn.region_from)

            connections.append(conn)

        region_list = list(regions_seen)

        region_list.sort(key=lambda x: float(x.strip(string.ascii_letters)))

        return RegionsData(start, goal, exclude, region_list, connections)

    def parse_regions_data_list(self, raw: dict[str, dict[str, typing.Any]]) -> dict[str, RegionsData]:
        return {name: self.parse_regions_data(data) for name, data in raw.items()}
