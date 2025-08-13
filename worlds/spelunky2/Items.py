from typing import Optional, NamedTuple
from BaseClasses import Item, ItemClassification


class Spelunky2Item(Item):
    game = "Spelunky 2"


class Spelunky2ItemData(NamedTuple):
    code: int
    classification: Optional[ItemClassification] = ItemClassification.filler
    amount: Optional[int] = 1


filler_items = {
    "Rope Pile": Spelunky2ItemData(1),
    "Bomb Bag": Spelunky2ItemData(2),
    "Bomb Box": Spelunky2ItemData(3),
    "Cooked Turkey": Spelunky2ItemData(4),
    "Royal Jelly": Spelunky2ItemData(5),
    "Gold Bar": Spelunky2ItemData(6),
}

characters = {
    # Excluded until I figure out how to randomize starting characters
    # "Ana Spelunky": Spelunky2ItemData(7, ItemClassification.filler),
    # "Margaret Tunnel": Spelunky2ItemData(8, ItemClassification.filler),
    # "Colin Northward": Spelunky2ItemData(9, ItemClassification.filler),
    # "Roffy D. Sloth": Spelunky2ItemData(10, ItemClassification.filler),
    "Alto Singh": Spelunky2ItemData(11, ItemClassification.filler),
    "Liz Mutton": Spelunky2ItemData(12, ItemClassification.filler),
    "Nekka the Eagle": Spelunky2ItemData(13, ItemClassification.filler),
    "LISE Project": Spelunky2ItemData(14, ItemClassification.filler),
    "Coco Von Diamonds": Spelunky2ItemData(15, ItemClassification.filler),
    "Manfred Tunnel": Spelunky2ItemData(16, ItemClassification.filler),
    "Little Jay": Spelunky2ItemData(17, ItemClassification.filler),
    "Tina Flan": Spelunky2ItemData(18, ItemClassification.filler),
    "Valerie Crump": Spelunky2ItemData(19, ItemClassification.filler),
    "Au": Spelunky2ItemData(20, ItemClassification.filler),
    "Demi Von Diamonds": Spelunky2ItemData(21, ItemClassification.filler),
    "Pilot": Spelunky2ItemData(22, ItemClassification.filler),
    "Princess Airyn": Spelunky2ItemData(23, ItemClassification.filler),
    "Dirk Yamaoka": Spelunky2ItemData(24, ItemClassification.filler),
    "Guy Spelunky": Spelunky2ItemData(25, ItemClassification.filler),
    "Classic Guy": Spelunky2ItemData(26, ItemClassification.filler)
}

key_items = {
    "Udjat Eye": Spelunky2ItemData(27, ItemClassification.progression),
    "Hedjet": Spelunky2ItemData(28, ItemClassification.progression),
    "Crown": Spelunky2ItemData(29, ItemClassification.progression),
    "Ankh": Spelunky2ItemData(30, ItemClassification.progression),
    "Tablet of Destiny": Spelunky2ItemData(31, ItemClassification.progression),
    "Excalibur": Spelunky2ItemData(32, ItemClassification.progression),
    "Scepter": Spelunky2ItemData(33, ItemClassification.progression),
    "Hou Yi's Bow": Spelunky2ItemData(34, ItemClassification.progression),
    "Arrow of Light": Spelunky2ItemData(35, ItemClassification.progression),
    "Ushabti": Spelunky2ItemData(36, ItemClassification.progression)  # Might change my mind about this one
}

permanent_upgrades = {
    "Starting Health Upgrade": Spelunky2ItemData(37, ItemClassification.useful, 16),
    "Starting Bomb Upgrade": Spelunky2ItemData(38, ItemClassification.useful, 6),
    "Starting Rope Upgrade": Spelunky2ItemData(39, ItemClassification.useful, 6),
    "Paste": Spelunky2ItemData(40, ItemClassification.useful),
    # "Four-Leaf Clover": Spelunky2ItemData(41, ItemClassification.useful),
    "Progressive Compass": Spelunky2ItemData(42, ItemClassification.progression, 2),
    "Eggplant": Spelunky2ItemData(43, ItemClassification.progression),
    "Cosmic Ocean Checkpoint": Spelunky2ItemData(44, ItemClassification.useful)  # No amount set since it depends on player settings
}

shortcuts = {
    # "Progressive Shortcut": Spelunky2ItemData(45, ItemClassification.progression, 3),
    # "Dwelling Shortcut": Spelunky2ItemData(46, ItemClassification.useful),
    # "Olmec's Lair Shortcut": Spelunky2ItemData(47, ItemClassification.progression),
    # "Ice Caves Shortcut": Spelunky2ItemData(48, ItemClassification.progression)
}

world_unlocks = {
    "Progressive World Unlock": Spelunky2ItemData(49, ItemClassification.progression, 7),
    "Jungle": Spelunky2ItemData(50, ItemClassification.progression),
    "Volcana": Spelunky2ItemData(51, ItemClassification.progression),
    "Olmec's Lair": Spelunky2ItemData(52, ItemClassification.progression),
    "Tide Pool": Spelunky2ItemData(53, ItemClassification.progression),
    "Temple": Spelunky2ItemData(54, ItemClassification.progression),
    "Ice Caves": Spelunky2ItemData(55, ItemClassification.progression),
    "Neo Babylon": Spelunky2ItemData(56, ItemClassification.progression),
    "Sunken City": Spelunky2ItemData(57, ItemClassification.progression),
    "Cosmic Ocean": Spelunky2ItemData(58, ItemClassification.progression),
}

traps = {
    "Poison Trap": Spelunky2ItemData(59, ItemClassification.trap),
    "Curse Trap": Spelunky2ItemData(60, ItemClassification.trap),
    "Ghost Trap": Spelunky2ItemData(61, ItemClassification.trap),
    "Stun Trap": Spelunky2ItemData(62, ItemClassification.trap),
    "Loose Bombs Trap": Spelunky2ItemData(63, ItemClassification.trap),
    "Blindness Trap": Spelunky2ItemData(64, ItemClassification.trap),
    # "Amnesia Trap": Spelunky2ItemData(65, ItemClassification.trap),
    # "Angry Shopkeepers Trap": Spelunky2ItemData(66, ItemClassification.trap),
    "Punish Ball Trap": Spelunky2ItemData(67, ItemClassification.trap)
}

item_data_table = {
    **filler_items,
    **characters,
    **key_items,
    **permanent_upgrades,
    # **shortcuts,
    **world_unlocks,
    **traps
}

filler_weights = {
            "Rope Pile": 15,
            "Bomb Bag": 15,
            "Bomb Box": 5,
            "Cooked Turkey": 20,
            "Royal Jelly": 5,
            "Gold Bar Gold": 40
        }

trap_weights = {
    "Poison Trap": 0,
    "Curse Trap": 0,
    "Ghost Trap": 0,
    "Stun Trap": 0,
    "Loose Bombs Trap": 0,
    "Blindness Trap": 0,
    # "Amnesia Trap": 0,
    # "Angry Shopkeepers Trap": 0,
    "Punish Ball Trap": 0
}
