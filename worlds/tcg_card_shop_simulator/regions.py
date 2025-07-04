from BaseClasses import Region, Entrance
from .locations import *

location_dict = {}
card_dict = {}
excludedLocs = []

def create_region(world, name: str, hint: str):
    region = Region(name, world.player, world.multiworld)
    create_locations(world, region, location_dict, card_dict)
    world.multiworld.regions.append(region)
    return region

def create_level_region(world, name: str, hint: str, final_region):
    region = Region(name, world.player, world.multiworld)
    match = re.search(r'\d+', name)
    if match and int(match.group()) <= final_region:
        create_locations(world, region, location_dict, card_dict)
    else:
        for (key, data) in location_dict.items():
            if data.region != name:
                continue
            excludedLocs.insert(len(excludedLocs), key)
            continue
    world.multiworld.regions.append(region)
    return region

def create_pack_region(world, name: str, hint: str, options, final_region):
    smallest_region_id = 110
    for reg in options:
        match = re.search(r'\d+', reg)
        if match and smallest_region_id > int(match.group()):
            smallest_region_id = int(match.group())
    if smallest_region_id > final_region:
        print(f"{name} is Beyond Level {final_region}")
        region = Region(name, world.player, world.multiworld)
        world.multiworld.regions.append(region)
    else:
        create_region(world, name, hint)

def connect_regions(world, from_name: str, to_name: str, entrance_name: str) -> Entrance:
    entrance_region = world.get_region(from_name)
    exit_region = world.get_region(to_name)
    return entrance_region.connect(exit_region, entrance_name)


def create_regions(world, loc_dict, card_locs, final_region):
    global location_dict, card_dict, excludedLocs
    location_dict = loc_dict.copy()
    card_dict = card_locs.copy()
    excludedLocs = []

    create_region(world, "Menu", "Menu Region")
    create_level_region(world, "Level 1-4", "Level 1-4",final_region)
    create_level_region(world, "Level 5-9", "Level 5-9",final_region)
    create_level_region(world, "Level 10-14", "Level 10-14",final_region)
    create_level_region(world, "Level 15-19", "Level 15-19",final_region)
    create_level_region(world, "Level 20-24", "Level 20-24",final_region)
    create_level_region(world, "Level 25-29", "Level 25-29",final_region)
    create_level_region(world, "Level 30-34", "Level 30-34",final_region)
    create_level_region(world, "Level 35-39", "Level 35-39",final_region)
    create_level_region(world, "Level 40-44", "Level 40-44",final_region)
    create_level_region(world, "Level 45-49", "Level 45-49",final_region)
    create_level_region(world, "Level 50-54", "Level 50-54",final_region)
    create_level_region(world, "Level 55-59", "Level 55-59",final_region)
    create_level_region(world, "Level 60-64", "Level 60-64",final_region)
    create_level_region(world, "Level 65-69", "Level 65-69",final_region)
    create_level_region(world, "Level 70-74", "Level 70-74",final_region)
    create_level_region(world, "Level 75-79", "Level 75-79",final_region)
    create_level_region(world, "Level 80-84", "Level 80-84",final_region)
    create_level_region(world, "Level 85-89", "Level 85-89",final_region)
    create_level_region(world, "Level 90-94", "Level 90-94",final_region)
    create_level_region(world, "Level 95-99", "Level 95-99",final_region)
    create_level_region(world, "Level 100-104", "Level 100-104",final_region)
    create_level_region(world, "Level 105-109", "Level 105-109",final_region)
    create_level_region(world, "Level 110-115", "Level 110-115",final_region)

    create_pack_region(world, "Common Card Pack", "Common Card Pack", [loc_dict["Sell Basic Card Pack 1"].region, loc_dict["Sell Basic Card Box 1"].region], final_region)
    create_pack_region(world, "Rare Card Pack", "Rare Card Pack", [loc_dict["Sell Rare Card Pack 1"].region, loc_dict["Sell Rare Card Box 1"].region], final_region)
    create_pack_region(world, "Epic Card Pack", "Epic Card Pack", [loc_dict["Sell Epic Card Pack 1"].region, loc_dict["Sell Epic Card Box 1"].region], final_region)
    create_pack_region(world, "Legendary Card Pack", "Legendary Card Pack", [loc_dict["Sell Legendary Card Pack 1"].region, loc_dict["Sell Legendary Card Box 1"].region], final_region)
    create_pack_region(world, "Destiny Common Card Pack", "Common Card Pack", [loc_dict["Sell Basic Destiny Pack 1"].region, loc_dict["Sell Basic Destiny Box 1"].region], final_region)
    create_pack_region(world, "Destiny Rare Card Pack", "Rare Card Pack", [loc_dict["Sell Rare Destiny Pack 1"].region, loc_dict["Sell Rare Destiny Box 1"].region], final_region)
    create_pack_region(world, "Destiny Epic Card Pack", "Epic Card Pack", [loc_dict["Sell Epic Destiny Pack 1"].region, loc_dict["Sell Epic Destiny Box 1"].region], final_region)
    create_pack_region(world, "Destiny Legendary Card Pack", "Legendary Card Pack", [loc_dict["Sell Legendary Destiny Pack 1"].region, loc_dict["Sell Legendary Destiny Box 1"].region], final_region)

    create_region(world, "Play Tables", "Play Tables")
    return excludedLocs

def connect_pack_region(world, card_region, options, loc_dict, final_region):
    smallest_region = "Menu"
    smallest_region_id = 110
    for reg in options:
        match = re.search(r'\d+', reg)
        if match and smallest_region_id > int(match.group()):
            smallest_region_id = int(match.group())
            smallest_region = reg
    if smallest_region_id > final_region:
        for key, value in list(loc_dict.items()):
            if value.region == card_region:
                del loc_dict[key]

    connect_regions(world, smallest_region, card_region, card_region)


def connect_entrances(world, loc_dict: Dict[str, LocData], final_region):
    global location_dict
    location_dict = loc_dict.copy()

    connect_pack_region(world, "Common Card Pack", [loc_dict["Sell Basic Card Pack 1"].region, loc_dict["Sell Basic Card Box 1"].region], location_dict, final_region)
    connect_pack_region(world, "Rare Card Pack", [loc_dict["Sell Rare Card Pack 1"].region, loc_dict["Sell Rare Card Box 1"].region], location_dict, final_region)
    connect_pack_region(world, "Epic Card Pack", [loc_dict["Sell Epic Card Pack 1"].region, loc_dict["Sell Epic Card Box 1"].region], location_dict, final_region)
    connect_pack_region(world, "Legendary Card Pack", [loc_dict["Sell Legendary Card Pack 1"].region, loc_dict["Sell Legendary Card Box 1"].region], location_dict, final_region)
    connect_pack_region(world, "Destiny Common Card Pack", [loc_dict["Sell Basic Destiny Pack 1"].region, loc_dict["Sell Basic Destiny Box 1"].region], location_dict, final_region)
    connect_pack_region(world, "Destiny Rare Card Pack", [loc_dict["Sell Rare Destiny Pack 1"].region, loc_dict["Sell Rare Destiny Box 1"].region], location_dict, final_region)
    connect_pack_region(world, "Destiny Epic Card Pack", [loc_dict["Sell Epic Destiny Pack 1"].region, loc_dict["Sell Epic Destiny Box 1"].region], location_dict, final_region)
    connect_pack_region(world, "Destiny Legendary Card Pack", [loc_dict["Sell Legendary Destiny Pack 1"].region, loc_dict["Sell Legendary Destiny Box 1"].region], location_dict, final_region)

    connect_regions(world, "Menu", "Level 1-4", "Level 1")
    connect_regions(world, "Menu", "Play Tables", "Play Table")
    connect_regions(world, "Level 1-4", "Level 5-9", "Level 5")
    connect_regions(world, "Level 5-9", "Level 10-14", "Level 10")
    connect_regions(world, "Level 10-14", "Level 15-19", "Level 15")
    connect_regions(world, "Level 15-19", "Level 20-24", "Level 20")
    connect_regions(world, "Level 20-24", "Level 25-29", "Level 25")
    connect_regions(world, "Level 25-29", "Level 30-34", "Level 30")
    connect_regions(world, "Level 30-34", "Level 35-39", "Level 35")
    connect_regions(world, "Level 35-39", "Level 40-44", "Level 40")
    connect_regions(world, "Level 40-44", "Level 45-49", "Level 45")
    connect_regions(world, "Level 45-49", "Level 50-54", "Level 50")
    connect_regions(world, "Level 50-54", "Level 55-59", "Level 55")
    connect_regions(world, "Level 55-59", "Level 60-64", "Level 60")
    connect_regions(world, "Level 60-64", "Level 65-69", "Level 65")
    connect_regions(world, "Level 65-69", "Level 70-74", "Level 70")
    connect_regions(world, "Level 70-74", "Level 75-79", "Level 75")
    connect_regions(world, "Level 75-79", "Level 80-84", "Level 80")
    connect_regions(world, "Level 80-84", "Level 85-89", "Level 85")
    connect_regions(world, "Level 85-89", "Level 90-94", "Level 90")
    connect_regions(world, "Level 90-94", "Level 95-99", "Level 95")
    connect_regions(world, "Level 95-99", "Level 100-104", "Level 100")
    connect_regions(world, "Level 100-104", "Level 105-109", "Level 105")
    connect_regions(world, "Level 105-109", "Level 110-115", "Level 110")

    return location_dict
