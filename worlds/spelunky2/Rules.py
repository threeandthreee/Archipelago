from typing import TYPE_CHECKING
from . import powerup_options, locked_items
from .enums import WorldName, RuleNames, ItemName, LocationName, JournalName

from BaseClasses import CollectionState
from worlds.generic.Rules import set_rule

if TYPE_CHECKING:
    from . import Spelunky2World

def has_or_unrestricted(world, state, player, item_name: str) -> bool:
    """
    Returns True if the item is in the player's possession OR
    is not in the AP-locked 'restricted_items' set (meaning it's free in-game).
    """
    return (item_name not in world.options.restricted_items.value) or state.has(item_name, player)

def set_common_rules(world: "Spelunky2World", player: int):

    # Primary Regions -- note starting from shortcuts is not currently in logic. When this is added, it might break certain entries (e.g. The Tusk Idol and chain requirements)
    set_rule(world.get_entrance(RuleNames.MENU_TO_DWELLING.value), lambda state: True)
    # set_rule(world.get_entrance(RuleNames.MENU_TO_OLMECS_LAIR.value), lambda state: state.has(ShortcutName.OLMECS_LAIR.value, player) or state.has(ShortcutName.PROGRESSIVE.value, player, 2))  # Not implemented yet
    # set_rule(world.get_entrance(RuleNames.MENU_TO_ICE_CAVES.value), lambda state: state.has(ShortcutName.ICE_CAVES.value, player) or state.has(ShortcutName.PROGRESSIVE.value, player, 3))  # Not implemented yet

    set_rule(world.get_entrance(RuleNames.DWELLING_TO_JUNGLE.value),
             lambda state: state.has(WorldName.JUNGLE.value, player) or state.has(WorldName.PROGRESSIVE.value, player))
    set_rule(world.get_entrance(RuleNames.DWELLING_TO_VOLCANA),
             lambda state: state.has(WorldName.VOLCANA.value, player) or state.has(WorldName.PROGRESSIVE.value, player))
    set_rule(world.get_entrance(RuleNames.JUNGLE_TO_OLMEC),
             lambda state: state.has(WorldName.OLMECS_LAIR.value, player) or state.has(WorldName.PROGRESSIVE.value, player, 2))
    set_rule(world.get_entrance(RuleNames.VOLCANA_TO_OLMEC),
             lambda state: state.has(WorldName.OLMECS_LAIR.value, player) or state.has(WorldName.PROGRESSIVE.value, player, 2))
    set_rule(world.get_entrance(RuleNames.OLMEC_TO_TIDE_POOL),
             lambda state: state.has(WorldName.TIDE_POOL.value, player) or state.has(WorldName.PROGRESSIVE.value, player, 3))
    set_rule(world.get_entrance(RuleNames.OLMEC_TO_TEMPLE),
             lambda state: state.has(WorldName.TEMPLE.value, player) or state.has(WorldName.PROGRESSIVE.value, player, 3))
    set_rule(world.get_entrance(RuleNames.TIDEPOOL_TO_ICE_CAVES),
             lambda state: state.has(WorldName.ICE_CAVES.value, player) or state.has(WorldName.PROGRESSIVE.value, player, 4))
    set_rule(world.get_entrance(RuleNames.TEMPLE_TO_ICE_CAVES),
             lambda state: state.has(WorldName.ICE_CAVES.value, player) or state.has(WorldName.PROGRESSIVE.value, player, 4))
    set_rule(world.get_entrance(RuleNames.ICE_CAVES_TO_NEO_BABYLON),
             lambda state: state.has(WorldName.NEO_BABYLON.value, player) or state.has(WorldName.PROGRESSIVE.value, player, 5))

    # Secondary Regions
    set_rule(world.get_entrance(RuleNames.DWELLING_TO_ANY_WORLD_2.value),
             lambda state: has_world_2(state, player))
    set_rule(world.get_entrance(RuleNames.JUNGLE_TO_BLACK_MARKET.value),
             lambda state: has_or_unrestricted(world, state, player, ItemName.UDJAT_EYE.value))  # TODO Udjat Skip setting
    set_rule(world.get_entrance(RuleNames.VOLCANA_TO_VLADS_CASTLE.value),
             lambda state: has_or_unrestricted(world, state, player, ItemName.UDJAT_EYE.value))  # TODO Udjat Skip setting
    set_rule(world.get_entrance(RuleNames.TIDEPOOL_TO_ABZU),
             lambda state: has_or_unrestricted(world, state, player, ItemName.ANKH.value))  # TODO Deathskip setting
    set_rule(world.get_entrance(RuleNames.TEMPLE_TO_CITY_OF_GOLD.value),
             lambda state: has_royalty(world, state, player) and has_or_unrestricted(world, state, player, ItemName.SCEPTER.value))
    set_rule(world.get_entrance(RuleNames.CITY_OF_GOLD_TO_DUAT.value),
             lambda state: has_or_unrestricted(world, state, player, ItemName.ANKH.value))
    set_rule(world.get_entrance(RuleNames.ICE_CAVES_TO_MOTHERSHIP.value),
             lambda state: can_access_mothership(state, player))

    # People Entries
    set_rule(world.get_location(JournalName.EGGPLANT_CHILD.value),
             lambda state: has_or_unrestricted(world, state, player, ItemName.EGGPLANT.value))
    # Bestiary Entries
    set_rule(world.get_location(JournalName.QILIN.value),
             lambda state: can_obtain_qilin(world, state, player))
    # Item Entries
    set_rule(world.get_location(JournalName.ALIEN_COMPASS.value),
             lambda state: can_obtain_alien_compass(state, player))
    set_rule(world.get_location(JournalName.UDJAT_EYE.value),
             lambda state: has_or_unrestricted(world, state, player, ItemName.UDJAT_EYE.value))
    set_rule(world.get_location(JournalName.HEDJET.value),
             lambda state: has_or_unrestricted(world, state, player, ItemName.HEDJET.value))
    set_rule(world.get_location(JournalName.CROWN.value),
             lambda state: has_or_unrestricted(world, state, player, ItemName.CROWN.value))
    set_rule(world.get_location(JournalName.ANKH.value),
             lambda state: has_or_unrestricted(world, state, player, ItemName.ANKH.value))
    set_rule(world.get_location(JournalName.TABLET_OF_DESTINY.value),
             lambda state: can_obtain_tablet(world, state, player))
    set_rule(world.get_location(JournalName.EXCALIBUR.value),
             lambda state: has_royalty(world, state, player) and has_or_unrestricted(world, state, player, ItemName.EXCALIBUR.value))
    set_rule(world.get_location(JournalName.SCEPTER.value),
             lambda state: has_or_unrestricted(world, state, player, ItemName.SCEPTER.value))
    set_rule(world.get_location(JournalName.HOU_YI_BOW.value),
             lambda state: has_or_unrestricted(world, state, player, ItemName.HOU_YI_BOW.value))
    set_rule(world.get_location(JournalName.USHABTI.value),
             lambda state: has_or_unrestricted(world, state, player, ItemName.USHABTI.value))
    set_rule(world.get_location(JournalName.EGGPLANT.value),
             lambda state: has_or_unrestricted(world, state, player, ItemName.EGGPLANT.value))


def set_sunken_city_rules(world: "Spelunky2World", player: int):
    # Entrance Rules
    set_rule(world.get_entrance(RuleNames.NEO_BABYLON_TO_SUNKEN_CITY.value),
             lambda state: can_access_sunken_city(world, state, player))
    set_rule(world.get_entrance(RuleNames.SUNKEN_CITY_TO_EGGPLANT_WORLD.value),
             lambda state: has_or_unrestricted(world, state, player, ItemName.EGGPLANT.value))
    set_rule(world.get_location(JournalName.ARROW_OF_LIGHT.value),
             lambda state: can_access_sunken_city(world, state, player))


def set_cosmic_ocean_rules(world: "Spelunky2World", player: int):
    set_rule(world.get_entrance(RuleNames.SUNKEN_CITY_TO_COSMIC_OCEAN.value),
             lambda state: can_access_cosmic_ocean(world, state, player))


def has_royalty(world: "Spelunky2World", state: CollectionState, player: int):
    return (
            has_or_unrestricted(world, state, player, ItemName.UDJAT_EYE.value)
            and (
                    state.has_all([WorldName.JUNGLE.value], player)
                    and has_or_unrestricted(world, state, player, ItemName.HEDJET.value)
                    or state.has_all([WorldName.VOLCANA.value], player)
                    and has_or_unrestricted(world, state, player, ItemName.CROWN.value)
                    or (
                            state.has(WorldName.PROGRESSIVE.value, player)
                            and (
                                    has_or_unrestricted(world, state, player, ItemName.HEDJET.value)
                                    or has_or_unrestricted(world, state, player, ItemName.CROWN.value)
                            )
                    )
            )
    )


def has_weapon(state: CollectionState, player: int) -> bool:  # Currently unused
    return (
            state.has_all([WorldName.TIDE_POOL.value, ItemName.EXCALIBUR.value], player)
            or state.has_all([WorldName.TEMPLE.value, ItemName.SCEPTER.value], player)
            or (
                    state.has(WorldName.PROGRESSIVE.value, player, 3)
                    and state.has_any([ItemName.EXCALIBUR.value, ItemName.SCEPTER.value], player)
            )
    )


def has_world_2(state: CollectionState, player: int) -> bool:
    return (
            state.has_any(
                [WorldName.JUNGLE.value, WorldName.VOLCANA.value],
                player
            )
            or state.has(WorldName.PROGRESSIVE.value, player)
    )

def has_world_4(state: CollectionState, player: int) -> bool:  # Currently unused
    return (
            state.has_any(
                [WorldName.TIDE_POOL.value, WorldName.TEMPLE.value],
                player
            )
            or state.has(WorldName.PROGRESSIVE.value, player, 3)
    )

def can_obtain_alien_compass(state: CollectionState, player: int) -> bool:
    return (
            state.has_all(
                [
                    WorldName.VOLCANA.value,
                    WorldName.OLMECS_LAIR.value,
                    WorldName.TEMPLE.value
                ],
                player
            )
            and state.can_reach(LocationName.VLADS_CASTLE.value, "Region", player)
            or state.has(WorldName.PROGRESSIVE.value, player, 3)
    )

# TODO Alien Compass Skip settings (Mothership can be found with various mobility items or even with nothing but bombs/landmines), currently identical to can_obtain_alien_compass
def can_access_mothership(state: CollectionState, player: int) -> bool:
    return can_obtain_alien_compass(state, player)

# TODO Excalibur Skip settings
def can_obtain_tablet(
        world: "Spelunky2World",
        state: CollectionState,
        player: int
) -> bool:
    return (
            has_or_unrestricted(
                world, state, player, ItemName.TABLET_OF_DESTINY.value
            )
            and (
                    state.can_reach(LocationName.DUAT.value, "Region", player)
                    or (
                            state.can_reach(LocationName.ABZU.value, "Region", player)
                            and state.can_reach(
                        JournalName.EXCALIBUR.value,
                        "Location",
                        player
                    )
                    )
            )
    )

def can_obtain_qilin(
        world: "Spelunky2World",
        state: CollectionState,
        player: int
) -> bool:
    return (
            can_obtain_tablet(world, state, player)
            and has_or_unrestricted(
        world, state, player, ItemName.USHABTI.value
    )
    )

# TODO Qilin Skip settings
def can_access_sunken_city(
        world: "Spelunky2World",
        state: CollectionState,
        player: int
) -> bool:
    return (
            can_obtain_qilin(world, state, player)
            and (
                    state.has(WorldName.SUNKEN_CITY.value, player)
                    or state.has(WorldName.PROGRESSIVE.value, player, 6)
            )
    )

def can_access_cosmic_ocean(
        world: "Spelunky2World",
        state: CollectionState,
        player: int
) -> bool:
    return (
            has_or_unrestricted(
                world, state, player, ItemName.HOU_YI_BOW.value
            )
            and has_or_unrestricted(world, state, player, ItemName.ARROW_OF_LIGHT.value)
            and (
                    state.has(WorldName.COSMIC_OCEAN.value, player)
                    or state.has(WorldName.PROGRESSIVE.value, player, 7)
            )
    )


def get_upgrade_item_name(item_name: str) -> str:
    return f"{item_name} Upgrade"


def get_waddler_item_name(item_name: str) -> str:
    return f"{item_name} Waddler Upgrade"


def set_starter_upgrade_rules(world: "Spelunky2World", player: int):
    """Ensure starter upgrades require their locked/quest counterpart first."""

    # Set rules for all possible Waddler upgrades.
    # We iterate over locked_items because the user can select any of these for Waddler storage.
    waddler_items_selected = world.options.waddler_upgrades.value
    for item_name in locked_items:
        if item_name in waddler_items_selected:
            waddler_name = get_waddler_item_name(item_name)
            try:
                loc = world.get_location(waddler_name)
                # Waddler items require their locked item counterpart
                name_enum = ItemName(item_name).value
                set_rule(
                    loc,
                    lambda state, name=name_enum: has_or_unrestricted(world, state, player, name)
                )
            except KeyError:
                pass

    # Set rules for all powerup upgrades that were NOT selected as Waddler items.
    item_upgrades_selected = world.options.item_upgrades.value
    for item_name in powerup_options:
        if item_name not in waddler_items_selected and item_name in item_upgrades_selected:
            upgrade_name = get_upgrade_item_name(item_name)
            try:
                loc = world.get_location(upgrade_name)
                # Upgrades require their locked item counterpart
                name_enum = ItemName(item_name).value
                set_rule(
                    loc,
                    lambda state, name=name_enum: has_or_unrestricted(world, state, player, name)
                )
            except KeyError:
                pass
