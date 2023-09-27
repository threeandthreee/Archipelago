from .locations.items import *
from .utils import formatText
from ..Items import LinksAwakeningItem
from ..Locations import LinksAwakeningLocation


hint_text_ids = [
    # Overworld owl statues
    0x1B6, 0x1B7, 0x1B8, 0x1B9, 0x1BA, 0x1BB, 0x1BC, 0x1BD, 0x1BE, 0x22D,

    0x288, 0x280,  # D1
    0x28A, 0x289, 0x281,  # D2
    0x282, 0x28C, 0x28B,  # D3
    0x283,  # D4
    0x28D, 0x284,  # D5
    0x285, 0x28F, 0x28E,  # D6
    0x291, 0x290, 0x286,  # D7
    0x293, 0x287, 0x292,  # D8
    0x263,  # D0

    # Hint books
    0x267,  # color dungeon
    0x201,  # Pre open: 0x200
    0x203,  # Pre open: 0x202
    0x205,  # Pre open: 0x204
    0x207,  # Pre open: 0x206
    0x209,  # Pre open: 0x208
    0x20B,  # Pre open: 0x20A
]

hints = [
    "{0} is at {1}",
    "If you want {0} start looking in {1}",
    "{1} holds {0}",
    "They say that {0} is at {1}",
    "You might want to look in {1} for a secret",
]

useless_hint = [
    ("Egg", "Mt. Tamaranch"),
    ("Marin", "Mabe Village"),
    ("Marin", "Mabe Village"),
    ("Witch", "Koholint Prairie"),
    ("Mermaid", "Martha's Bay"),
    ("Nothing", "Tabahl Wasteland"),
    ("Animals", "Animal Village"),
    ("Sand", "Yarna Desert"),
]


def add_hints(rom, rnd, multiworld, ap_setting):
    item_pool = get_item_pool(multiworld, ap_setting)
    rnd.shuffle(item_pool)
    text_ids = hint_text_ids.copy()
    rnd.shuffle(text_ids)
    for text_id in text_ids:
        hint = generate_hint(item_pool, rnd, multiworld, ap_setting)
        rom.texts[text_id] = formatText(hint)
    for text_id in range(0x200, 0x20C, 2):
        rom.texts[text_id] = formatText("Read this book?", ask="YES  NO")

def get_item_pool(multiworld, ap_setting):
    item_pool = multiworld.get_items().filter(is_hintable)
    if ap_setting['hint_classification'] == HintClassification.option_useful:
        item_pool = item_pool.filter(is_useful).filter(not_unshuffled_dungeon_item)
    elif ap_setting['hint_classification'] == HintClassification.option_progression:
        item_pool = item_pool.filter(is_progression).filter(not_unshuffled_dungeon_item)
    if ap_setting['hint_locality'] == HintLocality.option_our_items:
        item_pool = item_pool.filter(is_ours)
    elif ap_setting['hint_locality'] == HintLocality.option_local_items:
        item_pool = item_pool.filter(is_local)
    elif ap_setting['hint_locality'] == HintLocality.option_our_local_items:
        item_pool = item_pool.filter(is_ours).filter(is_local)
    return item_pool

def generate_hint(item_pool, rnd, multiworld, ap_setting):
    is_junk = rnd.uniform(0,100) < ap_setting['junk_hint_rate']
    if is_junk or not items:
        return rnd.choice(hints).format(*rnd.choice(useless_hint))
    item = item_pool.pop()
    name = "Your" if is_ours(item) else f"{multiworld.player_name[item.player]}'s"
    location_name = item.location.ladxr_item.metadata.name if in_ladx(item) else item.location.name
    hint = f"{name} {item.name} is at {location_name}"
    if not is_local(item):
        hint += f" in {multiworld.player_name[item.location.player]}'s world"
    # Cap hint size at 85
    # Realistically we could go bigger but let's be safe instead
    hint = hint[:85]
    return hint

def is_hintable(item):
    return item.location and item.code is not None and item.location.show_in_spoiler

def is_useful(item):
    return all(ItemClassification[type] not in item.classification for type in ['trap', 'filler'])

def is_progression(item):
    return any(ItemClassification[type] in item.classification for type in ['progression', 'progression_skip_balancing'])

def not_unshuffled_dungeon_item(item):
    is_unshuffled_dungeon_item = from_ladx(item) and isinstance(item.item_data, DungeonItemData) and item.location.parent_region and item.item_data.dungeon_index == item.location.parent_region.dungeon_index
    return not is_unshuffled_dungeon_item

def is_ours(item):
    return item.player == player_id

def is_local(item):
    return item.location.player == player_id

def in_ladx(item):
    return isinstance(item.location, LinksAwakeningLocation)

def from_ladx(item):
    return isinstance(item, LinksAwakeningItem)
