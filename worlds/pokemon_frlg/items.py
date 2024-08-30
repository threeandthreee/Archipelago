from typing import TYPE_CHECKING, Dict, FrozenSet, Optional
from BaseClasses import Item, ItemClassification
from .data import data, BASE_OFFSET

if TYPE_CHECKING:
    from . import PokemonFRLGWorld


ITEM_GROUPS = {
    "Badges": {
        "Boulder Badge",
        "Cascade Badge",
        "Thunder Badge",
        "Rainbow Badge",
        "Soul Badge",
        "Marsh Badge",
        "Volcano Badge",
        "Earth Badge"
    },
    "HMs": {
        "HM01 Cut",
        "HM02 Fly",
        "HM03 Surf",
        "HM04 Strength",
        "HM05 Flash",
        "HM06 Rock Smash",
        "HM07 Waterfall"
    },
    "HM01": {"HM01 Cut"},
    "HM02": {"HM02 Fly"},
    "HM03": {"HM03 Surf"},
    "HM04": {"HM04 Strength"},
    "HM05": {"HM05 Flash"},
    "HM06": {"HM06 Rock Smash"},
    "HM07": {"HM07 Waterfall"}
}


class PokemonFRLGItem(Item):
    game: str = "Pokemon FireRed and LeafGreen"
    tags: FrozenSet[str]

    def __init__(self, name: str, classification: ItemClassification, code: Optional[int], player: int) -> None:
        super().__init__(name, classification, code, player)

        if code is None:
            self.tags = frozenset(["Event"])
        else:
            self.tags = data.items[reverse_offset_item_value(code)].tags


def offset_item_value(item_value: int) -> int:
    return item_value + BASE_OFFSET


def reverse_offset_item_value(item_id: int) -> int:
    return item_id - BASE_OFFSET


def create_item_name_to_id_map() -> Dict[str, int]:
    """
    Creates a map from item names to their AP item ID (code)
    """
    name_to_id_map: Dict[str, int] = {}
    for item_value, attributes in data.items.items():
        name_to_id_map[attributes.name] = offset_item_value(item_value)

    return name_to_id_map


def get_item_classification(item_id: int) -> ItemClassification:
    """
    Returns the item classification for a given AP item id (code)
    """
    return data.items[reverse_offset_item_value(item_id)].classification


def get_random_item(world: "PokemonFRLGWorld", item_classification: ItemClassification = None) -> str:
    if item_classification is None:
        item_classification = ItemClassification.useful if world.random.random() < 0.20 else ItemClassification.filler
    items = [item for item in data.items.values()
             if item.classification == item_classification and "Unique" not in item.tags]
    return world.random.choice(items).name
