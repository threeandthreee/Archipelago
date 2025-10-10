import typing


from BaseClasses import Item, ItemClassification
from typing import Optional

class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    classification: ItemClassification

class TwistyCubeItem(Item):
    game: str = "Twisty Cube"

    def __init__(self, name: str, classification: ItemClassification, code: Optional[int],player: int):
        self.name = name
        self.classification = classification
        self.player = player
        self.code = code
        self.location = None

colors = ["White", "Yellow", "Red", "Orange", "Blue", "Green"]
item_groups = {
    color: [] for color in colors
}
item_table = {}
for i in range(1, 17):
    for j, color in enumerate(colors):
        item_groups[color].append(f"{color} Sticker #{i}")
        item_table[f"{colors[j]} Sticker #{i}"] = ItemData(267782000 + j * 16 + i, ItemClassification.progression)
  
item_table["filler"] = ItemData(267781999, ItemClassification.filler)

