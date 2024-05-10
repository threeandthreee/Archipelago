from typing import Counter

from BaseClasses import CollectionState
from .Options import FF6WCOptions


def has_dragons(prog_items_player: Counter[str], number: int) -> bool:
    from . import FF6WCWorld
    found: int = 0
    for dragon_event_name in FF6WCWorld.all_dragon_clears:
        found += prog_items_player[dragon_event_name]
        if found >= number:
            return True
    return False


def can_beat_final_kefka(options: FF6WCOptions, player: int, cs: CollectionState) -> bool:
    return (cs.has_group("characters", player, options.CharacterCount.value)
            and cs.has_group("espers", player, options.EsperCount.value)
            and has_dragons(cs.prog_items[player], options.DragonCount.value)
            and cs.has("Busted!", player, options.BossCount.value))
