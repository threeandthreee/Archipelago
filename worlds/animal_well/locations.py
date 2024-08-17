from enum import IntEnum
from typing import Dict, NamedTuple, Set, List
from .names import LocationNames as lname


class ByteSect(IntEnum):
    items = 1
    flames = 2
    bunnies = 3
    candles = 4
    house_key = 5


class AWLocationData(NamedTuple):
    offset: int  # location ID offset
    byte_section: int  # since where it is and what the length is varies
    byte_offset: int
    location_groups: List[str] = []


location_base_id = 11553377
# todo: add location groups for general regions
location_table: Dict[str, AWLocationData] = {
    # major items
    lname.b_wand_chest.value: AWLocationData(0, ByteSect.items, 68, ["Toys"]),
    lname.bb_wand_chest.value: AWLocationData(1, ByteSect.items, 95, ["Toys"]),
    lname.disc_spot.value: AWLocationData(2, ByteSect.items, 37, ["Toys"]),
    lname.yoyo_chest.value: AWLocationData(3, ByteSect.items, 97, ["Toys"]),
    lname.slink_chest.value: AWLocationData(4, ByteSect.items, 30, ["Toys"]),
    lname.flute_chest.value: AWLocationData(5, ByteSect.items, 46, ["Toys", "Egg Rewards"]),
    lname.top_chest.value: AWLocationData(6, ByteSect.items, 48, ["Toys", "Egg Rewards"]),
    lname.lantern_chest.value: AWLocationData(7, ByteSect.items, 75, ["Toys"]),
    lname.uv_lantern_chest.value: AWLocationData(8, ByteSect.items, 98, ["Toys"]),
    lname.b_ball_chest.value: AWLocationData(9, ByteSect.items, 15, ["Toys"]),
    lname.remote_chest.value: AWLocationData(10, ByteSect.items, 86, ["Toys"]),
    lname.wheel_chest.value: AWLocationData(11, ByteSect.items, 79, ["Toys"]),

    lname.mock_disc_chest.value: AWLocationData(12, ByteSect.items, 27, ["Toys"]),
    lname.fanny_pack_chest.value: AWLocationData(13, ByteSect.items, 100, ["Toys"]),

    lname.match_start_ceiling.value: AWLocationData(14, ByteSect.items, 70, ["Matches"]),
    lname.match_fish_mural.value: AWLocationData(15, ByteSect.items, 56, ["Matches"]),
    lname.match_dog_switch_bounce.value: AWLocationData(16, ByteSect.items, 11, ["Matches"]),
    lname.match_dog_upper_east.value: AWLocationData(17, ByteSect.items, 19, ["Matches"]),
    lname.match_bear.value: AWLocationData(18, ByteSect.items, 13, ["Matches"]),
    lname.match_above_egg_room.value: AWLocationData(19, ByteSect.items, 38, ["Matches"]),
    lname.match_center_well.value: AWLocationData(20, ByteSect.items, 21, ["Matches"]),
    lname.match_guard_room.value: AWLocationData(21, ByteSect.items, 81, ["Matches"]),
    lname.match_under_mouse_statue.value: AWLocationData(22, ByteSect.items, 63, ["Matches"]),

    lname.key_bear_lower.value: AWLocationData(23, ByteSect.items, 54, ["Keys"]),
    lname.key_bear_upper.value: AWLocationData(24, ByteSect.items, 34, ["Keys"]),
    lname.key_chest_mouse_head_lever.value: AWLocationData(25, ByteSect.items, 62, ["Keys"]),
    lname.key_frog_guard_room_west.value: AWLocationData(26, ByteSect.items, 82, ["Keys"]),
    lname.key_frog_guard_room_east.value: AWLocationData(27, ByteSect.items, 83, ["Keys"]),
    lname.key_dog.value: AWLocationData(28, ByteSect.items, 16, ["Keys"]),
    lname.key_house.value: AWLocationData(29, ByteSect.house_key, 4, ["Keys"]),
    lname.key_office.value: AWLocationData(30, ByteSect.items, 39, ["Keys"]),

    lname.medal_e.value: AWLocationData(31, ByteSect.items, 90, ["Keys", "Medals"]),
    lname.medal_s.value: AWLocationData(32, ByteSect.items, 41, ["Keys", "Medals"]),
    # lname.medal_k.value: AWLocationData(33, ["Keys", "Medals"]),

    # event only for now until modding tools maybe
    lname.flame_blue.value: AWLocationData(34, ByteSect.flames, 0x21E, ["Flames"]),
    lname.flame_green.value: AWLocationData(35, ByteSect.flames, 0x21F, ["Flames"]),
    lname.flame_violet.value: AWLocationData(36, ByteSect.flames, 0x220, ["Flames"]),
    lname.flame_pink.value: AWLocationData(37, ByteSect.flames, 0x221, ["Flames"]),

    # eggs, sorted by row top-to-bottom
    lname.egg_reference.value: AWLocationData(38, ByteSect.items, 0, ["Eggs"]),
    lname.egg_brown.value: AWLocationData(39, ByteSect.items, 1, ["Eggs"]),
    lname.egg_raw.value: AWLocationData(40, ByteSect.items, 2, ["Eggs"]),
    lname.egg_pickled.value: AWLocationData(41, ByteSect.items, 3, ["Eggs"]),
    lname.egg_big.value: AWLocationData(42, ByteSect.items, 4, ["Eggs"]),
    lname.egg_swan.value: AWLocationData(43, ByteSect.items, 5, ["Eggs"]),
    lname.egg_forbidden.value: AWLocationData(44, ByteSect.items, 6, ["Eggs"]),
    lname.egg_shadow.value: AWLocationData(45, ByteSect.items, 7, ["Eggs"]),
    lname.egg_vanity.value: AWLocationData(46, ByteSect.items, 8, ["Eggs"]),
    lname.egg_service.value: AWLocationData(47, ByteSect.items, 9, ["Eggs"]),

    lname.egg_depraved.value: AWLocationData(48, ByteSect.items, 12, ["Eggs"]),
    lname.egg_chaos.value: AWLocationData(49, ByteSect.items, 14, ["Eggs"]),
    lname.egg_upside_down.value: AWLocationData(50, ByteSect.items, 17, ["Eggs"]),
    lname.egg_evil.value: AWLocationData(51, ByteSect.items, 18, ["Eggs"]),
    lname.egg_sweet.value: AWLocationData(52, ByteSect.items, 20, ["Eggs"]),
    lname.egg_chocolate.value: AWLocationData(53, ByteSect.items, 22, ["Eggs"]),
    lname.egg_value.value: AWLocationData(54, ByteSect.items, 23, ["Eggs"]),
    lname.egg_plant.value: AWLocationData(55, ByteSect.items, 24, ["Eggs"]),
    lname.egg_red.value: AWLocationData(56, ByteSect.items, 25, ["Eggs"]),
    lname.egg_orange.value: AWLocationData(57, ByteSect.items, 26, ["Eggs"]),
    lname.egg_sour.value: AWLocationData(58, ByteSect.items, 28, ["Eggs"]),
    lname.egg_post_modern.value: AWLocationData(59, ByteSect.items, 29, ["Eggs"]),

    lname.egg_universal.value: AWLocationData(60, ByteSect.items, 31, ["Eggs"]),
    lname.egg_lf.value: AWLocationData(61, ByteSect.items, 32, ["Eggs"]),
    lname.egg_zen.value: AWLocationData(62, ByteSect.items, 33, ["Eggs"]),
    lname.egg_future.value: AWLocationData(63, ByteSect.items, 35, ["Eggs"]),
    lname.egg_friendship.value: AWLocationData(64, ByteSect.items, 36, ["Eggs"]),
    lname.egg_truth.value: AWLocationData(65, ByteSect.items, 40, ["Eggs"]),
    lname.egg_transcendental.value: AWLocationData(66, ByteSect.items, 42, ["Eggs"]),
    lname.egg_ancient.value: AWLocationData(67, ByteSect.items, 43, ["Eggs"]),
    lname.egg_magic.value: AWLocationData(68, ByteSect.items, 44, ["Eggs"]),
    lname.egg_mystic.value: AWLocationData(69, ByteSect.items, 45, ["Eggs"]),
    lname.egg_holiday.value: AWLocationData(70, ByteSect.items, 51, ["Eggs"]),
    lname.egg_rain.value: AWLocationData(71, ByteSect.items, 52, ["Eggs"]),
    lname.egg_razzle.value: AWLocationData(72, ByteSect.items, 53, ["Eggs"]),
    lname.egg_dazzle.value: AWLocationData(73, ByteSect.items, 55, ["Eggs"]),

    lname.egg_virtual.value: AWLocationData(74, ByteSect.items, 57, ["Eggs"]),
    lname.egg_normal.value: AWLocationData(75, ByteSect.items, 58, ["Eggs"]),
    lname.egg_great.value: AWLocationData(76, ByteSect.items, 59, ["Eggs"]),
    lname.egg_gorgeous.value: AWLocationData(77, ByteSect.items, 60, ["Eggs"]),
    lname.egg_planet.value: AWLocationData(78, ByteSect.items, 64, ["Eggs"]),
    lname.egg_moon.value: AWLocationData(79, ByteSect.items, 65, ["Eggs"]),
    lname.egg_galaxy.value: AWLocationData(80, ByteSect.items, 66, ["Eggs"]),
    lname.egg_sunset.value: AWLocationData(81, ByteSect.items, 67, ["Eggs"]),
    lname.egg_goodnight.value: AWLocationData(82, ByteSect.items, 69, ["Eggs"]),
    lname.egg_dream.value: AWLocationData(83, ByteSect.items, 71, ["Eggs"]),
    lname.egg_travel.value: AWLocationData(84, ByteSect.items, 72, ["Eggs"]),
    lname.egg_promise.value: AWLocationData(85, ByteSect.items, 73, ["Eggs"]),
    lname.egg_ice.value: AWLocationData(86, ByteSect.items, 74, ["Eggs"]),
    lname.egg_fire.value: AWLocationData(87, ByteSect.items, 76, ["Eggs"]),

    lname.egg_bubble.value: AWLocationData(88, ByteSect.items, 77, ["Eggs"]),
    lname.egg_desert.value: AWLocationData(89, ByteSect.items, 78, ["Eggs"]),
    lname.egg_clover.value: AWLocationData(90, ByteSect.items, 80, ["Eggs"]),
    lname.egg_brick.value: AWLocationData(91, ByteSect.items, 84, ["Eggs"]),
    lname.egg_neon.value: AWLocationData(92, ByteSect.items, 85, ["Eggs"]),
    lname.egg_iridescent.value: AWLocationData(93, ByteSect.items, 87, ["Eggs"]),
    lname.egg_rust.value: AWLocationData(94, ByteSect.items, 88, ["Eggs"]),
    lname.egg_scarlet.value: AWLocationData(95, ByteSect.items, 89, ["Eggs"]),
    lname.egg_sapphire.value: AWLocationData(96, ByteSect.items, 91, ["Eggs"]),
    lname.egg_ruby.value: AWLocationData(97, ByteSect.items, 92, ["Eggs"]),
    lname.egg_jade.value: AWLocationData(98, ByteSect.items, 93, ["Eggs"]),
    lname.egg_obsidian.value: AWLocationData(99, ByteSect.items, 94, ["Eggs"]),
    lname.egg_crystal.value: AWLocationData(100, ByteSect.items, 99, ["Eggs"]),
    lname.egg_golden.value: AWLocationData(101, ByteSect.items, 101, ["Eggs"]),

    lname.egg_65.value: AWLocationData(102, ByteSect.items, 47, ["Egg Rewards"]),

    # map things
    lname.map_chest.value: AWLocationData(103, ByteSect.items, 61, []),
    lname.stamp_chest.value: AWLocationData(104, ByteSect.items, 50, []),
    lname.pencil_chest.value: AWLocationData(105, ByteSect.items, 49, ["Egg Rewards"]),

    # bnnnnuyuy
    lname.bunny_mural.value: AWLocationData(106, ByteSect.bunnies, 15, ["Bunnies"]),
    lname.bunny_chinchilla_vine.value: AWLocationData(107, ByteSect.bunnies, 11, ["Bunnies"]),
    lname.bunny_water_spike.value: AWLocationData(108, ByteSect.bunnies, 0, ["Bunnies"]),
    lname.bunny_map.value: AWLocationData(109, ByteSect.bunnies, 7, ["Bunnies"]),
    lname.bunny_uv.value: AWLocationData(110, ByteSect.bunnies, 9, ["Bunnies"]),
    lname.bunny_fish.value: AWLocationData(111, ByteSect.bunnies, 6, ["Bunnies"]),
    lname.bunny_face.value: AWLocationData(112, ByteSect.bunnies, 4, ["Bunnies"]),
    lname.bunny_crow.value: AWLocationData(113, ByteSect.bunnies, 31, ["Bunnies"]),
    lname.bunny_duck.value: AWLocationData(114, ByteSect.bunnies, 22, ["Bunnies"]),
    lname.bunny_dream.value: AWLocationData(115, ByteSect.bunnies, 28, ["Bunnies"]),
    lname.bunny_file_bud.value: AWLocationData(116, ByteSect.bunnies, 10, ["Bunnies"]),
    lname.bunny_lava.value: AWLocationData(117, ByteSect.bunnies, 30, ["Bunnies"]),
    lname.bunny_tv.value: AWLocationData(118, ByteSect.bunnies, 8, ["Bunnies"]),
    lname.bunny_barcode.value: AWLocationData(119, ByteSect.bunnies, 2, ["Bunnies"]),
    lname.bunny_ghost_dog.value: AWLocationData(120, ByteSect.bunnies, 25, ["Bunnies"]),
    lname.bunny_disc_spike.value: AWLocationData(121, ByteSect.bunnies, 3, ["Bunnies"]),

    # candles
    lname.candle_first.value: AWLocationData(122, ByteSect.candles, 7, ["Candles"]),
    lname.candle_dog_dark.value: AWLocationData(123, ByteSect.candles, 4, ["Candles"]),
    lname.candle_dog_switch_box.value: AWLocationData(124, ByteSect.candles, 3, ["Candles"]),
    lname.candle_dog_many_switches.value: AWLocationData(125, ByteSect.candles, 2, ["Candles"]),
    lname.candle_dog_disc_switches.value: AWLocationData(126, ByteSect.candles, 1, ["Candles"]),
    lname.candle_dog_bat.value: AWLocationData(127, ByteSect.candles, 0, ["Candles"]),
    lname.candle_fish.value: AWLocationData(128, ByteSect.candles, 6, ["Candles"]),
    lname.candle_frog.value: AWLocationData(129, ByteSect.candles, 8, ["Candles"]),
    lname.candle_bear.value: AWLocationData(130, ByteSect.candles, 5, ["Candles"]),

    # extras
    lname.mama_cha.value: AWLocationData(131, ByteSect.items, 10, []),
}

location_name_to_id: Dict[str, int] = {name: location_base_id + data.offset for name, data in location_table.items()}

location_name_groups: Dict[str, Set[str]] = {}
for loc_name, loc_data in location_table.items():
    for location_group in loc_data.location_groups:
        location_name_groups.setdefault(location_group, set()).add(loc_name)
