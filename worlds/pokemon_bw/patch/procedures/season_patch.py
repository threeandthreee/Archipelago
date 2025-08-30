from typing import TYPE_CHECKING

from ...ndspy.rom import NintendoDSRom
from ...ndspy.code import saveOverlayTable
import pkgutil

from .. import otpp

if TYPE_CHECKING:
    from ...rom import PokemonBlackPatch


def patch(rom: NintendoDSRom, world_package: str, bw_patch_instance: "PokemonBlackPatch") -> None:
    otpp_patch: bytes = pkgutil.get_data(world_package, "patch/seasons_otpp/ov20_decomp")
    overlay_table = rom.loadArm9Overlays()
    ov20 = overlay_table[20]
    ov20.data = otpp.patch(ov20.data, otpp_patch)
    rom.files[ov20.fileID] = ov20.save(compress=True)
    rom.arm9OverlayTable = saveOverlayTable(overlay_table)

