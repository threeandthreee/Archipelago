from typing import TYPE_CHECKING
import sys

# Increase recursion limit to allow deep day chains (up to 1000). Default (~1000) is borderline once
# Archipelago stack usage adds frames. Set higher to prevent RecursionError.
sys.setrecursionlimit(5000)

from BaseClasses import Location, Entrance
from .Locations import (
    DISH_LOCATIONS,
    dish_dictionary
)

if TYPE_CHECKING:
    from . import PlateUpWorld

def set_rule(spot: Location | Entrance, rule):
    spot.access_rule = rule


def add_rule(spot: Location | Entrance, rule, combine="and"):
    old_rule = spot.access_rule
    if old_rule is Location.access_rule:
        spot.access_rule = rule if combine == "and" else old_rule
    else:
        if combine == "and":
            spot.access_rule = lambda state: rule(state) and old_rule(state)
        else:
            spot.access_rule = lambda state: rule(state) or old_rule(state)


def restrict_locations_by_progression(world: "PlateUpWorld"):
    dish_order = world.valid_dish_locations
    for i in range(len(dish_order) - 1):
        current_loc_name = dish_order[i]
        next_loc_name = dish_order[i + 1]
        if next_loc_name in world.location_name_to_id:
            try:
                loc = world.get_location(next_loc_name)
                loc.access_rule = lambda state, cur=current_loc_name: state.can_reach(cur, "Location", world.player)
            except KeyError:
                pass


def filter_selected_dishes(world: "PlateUpWorld"):
    dish_count = world.options.dish.value
    if dish_count == 0:
        world.selected_dishes = []
        world.valid_dish_locations = []
        return

    all_dishes = list(dish_dictionary.values())
    selected = world.random.sample(all_dishes, min(dish_count, len(all_dishes)))
    world.selected_dishes = selected

    valid_locs = []
    for dish in selected:
        for day in range(1, 15 + 1):
            loc_name = f"{dish} - Day {day}"
            if loc_name in DISH_LOCATIONS:
                valid_locs.append(loc_name)

    world.valid_dish_locations = valid_locs

def apply_rules(world: "PlateUpWorld"):
    goal_type = world.options.goal.value

    if goal_type == 1:
        # Chain day completions
        for i in range(2, 1001):  
            current_day = f"Complete Day {i}"
            prev_day = f"Complete Day {i-1}"
            try:
                loc_current = world.get_location(current_day)
                loc_current.access_rule = (
                    lambda state, p=prev_day: state.can_reach(p, "Location", world.player)
                )
            except KeyError:
                pass
        # Chain star completions (each star requires previous star)
        max_stars = (world.options.day_count.value + 2) // 3  # ceil(day_count/3)
        for i in range(2, max_stars + 1):
            current_star = f"Complete Star {i}"
            prev_star = f"Complete Star {i-1}"
            try:
                loc_current = world.get_location(current_star)
                loc_current.access_rule = (
                    lambda state, p=prev_star: state.can_reach(p, "Location", world.player)
                )
            except KeyError:
                pass
    else:
        # Chain franchise goal completions
        for i in range(2, 51):  # expanded to support up to 50 franchises
            suffix = "" if i - 1 == 1 else f" {i-1}"
            try:
                loc = world.get_location(f"Franchise {i} times")
                required_loc = f"Franchise - Complete Day 15 After Franchised{suffix}"
                loc.access_rule = lambda state, req=required_loc: state.can_reach(req, "Location", world.player)
            except KeyError:
                pass
        # Chain stars within each franchise run (each star after the first requires the previous in same run)
        star_labels = ["First Star", "Second Star", "Third Star", "Fourth Star", "Fifth Star"]
        for run in range(50):  # runs 0..49
            suffix = "" if run == 0 else (" After Franchised" if run == 1 else f" After Franchised {run}")
            # Build full names
            for idx in range(1, len(star_labels)):
                prev_name = f"Franchise - {star_labels[idx-1]}{suffix}"
                cur_name = f"Franchise - {star_labels[idx]}{suffix}"
                try:
                    loc_current = world.get_location(cur_name)
                    loc_current.access_rule = (
                        lambda state, p=prev_name: state.can_reach(p, "Location", world.player)
                    )
                except KeyError:
                    pass