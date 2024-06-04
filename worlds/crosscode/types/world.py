from dataclasses import dataclass, field
import typing

from .items import ItemData, ProgressiveItemChain, SingleItemData, ItemPoolEntry
from .locations import AccessInfo, LocationData
from .regions import RegionsData
from .condition import Condition

@dataclass
class WorldData:
    # regions.py
    region_packs: dict[str, RegionsData]
    modes: list[str] = field(init=False)

    # locations.py
    locations_dict: dict[str, LocationData]
    events_dict: dict[str, LocationData]

    # items.py
    single_items_dict: dict[str, SingleItemData]
    items_dict: dict[tuple[str, int], ItemData]
    items_by_full_name: dict[str, ItemData]
    keyring_items: set[str]

    # item_pools.py
    item_pools_template: dict[str, list[ItemPoolEntry]]

    # prog_items.py
    progressive_chains: dict[str, ProgressiveItemChain]
    progressive_items: dict[str, ItemData]

    # vars.py
    variable_definitions: dict[str, dict[str, list[Condition]]]

    def __post_init__(self):
        self.modes = list(self.region_packs.keys())
