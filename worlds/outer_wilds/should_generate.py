from enum import Enum
from typing import Optional
from .options import OuterWildsGameOptions


# logsanity only matters for locations, not items or connections
def should_generate_location(category: Optional[str], requires_logsanity: bool, options: OuterWildsGameOptions) -> bool:
    if requires_logsanity and not options.logsanity:
        return False
    return should_generate(category, options)


def should_generate(category: Optional[str], options: OuterWildsGameOptions) -> bool:
    if category is None:  # this item/location/connection gets generated no matter what the player options are
        return True
    elif category == 'base':  # is generated unless dlc_only is true
        return options.dlc_only.value == 0
    elif category == 'dlc':  # only generated if enable_eote_dlc is true
        return options.enable_eote_dlc.value == 1
    elif category == 'base+dlc':  # both base game and dlc must be enabled to generate; used only for victory events
        return options.enable_eote_dlc.value == 1 and options.dlc_only.value == 0
    # each story mod will be its own generation category
