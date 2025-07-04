import typing
from collections import defaultdict
from enum import auto, Enum

from BaseClasses import ItemClassification
from typing import Dict

from worlds.spire.Characters import character_list, NUM_CUSTOM


CHAR_OFFSET = 20

class ItemType(Enum):
    DRAW = auto()
    RARE_DRAW = auto()
    RELIC = auto()
    BOSS_RELIC = auto()
    GOLD = auto()
    EVENT = auto()
    CAMPFIRE = auto()
    SHOP_CARD = auto()
    SHOP_NEUTRAL = auto()
    SHOP_RELIC = auto()
    SHOP_POTION = auto()
    SHOP_REMOVE = auto()
    CHAR_UNLOCK = auto()
    POTION = auto()


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    type: ItemType
    classification: ItemClassification = ItemClassification.progression
    event: bool = False
    is_victory: bool = False

    @staticmethod
    def increment(base: 'ItemData', char_offset: int) -> 'ItemData':
        newcode = base.code + char_offset if base.code is not None else base.code
        return ItemData(newcode, base.type, base.classification, base.event, base.is_victory)

base_item_table: Dict[str, ItemData] = {
    'Card Draw': ItemData(1, ItemType.DRAW),
    'Rare Card Draw': ItemData(2, ItemType.RARE_DRAW),
    'Relic': ItemData(3, ItemType.RELIC),
    'Boss Relic': ItemData(4, ItemType.BOSS_RELIC),
    'One Gold': ItemData(5, ItemType.GOLD, ItemClassification.filler),
    'Five Gold': ItemData(6, ItemType.GOLD, ItemClassification.filler),
    '15 Gold': ItemData(15, ItemType.GOLD, ItemClassification.useful),
    '30 Gold': ItemData(16, ItemType.GOLD),
    'Boss Gold': ItemData(17, ItemType.GOLD),
    'Progressive Rest': ItemData(7, ItemType.CAMPFIRE),
    'Progressive Smith': ItemData(8, ItemType.CAMPFIRE),
    'Shop Card Slot': ItemData(9, ItemType.SHOP_CARD),
    'Neutral Shop Card Slot': ItemData(10, ItemType.SHOP_NEUTRAL),
    'Shop Relic Slot': ItemData(11, ItemType.SHOP_RELIC),
    'Shop Potion Slot': ItemData(12, ItemType.SHOP_POTION),
    'Progressive Shop Remove': ItemData(13, ItemType.SHOP_REMOVE),
    'Unlock': ItemData(14, ItemType.CHAR_UNLOCK),
    'Potion': ItemData(18, ItemType.POTION, ItemClassification.useful),

    # Event Items
    'Victory': ItemData(None, None, ItemClassification.progression, True, True),
    'Beat Act 1 Boss': ItemData(None, None, ItemClassification.progression, True),
    'Beat Act 2 Boss': ItemData(None, None, ItemClassification.progression, True),
    'Beat Act 3 Boss': ItemData(None, None, ItemClassification.progression, True),

}

base_event_item_pairs: Dict[str, str] = {
    "Heart Room": "Victory",
    "Act 1 Boss": "Beat Act 1 Boss",
    "Act 2 Boss": "Beat Act 2 Boss",
    "Act 3 Boss": "Beat Act 3 Boss"
}

def create_item_tables(vanilla_chars: typing.List[str], extras: int) -> typing.Tuple[dict[str, ItemData], dict[
    typing.Union[str, int],dict[str,ItemData]], dict[str,str]]:
    item_name_to_data = dict()
    characters_to_items: dict[typing.Union[str, int],dict[str, ItemData]] = defaultdict(lambda: dict())
    event_item_pairs: dict[str, str] = dict()
    char_num = 0

    for char in vanilla_chars:
        for key, data in base_item_table.items():
            newkey = f"{char} {key}"
            newval = ItemData.increment(data, char_num*CHAR_OFFSET)
            item_name_to_data[newkey] = newval
            characters_to_items[char][newkey] = newval
        for key, val in base_event_item_pairs.items():
            event_item_pairs[f"{char} {key}"] = f"{char} {val}"
        char_num += 1

    for i in range(extras):
        for key, data in base_item_table.items():
            newkey = f"Custom Character {i+1} {key}"
            newval = ItemData.increment(data, char_num * CHAR_OFFSET)
            item_name_to_data[newkey] = newval
            characters_to_items[i+1][newkey] = newval
        for key, val in base_event_item_pairs.items():
            event_item_pairs[f"Custom Character {i+1} {key}"] = f"Custom Character {i+1} {val}"
        char_num += 1


    return item_name_to_data, characters_to_items, event_item_pairs

def create_item_groups(chars_to_items: dict[typing.Union[str,int], dict[str, ItemData]]) -> dict[str, typing.Set[str]]:
    gold = set()
    campfire = set()
    shop = set()
    unlock = set()
    potion = set()
    junk = set()
    ret = dict()

    ret["Gold"] =  gold
    ret["Campfire"] = campfire
    ret["Shop"] = shop
    ret["Unlock"] = unlock
    ret["Junk"] = junk
    ret["Potion"] = potion

    for key, data in chars_to_items.items():
        char = key if type(key) == str else f"Custom Character {key+1}"
        char_gold = set()
        char_campfire = set()
        char_shop = set()

        ret[f"{char} Gold"] = char_gold
        ret[f"{char} Campfire"] = char_campfire
        ret[f"{char} Shop"] = char_shop

        for item_name, item_data in data.items():
            if item_data.code is None:
                continue
            if item_data.classification == 0:
                junk.add(item_name)
            if item_data.type == ItemType.GOLD:
                char_gold.add(item_name)
                gold.add(item_name)
            elif item_data.type == ItemType.CAMPFIRE:
                char_campfire.add(item_name)
                campfire.add(item_name)
            elif item_data.type in [ItemType.SHOP_RELIC, ItemType.SHOP_REMOVE, ItemType.SHOP_POTION, ItemType.SHOP_NEUTRAL, ItemType.SHOP_CARD]:
                char_shop.add(item_name)
                shop.add(item_name)
            elif item_data.type == ItemType.CHAR_UNLOCK:
                unlock.add(item_name)
            elif item_data.type == ItemType.POTION:
                potion.add(item_name)

    return ret

item_table, chars_to_items, event_item_pairs = create_item_tables(character_list, NUM_CUSTOM)

item_groups = create_item_groups(chars_to_items)