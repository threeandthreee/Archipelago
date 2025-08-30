import asyncio
import os
import pathlib
import zipfile

from .ndspy import rom as ndspy_rom

import Utils
from settings import get_settings
from worlds.Files import APAutoPatchInterface
from typing import TYPE_CHECKING, Any, Dict, Callable

from .patch.procedures import base_patch, season_patch

if TYPE_CHECKING:
    from . import PokemonBWWorld


cached_rom: list[str | None] = [None]


async def keep_cache_alive():
    while cached_rom[0] is not None:
        await asyncio.sleep(5)


class PokemonBlackPatch(APAutoPatchInterface):
    game = "Pokemon Black and White"
    bw_patch_format = (0, 2, 0)
    patch_file_ending = ".apblack"
    result_file_ending = ".nds"

    def __init__(self, path: str, player=None, player_name="", world=None):
        self.world: "PokemonBWWorld" = world
        self.files: dict[str, bytes] = {}
        super().__init__(path, player, player_name, "")

    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        super().write_contents(opened_zipfile)
        PatchMethods.write_contents(self, opened_zipfile)

    def get_manifest(self) -> Dict[str, Any]:
        return PatchMethods.get_manifest(self, super().get_manifest())

    def patch(self, target: str) -> None:
        PatchMethods.patch(self, target, "black")

    def read_contents(self, opened_zipfile: zipfile.ZipFile) -> Dict[str, Any]:
        return PatchMethods.read_contents(self, opened_zipfile, super().read_contents(opened_zipfile))

    def get_file(self, file: str) -> bytes:
        return PatchMethods.get_file(self, file)


class PokemonWhitePatch(APAutoPatchInterface):
    game = "Pokemon Black and White"
    bw_patch_format = (0, 2, 0)
    patch_file_ending = ".apwhite"
    result_file_ending = ".nds"

    def __init__(self, path: str, player=None, player_name="", world=None):
        self.world: "PokemonBWWorld" = world
        self.files: dict[str, bytes] = {}
        super().__init__(path, player, player_name, "")

    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        super().write_contents(opened_zipfile)
        PatchMethods.write_contents(self, opened_zipfile)

    def get_manifest(self) -> Dict[str, Any]:
        return PatchMethods.get_manifest(self, super().get_manifest())

    def patch(self, target: str) -> None:
        PatchMethods.patch(self, target, "white")

    def read_contents(self, opened_zipfile: zipfile.ZipFile) -> Dict[str, Any]:
        return PatchMethods.read_contents(self, opened_zipfile, super().read_contents(opened_zipfile))

    def get_file(self, file: str) -> bytes:
        return PatchMethods.get_file(self, file)


class PatchMethods:

    @staticmethod
    def write_contents(patch: PokemonBlackPatch | PokemonWhitePatch, opened_zipfile: zipfile.ZipFile) -> None:

        procedures: list[str] = ["base_patch"]
        if patch.world.options.season_control != "vanilla":
            procedures.append("season_patch")

        opened_zipfile.writestr("procedures.txt", "\n".join(procedures))

    @staticmethod
    def get_manifest(patch: PokemonBlackPatch | PokemonWhitePatch, manifest: dict[str, Any]) -> Dict[str, Any]:
        manifest["bw_patch_format"] = patch.bw_patch_format
        return manifest

    @staticmethod
    def patch(patch: PokemonBlackPatch | PokemonWhitePatch, target: str, version: str) -> None:
        patch.read()

        if not pathlib.Path(target).exists():
            base_data = get_base_rom_bytes(version)
            rom = ndspy_rom.NintendoDSRom(base_data)
            procedures: list[str] = str(patch.get_file("procedures.txt"), "utf-8").splitlines()
            for prod in procedures:
                patch_procedures[prod](rom, __name__, patch)
            with open(target, 'wb') as f:
                f.write(rom.save(updateDeviceCapacity=True))

        cached_rom[0] = patch.player_name
        asyncio.run_coroutine_threadsafe(keep_cache_alive(), asyncio.new_event_loop())

    @staticmethod
    def read_contents(patch: PokemonBlackPatch | PokemonWhitePatch, opened_zipfile: zipfile.ZipFile,
                      manifest: Dict[str, Any]) -> Dict[str, Any]:

        for file in opened_zipfile.namelist():
            if file not in ["archipelago.json"]:
                patch.files[file] = opened_zipfile.read(file)

        if tuple(manifest["bw_patch_format"]) > patch.bw_patch_format:
            raise Exception(f"File (BW patch version: {'.'.join(manifest['bw_patch_format'])} too new "
                            f"for this handler (BW patch version: {patch.bw_patch_format}). "
                            f"Please update your apworld.")

        return manifest

    @staticmethod
    def get_file(patch: PokemonBlackPatch | PokemonWhitePatch, file: str) -> bytes:
        if file not in patch.files:
            patch.read()
        return patch.files[file]


patch_procedures: dict[str, Callable[[ndspy_rom.NintendoDSRom, str, PokemonBlackPatch], None]] = {
    "base_patch": base_patch.patch,
    "season_patch": season_patch.patch,
}


def get_base_rom_bytes(version: str, file_name: str = "") -> bytes:
    if not file_name:
        file_name = get_base_rom_path(version, file_name)
    with open(file_name, "rb") as file:
        base_rom_bytes = bytes(file.read())
    if version == "black" and base_rom_bytes[:18] != b'POKEMON\x20B\0\0\0IRBO01':
        raise Exception(f"Supplied Base Rom appears to not be an english copy of Pokémon Black Version.")
    if version == "white" and base_rom_bytes[:18] != b'POKEMON\x20W\0\0\0IRAO01':
        raise Exception(f"Supplied Base Rom appears to not be an english copy of Pokémon White Version.")
    return base_rom_bytes


def get_base_rom_path(version: str, file_name: str = "") -> str:
    if not file_name:
        file_name = get_settings()["pokemon_bw_settings"][f"{version}_rom"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name
