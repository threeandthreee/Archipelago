import logging

from BaseClasses import Region, Location, Item, ItemClassification, CollectionState, Tutorial
from Fill import fill_restrictive, FillError
from worlds.AutoWorld import WebWorld, World
from typing import List, Callable, Dict, Any, Set

from . import Constants

from .Data import Items, Locations, Regions, Exits, Events
from .Options import AnodyneGameOptions, SmallKeyShuffle, StartBroom, VictoryCondition, BigKeyShuffle, \
    HealthCicadaShuffle, NexusGatesOpen, RedCaveAccess, PostgameMode, NexusGateShuffle, TrapsMode


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
            self.options.endgame_card_requirement.value = slot_data["endgame_card_requirement"]
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
                logging.warning(f"Player {self.player} requested more random Nexus gates than are available.")
                random_nexus_gate_count = len(available_gates)

            self.gates_unlocked = self.random.sample(available_gates, random_nexus_gate_count)

        if self.options.nexus_gate_shuffle != NexusGateShuffle.option_off:
            self.shuffled_gates = set(Regions.regions_with_nexus_gate) - set(self.gates_unlocked)

            if self.options.nexus_gate_shuffle == NexusGateShuffle.option_all_except_endgame:
                self.shuffled_gates -= set(Regions.endgame_nexus_gates)

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

    def create_regions(self) -> None:
        include_health_cicadas = self.options.health_cicada_shuffle
        include_big_keys = self.options.big_key_shuffle
        include_postgame: bool = (self.options.postgame_mode != PostgameMode.option_disabled)

        all_regions: Dict[str, Region] = {}

        for region_name in Regions.all_regions:
            if not include_postgame and region_name in Regions.postgame_regions:
                continue

            region = Region(region_name, self.player, self.multiworld)
            if region_name in Locations.locations_by_region:
                for location in Locations.locations_by_region[region_name]:
                    if include_health_cicadas == HealthCicadaShuffle.option_vanilla and location.health_cicada:
                        continue

                    if include_big_keys == BigKeyShuffle.option_vanilla and location.big_key:
                        continue

                    if self.options.red_cave_access == RedCaveAccess.option_vanilla and location.tentacle:
                        continue

                    if not self.options.split_windmill and location.name == "Windmill - Activation":
                        continue

                    if not include_postgame and location.postgame():
                        continue

                    if not self.options.forest_bunny_chest and location.name == "Deep Forest - Bunny Chest":
                        continue

                    if self.options.victory_condition == VictoryCondition.option_defeat_briar\
                            and location.name == "GO - Defeat Briar":
                        continue

                    if location.nexus_gate and location.region_name not in self.shuffled_gates:
                        continue

                    location_id = Constants.location_name_to_id[location.name]

                    new_location = AnodyneLocation(self.player, location.name, location_id, region)
                    new_location.access_rule = Constants.get_access_rule(location.reqs, region_name, self)
                    region.locations.append(new_location)

                    self.location_count += 1

            all_regions[region_name] = region

        for exit_vals in Exits.all_exits:
            exit1: str = exit_vals[0]
            exit2: str = exit_vals[1]

            if not include_postgame and (exit1 in Regions.postgame_regions or exit2 in Regions.postgame_regions):
                continue

            requirements: list[str] = exit_vals[2]

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
            if not include_postgame and region_name in Regions.postgame_regions:
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

    def set_rules(self) -> None:
        if not self.options.split_windmill:
            for statue in Items.statue_items:
                self.proxy_rules[statue] = ["Windmill activated"]

        if self.options.red_cave_access == RedCaveAccess.option_vanilla:
            self.proxy_rules["RedCave:Left"] = ["Center left tentacle hit"]
            self.proxy_rules["RedCave:Right"] = ["Center right tentacle hit"]
            self.proxy_rules["RedCave:Top"] = ["Left tentacle hit", "Right tentacle hit"]

        if self.options.randomize_color_puzzle:
            self.proxy_rules["GO Color Puzzle"] = ["Defeat Servants", "Defeat Watcher", "Defeat Manager"]
        else:
            self.proxy_rules["GO Color Puzzle"] = []

        if self.options.postgame_mode != PostgameMode.option_progressive:
            self.proxy_rules["Swap:1"] = ["Swap"]

            if self.options.postgame_mode == PostgameMode.option_vanilla:
                self.proxy_rules["Swap:2"] = ["Swap", "Defeat Briar"]
            elif self.options.postgame_mode == PostgameMode.option_unlocked:
                self.proxy_rules["Swap:2"] = ["Swap"]

        if self.options.postgame_mode == PostgameMode.option_disabled and self.options.endgame_card_requirement > 37:
            raise Exception("Postgame must be enabled in order to choose an endgame card requirement over 37.")

        self.proxy_rules["Endgame Access"] = [f"Cards:{self.options.endgame_card_requirement}"]

        if self.options.nexus_gate_shuffle or\
                any(region in self.gates_unlocked for region in Regions.post_temple_boss_regions):
            # There is one keyblock in Temple of the Seeing One that has conditional logic based on whether it is
            # possible for the player to access the exit of the dungeon early.
            self.proxy_rules["Temple Boss Access"] = ["Keys:Temple of the Seeing One:3"]
        else:
            self.proxy_rules["Temple Boss Access"] = ["Keys:Temple of the Seeing One:2"]

        victory_condition: VictoryCondition = self.options.victory_condition
        requirements: list[str] = []

        if victory_condition == VictoryCondition.option_defeat_briar:
            requirements.append("Defeat Briar")
        elif victory_condition == VictoryCondition.option_all_cards:
            if self.options.postgame_mode == PostgameMode.option_disabled:
                raise Exception("Postgame must be enabled in order to use the All Cards victory condition.")

            requirements.append("Cards:49")
            requirements.append("Open 49 card gate")

        self.multiworld.completion_condition[self.player] = Constants.get_access_rule(requirements, "Event", self)

    def create_items(self) -> None:
        item_pool: List[Item] = []
        local_item_pool: set[str] = set()
        non_local_item_pool: set[str] = set()

        small_key_shuffle: SmallKeyShuffle = self.options.small_key_shuffle
        health_cicada_shuffle = self.options.health_cicada_shuffle
        big_key_shuffle = self.options.big_key_shuffle
        start_broom: StartBroom = self.options.start_broom

        placed_items = 0

        excluded_items: set[str] = {
            *Items.small_key_item_count.keys(),
            *Items.big_keys,
            "Health Cicada",
            *Items.filler_items,
            *Items.trap_items,
            "Progressive Red Cave",
            "Progressive Swap",
            *Items.nexus_gate_items.keys(),
        }

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
        elif small_key_shuffle != SmallKeyShuffle.option_unlocked:
            for key_item, key_count in Items.small_key_item_count.items():
                placed_items += key_count

                for _ in range(key_count):
                    item_pool.append(self.create_item(key_item))

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

        # If we have space for filler, prioritize adding in the ??? items that would be in-logic. Also add traps,
        # if enabled.
        if placed_items < self.location_count:
            new_items = []

            remaining_items = self.location_count - placed_items
            num_traps = int(self.get_trap_percentage() * remaining_items)
            remaining_items -= num_traps

            for i in range(num_traps):
                new_items.append(self.random.choice(Items.trap_items))

            secret_items = Items.early_secret_items if self.options.postgame_mode == PostgameMode.option_disabled\
                else Items.secret_items

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

    def get_trap_percentage(self) -> float:
        traps_mode = self.options.traps_mode
        if traps_mode == TrapsMode.option_none:
            return 0.0
        elif traps_mode == TrapsMode.option_low:
            return 0.1
        elif traps_mode == TrapsMode.option_normal:
            return 0.25
        elif traps_mode == TrapsMode.option_many:
            return 0.5
        elif traps_mode == TrapsMode.option_chaos:
            return 1.0

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

            if dungeon == "Street" and self.options.small_key_shuffle == SmallKeyShuffle.option_original_dungeon and\
                    self.options.nexus_gates_open == NexusGatesOpen.option_street_only and\
                    self.options.start_broom == StartBroom.option_none:
                # This is a degenerate case; we need to prevent pre-fill from putting the Street small key in the Broom
                # chest because if it does, there are no reachable locations at the start of the game.
                dungeon_location_names.remove("Street - Broom Chest")

            dungeon_locations = [location for location in self.multiworld.get_locations(self.player)
                                 if location.name in dungeon_location_names]

            for attempts_remaining in range(2, -1, -1):
                self.random.shuffle(dungeon_locations)
                try:
                    fill_restrictive(self.multiworld, collection_state, dungeon_locations, confined_dungeon_items,
                                     single_player_placement=True, lock=True, allow_excluded=True)
                    break
                except FillError as exc:
                    if attempts_remaining == 0:
                        raise exc
                    logging.debug(f"Failed to shuffle dungeon items for player {self.player}. Retrying...")

    def fill_slot_data(self):
        return {
            "death_link": bool(self.options.death_link.value),
            "unlock_gates": self.options.small_key_shuffle == SmallKeyShuffle.option_unlocked,
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
            "endgame_card_requirement": int(self.options.endgame_card_requirement),
            "player_sprite": int(self.options.player_sprite),
            "randomize_color_puzzle": bool(self.options.randomize_color_puzzle),
            "seed": self.random.randint(0, 1000000)
        }

    # for the universal tracker, doesn't get called in standard gen
    @staticmethod
    def interpret_slot_data(slot_data: Dict[str, Any]) -> Dict[str, Any]:
        # returning slot_data so it regens, giving it back in multiworld.re_gen_passthrough
        return slot_data
