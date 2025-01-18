import re
from abc import ABC, abstractmethod
from BaseClasses import CollectionState
from worlds.minishoot.options import MinishootOptions

progressive_cannon = 'Progressive Cannon'
dash = 'Dash'
surf = 'Surf'
boost = 'Boost'
mercant = 'Mercant'
blacksmith = 'Blacksmith'
d1_small_key = 'Small Key (Dungeon 1)'
d1_boss_key = 'Boss Key (Dungeon 1)'
d1_reward = 'Dungeon 1 Reward'
supershot = 'Supershot'
d2_small_key = 'Small Key (Dungeon 2)'
d2_boss_key = 'Boss Key (Dungeon 2)'
d2_reward = 'Dungeon 2 Reward'
scarab_collector = 'Scarab Collector'
d3_small_key = 'Small Key (Dungeon 3)'
d3_boss_key = 'Boss Key (Dungeon 3)'
d3_reward = 'Dungeon 3 Reward'
spirit_dash = 'Spirit Dash'
dark_heart = 'Dark Heart'
bard = 'Bard'
d4_reward = 'Dungeon 4 Reward'
dark_key = 'Dark Key'
scarab_key = 'Scarab Key'
family_child = 'Family Child'
family_parent_1 = 'Family Parent 1'
family_parent_2 = 'Family Parent 2'
primordial_crystal = "Primordial Crystal"
power_of_protection = "Power of protection"
scarab = "Scarab"

d5_central_wing = 'Dungeon 5 - Central wing'
d5_west_wing = 'Dungeon 5 - West wing'
d5_east_wing = 'Dungeon 5 - East wing'
d5_boss = 'Dungeon 5 - Boss'
desert_grotto_west_drop = 'Desert Grotto - West Drop'
desert_grotto_east_drop = 'Desert Grotto - East Drop'
scarab_temple_bottom_left_torch = 'Scarab Temple - Bottom Left Torch'
scarab_temple_bottom_right_torch = 'Scarab Temple - Bottom Right Torch'
scarab_temple_top_left_torch = 'Scarab Temple - Top Left Torch'
scarab_temple_top_right_torch = 'Scarab Temple - Top Right Torch'
sunken_city_city = 'Sunken City - City'
sunken_city_east = 'Sunken City - East'
sunken_city_east_torch = 'Sunken City - East torch'
sunken_city_fountain = 'Sunken City - Fountain'
sunken_city_west_island = 'Sunken City - West Island'
sunken_city_west_torch = 'Sunken City - West torch'

# This is a rudimentary implementation of a rule parser for Minishoot logic.
# Basically, it allows for predicates to be defined in the form of strings, and then evaluated in the context of a given state.
# Those predicates can be combined using "and" and "or" operators, with "and" having higher precedence.
# For example, the expression "can_fight and can_surf or can_dash" would be parsed as "(can_fight and can_surf) or can_dash".
# Some predicates can take arguments, which are passed in parentheses after the predicate name (e.g. "have_d1_keys(2)").
def simple_parse(expression: str, state: CollectionState, world) -> bool:
    player = world.player
    options = world.options

    def can_fight(state: CollectionState, options: MinishootOptions, level: int = 1) -> bool:
        if options.cannon_level_logical_requirements:
            return state.has(progressive_cannon, player, level)
        return state.has(progressive_cannon, player)

    conditions = {
        'true': lambda state: True,
        'can_free_blacksmith': lambda state: state.has(blacksmith, player),
        'can_free_mercant': lambda state: state.has(mercant, player),
        'can_obtain_super_crystals': lambda state, arg: state.has(progressive_cannon, player) and state.has(dash, player) and state.has(supershot, player) and state.has(surf, player), # TODO: Implement this
        'can_fight': lambda state: state.has(progressive_cannon, player),
        'can_fight_lvl2': lambda state: can_fight(state, options, 2),
        'can_fight_lvl3': lambda state: can_fight(state, options, 3),
        'can_fight_lvl4': lambda state: can_fight(state, options, 4),
        'can_fight_lvl5': lambda state: can_fight(state, options, 5),
        'can_dash': lambda state: state.has(dash, player),
        'can_surf': lambda state: state.has(surf, player),
        'can_boost': lambda state: state.has(boost, player),
        'can_destroy_bushes': lambda state: state.has(progressive_cannon, player),
        'can_destroy_ruins': lambda state: state.has(progressive_cannon, player),
        'have_d1_keys': lambda state, arg: state.has(d1_small_key, player, arg),
        'have_d1_boss_key': lambda state: state.has(d1_boss_key, player),
        'can_dodge_homing_charges': lambda state: state.has(dash, player) or state.has(boost, player),
        'can_destroy_rocks': lambda state: state.has(supershot, player) or state.has(primordial_crystal, player),
        'can_dodge_fast_patterns': lambda state: state.has(dash, player) or state.has(boost, player),
        'can_destroy_pots': lambda state: state.has(progressive_cannon, player),
        'can_destroy_crystals': lambda state: state.has(progressive_cannon, player),
        'have_d2_keys': lambda state, arg: state.has(d2_small_key, player, arg),
        'have_d2_boss_key': lambda state: state.has(d2_boss_key, player),
        'can_destroy_walls': lambda state: state.has(supershot, player) or state.has(primordial_crystal, player),
        'can_obtain_scarabs': lambda state, arg: state.has(scarab, player, arg),
        'can_free_scarab_collector': lambda state: state.has(scarab_collector, player),
        'can_light_torches': lambda state: state.has(supershot, player),
        'can_destroy_plants': lambda state: state.has(progressive_cannon, player),
        'can_destroy_coconuts': lambda state: state.has(progressive_cannon, player),
        'can_destroy_shells': lambda state: state.has(progressive_cannon, player),
        'have_d3_keys': lambda state, arg: state.has(d3_small_key, player, arg),
        'have_d3_boss_key': lambda state: state.has(d3_boss_key, player),
        'can_light_all_scarab_temple_torches': lambda state: state.can_reach_region(scarab_temple_bottom_left_torch, player) and state.can_reach_region(scarab_temple_bottom_right_torch, player) and state.can_reach_region(scarab_temple_top_left_torch, player) and state.can_reach_region(scarab_temple_top_right_torch, player) and state.has(supershot, player),
        'can_dodge_purple_bullets': lambda state: state.has(dash, player) and state.has(spirit_dash, player),
        'can_unlock_final_boss_door': lambda state: state.has(dark_heart, player),
        'can_open_north_city_bridge': lambda state: state.can_reach_region(sunken_city_fountain, player) and can_fight(state, options, 4) and state.has(surf, player),
        'cannot_dash': lambda state: not state.has(dash, player),
        'can_free_bard': lambda state: state.has(bard, player),
        'have_all_spirits': lambda state: state.has(surf, player) and state.has(dash, player) and state.has(boost, player) and state.has(supershot, player), # TODO: Implement this
        'can_open_dungeon_5': lambda state: state.has(d1_reward, player) and state.has(d2_reward, player) and state.has(d3_reward, player) and state.has(d4_reward, player) and state.has(dark_key, player),
        'can_unlock_primordial_cave_door': lambda state: state.has(scarab_key, player),
        'can_light_city_torches': lambda state: state.has(supershot, player) and state.can_reach_region(sunken_city_west_torch, player) and state.can_reach_region(sunken_city_east_torch, player),
        'can_open_sunken_temple': lambda state: state.has(surf, player) and can_fight(state, options, 4) and state.can_reach_region(sunken_city_west_island, player) and state.can_reach_region(sunken_city_city, player) and state.can_reach_region(sunken_city_east, player),
        'can_light_desert_grotto_torches': lambda state: state.has(supershot, player) and state.can_reach_region(desert_grotto_west_drop, player) and state.can_reach_region(desert_grotto_east_drop, player),
        'can_clear_both_d5_arenas': lambda state: state.can_reach_region(d5_west_wing, player) and state.can_reach_region(d5_east_wing, player) and can_fight(state, options, 5) and state.has(dash, player),
        'can_free_family': lambda state: state.has(family_child, player) and state.has(family_parent_1, player) and state.has(family_parent_2, player),
        'cannot_surf': lambda state: not state.has(surf, player),
        'have_cleared_d5': lambda state: state.can_reach_region(d5_boss, player),
        'forest_is_blocked': lambda state: options.blocked_forest,
        'forest_is_open': lambda state: not options.blocked_forest,
        'can_blast_crystals': lambda state: state.has(power_of_protection, player) and state.has(progressive_cannon, player),
        'can_destroy_trees': lambda state: state.has(supershot, player),
    }

    # Split the expression by "or" and "and" using regular expressions
    try:
        or_parts = re.split(r'\s+or\s+', expression)
        for or_part in or_parts:
            and_parts = re.split(r'\s+and\s+', or_part)
            if all(
                conditions[cond.split('(')[0].strip()](state, int(cond.strip().split('(')[1].rstrip(')'))) if '(' in cond else conditions[cond.strip()](state)
                for cond in and_parts
            ):
                return True
        return False
    except KeyError:
        raise ValueError(f"Invalid condition: {expression}")
