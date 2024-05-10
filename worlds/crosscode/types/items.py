from ..codegen.util import BASE_ID, RESERVED_ITEM_IDS
from dataclasses import dataclass, field
import typing
from BaseClasses import Item, ItemClassification

@dataclass
class SingleItemData:
    name: str
    item_id: int
    classification: ItemClassification

@dataclass
class ItemData:
    item: SingleItemData
    amount: int
    combo_id: int
    name: str = field(init=False)

    def __post_init__(self):
        self.name = self.item.name if self.amount == 1 else f"{self.item.name} x{self.amount}"

class CrossCodeItem(Item):
    game: str = "CrossCode"
    data: ItemData

    def __init__(self, player: int, data: ItemData):
        super(CrossCodeItem, self).__init__(
            data.item.name,
            data.item.classification,
            data.combo_id,
            player,
        )

        self.data = data
