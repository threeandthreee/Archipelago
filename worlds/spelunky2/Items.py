from typing import Optional, NamedTuple
from BaseClasses import Item, ItemClassification
from . import locked_items, item_options
from .enums import ItemName, ShortcutName, WorldName

class Spelunky2Item(Item):
    game = "Spelunky 2"


class Spelunky2ItemData(NamedTuple):
    code: int
    classification: Optional[ItemClassification] = ItemClassification.filler
    amount: Optional[int] = 1


filler_items = {
    ItemName.ROPE_PILE.value:   Spelunky2ItemData(1),
    ItemName.BOMB_BAG.value:    Spelunky2ItemData(2),
    ItemName.BOMB_BOX.value:    Spelunky2ItemData(3),
    ItemName.COOKED_TURKEY.value: Spelunky2ItemData(4),
    ItemName.ROYAL_JELLY.value: Spelunky2ItemData(5),
    ItemName.GOLD_BAR.value:    Spelunky2ItemData(6),
    ItemName.EMERALD_GEM.value: Spelunky2ItemData(7),
    ItemName.SAPPHIRE_GEM.value: Spelunky2ItemData(8),
    ItemName.RUBY_GEM.value:    Spelunky2ItemData(9),
    ItemName.DIAMOND_GEM.value: Spelunky2ItemData(10),
}

characters = {  # 4 Characters randomly chosen, Ana/Margaret/Colin/Roffy will be found where non-starters exist
    # ItemName.ANA_SPELUNKY.value:      Spelunky2ItemData(101),
    # ItemName.MARGARET_TUNNEL.value:   Spelunky2ItemData(102),
    # ItemName.COLIN_NORTHWARD.value:   Spelunky2ItemData(103),
    # ItemName.ROFFY_D_SLOTH.value:     Spelunky2ItemData(104),
    ItemName.ALTO_SINGH.value:         Spelunky2ItemData(105),
    ItemName.LIZ_MUTTON.value:         Spelunky2ItemData(106),
    ItemName.NEKKA_THE_EAGLE.value:    Spelunky2ItemData(107),
    ItemName.LISE_PROJECT.value:       Spelunky2ItemData(108),
    ItemName.COCO_VON_DIAMONDS.value:  Spelunky2ItemData(109),
    ItemName.MANFRED_TUNNEL.value:     Spelunky2ItemData(110),
    ItemName.LITTLE_JAY.value:         Spelunky2ItemData(111),
    ItemName.TINA_FLAN.value:          Spelunky2ItemData(112),
    ItemName.VALERIE_CRUMP.value:      Spelunky2ItemData(113),
    ItemName.AU.value:                 Spelunky2ItemData(114),
    ItemName.DEMI_VON_DIAMONDS.value:  Spelunky2ItemData(115),
    ItemName.PILOT.value:              Spelunky2ItemData(116),
    ItemName.PRINCESS_AIRYN.value:     Spelunky2ItemData(117),
    ItemName.DIRK_YAMAOKA.value:       Spelunky2ItemData(118),
    ItemName.GUY_SPELUNKY.value:       Spelunky2ItemData(119),
    ItemName.CLASSIC_GUY.value:        Spelunky2ItemData(120),
}

locked_items_dict = {}
item_code = 200
for item_name in locked_items:
    item_code += 1
    locked_items_dict[item_name] = Spelunky2ItemData(item_code, ItemClassification.progression)

upgrade_items_dict = {}
item_code = 300
for item_name in item_options:
    item_code += 1
    upgrade_items_dict[f"{item_name} Upgrade"] = Spelunky2ItemData(item_code, ItemClassification.useful)

waddler_items_dict = {}
item_code = 400
for item_name in locked_items:
    item_code += 1
    waddler_items_dict[f"{item_name} Waddler Upgrade"] = Spelunky2ItemData(item_code, ItemClassification.useful)

permanent_upgrades = {
    ItemName.HEALTH_UPGRADE.value:           Spelunky2ItemData(501, ItemClassification.useful, 0),
    ItemName.BOMB_UPGRADE.value:             Spelunky2ItemData(502, ItemClassification.useful, 0),
    ItemName.ROPE_UPGRADE.value:             Spelunky2ItemData(503, ItemClassification.useful, 0),
    ItemName.COSMIC_OCEAN_CP.value:          Spelunky2ItemData(504, ItemClassification.useful, 0),  # Count set by player settings
}

shortcuts = {  # TODO: Maybe add more shortcuts by editing the Camp to allow specific world selection from camp
    # ShortcutName.PROGRESSIVE.value:      Spelunky2ItemData(601, ItemClassification.helpful),
    # ShortcutName.DWELLING.value:         Spelunky2ItemData(602, ItemClassification.helpful),
    # ShortcutName.JUNGLE.value:           Spelunky2ItemData(603, ItemClassification.helpful),
    # ShortcutName.VOLCANA.value:          Spelunky2ItemData(604, ItemClassification.helpful),
    # ShortcutName.OLMECS_LAIR.value:      Spelunky2ItemData(605, ItemClassification.helpful),
    # ShortcutName.TIDE_POOL.value:        Spelunky2ItemData(606, ItemClassification.helpful),
    # ShortcutName.TEMPLE.value:           Spelunky2ItemData(607, ItemClassification.helpful),
    # ShortcutName.ICE_CAVES.value:        Spelunky2ItemData(608, ItemClassification.helpful),
    # ShortcutName.NEO_BABYLON.value:      Spelunky2ItemData(609, ItemClassification.helpful),  # literal "Neo Babylon" vs enum is "Neo Babylon Shortcut"
    # ShortcutName.SUNKEN_CITY.value:      Spelunky2ItemData(610, ItemClassification.helpful),  # literal "Sunken City" vs enum is "Sunken City Shortcut"
}

world_unlocks = {
    WorldName.PROGRESSIVE.value: Spelunky2ItemData(701, ItemClassification.progression, 0),  # Count set by goal
    WorldName.JUNGLE.value:       Spelunky2ItemData(702, ItemClassification.progression, 0),
    WorldName.VOLCANA.value:      Spelunky2ItemData(703, ItemClassification.progression, 0),
    WorldName.OLMECS_LAIR.value:  Spelunky2ItemData(704, ItemClassification.progression, 0),
    WorldName.TIDE_POOL.value:    Spelunky2ItemData(705, ItemClassification.progression, 0),
    WorldName.TEMPLE.value:       Spelunky2ItemData(706, ItemClassification.progression, 0),
    WorldName.ICE_CAVES.value:    Spelunky2ItemData(707, ItemClassification.progression, 0),
    WorldName.NEO_BABYLON.value:  Spelunky2ItemData(708, ItemClassification.progression, 0),
    WorldName.SUNKEN_CITY.value:  Spelunky2ItemData(709, ItemClassification.progression, 0),
    WorldName.COSMIC_OCEAN.value: Spelunky2ItemData(710, ItemClassification.progression, 0),
}

traps = {
    ItemName.POISON_TRAP.value:      Spelunky2ItemData(801, ItemClassification.trap, 0),
    ItemName.CURSE_TRAP.value:       Spelunky2ItemData(802, ItemClassification.trap, 0),
    ItemName.GHOST_TRAP.value:       Spelunky2ItemData(803, ItemClassification.trap, 0),
    ItemName.STUN_TRAP.value:        Spelunky2ItemData(804, ItemClassification.trap, 0),
    ItemName.LOOSE_BOMBS_TRAP.value: Spelunky2ItemData(805, ItemClassification.trap, 0),
    ItemName.BLINDNESS_TRAP.value:   Spelunky2ItemData(806, ItemClassification.trap, 0),
    # ItemName.AMNESIA_TRAP.value:     Spelunky2ItemData(807, ItemClassification.trap, 0),
    # ItemName.ANGRY_SHOPKEEPERS_TRAP.value: Spelunky2ItemData(808, ItemClassification.trap, 0),
    ItemName.PUNISH_BALL_TRAP.value: Spelunky2ItemData(809, ItemClassification.trap, 0),
}

# Populate further with locked_items, starter_items and quest_items inside __init.py__ based on Options
item_data_table = {
    **filler_items,
    **characters,
    **locked_items_dict,
    **upgrade_items_dict,
    **waddler_items_dict,
    **permanent_upgrades,
    **world_unlocks,
    # **shortcuts,
    **traps
}

filler_weights = {
    ItemName.ROPE_PILE.value:    0,
    ItemName.BOMB_BAG.value:     0,
    ItemName.BOMB_BOX.value:     0,
    ItemName.COOKED_TURKEY.value:0,
    ItemName.ROYAL_JELLY.value:  0,
    ItemName.GOLD_BAR.value:     0,
    ItemName.EMERALD_GEM.value:  0,
    ItemName.SAPPHIRE_GEM.value: 0,
    ItemName.RUBY_GEM.value:     0,
    ItemName.DIAMOND_GEM.value:  0,
}

trap_weights = {
    ItemName.POISON_TRAP.value:      0,
    ItemName.CURSE_TRAP.value:       0,
    ItemName.GHOST_TRAP.value:       0,
    ItemName.STUN_TRAP.value:        0,
    ItemName.LOOSE_BOMBS_TRAP.value: 0,
    ItemName.BLINDNESS_TRAP.value:   0,
    # ItemName.AMNESIA_TRAP.value:         0,
    # ItemName.ANGRY_SHOPKEEPERS_TRAP.value:0,
    ItemName.PUNISH_BALL_TRAP.value: 0,
}
