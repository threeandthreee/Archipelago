from typing import Optional, NamedTuple

from ..Logic import *


class LocationData(NamedTuple):
    location_id: Optional[int]
    name: str
    access_rule: Optional[Callable[[CollectionState, int], bool]] = None


""" Oozla """
OOZLA_OUTSIDE_MEGACORP_STORE = LocationData(10, "Oozla: Outside Megacorp Store - Dynamo")
OOZLA_END_STORE_CUTSCENE = LocationData(11, "Oozla: End of Store Cutscene", can_dynamo)
OOZLA_MEGACORP_SCIENTIST = LocationData(12, "Oozla: Megacorp Scientist - Tractor Beam")
OOZLA_TRACTOR_PUZZLE_PB = LocationData(13, "Oozla: Tractor Puzzle - Platinum Bolt", can_tractor)
OOZLA_SWAMP_RUINS_PB = LocationData(14, "Oozla: Swamp Ruins - Platinum Bolt", can_dynamo)
OOZLA_SWAMP_MONSTER_II = LocationData(
    15, "Oozla: Swamp Monster II - Box Breaker",
    lambda state, player: can_dynamo(state, player) and can_gravity(state, player)
)

""" Maktar """
MAKTAR_ARENA_CHALLENGE = LocationData(20, "Maktar: Arena Challenge - Electrolyzer")
MAKTAR_PHOTO_BOOTH = LocationData(21, "Maktar: Photo Booth", can_electrolyze)
MAKTAR_DEACTIVATE_JAMMING_ARRAY = LocationData(22, "Maktar: Deactivate Jamming Array", can_tractor)
MAKTAR_JAMMING_ARRAY_PB = LocationData(23, "Maktar: Jamming Array - Platinum Bolt", can_tractor)
MAKTAR_CRANE_PB = LocationData(24, "Maktar: Crane - Platinum Bolt")

""" Endako """
ENDAKO_CLANK_APARTMENT_SS = LocationData(30, "Endako: Clank's Apartment - Swingshot")
ENDAKO_CLANK_APARTMENT_GB = LocationData(31, "Endako: Clank's Apartment - Grindboots")
ENDAKO_RESCUE_CLANK_HELI = LocationData(32, "Endako: Rescue Clank Heli-Pack", can_electrolyze)
ENDAKO_RESCUE_CLANK_THRUSTER = LocationData(33, "Endako: Rescue Clank Thruster-Pack", can_electrolyze)
ENDAKO_LEDGE_PB = LocationData(34, "Endako: Ledge - Platinum Bolt", )
ENDAKO_CRANE_PB = LocationData(35, "Endako: Crane - Platinum Bolt", can_electrolyze)
ENDAKO_CRANE_NT = LocationData(
    36, "Endako: Crane - Nanotech Boost",
    lambda state, player: can_electrolyze(state, player) and can_infiltrate(state, player)
)

""" Barlow """
BARLOW_INVENTOR = LocationData(40, "Barlow: Inventor - Thermanator", can_swingshot)
BARLOW_HOVERBIKE_RACE_TRANSMISSION = LocationData(
    41, "Barlow: Hoverbike Race Transmission",
    lambda state, player: can_improved_jump(state, player) and can_electrolyze(state, player)
)
BARLOW_HOVERBIKE_RACE_PB = LocationData(
    42, "Barlow: Hoverbike Race - Platinum Bolt",
    lambda state, player: can_improved_jump(state, player) and can_electrolyze(state, player)
)
BARLOW_HOUND_CAVE_PB = LocationData(43, "Barlow: Hound Cave - Platinum Bolt", can_swingshot)


""" Feltzin System """
FELTZIN_DEFEAT_THUG_SHIPS = LocationData(50, "Feltzin: Defeat Thug Ships")
FELTZIN_RACE_PB = LocationData(51, "Feltzin: Race - Platinum Bolt")
FELTZIN_CARGO_BAY_NT = LocationData(52, "Feltzin: Cargo Bay - Nanotech Boost")

""" Notak """
NOTAK_TOP_PIER_TELESCREEN = LocationData(
    60, "Notak: Top of Pier Telescreen",
    lambda state, player: can_improved_jump(state, player) and can_thermanate(state, player)
)
NOTAK_WORKER_BOTS = LocationData(
    61, "Notak: Worker Bots",
    lambda state, player: can_heli(state, player) and can_thermanate(state, player)
)
NOTAK_BEHIND_BUILDING_PB = LocationData(62, "Notak: Behind Building - Platinum Bolt")
NOTAK_PROMENADE_SIGN_PB = LocationData(63, "Notak: Promenade Sign - Platinum Bolt")
NOTAK_TIMED_DYNAMO_PB = LocationData(
    64, "Notak: Timed Dynamo - Platinum Bolt",
    lambda state, player:
        can_improved_jump(state, player)
        and can_thermanate(state, player)
        and can_dynamo(state, player)
)
NOTAK_PROMENADE_END_NT = LocationData(65, "Notak: Promenade End - Nanotech Boost")

""" Siberius """
SIBERIUS_DEFEAT_THIEF = LocationData(70, "Siberius: Defeat Thief", can_swingshot)
SIBERIUS_FLAMEBOT_LEDGE_PB = LocationData(71, "Siberius: Flamebot Ledge - Platinum Bolt", can_tractor)
SIBERIUS_FENCED_AREA_PB = LocationData(72, "Siberius: Fenced Area - Platinum Bolt", can_heli)

""" Tabora """
# NOTICE: Heli-Pack and Swingshot are already logically required in order to access this planet
TABORA_MEET_ANGELA = LocationData(80, "Tabora: Meet Angela")
TABORA_UNDERGROUND_MINES_END = LocationData(81, "Tabora: Underground Mines - Glider", can_thermanate)
TABORA_UNDERGROUND_MINES_PB = LocationData(82, "Tabora: Underground Mines - Platinum Bolt", can_thermanate)
TABORA_CANYON_GLIDE_PB = LocationData(
    83, "Tabora: Canyon Glide - Platinum Bolt",
    lambda state, player: can_thermanate(state, player) and can_glide(state, player)
)
TABORA_NORTHEAST_DESERT_PB = LocationData(84, "Tabora: Northeast Desert - Platinum Bolt")
TABORA_CANYON_GLIDE_PILLAR_NT = LocationData(
    85, "Tabora: Canyon Glide Pillar - Nanotech Boost",
    lambda state, player: can_thermanate(state, player) and can_glide(state, player)
)
TABORA_OMNIWRENCH_10000 = LocationData(86, "Tabora: OmniWrench 10000")

""" Dobbo """
DOBBO_DEFEAT_THUG_LEADER = LocationData(
    90, "Dobbo: Defeat Thug Leader",
    lambda state, player:
        can_improved_jump(state, player)
        and can_dynamo(state, player)
        and can_swingshot(state, player)
)
DOBBO_FACILITY_TERMINAL = LocationData(
    91, "Dobbo: Facility Terminal",
    lambda state, player:
        can_dynamo(state, player)
        and can_swingshot(state, player)
        and can_glide(state, player)
        and can_electrolyze(state, player)
)
DOBBO_SPIDERBOT_ROOM_PB = LocationData(
    92, "Dobbo: Spiderbot Room - Platinum Bolt",
    lambda state, player:
        can_dynamo(state, player)
        and can_swingshot(state, player)
        and can_spiderbot(state, player)
)
DOBBO_FACILITY_GLIDE_PB = LocationData(
    93, "Dobbo: Facility Glide End - Platinum Bolt",
    lambda state, player: can_dynamo(state, player) and can_swingshot(state, player) and can_glide(state, player)
)
DOBBO_FACILITY_GLIDE_NT = LocationData(
    94, "Dobbo: Facility Glide Beginning - Nanotech Boost",
    lambda state, player: can_dynamo(state, player) and can_swingshot(state, player) and can_glide(state, player)
)

""" Hrugis """
HRUGIS_DESTROY_DEFENSES = LocationData(100, "Hrugis Cloud: Destroy Defenses")
HRUGIS_RACE_PB = LocationData(101, "Hrugis Cloud: Race - Platinum Bolt")

""" Joba """
JOBA_FIRST_HOVERBIKE_RACE = LocationData(110, "Joba: First Hoverbike Race - Charge Boots", can_swingshot)
JOBA_SHADY_SALESMAN = LocationData(
    111, "Joba: Shady Salesman - Levitator",
    lambda state, player: can_dynamo(state, player) and can_improved_jump(state, player)
)
JOBA_ARENA_BATTLE = LocationData(
    112, "Joba: Arena Battle - Gravity Boots",
    lambda state, player:
        can_dynamo(state, player)
        and can_improved_jump(state, player)
        and can_levitate(state, player)
)
JOBA_ARENA_CAGE_MATCH = LocationData(
    113, "Joba: Arena Cage Match - Infiltrator",
    lambda state, player:
        can_dynamo(state, player)
        and can_improved_jump(state, player)
        and can_levitate(state, player)
)
JOBA_HIDDEN_CLIFF_PB = LocationData(
    114, "Joba: Hidden Cliff - Platinum Bolt",
    lambda state, player: can_dynamo(state, player) and can_swingshot(state, player)
)
JOBA_LEVITATOR_TOWER_PB = LocationData(
    115, "Joba: Levitator Tower - Platinum Bolt",
    lambda state, player:
        can_dynamo(state, player)
        and can_improved_jump(state, player)
        and can_levitate(state, player)
)
JOBA_HOVERBIKE_RACE_SHORTCUT_NT = LocationData(116, "Joba: Hoverbike Race Shortcut - Nanotech Boost", can_swingshot)
JOBA_TIMED_DYNAMO_NT = LocationData(117, "Joba: Timed Dynamo Course - Nanotech Boost", can_dynamo)

""" Todano """
TODANO_SEARCH_ROCKET_SILO = LocationData(
    120, "Todano: Search Rocket Silo",
    lambda state, player:
        can_improved_jump(state, player)
        and can_electrolyze(state, player)
        and can_infiltrate(state, player)
)
TODANO_STUART_ZURGO_TRADE = LocationData(
    121, "Todano: Stuart Zurgo Trade - Armor Magnetizer",
    lambda state, player:
        can_electrolyze(state, player)
        and can_tractor(state, player)
        and has_qwark_statuette(state, player)
)
TODANO_FACILITY_INTERIOR = LocationData(
    122, "Todano: Facility Interior - Sheepinator",
    lambda state, player: can_electrolyze(state, player) and can_tractor(state, player)
)
TODANO_NEAR_STUART_ZURGO_PB = LocationData(
    123, "Todano: Near Stuart Zurgo - Platinum Bolt",
    lambda state, player: can_electrolyze(state, player) and can_tractor(state, player)
)
TODANO_END_TOUR_PB = LocationData(124, "Todano: End of Tour - Platinum Bolt")
TODANO_SPIDERBOT_CONVEYOR_PB = LocationData(
    125, "Todano: Spiderbot Conveyor - Platinum Bolt",
    lambda state, player:
        can_electrolyze(state, player)
        and can_tractor(state, player)
        and can_improved_jump(state, player)
        and can_spiderbot(state, player)
)
TODANO_ROCKET_SILO_NT = LocationData(
    126, "Todano: Rocket Silo - Nanotech Boost",
    lambda state, player: can_electrolyze(state, player) and can_infiltrate(state, player)
)

""" Boldan """
BOLDAN_FIND_FIZZWIDGET = LocationData(
    130, "Boldan: Find Fizzwidget",
    lambda state, player:
        can_levitate(state, player)
        and can_gravity(state, player)
        and can_swingshot(state, player)
)
BOLDAN_SPIDERBOT_ALLEY_PB = LocationData(
    131, "Boldan: Spiderbot Alley - Platinum Bolt",
    lambda state, player: can_levitate(state, player) and can_spiderbot(state, player)
)
BOLDAN_FLOATING_PLATFORM_PB = LocationData(
    132, "Boldan: Floating Platform - Platinum Bolt",
    lambda state, player: can_levitate(state, player) and can_gravity(state, player)
)
BOLDAN_UPPER_DOME_PB = LocationData(
    133, "Boldan: Upper Dome - Platinum Bolt",
    lambda state, player:
        can_levitate(state, player)
        and can_gravity(state, player)
        and can_swingshot(state, player)
)
BOLDAN_FOUNTAIN_NT = LocationData(134, "Boldan: Fountain - Nanotech Boost", can_levitate)

""" Aranos Prison """
# NOTICE: Gravity Boots, Levitator and Infiltrator are already logically required in order to access this planet
ARANOS_CONTROL_ROOM = LocationData(140, "Aranos: Control Room")
ARANOS_PLUMBER = LocationData(141, "Aranos: Plumber - Qwark Statuette")
ARANOS_UNDER_SHIP_PB = LocationData(142, "Aranos: Under Ship - Platinum Bolt", can_heli)
ARANOS_OMNIWRENCH_12000 = LocationData(143, "Aranos: OmniWrench 12000")

""" Gorn """
GORN_DEFEAT_THUG_FLEET = LocationData(150, "Gorn: Defeat Thug Fleet")
GORN_RACE_PB = LocationData(151, "Gorn: Race - Platinum Bolt")

""" Snivelak """
SNIVELAK_RESCUE_ANGELA = LocationData(
    160, "Snivelak: Rescue Angela",
    lambda state, player:
        can_swingshot(state, player)
        and can_grind(state, player)
        and can_gravity(state, player)
        and can_dynamo(state, player)
)
SNIVELAK_DYNAMO_PLATFORMS_PB = LocationData(
    161, "Snivelak: Dynamo Platforms - Platinum Bolt",
    lambda state, player:
        can_swingshot(state, player)
        and can_grind(state, player)
        and can_gravity(state, player)
        and can_dynamo(state, player)
        and can_heli(state, player)
)
SNIVELAK_SWINGSHOT_TOWER_NT = LocationData(
    162, "Snivelak: Swingshot Tower - Nanotech Boost",
    lambda state, player: can_swingshot(state, player) and can_heli(state, player)
)

""" Smolg """
SMOLG_BALLOON_TRANSMISSION = LocationData(
    170, "Smolg: Balloon Transmission",
    lambda state, player:
        can_improved_jump(state, player)
        and can_dynamo(state, player)
        and can_electrolyze(state, player)
)
SMOLG_DISTRIBUTION_FACILITY_END = LocationData(
    171, "Smolg: Distribution Facility End - Hypnomatic Part",
    lambda state, player:
        can_improved_jump(state, player)
        and can_dynamo(state, player)
        and can_electrolyze(state, player)
        and can_grind(state, player)
        and can_infiltrate(state, player)
)
SMOLG_MUTANT_CRAB = LocationData(
    172, "Smolg: Mutant Crab",
    lambda state, player: can_swingshot(state, player) and can_levitate(state, player)
)
SMOLG_FLOATING_PLATFORM_PB = LocationData(
    173, "Smolg: Floating Platform - Platinum Bolt",
    lambda state, player: can_swingshot(state, player) and can_levitate(state, player)
)
SMOLG_WAREHOUSE_PB = LocationData(
    174, "Smolg: Warehouse - Platinum Bolt",
    lambda state, player: can_improved_jump(state, player) and can_dynamo(state, player)
)

""" Damosel """
DAMOSEL_HYPNOTIST = LocationData(
    180, "Damosel: Hypnotist",
    lambda state, player:
        can_swingshot(state, player)
        and can_improved_jump(state, player)
        and can_thermanate(state, player)
        and has_hypnomatic_parts(state, player)
)
DAMOSEL_TRAIN_RAILS = LocationData(181, "Damosel: Train Rails - Hypnomatic Part", can_grind)
DAMOSEL_DEFEAT_MOTHERSHIP = LocationData(182, "Damosel: Defeat Mothership - Mapper")
DAMOSEL_FROZEN_FOUNTAIN_PB = LocationData(
    183, "Damosel: Frozen Fountain - Platinum Bolt",
    lambda state, player:
        can_swingshot(state, player)
        and can_improved_jump(state, player)
        and can_thermanate(state, player)
        and can_grind(state, player)
)
DAMOSEL_PYRAMID_PB = LocationData(
    184, "Damosel: Pyramid - Platinum Bolt",
    lambda state, player:
        can_swingshot(state, player)
        and can_improved_jump(state, player)
        and can_thermanate(state, player)
        and can_hypnotize(state, player)
)

""" Grelbin """
GRELBIN_FIND_ANGELA = LocationData(190, "Grelbin: Find Angela", can_hypnotize)
GRELBIN_MYSTIC_MORE_MOONSTONES = LocationData(
    191, "Grelbin: Mystic More Moonstones - Hypnomatic Part",
    lambda state, player: can_glide(state, player) and can_infiltrate(state, player)
)
GRELBIN_ICE_PLAINS_PB = LocationData(
    192, "Grelbin: Ice Plains - Platinum Bolt",
    lambda state, player: can_glide(state, player) and can_infiltrate(state, player)
)
GRELBIN_UNDERWATER_TUNNEL_PB = LocationData(193, "Grelbin: Underwater Tunnel - Platinum Bolt", can_hypnotize)
GRELBIN_YETI_CAVE_PB = LocationData(
    194, "Grelbin: Yeti Cave - Platinum Bolt",
    lambda state, player:
        can_glide(state, player)
        and can_infiltrate(state, player)
        and can_hypnotize(state, player)
)

""" Yeedil """
YEEDIL_DEFEAT_MUTATED_PROTOPET = LocationData(
    None, "Yeedil: Defeat Mutated Protopet",
    lambda state, player:
        can_swingshot(state, player)
        and can_hypnotize(state, player)
        and can_improved_jump(state, player)
        and can_dynamo(state, player)
        and can_infiltrate(state, player)
        and can_electrolyze(state, player)
)
YEEDIL_BRIDGE_GRINDRAIL_PB = LocationData(200, "Yeedil: Bridge Grindrail - Platinum Bolt", can_grind)
YEEDIL_TRACTOR_PILLAR_PB = LocationData(
    201, "Yeedil: Tractor Pillar - Platinum Bolt",
    lambda state, player:
        can_swingshot(state, player)
        and can_hypnotize(state, player)
        and can_improved_jump(state, player)
        and can_dynamo(state, player)
        and can_infiltrate(state, player)
        and can_electrolyze(state, player)
        and can_tractor(state, player)
        and can_grind(state, player)
)
