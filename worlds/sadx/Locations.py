from typing import List, TypedDict, Dict

from BaseClasses import Location, Region
from .Enums import Area, pascal_to_space, SADX_BASE_ID
from .Logic import level_location_table, upgrade_location_table, sub_level_location_table, field_emblem_location_table, \
    capsule_location_table, boss_location_table, mission_location_table, chao_egg_location_table, \
    chao_race_location_table, enemy_location_table
from .Names import LocationName


class LocationInfo(TypedDict):
    id: int
    name: str


def get_location_from_level() -> List[LocationInfo]:
    locations: List[LocationInfo] = []
    for level in level_location_table:
        locations += [{"id": level.locationId, "name": level.get_level_name()}]
    return locations


def get_location_from_upgrade() -> List[LocationInfo]:
    locations: List[LocationInfo] = []
    for upgrade in upgrade_location_table:
        locations += [{"id": upgrade.locationId, "name": upgrade.locationName}]
    return locations


def get_location_from_sub_level() -> List[LocationInfo]:
    locations: List[LocationInfo] = []
    for sub_level in sub_level_location_table:
        sub_level_name = f"{pascal_to_space(sub_level.subLevel.name)} (Sub-Level - Mission {sub_level.subLevelMission.name})"
        locations += [{"id": sub_level.locationId, "name": sub_level_name}]
    return locations


def get_location_from_emblem() -> List[LocationInfo]:
    locations: List[LocationInfo] = []
    for emblem in field_emblem_location_table:
        locations += [{"id": emblem.locationId, "name": emblem.emblemName}]
    return locations


def get_location_from_capsule() -> List[LocationInfo]:
    locations: List[LocationInfo] = []
    for capsule in capsule_location_table:
        level_name: str = f"{pascal_to_space(capsule.area.name)} ({capsule.character.name}) - Capsule {capsule.capsuleNumber:02d} ({pascal_to_space(capsule.type.name)})"
        locations += [{"id": capsule.locationId, "name": level_name}]
    return locations


def get_location_from_boss() -> List[LocationInfo]:
    locations: List[LocationInfo] = []
    for boss_fight in boss_location_table:
        location_name = boss_fight.get_boss_name()
        locations += [{"id": boss_fight.locationId, "name": location_name}]
    return locations


def get_location_from_mission() -> List[LocationInfo]:
    locations: List[LocationInfo] = []
    for mission in mission_location_table:
        locations += [{"id": mission.locationId, "name": mission.get_mission_name()}]
    return locations


def get_location_from_eggs() -> List[LocationInfo]:
    locations: List[LocationInfo] = []
    for egg in chao_egg_location_table:
        locations += [{"id": egg.locationId, "name": egg.eggName}]
    return locations


def get_location_from_races() -> List[LocationInfo]:
    locations: List[LocationInfo] = []
    for race in chao_race_location_table:
        locations += [{"id": race.locationId, "name": race.name}]
    return locations


def get_location_from_enemies() -> List[LocationInfo]:
    locations: List[LocationInfo] = []
    for enemy in enemy_location_table:
        level_name: str = f"{pascal_to_space(enemy.area.name)} ({enemy.character.name}) - Enemy {enemy.enemyNumber:02d} ({pascal_to_space(enemy.type.name)})"
        locations += [{"id": enemy.locationId, "name": level_name}]
    return locations


all_location_table: List[LocationInfo] = (
        get_location_from_level() +
        get_location_from_upgrade() +
        get_location_from_sub_level() +
        get_location_from_emblem() +
        get_location_from_capsule() +
        get_location_from_boss() +
        get_location_from_mission() +
        get_location_from_eggs() +
        get_location_from_races() +
        get_location_from_enemies() +
        [{"id": 9, "name": "Perfect Chaos Fight"}]
)


def get_location_name_by_level(level_name: str) -> List[str]:
    return [location["name"] for location in get_location_from_level() if level_name in location["name"]] + \
        [location["name"] for location in get_location_from_capsule() if level_name in location["name"]] + \
        [location["name"] for location in get_location_from_enemies() if level_name in location["name"]]


group_location_table: Dict[str, List[str]] = {
    LocationName.Groups.UpgradePoints: [location["name"] for location in get_location_from_upgrade()],
    LocationName.Groups.FieldEmblems: [location["name"] for location in get_location_from_emblem()],
    LocationName.Groups.Levels: [location["name"] for location in get_location_from_level()],
    LocationName.Groups.Sublevels: [location["name"] for location in get_location_from_sub_level()],
    LocationName.Groups.Capsules: [location["name"] for location in get_location_from_capsule()],
    LocationName.Groups.Bosses: [location["name"] for location in get_location_from_boss()],
    LocationName.Groups.Missions: [location["name"] for location in get_location_from_mission()],
    LocationName.Groups.ChaoEggs: [location["name"] for location in get_location_from_eggs()],
    LocationName.Groups.ChaoRaces: [location["name"] for location in get_location_from_races()],
    LocationName.Groups.Enemies: [location["name"] for location in get_location_from_enemies()],
    pascal_to_space(Area.EmeraldCoast.name): get_location_name_by_level(pascal_to_space(Area.EmeraldCoast.name)),
    pascal_to_space(Area.WindyValley.name): get_location_name_by_level(pascal_to_space(Area.WindyValley.name)),
    pascal_to_space(Area.Casinopolis.name): get_location_name_by_level(pascal_to_space(Area.Casinopolis.name)),
    pascal_to_space(Area.IceCap.name): get_location_name_by_level(pascal_to_space(Area.IceCap.name)),
    pascal_to_space(Area.TwinklePark.name): get_location_name_by_level(pascal_to_space(Area.TwinklePark.name)),
    pascal_to_space(Area.SpeedHighway.name): get_location_name_by_level(pascal_to_space(Area.SpeedHighway.name)),
    pascal_to_space(Area.RedMountain.name): get_location_name_by_level(pascal_to_space(Area.RedMountain.name)),
    pascal_to_space(Area.SkyDeck.name): get_location_name_by_level(pascal_to_space(Area.SkyDeck.name)),
    pascal_to_space(Area.LostWorld.name): get_location_name_by_level(pascal_to_space(Area.LostWorld.name)),
    pascal_to_space(Area.FinalEgg.name): get_location_name_by_level(pascal_to_space(Area.FinalEgg.name)),
    pascal_to_space(Area.HotShelter.name): get_location_name_by_level(pascal_to_space(Area.HotShelter.name)),

}


def get_location_by_id(location_id: int) -> LocationInfo:
    for location in all_location_table:
        if location["id"] == location_id:
            return location


def get_location_by_name(location_name: str) -> LocationInfo:
    for location in all_location_table:
        if location["name"] == location_name:
            return location


class SonicAdventureDXLocation(Location):
    game: str = "Sonic Adventure DX"

    def __init__(self, player, location_id: int, parent: Region):
        location = get_location_by_id(location_id)
        super().__init__(player, location["name"], location["id"] + SADX_BASE_ID, parent)
