from typing import TYPE_CHECKING, Any

from ...ndspy.rom import NintendoDSRom
from ...ndspy.fnt import Folder
import orjson

if TYPE_CHECKING:
    from ...rom import PokemonBlackPatch


def add_slot_data_file(rom: NintendoDSRom, world_package: str, bw_patch_instance: "PokemonBlackPatch") -> None:
    data: dict[str, Any] = {
        "slot_data": orjson.loads(bw_patch_instance.get_file("slot_data.json")),
        "player_name": bw_patch_instance.player_name,
        "data_package": orjson.loads(bw_patch_instance.get_file("datapackage.json")),
    }
    rom.files.append(orjson.dumps(data))
    rom.filenames.folders.append(("patch", Folder(None, ["slot_data.json"], len(rom.files)-1)))
