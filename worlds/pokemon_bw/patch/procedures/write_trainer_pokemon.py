import zipfile
from typing import TYPE_CHECKING

from ...ndspy.rom import NintendoDSRom
from ...ndspy.narc import NARC

if TYPE_CHECKING:
    from ...rom import PokemonBWPatch


def write_species(bw_patch_instance: "PokemonBWPatch", opened_zipfile: zipfile.ZipFile) -> None:
    from ...data.pokemon.species import by_name

    slots: list[bytearray] = [
        bytearray(6*3)
        for _ in range(616)
    ]

    for pokemon in bw_patch_instance.world.trainer_teams:
        address = 3 * pokemon.team_number
        species_data = by_name[pokemon.species]
        slots[pokemon.trainer_id][address:address+2] = species_data.dex_number.to_bytes(2, "little")
        slots[pokemon.trainer_id][address+2] = species_data.form

    for file in range(1, 616):
        data = bytes(slots[file])
        while data[-3:] == b'\0\0\0':
            data = data[:-3]
        opened_zipfile.writestr(f"trainer/{file}_pokemon", data)


def patch_species(rom: NintendoDSRom, world_package: str, bw_patch_instance: "PokemonBWPatch") -> None:

    trainer_narc = NARC(rom.getFileByName("a/0/9/2"))
    pokemon_narc = NARC(rom.getFileByName("a/0/9/3"))

    for file_num in range(1, 616):

        trainer_file = trainer_narc.files[file_num]
        pokemon_file = bytearray(pokemon_narc.files[file_num])
        patch_file = bw_patch_instance.get_file(f"trainer/{file_num}_pokemon")
        unique_moves = trainer_file[0] % 2 == 1
        held_items = trainer_file[0] >= 2
        entry_length = 8 + (8 if unique_moves else 0) + (2 if held_items else 0)

        for team_slot in range(len(patch_file)//3):

            patch_address = team_slot * 3
            if patch_file[patch_address:patch_address+2] == b'\0\0':
                continue

            file_address = team_slot * entry_length + 4
            pokemon_file[file_address:file_address+3] = patch_file[patch_address:patch_address+3]

        pokemon_narc.files[file_num] = bytes(pokemon_file)

    rom.setFileByName("a/0/9/3", pokemon_narc.save())
