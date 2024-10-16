from worlds.generic.Rules import set_rule, forbid_items_for_player, add_rule
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import EarthBoundWorld


def set_location_rules(world: "EarthBoundWorld") -> None:
    player = world.player
    twoson_paula_room_present = world.get_location("Twoson - Paula's Room Present")
    can_buy_pizza = world.get_location("Threed - Downtown Trashcan")

    set_rule(world.multiworld.get_location("Onett - Traveling Entertainer", player), lambda state: state.has("Key to the Shack", player))
    set_rule(world.multiworld.get_location("Onett - South Road Present", player), lambda state: state.has("Police Badge", player))
    set_rule(world.multiworld.get_location("Twoson - Paula's Mother", player), lambda state: state.has("Paula", player))
    set_rule(world.multiworld.get_location("Twoson - Everdred Meeting", player), lambda state: state.has("Paula", player))
    set_rule(world.multiworld.get_location("Twoson - Insignificant Location", player), lambda state: state.has("Insignificant Item", player))
    set_rule(world.multiworld.get_location("Happy-Happy Village - Defeat Carpainter", player), lambda state: state.has("Franklin Badge", player))
    set_rule(world.multiworld.get_location("Happy-Happy Village - Prisoner", player), lambda state: state.has("Key to the Cabin", player))
    set_rule(world.multiworld.get_location("Threed - Boogey Tent Trashcan", player), lambda state: state.has("Jeff", player))
    set_rule(world.multiworld.get_location("Threed - Zombie Prisoner", player), lambda state: state.has("Bad Key Machine", player))
    set_rule(world.multiworld.get_location("Saturn Valley - Post Belch Gift #1", player), lambda state: state.has("Threed Tunnels Clear", player))
    set_rule(world.multiworld.get_location("Saturn Valley - Post Belch Gift #2", player), lambda state: state.has("Threed Tunnels Clear", player))
    set_rule(world.multiworld.get_location("Saturn Valley - Post Belch Gift #3", player), lambda state: state.has("Threed Tunnels Clear", player))
    set_rule(world.multiworld.get_location("Monkey Caves - Talah Rama Chest #1", player), lambda state: state.has("Pencil Eraser", player))
    set_rule(world.multiworld.get_location("Monkey Caves - Talah Rama Chest #2", player), lambda state: state.has("Pencil Eraser", player))
    set_rule(world.multiworld.get_location("Monkey Caves - Talah Rama Gift", player), lambda state: state.has("Pencil Eraser", player))
    set_rule(world.multiworld.get_location("Monkey Caves - Monkey Power", player), lambda state: state.has("Pencil Eraser", player))
    set_rule(world.multiworld.get_location("Dusty Dunes - Mine Reward", player), lambda state: state.has("Mining Permit", player))
    set_rule(world.multiworld.get_location("Snow Wood - Upper Right Locker", player), lambda state: state.has("Key to the Locker", player))
    set_rule(world.multiworld.get_location("Snow Wood - Upper Left Locker", player), lambda state: state.has("Key to the Locker", player))
    set_rule(world.multiworld.get_location("Snow Wood - Bottom Right Locker", player), lambda state: state.has("Key to the Locker", player))
    set_rule(world.multiworld.get_location("Snow Wood - Bottom Left Locker", player), lambda state: state.has("Key to the Locker", player))
    set_rule(world.multiworld.get_location("Fourside - Bakery 2F Gift", player), lambda state: state.has("Contact Lens", player))
    set_rule(world.multiworld.get_location("Fourside - Department Store Blackout", player), lambda state: state.has("Jeff", player))
    set_rule(world.multiworld.get_location("Fourside - Venus Gift", player), lambda state: state.has("Diamond", player))
    set_rule(world.multiworld.get_location("Summers - Museum Item", player), lambda state: state.has("Tiny Ruby", player))
    set_rule(world.multiworld.get_location("Dalaam - Trial of Mu", player), lambda state: state.has("Poo", player))
    set_rule(world.multiworld.get_location("Poo Starting Item", player), lambda state: state.has("Poo", player))
    set_rule(world.multiworld.get_location("Tenda Village - Tenda Tea", player), lambda state: state.has("Shyness Book", player))
    set_rule(world.multiworld.get_location("Tenda Village - Tenda Gift", player), lambda state: state.has("Shyness Book", player))
    set_rule(world.multiworld.get_location("Tenda Village - Tenda Gift #2", player), lambda state: state.has("Shyness Book", player))
    set_rule(world.multiworld.get_location("Lost Underworld - Talking Rock", player), lambda state: state.has("Tendakraut", player))
    set_rule(world.multiworld.get_location("Sanctuary Goal", player), lambda state: state.has("Melody", player, world.options.sanctuaries_required.value))
    forbid_items_for_player(world.multiworld.get_location("Poo Starting Item", player), {"Poo"}, player)

    if world.options.giygas_required:
        set_rule(world.multiworld.get_location("Giygas", player), lambda state: state.has("Paula", player))

    if world.options.monkey_caves_mode < 2:
        set_rule(world.multiworld.get_location("Monkey Caves - West 2F Left Chest", player), lambda state: (twoson_paula_room_present.can_reach(state) or can_buy_pizza.can_reach(state)))
        set_rule(world.multiworld.get_location("Monkey Caves - East 2F Left Chest", player), lambda state: (twoson_paula_room_present.can_reach(state) or can_buy_pizza.can_reach(state)))
        set_rule(world.multiworld.get_location("Monkey Caves - East End Chest", player), lambda state: (twoson_paula_room_present.can_reach(state) or can_buy_pizza.can_reach(state)))
        set_rule(world.multiworld.get_location("Monkey Caves - East End Trashcan", player), lambda state: (twoson_paula_room_present.can_reach(state) or can_buy_pizza.can_reach(state)))
        set_rule(world.multiworld.get_location("Monkey Caves - East West 3F Right Chest #1", player), lambda state: (twoson_paula_room_present.can_reach(state) or can_buy_pizza.can_reach(state)))
        set_rule(world.multiworld.get_location("Monkey Caves - East West 3F Right Chest #2", player), lambda state: (twoson_paula_room_present.can_reach(state) or can_buy_pizza.can_reach(state)))

        add_rule(world.multiworld.get_location("Monkey Caves - Talah Rama Chest #1", player), lambda state: (twoson_paula_room_present.can_reach(state) or can_buy_pizza.can_reach(state)))
        add_rule(world.multiworld.get_location("Monkey Caves - Talah Rama Chest #2", player), lambda state: (twoson_paula_room_present.can_reach(state) or can_buy_pizza.can_reach(state)))
        add_rule(world.multiworld.get_location("Monkey Caves - Talah Rama Gift", player), lambda state: (twoson_paula_room_present.can_reach(state) or can_buy_pizza.can_reach(state)))
        add_rule(world.multiworld.get_location("Monkey Caves - Monkey Power", player), lambda state: (twoson_paula_room_present.can_reach(state) or can_buy_pizza.can_reach(state)))
