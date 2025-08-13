# Regions.py
import logging
import math
from typing import TYPE_CHECKING

from BaseClasses import Region, LocationProgressType  # <-- IMPORT LocationProgressType
from .Locations import (
    PlateUpLocation,
    EXCLUDED_LOCATIONS,
    FRANCHISE_LOCATION_DICT,
    DAY_LOCATION_DICT
)

if TYPE_CHECKING:
    from . import PlateUpWorld

def create_plateup_regions(world: "PlateUpWorld"):

    menu_region = Region("Menu", world.player, world.multiworld)
    progression_region = Region("Progression", world.player, world.multiworld)
    dish_region = Region("Dish Checks", world.player, world.multiworld)

    world.multiworld.regions.extend([menu_region, progression_region, dish_region])
    menu_region.connect(progression_region)
    progression_region.connect(dish_region)

    user_goal = world.options.goal.value
    progression_locs = []

    if user_goal == 0:
        # Franchise goal
        for loc_id in DAY_LOCATION_DICT.values():
            EXCLUDED_LOCATIONS.add(loc_id)

        required_franchises = world.options.franchise_count.value
        max_franchise_id = (required_franchises + 1) * 100000

        for name, loc_id in FRANCHISE_LOCATION_DICT.items():
            if loc_id < max_franchise_id or name == f"Franchise {required_franchises} times":
                loc = PlateUpLocation(world.player, name, loc_id, parent=progression_region)
                # Mark location as excluded if it's in EXCLUDED_LOCATIONS
                if loc_id in EXCLUDED_LOCATIONS:
                    loc.progress_type = LocationProgressType.EXCLUDED
                progression_region.locations.append(loc)
                progression_locs.append(name)
            else:
                world.excluded_locations.add(loc_id)

    elif user_goal == 1:
        # Day goal
        # Exclude all franchise locations
        for loc_id in FRANCHISE_LOCATION_DICT.values():
            world.excluded_locations.add(loc_id)

        required_days = world.options.day_count.value
        max_stars = math.ceil(required_days / 3)

        # Only add "Complete Day" locations that are within the required days
        for name, loc_id in DAY_LOCATION_DICT.items():
            if name.startswith("Complete Day "):
                day = int(name.removeprefix("Complete Day ").strip())
                if day <= required_days:
                    loc = PlateUpLocation(world.player, name, loc_id, parent=progression_region)
                    # Mark location as excluded if it's in EXCLUDED_LOCATIONS
                    if loc_id in EXCLUDED_LOCATIONS:
                        loc.progress_type = LocationProgressType.EXCLUDED
                    progression_locs.append(name)
                    progression_region.locations.append(loc)
                else:
                    world.excluded_locations.add(loc_id)

        # Only add "Complete Star" locations that are within the allowed stars
        for name, loc_id in DAY_LOCATION_DICT.items():
            if name.startswith("Complete Star "):
                star = int(name.removeprefix("Complete Star ").strip())
                if star <= max_stars:
                    loc = PlateUpLocation(world.player, name, loc_id, parent=progression_region)
                    # Mark location as excluded if it's in EXCLUDED_LOCATIONS
                    if loc_id in EXCLUDED_LOCATIONS:
                        loc.progress_type = LocationProgressType.EXCLUDED
                    progression_locs.append(name)
                    progression_region.locations.append(loc)
                else:
                    world.excluded_locations.add(loc_id)

    world.progression_locations = progression_locs
    logging.debug(f"[Player {world.multiworld.player_name[world.player]}] Final progression-locs: {progression_locs}")