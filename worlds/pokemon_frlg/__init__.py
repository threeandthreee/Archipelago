"""
Archipelago World definition for Pokémon FireRed/LeafGreen
"""
import copy
import logging
import os.path
import threading
import settings
import pkgutil

from typing import Any, ClassVar, Dict, List, Set, TextIO, Tuple

from BaseClasses import Tutorial, MultiWorld, ItemClassification, LocationProgressType
from Fill import fill_restrictive, FillError
from worlds.AutoWorld import WebWorld, World
from .client import PokemonFRLGClient
from .data import (data as frlg_data, LEGENDARY_POKEMON, EventData, MapData, MiscPokemonData, SpeciesData, StarterData,
                   TrainerData)
from .items import (ITEM_GROUPS, create_item_name_to_id_map, get_random_item, get_item_classification,
                    reverse_offset_item_value, PokemonFRLGItem)
from .level_scaling import ScalingData, create_scaling_data, level_scaling
from .locations import (LOCATION_GROUPS, create_location_name_to_id_map, create_locations_from_tags, set_free_fly,
                        PokemonFRLGLocation)
from .options import (PokemonFRLGOptions, CeruleanCaveRequirement, FreeFlyLocation, GameVersion,
                      RandomizeLegendaryPokemon, RandomizeMiscPokemon, RandomizeWildPokemon, ShuffleHiddenItems,
                      ShuffleBadges, TownMapFlyLocation, ViridianCityRoadblock)
from .pokemon import (randomize_abilities, randomize_legendaries, randomize_misc_pokemon, randomize_moves,
                      randomize_starters, randomize_tm_hm_compatibility, randomize_tm_moves,
                      randomize_trainer_parties, randomize_types, randomize_wild_encounters)
from .rom import get_tokens, PokemonFireRedProcedurePatch, PokemonLeafGreenProcedurePatch
from .util import int_to_bool_array, HM_TO_COMPATIBILITY_ID


class PokemonFRLGWebWorld(WebWorld):
    """
    Webhost info for Pokémon FireRed and LeafGreen
    """
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Pokémon FireRed and LeafGreen with Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Vyneras"]
    )

    tutorials = [setup_en]


class PokemonFRLGSettings(settings.Group):
    class PokemonFireRedRomFile(settings.UserFilePath):
        """File name of your English Pokémon FireRed ROM"""
        description = "Pokemon FireRed ROM File"
        copy_to = "Pokemon - FireRed Version (USA, Europe).gba"
        md5s = PokemonFireRedProcedurePatch.hash

    class PokemonLeafGreenRomFile(settings.UserFilePath):
        """File name of your English Pokémon LeafGreen ROM"""
        description = "Pokemon LeafGreen ROM File"
        copy_to = "Pokemon - LeafGreen Version (USA, Europe).gba"
        md5s = PokemonLeafGreenProcedurePatch.hash

    firered_rom_file: PokemonFireRedRomFile = PokemonFireRedRomFile(PokemonFireRedRomFile.copy_to)
    leafgreen_rom_file: PokemonLeafGreenRomFile = PokemonLeafGreenRomFile(PokemonLeafGreenRomFile.copy_to)


class PokemonFRLGWorld(World):
    """
    Pokémon FireRed and LeafGreen are remakes of the very first Pokémon games.
    Experience the Kanto region with several updated features from Gen III.
    Catch, train, and battle Pokémon, face off against the evil organization Team Rocket, challenge Gyms in order to
    earn Badges, help resolve the many crises on the Sevii Islands, and become the Pokémon Champion!
    """
    game = "Pokemon FireRed and LeafGreen"
    web = PokemonFRLGWebWorld()
    topology_present = True

    settings_key = "pokemon_frlg_settings"
    settings: ClassVar[PokemonFRLGSettings]

    options_dataclass = PokemonFRLGOptions
    options: PokemonFRLGOptions

    item_name_to_id = create_item_name_to_id_map()
    location_name_to_id = create_location_name_to_id_map()
    item_name_groups = ITEM_GROUPS
    location_name_groups = LOCATION_GROUPS

    required_client_version = (0, 5, 0)

    free_fly_location_id: int
    town_map_fly_location_id: int
    modified_species: Dict[int, SpeciesData]
    modified_maps: Dict[str, MapData]
    modified_starters: Dict[str, StarterData]
    modified_events: Dict[str, EventData]
    modified_legendary_pokemon: Dict[str, MiscPokemonData]
    modified_misc_pokemon: Dict[str, MiscPokemonData]
    modified_trainers: Dict[str, TrainerData]
    modified_tmhm_moves: List[int]
    hm_compatibility: Dict[str, List[str]]
    per_species_tmhm_moves: Dict[int, List[int]]
    trade_pokemon: List[Tuple[str, str]]
    blacklisted_wild_pokemon: Set[int]
    blacklisted_starters: Set[int]
    blacklisted_trainer_pokemon: Set[int]
    blacklisted_abilities: Set[int]
    blacklisted_moves: Set[int]
    trainer_name_level_dict: Dict[str, int]
    trainer_name_list: List[str]
    trainer_level_list: List[int]
    encounter_name_level_dict: Dict[str, int]
    encounter_name_list: List[str]
    encounter_level_list: List[int]
    scaling_data: List[ScalingData]
    auth: bytes

    def __init__(self, multiworld, player):
        super(PokemonFRLGWorld, self).__init__(multiworld, player)
        self.free_fly_location_id = 0
        self.town_map_fly_location_id = 0
        self.modified_species = copy.deepcopy(frlg_data.species)
        self.modified_maps = copy.deepcopy(frlg_data.maps)
        self.modified_starters = copy.deepcopy(frlg_data.starters)
        self.modified_events = copy.deepcopy(frlg_data.events)
        self.modified_legendary_pokemon = copy.deepcopy(frlg_data.legendary_pokemon)
        self.modified_misc_pokemon = copy.deepcopy(frlg_data.misc_pokemon)
        self.modified_trainers = copy.deepcopy(frlg_data.trainers)
        self.modified_tmhm_moves = copy.deepcopy(frlg_data.tmhm_moves)
        self.hm_compatibility = {}
        self.per_species_tmhm_moves = {}
        self.trade_pokemon = []
        self.trainer_name_level_dict = {}
        self.trainer_name_list = []
        self.trainer_level_list = []
        self.encounter_name_level_dict = {}
        self.encounter_name_list = []
        self.encounter_level_list = []
        self.scaling_data = []
        self.finished_level_scaling = threading.Event()

    @classmethod
    def stage_assert_generate(cls, multiworld: MultiWorld) -> None:
        from .sanity_check import validate_regions

        assert validate_regions()

    def get_filler_item_name(self) -> str:
        return get_random_item(self, ItemClassification.filler)

    def generate_early(self) -> None:
        self.blacklisted_wild_pokemon = {
            species.species_id for species in self.modified_species.values()
            if species.name in self.options.wild_pokemon_blacklist.value
        }
        if "Legendaries" in self.options.wild_pokemon_blacklist.value:
            self.blacklisted_wild_pokemon |= LEGENDARY_POKEMON

        self.blacklisted_starters = {
            species.species_id for species in self.modified_species.values()
            if species.name in self.options.starter_blacklist.value
        }
        if "Legendaries" in self.options.starter_blacklist.value:
            self.blacklisted_starters |= LEGENDARY_POKEMON

        self.blacklisted_trainer_pokemon = {
            species.species_id for species in self.modified_species.values()
            if species.name in self.options.trainer_blacklist.value
        }
        if "Legendaries" in self.options.trainer_blacklist.value:
            self.blacklisted_trainer_pokemon |= LEGENDARY_POKEMON

        self.blacklisted_abilities = {frlg_data.abilities[name] for name in self.options.ability_blacklist.value}
        self.blacklisted_moves = {frlg_data.moves[name] for name in self.options.move_blacklist.value}

        if (self.options.kanto_only and
                self.options.cerulean_cave_requirement == CeruleanCaveRequirement.option_vanilla or
                self.options.cerulean_cave_requirement == CeruleanCaveRequirement.option_restore_network):
            logging.warning("Pokemon FRLG: Cerulean Cave Requirement for Player %s (%s) incompatible with Kanto Only. "
                            "Setting requirement to Defeat Champion.", self.player, self.player_name)
            self.options.cerulean_cave_requirement.value = CeruleanCaveRequirement.option_champion

        create_scaling_data(self)
        randomize_types(self)
        randomize_abilities(self)
        randomize_moves(self)
        randomize_wild_encounters(self)
        randomize_starters(self)
        randomize_legendaries(self)
        randomize_misc_pokemon(self)
        randomize_tm_hm_compatibility(self)
        self.create_hm_compatibility_dict()

    def create_regions(self) -> None:
        from .regions import create_indirect_conditions, create_regions

        regions = create_regions(self)

        tags = {"Badge", "HM", "KeyItem", "FlyUnlock", "Overworld", "NPCGift"}
        if self.options.shuffle_hidden == ShuffleHiddenItems.option_all:
            tags.add("Hidden")
            tags.add("Recurring")
        elif self.options.shuffle_hidden == ShuffleHiddenItems.option_nonrecurring:
            tags.add("Hidden")
        if self.options.extra_key_items:
            tags.add("ExtraKeyItem")
        if self.options.trainersanity:
            tags.add("Trainer")
        create_locations_from_tags(self, regions, tags)

        self.multiworld.regions.extend(regions.values())

        create_indirect_conditions(self)

    def create_items(self) -> None:
        item_locations: List[PokemonFRLGLocation] = [
            location for location in self.multiworld.get_locations(self.player) if location.address is not None
        ]

        if not self.options.shuffle_badges:
            item_locations = [location for location in item_locations if "Badge" not in location.tags]
        if not self.options.shuffle_fly_destination_unlocks:
            item_locations = [location for location in item_locations if "FlyUnlock" not in location.tags]

        itempool = [self.create_item_by_id(location.default_item_id) for location in item_locations]

        if self.options.kanto_only:
            items_to_add = ["HM06 Rock Smash", "HM07 Waterfall"]
            for item_name in items_to_add:
                itempool.append(self.create_item(item_name))
                filler_items = [item for item in itempool
                                if item.classification == ItemClassification.filler and "Unique" not in item.tags]
                item_to_remove = self.random.choice(filler_items)
                itempool.remove(item_to_remove)

        for item in self.options.start_inventory.keys():
            if "Unique" in frlg_data.items[reverse_offset_item_value(self.item_name_to_id[item])].tags:
                itempool_len = len(itempool)
                itempool = [i for i in itempool if i.name != item]
                removed_items_count = itempool_len - len(itempool)
                while removed_items_count > 0:
                    itempool.append(self.create_item(get_random_item(self, ItemClassification.filler)))
                    removed_items_count -= 1

        self.multiworld.itempool += itempool

    def set_rules(self) -> None:
        from .rules import set_rules
        set_rules(self)

    def generate_basic(self) -> None:
        # Create auth
        self.auth = self.random.getrandbits(16 * 8).to_bytes(16, "little")

        set_free_fly(self)

        def create_events_for_unrandomized_items(tag: str) -> None:
            locations = [location for location in self.multiworld.get_locations(self.player)
                         if tag in location.tags]
            for location in locations:
                location.place_locked_item(PokemonFRLGItem(self.item_id_to_name[location.default_item_id],
                                                           ItemClassification.progression,
                                                           None,
                                                           self.player))
                location.progress_type = LocationProgressType.DEFAULT
                location.address = None

        if not self.options.shuffle_fly_destination_unlocks:
            create_events_for_unrandomized_items("FlyUnlock")

    def pre_fill(self) -> None:
        # If badges aren't shuffled among all locations, shuffle them among themselves
        if not self.options.shuffle_badges:
            badge_locations: List[PokemonFRLGLocation] = [
                location for location in self.multiworld.get_locations(self.player) if "Badge" in location.tags
            ]
            badge_items: List[PokemonFRLGItem] = [
                self.create_item_by_id(location.default_item_id) for location in badge_locations
            ]

            collection_state = self.multiworld.get_all_state(False)

            attempts_remaining = 2
            while attempts_remaining > 0:
                attempts_remaining -= 1
                self.random.shuffle(badge_locations)
                try:
                    fill_restrictive(self.multiworld, collection_state, badge_locations, badge_items,
                                     single_player_placement=True, lock=True, allow_excluded=True)
                    break
                except FillError as exc:
                    if attempts_remaining == 0:
                        raise exc

        if self.options.viridian_city_roadblock == ViridianCityRoadblock.option_early_parcel:
            self.multiworld.local_early_items[self.player]["Oak's Parcel"] = 1

        # Delete evolutions that are not in logic in an all_state so that the accessibility check doesn't fail
        collection_state = self.multiworld.get_all_state(False)
        evolution_region = self.multiworld.get_region("Evolutions", self.player)
        for location in evolution_region.locations.copy():
            if not collection_state.can_reach(location, player=self.player):
                evolution_region.locations.remove(location)

        # Delete trades that are not in logic in an all_state so that the accessibility check doesn't fail
        for trade in self.trade_pokemon:
            location = self.multiworld.get_location(trade[1], self.player)
            if not collection_state.can_reach(location, player=self.player):
                region = self.multiworld.get_region(trade[0], self.player)
                region.locations.remove(location)

    @classmethod
    def stage_post_fill(cls, multiworld):
        # Change all but one instance of a Pokémon in each sphere to useful classification
        # This cuts down on time calculating the playthrough
        found_mons = set()
        pokemon = {species.name for species in frlg_data.species.values()}
        for sphere in multiworld.get_spheres():
            for location in sphere:
                if (location.game == "Pokemon FireRed and LeafGreen" and
                        (location.item.name in pokemon or "Static " in location.item.name)
                        and location.item.advancement):
                    key = (location.player, location.item.name)
                    if key in found_mons:
                        location.item.classification = ItemClassification.useful
                    else:
                        found_mons.add(key)

    @classmethod
    def stage_generate_output(cls, multiworld, output_directory):
        level_scaling(multiworld)

    def generate_output(self, output_directory: str) -> None:
        # Modify catch rate
        min_catch_rate = min(self.options.min_catch_rate.value, 255)
        for species in self.modified_species.values():
            species.catch_rate = max(species.catch_rate, min_catch_rate)

        self.finished_level_scaling.wait()

        randomize_tm_moves(self)
        randomize_trainer_parties(self)

        if self.options.game_version == GameVersion.option_firered:
            patch = PokemonFireRedProcedurePatch(player=self.player, player_name=self.player_name)
            patch.write_file("base_patch_rev0.bsdiff4",
                             pkgutil.get_data(__name__, "data/base_patch_firered.bsdiff4"))
            patch.write_file("base_patch_rev1.bsdiff4",
                             pkgutil.get_data(__name__, "data/base_patch_firered_rev1.bsdiff4"))
        else:
            patch = PokemonLeafGreenProcedurePatch(player=self.player, player_name=self.player_name)
            patch.write_file("base_patch_rev0.bsdiff4",
                             pkgutil.get_data(__name__, "data/base_patch_leafgreen.bsdiff4"))
            patch.write_file("base_patch_rev1.bsdiff4",
                             pkgutil.get_data(__name__, "data/base_patch_leafgreen_rev1.bsdiff4"))

        tokens_rev0 = get_tokens(self, 0)
        tokens_rev1 = get_tokens(self, 1)

        patch.write_file("token_data_rev0.bin", tokens_rev0.get_token_binary())
        patch.write_file("token_data_rev1.bin", tokens_rev1.get_token_binary())

        # Write output
        out_file_name = self.multiworld.get_out_file_name_base(self.player)
        patch.write(os.path.join(output_directory, f"{out_file_name}{patch.patch_file_ending}"))

        del self.modified_species
        del self.modified_maps
        del self.modified_starters
        del self.modified_events
        del self.modified_legendary_pokemon
        del self.modified_misc_pokemon
        del self.trade_pokemon
        del self.trainer_name_level_dict
        del self.trainer_name_list
        del self.trainer_level_list
        del self.encounter_name_level_dict
        del self.encounter_name_list
        del self.encounter_level_list
        del self.scaling_data

    def write_spoiler_header(self, spoiler_handle: TextIO) -> None:
        if self.options.free_fly_location != FreeFlyLocation.option_off:
            free_fly_location = self.multiworld.get_location("Free Fly Location", self.player)
            spoiler_handle.write(f"Free Fly Location:               {free_fly_location.item.name[4:]}\n")
        if self.options.town_map_fly_location != TownMapFlyLocation.option_off:
            town_map_fly_location = self.multiworld.get_location("Town Map Fly Location", self.player)
            spoiler_handle.write(f"Town Map Fly Location:           {town_map_fly_location.item.name[4:]}\n")

    def write_spoiler(self, spoiler_handle: TextIO) -> None:
        # Add Pokémon locations to the spoiler log if they are not vanilla
        if (self.options.wild_pokemon != RandomizeWildPokemon.option_vanilla or
                self.options.misc_pokemon != RandomizeMiscPokemon.option_vanilla or
                self.options.legendary_pokemon != RandomizeLegendaryPokemon.option_vanilla):
            spoiler_handle.write(f"\n\nPokemon Locations ({self.multiworld.player_name[self.player]}):\n\n")

        if self.options.wild_pokemon != RandomizeWildPokemon.option_vanilla:
            pokemon_locations: List[PokemonFRLGLocation] = [
                location for location in self.multiworld.get_locations(self.player)
                if "Pokemon" in location.tags and "Wild" in location.tags
            ]
            for location in pokemon_locations:
                spoiler_handle.write(location.name + ": " + location.item.name + "\n")

        if self.options.misc_pokemon != RandomizeMiscPokemon.option_vanilla:
            pokemon_locations: List[PokemonFRLGLocation] = [
                location for location in self.multiworld.get_locations(self.player)
                if "Pokemon" in location.tags and "Misc" in location.tags
            ]
            for location in pokemon_locations:
                if location.item.name.startswith("Static") or location.item.name.startswith("Missable"):
                    name = location.item.name.split()[1]
                else:
                    name = location.item.name
                spoiler_handle.write(location.name + ": " + name + "\n")

        if self.options.legendary_pokemon != RandomizeLegendaryPokemon.option_vanilla:
            pokemon_locations: List[PokemonFRLGLocation] = [
                location for location in self.multiworld.get_locations(self.player)
                if "Pokemon" in location.tags and "Legendary" in location.tags
            ]
            for location in pokemon_locations:
                if location.item.name.startswith("Static") or location.item.name.startswith("Missable"):
                    name = location.item.name.split()[1]
                else:
                    name = location.item.name
                spoiler_handle.write(location.name + ": " + name + "\n")

    def modify_multidata(self, multidata: Dict[str, Any]):
        import base64
        multidata["connect_names"][base64.b64encode(self.auth).decode("ascii")] = \
            multidata["connect_names"][self.player_name]

    def fill_slot_data(self) -> Dict[str, Any]:
        slot_data = self.options.as_dict(
            "kanto_only",
            "shuffle_badges",
            "shuffle_hidden",
            "extra_key_items",
            "trainersanity",
            "shuffle_fly_destination_unlocks",
            "itemfinder_required",
            "flash_required",
            "remove_badge_requirement",
            "oaks_aide_route_2",
            "oaks_aide_route_10",
            "oaks_aide_route_11",
            "oaks_aide_route_16",
            "oaks_aide_route_15",
            "viridian_city_roadblock",
            "pewter_city_roadblock",
            "cerulean_city_roadblocks",
            "viridian_gym_requirement",
            "viridian_gym_count",
            "route22_gate_requirement",
            "route22_gate_count",
            "route23_guard_requirement",
            "route23_guard_count",
            "elite_four_requirement",
            "elite_four_count",
            "cerulean_cave_requirement",
            "cerulean_cave_count",
        )
        slot_data["free_fly_location_id"] = self.free_fly_location_id
        slot_data["town_map_fly_location_id"] = self.town_map_fly_location_id
        return slot_data

    def create_item(self, name: str) -> "PokemonFRLGItem":
        return self.create_item_by_id(self.item_name_to_id[name])

    def create_item_by_id(self, item_id: int):
        return PokemonFRLGItem(
            self.item_id_to_name[item_id],
            get_item_classification(item_id),
            item_id,
            self.player
        )

    def create_hm_compatibility_dict(self):
        hms = frozenset({"Cut", "Fly", "Surf", "Strength", "Flash", "Rock Smash", "Waterfall"})
        for hm in hms:
            self.hm_compatibility[hm] = list()
            for species in self.modified_species.values():
                combatibility_array = int_to_bool_array(species.tm_hm_compatibility)
                if combatibility_array[HM_TO_COMPATIBILITY_ID[hm]] == 1:
                    self.hm_compatibility[hm].append(species.name)
