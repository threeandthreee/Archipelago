from typing import List

from .RegionBase import JakAndDaxterRegion
from ..Options import EnableOrbsanity
from .. import JakAndDaxterWorld
from ..Rules import can_reach_orbs_level
from ..locs import ScoutLocations as Scouts


def build_regions(level_name: str, world: JakAndDaxterWorld) -> List[JakAndDaxterRegion]:
    multiworld = world.multiworld
    options = world.options
    player = world.player

    main_area = JakAndDaxterRegion("Main Area", player, multiworld, level_name, 50)
    main_area.add_cell_locations([92, 93])
    main_area.add_fly_locations(Scouts.locGR_scoutTable.keys())  # All Flies here are accessible with blue eco.

    cliff = JakAndDaxterRegion("Cliff", player, multiworld, level_name, 0)
    cliff.add_cell_locations([94])

    main_area.connect(cliff, rule=lambda state:
                      state.has("Double Jump", player)
                      or state.has_all({"Crouch", "Crouch Jump"}, player)
                      or state.has_all({"Crouch", "Crouch Uppercut"}, player))

    cliff.connect(main_area)  # Jump down or ride blue eco elevator.

    multiworld.regions.append(main_area)
    multiworld.regions.append(cliff)

    # If Per-Level Orbsanity is enabled, build the special Orbsanity Region. This is a virtual region always
    # accessible to Main Area. The Locations within are automatically checked when you collect enough orbs.
    if options.enable_orbsanity == EnableOrbsanity.option_per_level:
        orbs = JakAndDaxterRegion("Orbsanity", player, multiworld, level_name)

        bundle_count = 50 // world.orb_bundle_size
        for bundle_index in range(bundle_count):
            orbs.add_orb_locations(0,
                                   bundle_index,
                                   access_rule=lambda state, level=level_name, bundle=bundle_index:
                                   can_reach_orbs_level(state, player, world, level, bundle))
        multiworld.regions.append(orbs)
        main_area.connect(orbs)

    return [main_area]