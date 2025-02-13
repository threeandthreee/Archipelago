from BaseClasses import Region
from typing import TYPE_CHECKING
from .names import item_names, location_names
from .locations import (green_greens_locations, float_islands_locations, bubbly_clouds_locations, mt_dedede_locations,
                        peanut_plains_locations, mallow_castle_locations, cocoa_cave_locations, candy_mountain_locations,
                        dyna_blade_nest_locations, gourmet_race_locations, subtree_locations, crystal_locations,
                        old_tower_locations, garden_locations, romk_chapter_1_locations, romk_chapter_2_locations,
                        romk_chapter_3_locations, romk_chapter_4_locations, romk_chapter_5_locations,
                        romk_chapter_6_locations, romk_chapter_7_locations, floria_locations, aqualiss_locations,
                        skyhigh_locations, hotbeat_locations, cavios_locations, mecheye_locations, halfmoon_locations,
                        copy_planet_locations, space_locations, the_arena_locations, KSSLocation)

if TYPE_CHECKING:
    from . import KSSWorld

class KSSRegion(Region):
    game = "Kirby Super Star"


def create_region(name, world: "KSSWorld"):
    return KSSRegion(name, world.player, world.multiworld)


def create_trivial_regions(world: "KSSWorld", menu: KSSRegion):
    if "Gourmet Race" in world.options.included_subgames:
        gourmet_race = create_region("Gourmet Race", world)
        gourmet_race.add_locations(gourmet_race_locations, KSSLocation)
        menu.connect(gourmet_race, None, lambda state: state.has(item_names.gourmet_race, world.player))
        world.get_location(location_names.gr_complete).place_locked_item(
            world.create_item(item_names.gourmet_race_complete))
        world.multiworld.regions.append(gourmet_race)

    if "The Arena" in world.options.included_subgames:
        arena = create_region("The Arena", world)
        arena.add_locations(the_arena_locations, KSSLocation)
        menu.connect(arena, None, lambda state: state.has(item_names.the_arena, world.player))
        world.get_location(location_names.arena_complete).place_locked_item(
            world.create_item(item_names.the_arena_complete))
        world.multiworld.regions.append(arena)


def create_spring_breeze(world: "KSSWorld", menu: KSSRegion):
    spring_breeze = create_region("Spring Breeze", world)
    green_greens = create_region("Green Greens", world)
    float_islands = create_region("Float Islands", world)
    bubbly_clouds = create_region("Bubbly Clouds", world)
    mt_dedede = create_region("Mt. Dedede", world)

    for region, connection, locations in zip((green_greens, float_islands, bubbly_clouds, mt_dedede),
                                             (float_islands, bubbly_clouds, mt_dedede, None),
                                             (green_greens_locations, float_islands_locations, bubbly_clouds_locations,
                                              mt_dedede_locations)
                                             ):
        if connection:
            region.connect(connection)
        region.add_locations(locations, KSSLocation)

    menu.connect(spring_breeze, None, lambda state: state.has(item_names.spring_breeze, world.player))
    spring_breeze.connect(green_greens)
    world.get_location(location_names.sb_complete).place_locked_item(
        world.create_item(item_names.spring_breeze_complete))
    world.multiworld.regions.extend([spring_breeze, green_greens, float_islands, bubbly_clouds, mt_dedede])


def create_dyna_blade(world: "KSSWorld", menu: KSSRegion):
    dyna_blade = create_region("Dyna Blade", world)
    peanut_plains = create_region("Peanut Plains", world)
    mallow_castle = create_region("Mallow Castle", world)
    cocoa_cave = create_region("Cocoa Cave", world)
    candy_mountain = create_region("Candy Mountain", world)
    dyna_blade_nest = create_region("Dyna Blade's Nest", world)

    for region, connection, locations in zip((peanut_plains, mallow_castle, cocoa_cave, candy_mountain, dyna_blade_nest),
                                             (mallow_castle, cocoa_cave, candy_mountain, dyna_blade_nest, None),
                                             (peanut_plains_locations, mallow_castle_locations, cocoa_cave_locations,
                                              candy_mountain_locations, dyna_blade_nest_locations)
                                             ):
        if connection:
            region.connect(connection)
        region.add_locations(locations, KSSLocation)

    menu.connect(dyna_blade, None, lambda state: state.has(item_names.dyna_blade, world.player))
    dyna_blade.connect(peanut_plains)
    world.get_location(location_names.db_complete).place_locked_item(world.create_item(item_names.dyna_blade_complete))
    world.multiworld.regions.extend([dyna_blade, peanut_plains, mallow_castle, cocoa_cave,
                                     candy_mountain, dyna_blade_nest])


def create_great_cave_offensive(world: "KSSWorld", menu: KSSRegion):
    tgco = create_region("The Great Cave Offensive", world)
    subtree = create_region("Sub-Tree", world)
    crystal = create_region("Crystal", world)
    old_tower = create_region("Old Tower", world)
    garden = create_region("Garden", world)

    for region, connection, locations in zip((subtree, crystal, old_tower, garden),
                                             (crystal, old_tower, garden, None),
                                             (subtree_locations, crystal_locations, old_tower_locations,
                                              garden_locations)
                                             ):
        if connection:
            region.connect(connection)
        region.add_locations(locations, KSSLocation)

    menu.connect(tgco, None, lambda state: state.has(item_names.great_cave_offensive, world.player))
    tgco.connect(subtree)
    world.get_location(location_names.tgco_complete).place_locked_item(
        world.create_item(item_names.great_cave_offensive_complete))
    world.multiworld.regions.extend([tgco, subtree, crystal, old_tower, garden])


def create_revenge_meta_knight(world: "KSSWorld", menu: KSSRegion):
    revenge_of_meta_knight = create_region("Revenge of Meta Knight", world)
    chapter_1 = create_region("RoMK - Chapter 1", world)
    chapter_2 = create_region("RoMK - Chapter 2", world)
    chapter_3 = create_region("RoMK - Chapter 3", world)
    chapter_4 = create_region("RoMK - Chapter 4", world)
    chapter_5 = create_region("RoMK - Chapter 5", world)
    chapter_6 = create_region("RoMK - Chapter 6", world)
    chapter_7 = create_region("RoMK - Chapter 7", world)

    for region, connection, locations in zip((chapter_1, chapter_2, chapter_3, chapter_4,
                                              chapter_5, chapter_6, chapter_7),
                                             (chapter_2, chapter_3, chapter_4, chapter_5,
                                              chapter_6, chapter_7, None),
                                             (romk_chapter_1_locations, romk_chapter_2_locations,
                                              romk_chapter_3_locations, romk_chapter_4_locations,
                                              romk_chapter_5_locations, romk_chapter_6_locations,
                                              romk_chapter_7_locations)
                                             ):
        if connection:
            region.connect(connection)
        region.add_locations(locations, KSSLocation)

    menu.connect(revenge_of_meta_knight, None, lambda state: state.has(item_names.revenge_of_meta_knight, world.player))
    revenge_of_meta_knight.connect(chapter_1)
    world.get_location(location_names.romk_complete).place_locked_item(
        world.create_item(item_names.revenge_of_meta_knight_complete))

    world.multiworld.regions.extend([revenge_of_meta_knight, chapter_1, chapter_2, chapter_3, chapter_4, chapter_5,
                                     chapter_6, chapter_7])


def create_milky_way_wishes(world: "KSSWorld", menu: KSSRegion):
    milky_way_wishes = create_region("Milky Way Wishes", world)
    floria = create_region("Floria", world)
    aqualiss = create_region("Aqualiss", world)
    skyhigh = create_region("Skyhigh", world)
    hotbeat = create_region("Hotbeat", world)
    cavios = create_region("Cavios", world)
    mecheye = create_region("Mecheye", world)
    halfmoon = create_region("Halfmoon", world)
    copy_planet = create_region("???", world)

    for region, locations, item in zip((floria, aqualiss, skyhigh, hotbeat, cavios, mecheye, halfmoon, copy_planet),
                                       (floria_locations, aqualiss_locations, skyhigh_locations, hotbeat_locations,
                                        cavios_locations, mecheye_locations, halfmoon_locations, copy_planet_locations),
                                       (item_names.floria, item_names.aqualiss, item_names.skyhigh, item_names.hotbeat,
                                        item_names.cavios, item_names.mecheye, item_names.halfmoon,
                                        item_names.copy_planet)
                                 ):
        region.add_locations(locations, KSSLocation)
        milky_way_wishes.connect(region, None, lambda state, required=item: state.has(required, world.player))

    milky_way_wishes.add_locations(space_locations, KSSLocation)
    menu.connect(milky_way_wishes, None, lambda state: state.has(item_names.milky_way_wishes, world.player))

    world.get_location(location_names.mww_complete).place_locked_item(
        world.create_item(item_names.milky_way_wishes_complete))

    world.multiworld.regions.extend([milky_way_wishes, floria, aqualiss, skyhigh, hotbeat, cavios,
                                     mecheye, halfmoon, copy_planet])


def create_regions(world: "KSSWorld"):
    menu = create_region("Menu", world)
    world.multiworld.regions.append(menu)
    create_trivial_regions(world, menu)
    if "Spring Breeze" in world.options.included_subgames:
        create_spring_breeze(world, menu)
    if "Dyna Blade" in world.options.included_subgames:
        create_dyna_blade(world, menu)
    if "The Great Cave Offensive" in world.options.included_subgames:
        create_great_cave_offensive(world, menu)
    if "Revenge of Meta Knight" in world.options.included_subgames:
        create_revenge_meta_knight(world, menu)
    if "Milky Way Wishes" in world.options.included_subgames:
        create_milky_way_wishes(world, menu)
