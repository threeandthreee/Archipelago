from typing import TYPE_CHECKING

from BaseClasses import CollectionState
from worlds.generic.Rules import set_rule

if TYPE_CHECKING:
    from . import Spelunky2World


def set_common_rules(world: "Spelunky2World", player: int):

    # Entrance Rules
    set_rule(world.get_entrance("Menu -> Dwelling"), lambda state: True)
    # set_rule(world.get_entrance("Menu -> Olmec's Lair"), lambda state: state.has("Olmec's Lair Shortcut", player) or state.has("Progressive Shortcut", player, 2)) - Not implemented yet
    # set_rule(world.get_entrance("Menu -> Ice Caves"), lambda state: state.has("Ice Caves Shortcut", player) or state.has("Progressive Shortcut", player, 3)) - Not implemeneted yet
    set_rule(world.get_entrance("Dwelling -> Jungle"), lambda state: state.has("Jungle", player) or state.has("Progressive World Unlock", player))
    set_rule(world.get_entrance("Dwelling -> Volcana"), lambda state: state.has("Volcana", player) or state.has("Progressive World Unlock", player))
    set_rule(world.get_entrance("Jungle -> Olmec's Lair"), lambda state: state.has_all(["Jungle", "Olmec's Lair"], player) or state.has("Progressive World Unlock", player, 2))
    set_rule(world.get_entrance("Volcana -> Olmec's Lair"), lambda state: state.has_all(["Volcana", "Olmec's Lair"], player) or state.has("Progressive World Unlock", player, 2))
    set_rule(world.get_entrance("Olmec's Lair -> Tide Pool"), lambda state: (state.has_any(["Jungle", "Volcana"], player) and state.has_all(["Olmec's Lair", "Tide Pool"], player)) or state.has("Progressive World Unlock", player, 3))
    set_rule(world.get_entrance("Olmec's Lair -> Temple"), lambda state: (state.has_any(["Jungle", "Volcana"], player) and state.has_all(["Olmec's Lair", "Temple"], player)) or state.has("Progressive World Unlock", player, 3))
    set_rule(world.get_entrance("Tide Pool -> Ice Caves"), lambda state: (state.has_any(["Jungle", "Volcana"], player) and state.has_all(["Olmec's Lair", "Tide Pool", "Ice Caves"], player)) or state.has("Progressive World Unlock", player, 4))
    set_rule(world.get_entrance("Temple -> Ice Caves"), lambda state: (state.has_any(["Jungle", "Volcana"], player) and state.has_all(["Olmec's Lair", "Temple", "Ice Caves"], player)) or state.has("Progressive World Unlock", player, 4))
    set_rule(world.get_entrance("Ice Caves -> Neo Babylon"), lambda state: (state.has_any(["Jungle", "Volcana"], player) and state.has_any(["Tide Pool", "Temple"], player) and state.has_all(["Olmec's Lair", "Ice Caves", "Neo Babylon"], player)) or state.has("Progressive World Unlock", player, 5))

    # Place Entries
    set_rule(world.get_location("Abzu Journal Entry"), lambda state: state.has("Ankh", player))
    set_rule(world.get_location("The City of Gold Journal Entry"), lambda state: has_royalty(state, player) and state.has("Scepter", player))
    set_rule(world.get_location("Duat Journal Entry"), lambda state: state.can_reach("The City of Gold Journal Entry", "Location", player) and state.has("Ankh", player))

    # People Entries
    set_rule(world.get_location("Nekka the Eagle Journal Entry"), lambda state: state.has("Udjat Eye", player))
    set_rule(world.get_location("Coco Von Diamonds Journal Entry"), lambda state: state.has("Udjat Eye", player))
    set_rule(world.get_location("Tina Flan Journal Entry"), lambda state: state.has("Ankh", player))
    set_rule(world.get_location("Au Journal Entry"), lambda state: has_royalty(state, player) and state.has("Scepter", player))
    set_rule(world.get_location("Pilot Journal Entry"), lambda state: can_access_mothership(state, player))
    set_rule(world.get_location("Terra Tunnel Journal Entry"), lambda state: has_world_2(state, player))
    set_rule(world.get_location("Tun Journal Entry"), lambda state: has_world_2(state, player))
    set_rule(world.get_location("Sparrow Journal Entry"), lambda state: has_world_2(state, player))
    set_rule(world.get_location("Beg Journal Entry"), lambda state: has_world_2(state, player))

    # Bestiary Entries
    set_rule(world.get_location("Vampire Journal Entry"), lambda state: state.has("Udjat Eye", player))
    set_rule(world.get_location("Vlad Journal Entry"), lambda state: state.has("Udjat Eye", player))
    set_rule(world.get_location("Kingu Journal Entry"), lambda state: state.can_reach("Abzu Journal Entry", "Location", player))
    set_rule(world.get_location("Ammit Journal Entry"), lambda state: state.can_reach("Duat Journal Entry", "Location", player))
    set_rule(world.get_location("Apep Journal Entry"), lambda state: state.can_reach("Duat Journal Entry", "Location", player))
    set_rule(world.get_location("Anubis II Journal Entry"), lambda state: state.can_reach("Duat Journal Entry", "Location", player))
    set_rule(world.get_location("Osiris Journal Entry"), lambda state: state.can_reach("Duat Journal Entry", "Location", player))
    set_rule(world.get_location("Lamahu Journal Entry"), lambda state: can_access_mothership(state, player))
    set_rule(world.get_location("Proto Shopkeeper Journal Entry"), lambda state: can_access_mothership(state, player))
    set_rule(world.get_location("Golden Monkey Journal Entry"), lambda state: has_world_2(state, player))
    set_rule(world.get_location("Leprechaun Journal Entry"), lambda state: has_world_2(state, player))

    set_rule(world.get_location("Qilin Journal Entry"), lambda state: state.can_reach("Tablet of Destiny Journal Entry", "Location", player))

    # Item Entries
    set_rule(world.get_location("Alien Compass Journal Entry"), lambda state: can_access_mothership(state, player))
    set_rule(world.get_location("Udjat Eye Journal Entry"), lambda state: state.has("Udjat Eye", player))
    set_rule(world.get_location("Kapala Journal Entry"), lambda state: has_world_2(state, player))
    set_rule(world.get_location("Hedjet Journal Entry"), lambda state: state.has("Udjat Eye", player))
    set_rule(world.get_location("Crown Journal Entry"), lambda state: state.has("Udjat Eye", player))
    set_rule(world.get_location("Ankh Journal Entry"), lambda state: state.has("Ankh", player))
    set_rule(world.get_location("Tablet of Destiny Journal Entry"), lambda state: state.can_reach("Duat Journal Entry", "Location", player))
    set_rule(world.get_location("Cape Journal Entry"), lambda state: state.has("Udjat Eye", player))
    set_rule(world.get_location("Vlad's Cape Journal Entry"), lambda state: state.has("Udjat Eye", player))
    set_rule(world.get_location("Telepack Journal Entry"), lambda state: state.has("Udjat Eye", player))
    set_rule(world.get_location("Hoverpack Journal Entry"), lambda state: state.has("Udjat Eye", player))
    set_rule(world.get_location("Powerpack Journal Entry"), lambda state: state.has("Udjat Eye", player))
    set_rule(world.get_location("Teleporter Journal Entry"), lambda state: state.has("Udjat Eye", player))
    set_rule(world.get_location("Mattock Journal Entry"), lambda state: has_world_2(state, player))
    set_rule(world.get_location("Excalibur Journal Entry"), lambda state: has_royalty(state, player) and state.has("Excalibur", player))
    set_rule(world.get_location("Plasma Cannon Journal Entry"), lambda state: can_access_mothership(state, player))
    set_rule(world.get_location("Scepter Journal Entry"), lambda state: state.has("Scepter", player))
    set_rule(world.get_location("Four-Leaf Clover Journal Entry"), lambda state: has_world_2(state, player))

def set_sunken_city_rules(world: "Spelunky2World", player: int):

    # Entrance Rules
    set_rule(world.get_entrance("Neo Babylon -> Sunken City"), lambda state: can_access_sunken_city(state, player))

    # Place Entries
    set_rule(world.get_location("Eggplant World Journal Entry"), lambda state: state.has("Eggplant", player))

    # Bestiary Entries
    set_rule(world.get_location("Eggplant Minister Journal Entry"), lambda state: state.has("Eggplant", player))
    set_rule(world.get_location("Eggplup Journal Entry"), lambda state: state.has("Eggplant", player))

    # Item Entries
    set_rule(world.get_location("Eggplant Crown Journal Entry"), lambda state: state.can_reach("Eggplant World Journal Entry", "Location", player))


def set_cosmic_ocean_rules(world: "Spelunky2World", player: int):
    set_rule(world.get_entrance("Sunken City -> Cosmic Ocean"), lambda state: state.can_reach("Sunken City", "Region", player) and state.has_all(["Hou Yi's Bow", "Arrow of Light"], player))


def has_royalty(state: CollectionState, player: int):
    return (state.has("Udjat Eye", player)
            and (state.has_all(["Jungle", "Hedjet"], player)
            or state.has_all(["Volcana", "Crown"], player)
            or (state.has("Progressive World Unlock", player) and state.has_any(["Hedjet", "Crown"], player))))


def has_weapon(state: CollectionState, player: int) -> bool:
    return (state.has_all(["Tide Pool", "Excalibur"], player)
            or state.has_all(["Temple", "Scepter"], player)
            or (state.has("Progressive World Unlock", player, 3) and state.has_any(["Excalibur", "Scepter"], player)))


def has_world_2(state: CollectionState, player: int) -> bool:
    return state.has_any(["Jungle", "Volcana"], player) or state.has("Progressive World Unlock", player)


def has_world_4(state: CollectionState, player: int) -> bool:
    return state.has_any(["Tide Pool", "Temple"], player) or state.has("Progressive World Unlock", player, 3)


def can_access_mothership(state: CollectionState, player: int) -> bool:
    return (state.has_all(["Volcana", "Olmec's Lair", "Temple", "Ice Caves"], player)
            or state.has("Progressive World Unlock", player, 4))


def can_access_sunken_city(state: CollectionState, player: int) -> bool:
    return ((has_royalty(state, player) and has_weapon(state, player) and state.has_all(["Tablet of Destiny", "Ushabti"], player))
            and (state.can_reach("Neo Babylon", "Region", player) and state.has("Sunken City", player))
            or state.has("Progressive World Unlock", player, 6))
