from typing import Dict, Any, ClassVar, Tuple, Callable, Optional, Union, List
from math import ceil
import Utils
import settings
from Options import OptionGroup

from Utils import local_path
from BaseClasses import (Item,
                         ItemClassification as ItemClass,
                         Tutorial,
                         CollectionState)
from .GameID import jak1_id, jak1_name, jak1_max
from . import Options
from .Locations import (JakAndDaxterLocation,
                        location_table,
                        cell_location_table,
                        scout_location_table,
                        special_location_table,
                        cache_location_table,
                        orb_location_table)
from .Items import (JakAndDaxterItem,
                    item_table,
                    cell_item_table,
                    scout_item_table,
                    special_item_table,
                    move_item_table,
                    orb_item_table)
from .Levels import level_table, level_table_with_global
from .locs import (CellLocations as Cells,
                   ScoutLocations as Scouts,
                   SpecialLocations as Specials,
                   OrbCacheLocations as Caches,
                   OrbLocations as Orbs)
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import components, Component, launch_subprocess, Type, icon_paths


def launch_client():
    from .Client import launch
    launch_subprocess(launch, name="JakAndDaxterClient")


components.append(Component("Jak and Daxter Client",
                            func=launch_client,
                            component_type=Type.CLIENT,
                            icon="egg"))

icon_paths["egg"] = local_path("worlds", "jakanddaxter", "icons", "egg.png")


class JakAndDaxterSettings(settings.Group):
    class RootDirectory(settings.UserFolderPath):
        """Path to folder containing the ArchipelaGOAL mod executables (gk.exe and goalc.exe).
        Ensure this path contains forward slashes (/) only. This setting only applies if
        Auto Detect Root Directory is set to false."""
        description = "ArchipelaGOAL Root Directory"

    class AutoDetectRootDirectory(settings.Bool):
        """Attempt to find the OpenGOAL installation and the mod executables (gk.exe and goalc.exe)
        automatically. If set to true, the ArchipelaGOAL Root Directory setting is ignored."""
        description = "ArchipelaGOAL Auto Detect Root Directory"

    class EnforceFriendlyOptions(settings.Bool):
        """Enforce friendly player options in both single and multiplayer seeds. Disabling this allows for
        more disruptive and challenging options, but may impact seed generation. Use at your own risk!"""
        description = "ArchipelaGOAL Enforce Friendly Options"

    root_directory: RootDirectory = RootDirectory(
        "%programfiles%/OpenGOAL-Launcher/features/jak1/mods/JakMods/archipelagoal")
    auto_detect_root_directory: Union[AutoDetectRootDirectory, bool] = True
    enforce_friendly_options: Union[EnforceFriendlyOptions, bool] = True


class JakAndDaxterWebWorld(WebWorld):
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up ArchipelaGOAL (Archipelago on OpenGOAL).",
        "English",
        "setup_en.md",
        "setup/en",
        ["markustulliuscicero"]
    )

    tutorials = [setup_en]

    option_groups = [
        OptionGroup("Orbsanity", [
            Options.EnableOrbsanity,
            Options.GlobalOrbsanityBundleSize,
            Options.PerLevelOrbsanityBundleSize,
        ]),
        OptionGroup("Power Cell Counts", [
            Options.EnableOrderedCellCounts,
            Options.FireCanyonCellCount,
            Options.MountainPassCellCount,
            Options.LavaTubeCellCount,
        ]),
        OptionGroup("Orb Trade Counts", [
            Options.CitizenOrbTradeAmount,
            Options.OracleOrbTradeAmount,
        ]),
    ]


class JakAndDaxterWorld(World):
    """
    Jak and Daxter: The Precursor Legacy is a 2001 action platformer developed by Naughty Dog
    for the PlayStation 2. The game follows the eponymous protagonists, a young boy named Jak
    and his friend Daxter, who has been transformed into an ottsel. With the help of Samos
    the Sage of Green Eco and his daughter Keira, the pair travel north in search of a cure for Daxter,
    discovering artifacts created by an ancient race known as the Precursors along the way. When the
    rogue sages Gol and Maia Acheron plan to flood the world with Dark Eco, they must stop their evil plan
    and save the world.
    """
    # ID, name, version
    game = jak1_name
    required_client_version = (0, 4, 6)

    # Options
    settings: ClassVar[JakAndDaxterSettings]
    options_dataclass = Options.JakAndDaxterOptions
    options: Options.JakAndDaxterOptions

    # Web world
    web = JakAndDaxterWebWorld()

    # Stored as {ID: Name} pairs, these must now be swapped to {Name: ID} pairs.
    # Remember, the game ID and various offsets for each item type have already been calculated.
    item_name_to_id = {item_table[k]: k for k in item_table}
    location_name_to_id = {location_table[k]: k for k in location_table}
    item_name_groups = {
        "Power Cells": set(cell_item_table.values()),
        "Scout Flies": set(scout_item_table.values()),
        "Specials": set(special_item_table.values()),
        "Moves": set(move_item_table.values()),
        "Precursor Orbs": set(orb_item_table.values()),
    }
    location_name_groups = {
        "Power Cells": set(cell_location_table.values()),
        "Scout Flies": set(scout_location_table.values()),
        "Specials": set(special_location_table.values()),
        "Orb Caches": set(cache_location_table.values()),
        "Precursor Orbs": set(orb_location_table.values()),
        "Trades": {location_table[Cells.to_ap_id(k)] for k in
                   {11, 12, 31, 32, 33, 96, 97, 98, 99, 13, 14, 34, 35, 100, 101}},
        "'Free 7 Scout Flies' Power Cells": set(Cells.loc7SF_cellTable.values()),
    }

    # These functions and variables are Options-driven, keep them as instance variables here so that we don't clog up
    # the seed generation routines with options checking. So we set these once, and then just use them as needed.
    can_trade: Callable[[CollectionState, int, Optional[int]], bool]
    orb_bundle_item_name: str = ""
    orb_bundle_size: int = 0
    total_trade_orbs: int = 0
    power_cell_thresholds: List[int] = []

    # Handles various options validation, rules enforcement, and caching of important information.
    def generate_early(self) -> None:

        # Cache the power cell threshold values for quicker reference.
        self.power_cell_thresholds = []
        self.power_cell_thresholds.append(self.options.fire_canyon_cell_count.value)
        self.power_cell_thresholds.append(self.options.mountain_pass_cell_count.value)
        self.power_cell_thresholds.append(self.options.lava_tube_cell_count.value)
        self.power_cell_thresholds.append(100)  # The 100 Power Cell Door.

        # Order the thresholds ascending and set the options values to the new order.
        # TODO - How does this affect region access rules and other things?
        try:
            if self.options.enable_ordered_cell_counts:
                self.power_cell_thresholds.sort()
                self.options.fire_canyon_cell_count.value = self.power_cell_thresholds[0]
                self.options.mountain_pass_cell_count.value = self.power_cell_thresholds[1]
                self.options.lava_tube_cell_count.value = self.power_cell_thresholds[2]
        except IndexError:
            pass  # Skip if not possible.

        # For the fairness of other players in a multiworld game, enforce some friendly limitations on our options,
        # so we don't cause chaos during seed generation. These friendly limits should **guarantee** a successful gen.
        enforce_friendly_options = Utils.get_settings()["jakanddaxter_options"]["enforce_friendly_options"]
        if enforce_friendly_options:
            if self.multiworld.players > 1:
                from .Rules import enforce_multiplayer_limits
                enforce_multiplayer_limits(self)
            else:
                from .Rules import enforce_singleplayer_limits
                enforce_singleplayer_limits(self)

        # Verify that we didn't overload the trade amounts with more orbs than exist in the world.
        # This is easy to do by accident even in a singleplayer world.
        self.total_trade_orbs = (9 * self.options.citizen_orb_trade_amount) + (6 * self.options.oracle_orb_trade_amount)
        from .Rules import verify_orb_trade_amounts
        verify_orb_trade_amounts(self)

        # Cache the orb bundle size and item name for quicker reference.
        if self.options.enable_orbsanity == Options.EnableOrbsanity.option_per_level:
            self.orb_bundle_size = self.options.level_orbsanity_bundle_size.value
            self.orb_bundle_item_name = orb_item_table[self.orb_bundle_size]
        elif self.options.enable_orbsanity == Options.EnableOrbsanity.option_global:
            self.orb_bundle_size = self.options.global_orbsanity_bundle_size.value
            self.orb_bundle_item_name = orb_item_table[self.orb_bundle_size]
        else:
            self.orb_bundle_size = 0
            self.orb_bundle_item_name = ""

        # Options drive which trade rules to use, so they need to be setup before we create_regions.
        from .Rules import set_orb_trade_rule
        set_orb_trade_rule(self)

    # This will also set Locations, Location access rules, Region access rules, etc.
    def create_regions(self) -> None:
        from .Regions import create_regions
        create_regions(self)

        # from Utils import visualize_regions
        # visualize_regions(self.multiworld.get_region("Menu", self.player), "jakanddaxter.puml")

    # Helper function to reuse some nasty if/else trees. This outputs a list of pairs of item count and classification.
    # For instance, not all 101 power cells need to be marked progression if you only need 72 to beat the game. So we
    # will have 72 Progression Power Cells, and 29 Filler Power Cells.
    def item_type_helper(self, item) -> List[Tuple[int, ItemClass]]:
        counts_and_classes: List[Tuple[int, ItemClass]] = []

        # Make 101 Power Cells. We only want AP's Progression Fill routine to handle the amount of cells we need
        # to reach the furthest possible region. Even for early completion goals, all areas in the game must be
        # reachable or generation will fail. TODO - Option-driven region creation would be an enormous refactor.
        if item in range(jak1_id, jak1_id + Scouts.fly_offset):

            # If for some unholy reason we don't have the list of power cell thresholds, have a fallback plan.
            if self.power_cell_thresholds:
                prog_count = max(self.power_cell_thresholds[:3])
                non_prog_count = 101 - prog_count

                if self.options.jak_completion_condition == Options.CompletionCondition.option_open_100_cell_door:
                    counts_and_classes.append((100, ItemClass.progression_skip_balancing))
                    counts_and_classes.append((1, ItemClass.filler))
                else:
                    counts_and_classes.append((prog_count, ItemClass.progression_skip_balancing))
                    counts_and_classes.append((non_prog_count, ItemClass.filler))
            else:
                counts_and_classes.append((101, ItemClass.progression_skip_balancing))

        # Make 7 Scout Flies per level.
        elif item in range(jak1_id + Scouts.fly_offset, jak1_id + Specials.special_offset):
            counts_and_classes.append((7, ItemClass.progression_skip_balancing))

        # Make only 1 of each Special Item.
        elif item in range(jak1_id + Specials.special_offset, jak1_id + Caches.orb_cache_offset):
            counts_and_classes.append((1, ItemClass.progression | ItemClass.useful))

        # Make only 1 of each Move Item.
        elif item in range(jak1_id + Caches.orb_cache_offset, jak1_id + Orbs.orb_offset):
            counts_and_classes.append((1, ItemClass.progression | ItemClass.useful))

        # Make N Precursor Orb bundles, where N is 2000 // bundle size. Like Power Cells, only a fraction of these will
        # be marked as Progression with the remainder as Filler, but they are still entirely fungible.
        elif item in range(jak1_id + Orbs.orb_offset, jak1_max):

            # Don't divide by zero!
            if self.orb_bundle_size > 0:
                item_count = 2000 // self.orb_bundle_size  # Integer division here, bundle size is a factor of 2000.

                # Have enough bundles to do all trades. The rest can be filler.
                prog_count = ceil(self.total_trade_orbs / self.orb_bundle_size)
                non_prog_count = item_count - prog_count

                counts_and_classes.append((prog_count, ItemClass.progression_skip_balancing))
                counts_and_classes.append((non_prog_count, ItemClass.filler))
            else:
                counts_and_classes.append((0, ItemClass.filler))  # No orbs in a bundle means no bundles.

        # Under normal circumstances, we create 0 green eco fillers. We will manually create filler items as needed.
        elif item == jak1_max:
            counts_and_classes.append((0, ItemClass.filler))

        # If we try to make items with ID's higher than we've defined, something has gone wrong.
        else:
            raise KeyError(f"Tried to fill item pool with unknown ID {item}.")

        return counts_and_classes

    def create_items(self) -> None:
        for item_name in self.item_name_to_id:
            item_id = self.item_name_to_id[item_name]

            # Handle Move Randomizer option.
            # If it is OFF, put all moves in your starting inventory instead of the item pool,
            # then fill the item pool with a corresponding amount of filler items.
            if item_name in self.item_name_groups["Moves"] and not self.options.enable_move_randomizer:
                self.multiworld.push_precollected(self.create_item(item_name))
                self.multiworld.itempool.append(self.create_filler())
                continue

            # Handle Orbsanity option.
            # If it is OFF, don't add any orb bundles to the item pool, period.
            # If it is ON, don't add any orb bundles that don't match the chosen option.
            if (item_name in self.item_name_groups["Precursor Orbs"]
                and (self.options.enable_orbsanity == Options.EnableOrbsanity.option_off
                     or item_name != self.orb_bundle_item_name)):
                continue

            # In every other scenario, do this. Not all items with the same name will have the same classification.
            counts_and_classes = self.item_type_helper(item_id)
            for (count, classification) in counts_and_classes:
                self.multiworld.itempool += [JakAndDaxterItem(item_name, classification, item_id, self.player)
                                             for _ in range(count)]

    def create_item(self, name: str) -> Item:
        item_id = self.item_name_to_id[name]
        _, classification = self.item_type_helper(item_id)[0]  # Use first tuple (will likely be the most important).
        return JakAndDaxterItem(name, classification, item_id, self.player)

    def get_filler_item_name(self) -> str:
        return "Green Eco Pill"

    def collect(self, state: CollectionState, item: Item) -> bool:
        change = super().collect(state, item)
        if change:
            # Orbsanity as an option is no-factor to these conditions. Matching the item name implies Orbsanity is ON,
            # so we don't need to check the option. When Orbsanity is OFF, there won't even be any orb bundle items
            # to collect.

            # Orb items do not intrinsically unlock anything that contains more Reachable Orbs, so they do not need to
            # set the cache to stale. They just change how many orbs you have to trade with.
            if item.name == self.orb_bundle_item_name:
                state.prog_items[self.player]["Tradeable Orbs"] += self.orb_bundle_size  # Give a bundle of Trade Orbs

            # Scout Flies ALSO do not unlock anything that contains more Reachable Orbs, NOR do they give you more
            # tradeable orbs. So let's just pass on them.
            elif item.name in self.item_name_groups["Scout Flies"]:
                pass

            # Power Cells DO unlock new regions that contain more Reachable Orbs - the connector levels and new
            # hub levels - BUT they only do that when you have a number of them equal to one of the threshold values.
            elif (item.name == "Power Cell"
                  and state.count("Power Cell", self.player) not in self.power_cell_thresholds):
                pass

            # However, every other item that changes the CollectionState should set the cache to stale, because they
            # likely made it possible to reach more orb locations (level unlocks, region unlocks, etc.).
            else:
                state.prog_items[self.player]["Reachable Orbs Fresh"] = False
        return change

    def remove(self, state: CollectionState, item: Item) -> bool:
        change = super().remove(state, item)
        if change:

            # Do the same thing we did in collect, except subtract trade orbs instead of add.
            if item.name == self.orb_bundle_item_name:
                state.prog_items[self.player]["Tradeable Orbs"] -= self.orb_bundle_size  # Take a bundle of Trade Orbs

            # Ditto Scout Flies.
            elif item.name in self.item_name_groups["Scout Flies"]:
                pass

            # Ditto Power Cells, but check count + 1, because we potentially crossed the threshold in the opposite
            # direction. E.g. we've removed the 20th power cell, our count is now 19, so we should stale the cache.
            elif (item.name == "Power Cell"
                  and state.count("Power Cell", self.player) + 1 not in self.power_cell_thresholds):
                pass

            # Ditto everything else.
            else:
                state.prog_items[self.player]["Reachable Orbs Fresh"] = False

            # TODO - Python 3.8 compatibility, remove this block when no longer required.
            if state.prog_items[self.player]["Tradeable Orbs"] < 1:
                del state.prog_items[self.player]["Tradeable Orbs"]
            if state.prog_items[self.player]["Reachable Orbs"] < 1:
                del state.prog_items[self.player]["Reachable Orbs"]
            for level in level_table:
                if state.prog_items[self.player][f"{level} Reachable Orbs".strip()] < 1:
                    del state.prog_items[self.player][f"{level} Reachable Orbs".strip()]

        return change

    def fill_slot_data(self) -> Dict[str, Any]:
        return self.options.as_dict("enable_move_randomizer",
                                    "enable_orbsanity",
                                    "global_orbsanity_bundle_size",
                                    "level_orbsanity_bundle_size",
                                    "fire_canyon_cell_count",
                                    "mountain_pass_cell_count",
                                    "lava_tube_cell_count",
                                    "citizen_orb_trade_amount",
                                    "oracle_orb_trade_amount",
                                    "jak_completion_condition",
                                    "require_punch_for_klaww",)
