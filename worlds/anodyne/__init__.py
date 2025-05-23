import itertools
import logging
import typing
from collections import defaultdict
from dataclasses import dataclass

from BaseClasses import Region, Location, Item, ItemClassification, CollectionState, Tutorial
from Fill import fill_restrictive, FillError
from Options import Accessibility
from worlds.AutoWorld import WebWorld, World
from typing import List, Callable, Dict, Any, Set, Iterable, Mapping, Type, Tuple

from . import Constants
from .Constants import AccessRule

from .Data import Items, Locations, Regions, Exits, Events
from .Data.Items import big_keys
from .Options import AnodyneGameOptions, SmallKeyShuffle, StartBroom, VictoryCondition, BigKeyShuffle, \
    HealthCicadaShuffle, NexusGatesOpen, RedCaveAccess, PostgameMode, NexusGateShuffle, TrapPercentage, SmallKeyMode, \
    Dustsanity, GateType, gatereq_classes, CardAmount, EndgameRequirement, GateRequirements, MitraHints, gate_lookup, \
    OverworldFieldsGate


class AnodyneLocation(Location):
    game = "Anodyne"


class AnodyneItem(Item):
    game = "Anodyne"


class AnodyneWebWorld(WebWorld):
    theme = "dirt"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Anodyne with Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["PixieCatSupreme", "SephDB", "hatkirby"]
    )]


class AnodyneWorld(World):
    """
    Anodyne is a unique Zelda-like game, influenced by games such as Yume Nikki and Link's Awakening. 
    In Anodyne, you'll visit areas urban, natural, and bizarre, fighting your way through dungeons 
    and areas in Young's subconscious.
    """
    game = "Anodyne"  # name of the game/world
    web = AnodyneWebWorld()

    options_dataclass = AnodyneGameOptions
    options: AnodyneGameOptions
    topology_present = False  # show path to required location checks in spoiler

    ut_can_gen_without_yaml = True

    data_version = 1

    item_name_to_id = Constants.item_name_to_id
    location_name_to_id = Constants.location_name_to_id
    item_name_groups = Items.item_groups
    location_name_groups = Locations.location_groups

    gates_unlocked: List[str]
    location_count: int
    dungeon_items: Dict[str, List[Item]]
    proxy_rules: Dict[str, List[str]]
    shuffled_gates: Set[str]

    def generate_early(self):
        self.gates_unlocked = []
        self.location_count = 0
        self.dungeon_items = dict()
        self.proxy_rules = dict()
        self.shuffled_gates = set()

        nexus_gate_open = self.options.nexus_gates_open

        # Street is always unlocked
        if hasattr(self.multiworld, "re_gen_passthrough") and "Anodyne" in self.multiworld.re_gen_passthrough:
            # Universal tracker; ignored during normal gen.
            slot_data = self.multiworld.re_gen_passthrough["Anodyne"]

            self.gates_unlocked = slot_data["nexus_gates_unlocked"]
            self.options.big_key_shuffle.value = slot_data["shuffle_big_gates"]
            self.options.split_windmill.value = slot_data["split_windmill"]
            self.options.postgame_mode.value = slot_data["postgame_mode"]
            self.options.nexus_gate_shuffle.value = slot_data["nexus_gate_shuffle"]
            self.options.victory_condition.value = slot_data["victory_condition"]
            self.options.forest_bunny_chest.value = slot_data.get("forest_bunny_chest", False)
            self.options.fields_secret_paths.value = slot_data.get("fields_secret_paths", False)
            if "endgame_card_requirement" in slot_data:
                EndgameRequirement.cardoption(self.options).value = slot_data["endgame_card_requirement"]

            self.options.card_amount.value = slot_data.get("card_amount", CardAmount.option_vanilla)
            #For universal tracker, slot data already has final value for card amount + extra, extra can be set to 0
            self.options.extra_cards.value = 0
            for c in gatereq_classes:
                option_name: str = slot_data.get(c.typename(), c.shorthand(self.options))
                type_option = c.typeoption(self.options)
                if option_name.startswith("cards"):
                    type_option.value = GateType.CARDS
                    c.cardoption(self.options).value = int(option_name[len("cards_"):])
                elif option_name.startswith("bosses"):
                    type_option.value = GateType.BOSSES
                    c.bossoption(self.options).value = int(option_name[len("bosses_"):])
                else:
                    type_option.value = type_option.from_text(option_name).value
            self.options.dustsanity.value = 0 if str(slot_data.get("dust_sanity_base", "Disabled")) == "Disabled" else 1
        elif len(self.options.custom_nexus_gates_open.value) > 0:
            self.gates_unlocked.extend(self.options.custom_nexus_gates_open.value)
        elif nexus_gate_open == NexusGatesOpen.option_street_and_fields:
            self.gates_unlocked.append("Fields")
        elif nexus_gate_open == NexusGatesOpen.option_early:
            for region_name in Regions.early_nexus_gates:
                self.gates_unlocked.append(region_name)
        elif nexus_gate_open == NexusGatesOpen.option_all:
            for region_name in Regions.regions_with_nexus_gate:
                self.gates_unlocked.append(region_name)
        elif nexus_gate_open in [NexusGatesOpen.option_random_count, NexusGatesOpen.option_random_pre_endgame]:
            random_nexus_gate_count = int(self.options.random_nexus_gate_open_count)

            available_gates = Regions.regions_with_nexus_gate.copy()
            if nexus_gate_open == NexusGatesOpen.option_random_pre_endgame:
                for gate in Regions.endgame_nexus_gates:
                    available_gates.remove(gate)

            if random_nexus_gate_count > len(available_gates):
                logging.warning(
                    f"Player {self.player_name} requested more random Nexus gates than are available. Adjusting down to {len(available_gates)}")
                random_nexus_gate_count = len(available_gates)

            self.gates_unlocked = self.random.sample(available_gates, random_nexus_gate_count)

        if self.options.small_key_mode == SmallKeyMode.option_key_rings and self.options.small_key_shuffle == SmallKeyShuffle.option_vanilla:
            self.options.small_key_shuffle.value = SmallKeyShuffle.option_original_dungeon
            self.options.small_key_mode.value = SmallKeyMode.option_small_keys
            logging.warning(
                f"Player {self.player_name} requested vanilla small keys with key rings on, changing to small key original dungeon")

        if self.options.nexus_gate_shuffle != NexusGateShuffle.option_off:
            self.shuffled_gates = set(Regions.regions_with_nexus_gate) - set(self.gates_unlocked)

            if self.options.nexus_gate_shuffle == NexusGateShuffle.option_all_except_endgame:
                self.shuffled_gates -= set(Regions.endgame_nexus_gates)
        if self.options.victory_condition == VictoryCondition.option_final_gate and self.options.postgame_mode == PostgameMode.option_disabled:
            logging.warning(
                f"Player {self.player_name} requested the final gate victory condition but turned off postgame. Changing goal to Briar")
            self.options.victory_condition.value = VictoryCondition.option_defeat_briar

        if all(gate in Regions.wrong_big_key_early_locked_nexus_gates for gate in self.gates_unlocked) and \
                self.options.nexus_gate_shuffle == NexusGateShuffle.option_off and \
                self.options.big_key_shuffle == BigKeyShuffle.option_vanilla and \
                OverworldFieldsGate.typeoption(self.options) in [GateType.BLUE, GateType.RED]:
            logging.warning(
                f"Player {self.player_name} has locked themselves into the starting area with no escape. Reverting Overworld->Fields gate to default")
            OverworldFieldsGate.typeoption(self.options).value = GateType.GREEN

    def create_item(self, name: str) -> Item:
        if name in Items.progression_items:
            item_class = ItemClassification.progression
        elif name in Items.useful_items:
            item_class = ItemClassification.useful
        elif name in Items.trap_items:
            item_class = ItemClassification.trap
        else:
            item_class = ItemClassification.filler

        return AnodyneItem(name, item_class, self.item_name_to_id.get(name, None), self.player)

    def create_items(self) -> None:
        item_pool: List[Item] = []
        local_item_pool: set[str] = set()
        non_local_item_pool: set[str] = set()

        small_key_mode: SmallKeyMode = self.options.small_key_mode
        small_key_shuffle: SmallKeyShuffle = self.options.small_key_shuffle
        health_cicada_shuffle = self.options.health_cicada_shuffle
        big_key_shuffle = self.options.big_key_shuffle
        start_broom: StartBroom = self.options.start_broom

        placed_items = 0

        excluded_items: set[str] = {
            *Items.small_key_item_count.keys(),
            *Items.key_rings,
            *Items.big_keys,
            "Health Cicada",
            *Items.filler_items,
            *Items.trap_items,
            "Progressive Red Cave",
            "Progressive Swap",
            *Items.nexus_gate_items.keys(),
            *Items.cards
        }

        if small_key_mode == SmallKeyMode.option_small_keys:
            if small_key_shuffle == SmallKeyShuffle.option_vanilla:
                for location in Locations.all_locations:
                    if location.small_key:
                        dungeon = Regions.dungeon_area_to_dungeon[location.region_name]
                        item_name = f"Small Key ({dungeon})"
                        self.multiworld.get_location(location.name, self.player).place_locked_item(
                            self.create_item(item_name))
                        placed_items += 1
            elif small_key_shuffle == SmallKeyShuffle.option_original_dungeon:
                for dungeon in Regions.dungeon_areas.keys():
                    small_key_name = f"Small Key ({dungeon})"
                    items = self.dungeon_items.setdefault(dungeon, [])

                    for _ in range(Items.small_key_item_count[small_key_name]):
                        items.append(self.create_item(small_key_name))
                        placed_items += 1
            else:
                for key_item, key_count in Items.small_key_item_count.items():
                    placed_items += key_count

                    for _ in range(key_count):
                        item_pool.append(self.create_item(key_item))

                    if small_key_shuffle == SmallKeyShuffle.option_own_world:
                        local_item_pool.add(key_item)
                    elif small_key_shuffle == SmallKeyShuffle.option_different_world:
                        non_local_item_pool.add(key_item)
        elif small_key_mode == SmallKeyMode.option_key_rings:
            for key_item in Items.key_rings:
                placed_items += 1
                item = self.create_item(key_item)

                if small_key_shuffle == SmallKeyShuffle.option_original_dungeon:
                    self.dungeon_items.setdefault(key_item[len("Key Ring ("):-1], []).append(item)
                else:
                    item_pool.append(item)

                    if small_key_shuffle == SmallKeyShuffle.option_own_world:
                        local_item_pool.add(key_item)
                    elif small_key_shuffle == SmallKeyShuffle.option_different_world:
                        non_local_item_pool.add(key_item)

        start_broom_item: str = ""
        if start_broom == StartBroom.option_normal:
            start_broom_item = "Broom"
        elif start_broom == StartBroom.option_wide:
            start_broom_item = "Widen"
        elif start_broom == StartBroom.option_long:
            start_broom_item = "Extend"
        elif start_broom == StartBroom.option_swap:
            if self.options.postgame_mode == PostgameMode.option_progressive:
                # This is kind of an odd combination of options tbh.
                start_broom_item = "Progressive Swap"
            else:
                start_broom_item = "Swap"

        if start_broom_item != "":
            self.multiworld.push_precollected(self.create_item(start_broom_item))
            excluded_items.add(start_broom_item)

        if health_cicada_shuffle != HealthCicadaShuffle.option_vanilla:
            health_cicada_amount = len([location for location in Locations.all_locations if location.health_cicada])
            placed_items += health_cicada_amount
            item_name = "Health Cicada"

            if health_cicada_shuffle == HealthCicadaShuffle.option_own_world:
                local_item_pool.add(item_name)
            elif health_cicada_shuffle == HealthCicadaShuffle.option_different_world:
                non_local_item_pool.add(item_name)

            for _ in range(health_cicada_amount):
                item_pool.append(self.create_item(item_name))

        if big_key_shuffle not in [BigKeyShuffle.option_vanilla, BigKeyShuffle.option_unlocked]:
            placed_items += len(Items.big_keys)

            for big_key in Items.big_keys:
                item_pool.append(self.create_item(big_key))

                if big_key_shuffle == BigKeyShuffle.option_own_world:
                    local_item_pool.add(big_key)
                elif big_key_shuffle == BigKeyShuffle.option_different_world:
                    non_local_item_pool.add(big_key)

        if self.options.red_cave_access != RedCaveAccess.option_vanilla:
            placed_items += 3

            pool: List[Item] = item_pool
            if self.options.red_cave_access == RedCaveAccess.option_original_dungeon:
                pool = self.dungeon_items.setdefault("Red Cave", [])

            for _ in range(3):
                pool.append(self.create_item("Progressive Red Cave"))

        if not self.options.split_windmill:
            excluded_items.update(Items.statue_items)

        if self.options.postgame_mode == PostgameMode.option_disabled:
            excluded_items.update(Items.postgame_cards)

        if self.options.postgame_mode == PostgameMode.option_progressive:
            item_pool.append(self.create_item("Progressive Swap"))
            placed_items += 1

            if start_broom != StartBroom.option_swap:
                item_pool.append(self.create_item("Progressive Swap"))
                placed_items += 1

            excluded_items.add("Swap")

        if self.options.nexus_gate_shuffle != NexusGateShuffle.option_off:
            nexus_gate_items = [item_name for item_name, region in Items.nexus_gate_items.items()
                                if region in self.shuffled_gates]
            item_pool.extend(self.create_item(item_name) for item_name in nexus_gate_items)
            placed_items += len(nexus_gate_items)

        for name in Items.all_items:
            if name not in excluded_items:
                placed_items += 1
                item_pool.append(self.create_item(name))

        max_cards = self.location_count - placed_items
        card_gates_in_logic = [cls for cls in gatereq_classes
                               if cls.typeoption(self.options) == GateType.CARDS and
                               (
                                       self.options.postgame_mode != PostgameMode.option_disabled
                                       or cls.GateCardReq.default <= 36)]
        requested_cards = max((cls.cardoption(self.options) for cls in card_gates_in_logic), default=0)
        if self.options.extra_cards > max_cards:
            # make sure extra cards can't overflow the game's card list
            self.options.extra_cards.value = max_cards
        if self.options.card_amount == CardAmount.option_vanilla:
            self.options.card_amount.value = 37 if self.options.postgame_mode == PostgameMode.option_disabled else 49
        elif self.options.card_amount == CardAmount.option_auto:
            self.options.card_amount.value = int(requested_cards)
        if self.options.card_amount + self.options.extra_cards > max_cards:
            self.options.card_amount.value = max_cards - self.options.extra_cards

        for cls in card_gates_in_logic:
            if cls.cardoption(self.options) > self.options.card_amount:
                cls.cardoption(self.options).value = self.options.card_amount.value

        for card in Items.cards[:self.options.card_amount + self.options.extra_cards]:
            placed_items += 1
            item_pool.append(self.create_item(card))

        # If we have space for filler, prioritize adding in the ??? items that would be in-logic. Also add traps,
        # if enabled.
        if placed_items < self.location_count:
            new_items = []

            remaining_items = self.location_count - placed_items
            num_traps = int(self.options.traps_percentage / 100 * remaining_items)
            remaining_items -= num_traps

            for i in range(num_traps):
                new_items.append(self.random.choice(Items.trap_items))

            secret_items = Items.early_secret_items if self.options.postgame_mode == PostgameMode.option_disabled \
                else Items.secret_items

            if self.options.postgame_mode == PostgameMode.option_disabled and self.options.fields_secret_paths:
                secret_items = [*secret_items, *Items.secret_items_secret_paths]

            if len(secret_items) <= remaining_items:
                new_items.extend(secret_items)
            else:
                new_items.extend(self.random.sample(secret_items, remaining_items))

            item_pool.extend(self.create_item(name) for name in new_items)
            placed_items += len(new_items)

        # If there's any space left after that, fill the slots with random filler.
        if placed_items < self.location_count:
            item_pool.extend(self.create_filler() for _ in range(self.location_count - placed_items))

        self.multiworld.itempool += item_pool

        self.options.local_items.value |= local_item_pool
        self.options.non_local_items.value |= non_local_item_pool

    def create_regions(self) -> None:
        include_health_cicadas = self.options.health_cicada_shuffle
        include_big_keys = self.options.big_key_shuffle
        include_postgame: bool = (self.options.postgame_mode != PostgameMode.option_disabled)
        dustsanity: bool = bool(self.options.dustsanity.value)

        postgame_regions = Regions.postgame_regions if self.options.fields_secret_paths.value else Regions.postgame_regions + Regions.postgame_without_secret_paths

        all_regions: Dict[str, Region] = {}

        for region_name in Regions.all_regions:
            if not include_postgame and region_name in postgame_regions:
                continue

            region = Region(region_name, self.player, self.multiworld)
            if region_name in Locations.locations_by_region:
                for location in Locations.locations_by_region[region_name]:
                    reqs: list[str] = location.reqs.copy()

                    if include_health_cicadas == HealthCicadaShuffle.option_vanilla and location.health_cicada:
                        continue

                    if include_big_keys == BigKeyShuffle.option_vanilla and location.big_key:
                        continue

                    if self.options.red_cave_access == RedCaveAccess.option_vanilla and location.tentacle:
                        continue

                    if not self.options.split_windmill and location.name == "Windmill - Activation":
                        continue

                    if not include_postgame and location.postgame(bool(self.options.fields_secret_paths.value)):
                        continue

                    if not self.options.forest_bunny_chest and location.name == "Deep Forest - Bunny Chest":
                        continue

                    if self.options.victory_condition == VictoryCondition.option_defeat_briar \
                            and location.name == "GO - Defeat Briar":
                        continue

                    if location.nexus_gate and location.region_name not in self.shuffled_gates:
                        continue

                    if location.dust:
                        if dustsanity:
                            reqs.append("Combat")
                        else:
                            continue

                    location_id = Constants.location_name_to_id[location.name]

                    new_location = AnodyneLocation(self.player, location.name, location_id, region)
                    new_location.access_rule = Constants.get_access_rule(reqs, region_name, self)
                    region.locations.append(new_location)

                    self.location_count += 1

            all_regions[region_name] = region

        for exit_vals in (
                Exits.all_exits if not self.options.fields_secret_paths.value else Exits.all_exits + Exits.secret_path_connections):
            exit1: str = exit_vals[0]
            exit2: str = exit_vals[1]
            requirements: list[str] = exit_vals[2]

            if not include_postgame and (exit1 in postgame_regions or exit2 in postgame_regions or "Progressive Swap:2" in requirements):
                continue

            r1 = all_regions[exit1]
            r2 = all_regions[exit2]

            e = r1.create_exit(f"{exit1} to {exit2} exit")
            e.connect(r2)
            e.access_rule = Constants.get_access_rule(requirements, exit1, self)

        for region_name in self.gates_unlocked:
            all_regions["Nexus bottom"].create_exit(f"{region_name} Nexus Gate").connect(all_regions[region_name])

        if self.options.nexus_gate_shuffle != NexusGateShuffle.option_off:
            for item_name, region_name in Items.nexus_gate_items.items():
                if region_name in self.shuffled_gates:
                    e = all_regions["Nexus bottom"].create_exit(f"{region_name} Nexus Gate")
                    e.connect(all_regions[region_name])
                    e.access_rule = Constants.get_access_rule([item_name], "Nexus bottom", self)

        for region_name, events in Events.events_by_region.items():
            if not include_postgame and region_name in postgame_regions:
                continue

            for event_name in events:
                if include_big_keys != BigKeyShuffle.option_vanilla and event_name in Items.big_keys:
                    continue

                requirements: list[str] = Events.events_by_region[region_name][event_name]
                self.create_event(all_regions[region_name], event_name, Constants.get_access_rule(requirements,
                                                                                                  region_name, self))

        self.multiworld.regions += all_regions.values()

        if Constants.debug_mode:
            from Utils import visualize_regions

            visualize_regions(self.multiworld.get_region("Menu", self.player), "my_world.puml")

    def create_gate_proxy_rule(self, cls: typing.Type[GateRequirements]):
        rules = []

        gatetype = cls.typeoption(self.options)
        if gatetype == GateType.CARDS:
            rules = [f"Cards:{cls.cardoption(self.options)}"]
        elif gatetype == GateType.BOSSES:
            rules = [f"Bosses:{cls.bossoption(self.options)}"]
        elif gatetype == GateType.UNLOCKED:
            pass
        else:
            rules = [f"{GateType(gatetype).name.title()} Key"]

        self.proxy_rules[cls.typename()] = rules

    def set_rules(self) -> None:
        if not self.options.split_windmill:
            for statue in Items.statue_items:
                self.proxy_rules[statue] = ["Windmill activated"]

        if self.options.big_key_shuffle == BigKeyShuffle.option_unlocked:
            for big_key in big_keys:
                self.proxy_rules[big_key] = []
        elif self.options.big_key_shuffle == BigKeyShuffle.option_vanilla:
            for big_key in big_keys:
                self.proxy_rules[big_key] = [f"Grab {big_key}"]

        if self.options.small_key_mode == SmallKeyMode.option_unlocked:
            for dungeon, amount in Items.small_key_item_count.items():
                for i in range(amount):
                    self.proxy_rules[f"{dungeon}:{i + 1}"] = []
        elif self.options.small_key_mode == SmallKeyMode.option_key_rings:
            for dungeon, amount in Items.small_key_item_count.items():
                dungeon_name = dungeon[len("Small Key ("):-1]
                for i in range(amount):
                    self.proxy_rules[f"{dungeon}:{i + 1}"] = [f"Key Ring ({dungeon_name})"]
        elif self.options.small_key_mode == SmallKeyMode.option_small_keys and self.options.small_key_shuffle == SmallKeyShuffle.option_vanilla:
            # For vanilla key placement, the regular rules don't quite match up in this dungeon, but the dungeon is still solvable
            for i in range(Items.small_key_item_count["Small Key (Hotel)"]):
                self.proxy_rules[f"Small Key (Hotel):{i + 1}"] = []

        if self.options.red_cave_access == RedCaveAccess.option_vanilla:
            self.proxy_rules["RedCave-Left"] = ["Center left tentacle hit"]
            self.proxy_rules["RedCave-Right"] = ["Center right tentacle hit"]
            self.proxy_rules["RedCave-Top"] = ["Left tentacle hit", "Right tentacle hit"]
        else:
            self.proxy_rules["RedCave-Left"] = ["Progressive Red Cave"]
            self.proxy_rules["RedCave-Right"] = ["Progressive Red Cave:2"]
            self.proxy_rules["RedCave-Top"] = ["Progressive Red Cave:3"]

        if self.options.randomize_color_puzzle:
            self.proxy_rules["GO Color Puzzle"] = ["Defeat Servants", "Defeat Watcher", "Defeat Manager"]
        else:
            self.proxy_rules["GO Color Puzzle"] = []

        if self.options.postgame_mode != PostgameMode.option_progressive:
            self.proxy_rules["Progressive Swap:1"] = ["Swap"]

            if self.options.postgame_mode == PostgameMode.option_vanilla:
                self.proxy_rules["Progressive Swap:2"] = ["Swap", "Defeat Briar"]
            elif self.options.postgame_mode == PostgameMode.option_unlocked:
                self.proxy_rules["Progressive Swap:2"] = ["Swap"]
            else:
                self.proxy_rules["Progressive Swap:2"] = ["Impossible"] #Shouldn't ever be asked for, but gives nice errors if it does

        for cls in gatereq_classes:
            self.create_gate_proxy_rule(cls)

        if self.options.fields_secret_paths.value:
            self.proxy_rules["SwapOrSecret"] = []
        else:
            self.proxy_rules["SwapOrSecret"] = ["Progressive Swap:2"]

        if self.options.nexus_gate_shuffle or \
                any(region in self.gates_unlocked for region in Regions.post_temple_boss_regions) and \
                self.options.small_key_shuffle != SmallKeyShuffle.option_vanilla:
            # There is one keyblock in Temple of the Seeing One that has conditional logic based on whether it is
            # possible for the player to access the exit of the dungeon early.
            self.proxy_rules["Temple Boss Access"] = ["Small Key (Temple of the Seeing One):3"]
        else:
            self.proxy_rules["Temple Boss Access"] = ["Small Key (Temple of the Seeing One):2"]

        victory_condition: VictoryCondition = self.options.victory_condition
        requirements: list[str] = []

        if victory_condition == VictoryCondition.option_defeat_briar:
            requirements.append("Defeat Briar")
        elif victory_condition == VictoryCondition.option_final_gate:
            requirements.append("Open final gate")

        self.multiworld.completion_condition[self.player] = Constants.get_access_rule(requirements, "Event", self)

        self.test_gate_requirements()

    def test_gate_requirements(self):
        state = CollectionState(self.multiworld)
        #This function runs before start_inventory gets put in precollected, so need to put them there ourselves
        for item, amount in self.options.start_inventory:
            for _ in range(amount):
                state.collect(self.create_item(item), True)
        state.sweep_for_advancements(self.multiworld.get_locations(self.player))

        #Counter to keep track of how much extra progression items we've placed
        placed_progression = 0

        def finished():
            return self.multiworld.has_beaten_game(state, self.player) and all(loc.can_reach(state) for loc in self.multiworld.get_locations(self.player))

        def sort_key(req:AnodyneWorld.LogicRequirement):
            # Reverse order for sorting lexicographically
            return (
                req.is_big_key_locked(), # Will only ever be true if big keys are fixed events
                req.needed_bosses(),
                req.unlockable_by_num_items(state),
                req.needed_cards(),
                req.name # Name to ensure unique and consistent sort order across seeds
            )

        gate_max_cards:Dict[Type[GateRequirements],int] = defaultdict(lambda:49)

        while not finished():
            max_placeable = len(self.multiworld.get_placeable_locations(state, self.player)) - placed_progression

            #Sorting on location and entrance name to have consistent sorting
            requirements = self.get_blocking_rules(state)
            for gate in (gate for r in requirements for gate in r.gates if r.is_gate_locked()):
                gate_max_cards[gate] = min(gate_max_cards[gate], max_placeable + state.count_group("Cards", self.player))

            requirements.sort(key=sort_key)
            to_fulfill = requirements[0]

            if to_fulfill.is_unlockable_by_items() and to_fulfill.unlockable_by_num_items(state) <= max_placeable:
                logging.debug(f"{len(requirements)},{to_fulfill.unlockable_by_num_items(state)},"
                              f"{to_fulfill._unlock_dict(state)}")
            else:
                unlockable_gates = [r for r in requirements if
                               r.is_gate_locked() and r.unlockable_by_num_items(state) - r.remaining_cards(
                                   state) <= max_placeable]
                if len(unlockable_gates) == 0:
                    logging.error("No gate to adjust and ran out of locations to put progression!")
                    return
                to_fulfill = unlockable_gates[0]

            if to_fulfill.gates:
                max_cards = (max_placeable - to_fulfill.unlockable_by_num_items(state) +
                             to_fulfill.remaining_cards(state) + state.count_group("Cards",self.player))
                if self.options.accessibility == Accessibility.option_minimal:
                    #Minimal can get itself very easily stuck behind card gates
                    max_cards = min(gate_max_cards[gate] for gate in to_fulfill.gates)
                max_bosses = state.count_from_list(Constants.groups["Bosses"], self.player)
                for cls in to_fulfill.gates:
                    if cls.typeoption(self.options) == GateType.BOSSES:
                        logging.warning(
                            f"Player {self.player_name} requested impossible gate. Adjusting {cls.typename()} down to {max_bosses} Bosses")
                        cls.bossoption(self.options).value = max_bosses
                    elif cls.typeoption(self.options) == GateType.CARDS:
                        opt = cls.cardoption(self.options)
                        if opt.value > max_cards:
                            logging.warning(
                                f"Player {self.player_name} requested impossible gate. Adjusting {cls.typename()} down to {max_cards} Cards")
                        opt.value = min(opt.value, max_cards)
                    else:
                        logging.warning(f"Player {self.player} requested self-locking big key gate. Opening up {cls.typename()}")
                        cls.typeoption(self.options).value = GateType.UNLOCKED
                    self.create_gate_proxy_rule(cls)  #Actually change the rule
                    state.stale[self.player] = True

            placed_progression += to_fulfill.unlockable_by_num_items(state)
            to_fulfill.collect(state)


            state.sweep_for_advancements(self.multiworld.get_locations(self.player))

    class LogicRequirement:
        def __init__(self, reqs: Iterable[str], world: "AnodyneWorld", name: str):
            self.requirements: Dict[str, int] = defaultdict(int)
            self.gates: Set[Type[GateRequirements]] = set()
            self.world = world
            self.name = name
            for item in reqs:
                if item in gate_lookup:
                    self.gates.add(gate_lookup[item])
                    continue
                count = 1
                if ':' in item:
                    item, count = item.split(':')
                    count = int(count)
                if self.requirements[item] < count:
                    self.requirements[item] = count

        def is_event_locked(self):
            return any(req in Events.all_events for req in self.requirements)

        def is_gate_locked(self):
            return len(self.gates) > 0

        def is_big_key_locked(self):
            return any(cls.typeoption(self.world.options) in [GateType.BLUE,GateType.RED,GateType.GREEN] for cls in self.gates)

        def is_unlockable_by_items(self):
            return not self.is_event_locked() and all(
                cls.typeoption(self.world.options) != GateType.BOSSES for cls in self.gates)

        def needed_bosses(self):
            return max([0, *[cls.bossoption(self.world.options) for cls in self.gates if
                             cls.typeoption(self.world.options) == GateType.BOSSES]])

        def needed_cards(self):
            return max([0, *[cls.cardoption(self.world.options) for cls in self.gates if
                             cls.typeoption(self.world.options) == GateType.CARDS]])

        def remaining_cards(self, state: CollectionState):
            return max(0, self.needed_cards() - state.count_group("Cards", self.world.player))

        def _unlock_dict(self, state: CollectionState):
            ret: Dict[str, int] = {}
            for item, amount in self.requirements.items():
                ret[item] = max(0, amount - state.count(item, self.world.player))
            for card in itertools.islice((c for c in Items.cards if not state.has(c, self.world.player)),
                                         self.remaining_cards(state)):
                ret[card] = 1
            return ret

        def unlockable_by_num_items(self, state: CollectionState):
            return sum(self._unlock_dict(state).values())

        def collect(self, state: CollectionState):
            for item in itertools.chain.from_iterable(itertools.repeat(i, n) for i, n in self._unlock_dict(state).items()):
                state.collect(self.world.create_item(item), True)

    def get_blocking_rules(self, state: CollectionState):
        blocked_rules: List[Tuple[AccessRule, str]] = [(loc.access_rule, loc.name) for region in
                                                       state.reachable_regions[self.player] for loc in
                                                       region.locations if not loc.access_rule(state)]
        # All our rules are of type AccessRule
        # noinspection PyTypeChecker
        blocked_rules.extend((e.access_rule, e.name) for e in state.blocked_connections[self.player])

        gate_types = [GateType.CARDS,GateType.BOSSES]
        if self.options.big_key_shuffle == BigKeyShuffle.option_vanilla:
            gate_types.extend([GateType.BLUE,GateType.RED,GateType.GREEN])

        def reqs(r: str) -> Iterable[str]:
            if r in self.proxy_rules and not (
                    r in gate_lookup and gate_lookup[r].typeoption(self.options) in gate_types):
                return itertools.chain(*[reqs(sub_r) for sub_r in self.proxy_rules[r]])
            elif not Constants.check_access(state, self, r, "blocking_check"):
                if r in Constants.groups:
                    #If it's a group, return any of them(mostly used for the Combat group)
                    return [Constants.groups[r][0]]
                else:
                    return [r]
            return []

        requirements = [
            AnodyneWorld.LogicRequirement(itertools.chain.from_iterable(reqs(r) for r in rule.reqs), self, name) for
            (rule, name) in blocked_rules]

        return [r for r in requirements if not r.is_event_locked()]

    def get_filler_item_name(self) -> str:
        return self.random.choice(Items.non_secret_filler_items)

    def create_event(self, region: Region, event_name: str, access_rule: Callable[[CollectionState], bool]) -> None:
        loc = AnodyneLocation(self.player, event_name, None, region)
        loc.place_locked_item(self.create_event_item(event_name))
        loc.access_rule = access_rule
        region.locations.append(loc)

    def create_event_item(self, name: str) -> Item:
        item = self.create_item(name)
        item.classification = ItemClassification.progression
        return item

    def pre_fill(self):
        for dungeon, confined_dungeon_items in self.dungeon_items.items():
            if len(confined_dungeon_items) == 0:
                continue

            collection_state = self.multiworld.get_all_state(False)
            for other_dungeon, other_dungeon_items in self.dungeon_items.items():
                if other_dungeon == dungeon:
                    continue

                for other_dungeon_item in other_dungeon_items:
                    collection_state.collect(other_dungeon_item)

            dungeon_location_names = [location.name
                                      for region_name in Regions.dungeon_areas[dungeon]
                                      for location in Locations.locations_by_region.get(region_name, [])]

            if dungeon == "Street" and self.options.small_key_shuffle == SmallKeyShuffle.option_original_dungeon and \
                    self.options.nexus_gates_open == NexusGatesOpen.option_street_only and \
                    self.options.start_broom == StartBroom.option_none:
                # This is a degenerate case; we need to prevent pre-fill from putting the Street small key in the Broom
                # chest because if it does, there are no reachable locations at the start of the game.
                dungeon_location_names.remove("Street - Broom Chest")

            dungeon_locations = [location for location in self.multiworld.get_locations(self.player)
                                 if location.name in dungeon_location_names and location.item is None]

            for attempts_remaining in range(6, -1, -1):
                self.random.shuffle(dungeon_locations)
                items = confined_dungeon_items.copy()
                locations = dungeon_locations.copy()
                try:
                    fill_restrictive(self.multiworld, collection_state, locations, items,
                                     single_player_placement=True, lock=True)
                    if len(items) == 0:
                        break
                except FillError as exc:
                    if attempts_remaining == 0:
                        raise exc
                    logging.debug(f"Failed to shuffle dungeon items for player {self.player}. Retrying...")
                #Reset locations fill_restrictive tried setting but failed to complete
                for loc in dungeon_locations:
                    if loc.locked and loc.item is not None:
                        loc.locked = False
                        loc.item = None
            confined_dungeon_items.clear()

    def fill_slot_data(self):
        return {
            "death_link": bool(self.options.death_link.value),
            "small_keys": self.options.small_key_mode.current_key if self.options.small_key_mode != SmallKeyMode.option_small_keys else ("vanilla" if self.options.small_key_shuffle == SmallKeyShuffle.option_vanilla else "shuffled"),
            # Mostly useless slots given that small_keys encapsulates all three as far as clients/trackers are concerned, but here for backwards compat
            "unlock_gates": self.options.small_key_mode == SmallKeyMode.option_unlocked,
            "small_key_mode": int(self.options.small_key_mode),
            "shuffle_small_keys": int(self.options.small_key_shuffle),

            "shuffle_big_gates": int(self.options.big_key_shuffle),
            "vanilla_health_cicadas": self.options.health_cicada_shuffle == HealthCicadaShuffle.option_vanilla,
            "nexus_gates_unlocked": self.gates_unlocked,
            "vanilla_red_cave": self.options.red_cave_access == RedCaveAccess.option_vanilla,
            "split_windmill": bool(self.options.split_windmill),
            "postgame_mode": int(self.options.postgame_mode),
            "nexus_gate_shuffle": int(self.options.nexus_gate_shuffle),
            "victory_condition": int(self.options.victory_condition),
            "forest_bunny_chest": bool(self.options.forest_bunny_chest.value),
            "dustsanity": bool(self.options.dustsanity),
            "dust_sanity_base": self.location_name_to_id[
                next(l for l in Locations.all_locations if l.dust).name] if self.options.dustsanity else "Disabled",
            "seed": self.random.randint(0, 1000000),
            "card_amount": self.options.card_amount + self.options.extra_cards,
            "fields_secret_paths": bool(self.options.fields_secret_paths),
            #"shop_items": self.get_shop_items(),
            #"mitra_hints": self.get_mitra_hints(0 if self.options.mitra_hints == MitraHints.option_none else 8 + 1),
            **{c.typename(): c.shorthand(self.options) for c in gatereq_classes}
        }

    @dataclass
    class ShopItem:
        player: int = -1
        item: int = -1

    @dataclass
    class ItemHint:
        item: int = -1
        location: int = -1
        location_player: int = -1

    def get_shop_items(self) -> List[ShopItem]:
        # Do not change shop items if playing solo
        if self.multiworld.players == 1:
            return []
        else:
            items = self.random.sample(
                [item for item in self.multiworld.itempool if
                 item.classification == ItemClassification.progression
                 and item.player != self.player],
                3)
            return [AnodyneWorld.ShopItem(item.player, item.code) for item in items]

    def get_mitra_hints(self, count: int) -> List[ItemHint]:
        possible_items =[item for item in self.multiworld.itempool if
             item.classification == ItemClassification.progression
             and item.player == self.player and item.location is not None]
        items = self.random.sample(
            possible_items,
            min(count,len(possible_items)))

        hints: List[AnodyneWorld.ItemHint] = []

        for item in items:
            location = self.multiworld.find_item(item.name, self.player)
            hints.append(AnodyneWorld.ItemHint(item.code, location.address, location.player))

        return hints

    # for the universal tracker, doesn't get called in standard gen
    @staticmethod
    def interpret_slot_data(slot_data: Dict[str, Any]) -> Dict[str, Any]:
        # returning slot_data so it regens, giving it back in multiworld.re_gen_passthrough
        return slot_data
