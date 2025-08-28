from BaseClasses import LocationProgressType
from .. import ProgressTypeMethod


always_priority: ProgressTypeMethod = lambda world: LocationProgressType.PRIORITY

always_default: ProgressTypeMethod = lambda world: LocationProgressType.DEFAULT

always_excluded: ProgressTypeMethod = lambda world: LocationProgressType.EXCLUDED

season_dependant: ProgressTypeMethod = lambda world: (
    LocationProgressType.EXCLUDED if world.options.season_control == "vanilla" else LocationProgressType.DEFAULT
)

key_item_location: ProgressTypeMethod = lambda world: (
    LocationProgressType.PRIORITY if "Prioritize key item locations" in world.options.modify_logic
    else LocationProgressType.DEFAULT
)
