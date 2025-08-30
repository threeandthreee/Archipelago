import datetime
import os
from typing import ClassVar, Mapping, Any, List

import settings
from BaseClasses import MultiWorld, Tutorial, Item, Location
from Options import Option
from worlds.AutoWorld import World, WebWorld
from . import items, locations, options, bizhawk_client, rom, groups


bizhawk_client.register_client()


class PokemonBWSettings(settings.Group):

    class PokemonBlackRomFile(settings.UserFilePath):
        """File name of your Pokémon Black Version ROM"""
        description = "Pokemon Black Version ROM"
        copy_to = "PokemonBlack.nds"

    class PokemonWhiteRomFile(settings.UserFilePath):
        """File name of your Pokémon White Version ROM"""
        description = "Pokemon White Version ROM"
        copy_to = "PokemonWhite.nds"

    black_rom: PokemonBlackRomFile = PokemonBlackRomFile(PokemonBlackRomFile.copy_to)
    white_rom: PokemonWhiteRomFile = PokemonWhiteRomFile(PokemonWhiteRomFile.copy_to)


class PokemonBWWeb(WebWorld):
    rich_text_options_doc = True
    theme = ("grassFlowers", "ocean", "dirt", "ice")[(datetime.datetime.now().month - 1) % 4]
    game_info_languages = ["en"]
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Pokémon Black and White with Archipelago:",
        "English",
        "setup_en.md",
        "setup/en",
        ["BlastSlimey"]
    )
    tutorials = [setup_en]


class PokemonBWWorld(World):
    """
    Pokémon Black and White are the introduction to the fifth generation of the Pokémon franchise.
    Travel through the Unova region, catch a variety of brand-new Pokémon you have never seen before,
    collect the eight gym badges, fight Team Plasma, who claim to be the saviors of all the Pokémon,
    and become the champion of the region.
    These games present themselves in 2.5D graphics,
    while still using the well-known grid-based movement mechanics and battle UI.
    """
    game = "Pokemon Black and White"
    options_dataclass = options.PokemonBWOptions
    options: options.PokemonBWOptions
    topology_present = True
    web = PokemonBWWeb()
    item_name_to_id = items.get_item_lookup_table()
    location_name_to_id = locations.get_location_lookup_table()
    settings_key = "pokemon_bw_settings"
    settings: ClassVar[PokemonBWSettings]
    item_name_groups = groups.get_item_groups()
    location_name_groups = groups.get_location_groups()

    ut_can_gen_without_yaml = True
    tracker_world = {
        "map_page_folder": "tracker",
        "map_page_maps": "maps/maps.json",
        "map_page_locations": "locations/locations.json"
    }

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)

        self.strength_species: set[str] = set()
        self.cut_species: set[str] = set()
        self.surf_species: set[str] = set()
        self.dive_species: set[str] = set()
        self.waterfall_species: set[str] = set()
        self.flash_species: set[str] = set()
        self.fighting_type_species: set[str] = set()  # Needed for challenge rock outside of pinwheel forest
        self.to_be_filled_locations: int = 0
        self.seed: int = 0
        self.to_be_locked_items: dict[str, list[items.PokemonBWItem] | dict[str, items.PokemonBWItem]] = {}

        self.ut_active: bool = False

    def generate_early(self) -> None:

        # Load values from UT if this is a regenerated world
        if hasattr(self.multiworld, "re_gen_passthrough"):
            if self.game in self.multiworld.re_gen_passthrough:
                self.ut_active = True
                re_ge_slot_data: dict[str, Any] = self.multiworld.re_gen_passthrough[self.game]
                re_gen_options: dict[str, Any] = re_ge_slot_data["options"]
                # Populate options from UT
                for key, value in re_gen_options.items():
                    opt: Option | None = getattr(self.options, key, None)
                    if opt is not None:
                        setattr(self.options, key, opt.from_any(value))
                self.seed = re_ge_slot_data["seed"]
                self.random.seed(self.seed)
                return

        self.seed = self.random.getrandbits(64)
        self.random.seed(self.seed)

    def create_item(self, name: str) -> items.PokemonBWItem:
        return items.generate_item(name, self)

    def get_filler_item_name(self) -> str:
        return items.generate_filler(self)

    def create_regions(self) -> None:
        regions = locations.get_regions(self)
        rules = locations.create_rule_dict(self)
        locations.connect_regions(self, regions, rules)
        locations.cleanup_regions(regions)
        catchable_species_data = locations.create_and_place_event_locations(self, regions, rules)
        locations.create_and_place_locations(self, regions, rules, catchable_species_data)
        self.to_be_filled_locations = locations.count_to_be_filled_locations(regions)
        self.multiworld.regions.extend(regions.values())

    def create_items(self) -> None:
        item_pool = items.get_main_item_pool(self)
        items.populate_starting_inventory(self, item_pool)
        if len(item_pool) > self.to_be_filled_locations:
            raise Exception(f"Player {self.player_name} has more guaranteed items than to-be-filled locations."
                            f"Please report this to the devs and provide the yaml used for generating.")
        for _ in range(self.to_be_filled_locations-len(item_pool)):
            item_pool.append(self.create_item(self.get_filler_item_name()))
        items.reserve_locked_items(self, item_pool)
        self.multiworld.itempool += item_pool

    def get_pre_fill_items(self) -> List[Item]:
        return [
            item
            for item_list in self.to_be_locked_items if isinstance(item_list, list)
            for item in item_list
        ] + [
            item_dict[name]
            for item_dict in self.to_be_locked_items if isinstance(item_dict, dict)
            for name in item_dict
        ]

    def pre_fill(self) -> None:
        from .generate.locked_placement import place_badges_pre_fill, place_tm_hm_pre_fill

        place_badges_pre_fill(self)
        place_tm_hm_pre_fill(self)

    def fill_hook(self,
                  progitempool: List[Item],
                  usefulitempool: List[Item],
                  filleritempool: List[Item],
                  fill_locations: List[Location]) -> None:
        from .generate.locked_placement import place_tm_hm_fill, place_badges_fill

        place_badges_fill(self, progitempool, fill_locations)
        place_tm_hm_fill(self, progitempool, usefulitempool, filleritempool, fill_locations)

    def generate_output(self, output_directory: str) -> None:
        if self.options.version == "black":
            rom.PokemonBlackPatch(
                path=os.path.join(
                    output_directory,
                    self.multiworld.get_out_file_name_base(self.player) + rom.PokemonBlackPatch.patch_file_ending
                ), world=self, player=self.player, player_name=self.player_name
            ).write()
        else:
            rom.PokemonWhitePatch(
                path=os.path.join(
                    output_directory,
                    self.multiworld.get_out_file_name_base(self.player) + rom.PokemonWhitePatch.patch_file_ending
                ), world=self, player=self.player, player_name=self.player_name
            ).write()

    def fill_slot_data(self) -> Mapping[str, Any]:
        # Some options and data are included for UT
        return {
            "options": {
                "goal": self.options.goal.current_key,
                "version": self.options.version.current_key,
                "shuffle_badges": self.options.shuffle_badges.current_key,
                "shuffle_tm_hm": self.options.shuffle_tm_hm.current_key,
                "dexsanity": self.options.dexsanity.value,
                "season_control": self.options.season_control.current_key,
                "modify_item_pool": self.options.modify_item_pool.value,
                "modify_logic": self.options.modify_logic.value,
            },
            "seed": self.seed,
        }

    def interpret_slot_data(self, slot_data: dict[str, Any]) -> dict[str, Any]:
        """Helper function for Universal Tracker"""
        _ = self  # Damn PyCharm saying "meThoD mAy bE stAtiC"
        return slot_data
