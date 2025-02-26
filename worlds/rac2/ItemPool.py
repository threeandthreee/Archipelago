from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, Item
from .data import Items
from .data.Items import CoordData, EquipmentData, ProgressiveUpgradeData

if TYPE_CHECKING:
    from . import Rac2World


def get_classification(item_name: str) -> ItemClassification:
    item = Items.from_name(item_name)
    if item in Items.COORDS:
        return ItemClassification.progression
    if item in [
        Items.HELI_PACK,
        Items.THRUSTER_PACK,
        Items.LEVITATOR,
        Items.SWINGSHOT,
        Items.GRAVITY_BOOTS,
        Items.GRIND_BOOTS,
        Items.GLIDER,
        Items.DYNAMO,
        Items.ELECTROLYZER,
        Items.THERMANATOR,
        Items.TRACTOR_BEAM,
        Items.QWARK_STATUETTE,
        Items.INFILTRATOR,
        Items.HYPNOMATIC,
        Items.SPIDERBOT_GLOVE,
        Items.HYPNOMATIC_PART,
    ]:
        return ItemClassification.progression
    if item in [
        Items.MAPPER,
        Items.ARMOR_MAGNETIZER,
        Items.BOX_BREAKER,
        Items.CHARGE_BOOTS,
        Items.PLATINUM_BOLT,
        Items.NANOTECH_BOOST,
    ]:
        return ItemClassification.useful
    if item in Items.WEAPONS or item in Items.UPGRADES:
        return ItemClassification.useful

    return ItemClassification.filler
    

def create_planets(world: "Rac2World") -> list["Item"]:
    coords_to_add: list[CoordData] = list(Items.COORDS)
    world.multiworld.random.shuffle(coords_to_add)
    precollected_ids: list[int] = [item.code for item in world.multiworld.precollected_items[world.player]]

    # determine starting coords
    # There should be at least 3 coords that lead to eligible starting planets in the player's starting inventory.
    # If the player manually added any eligible coords to their starting inventory, those will get used first.
    # If there are still less than 3, pick the rest of the starting coords randomly from the eligible coords.
    starting_coords: list[CoordData] = [coord for coord in coords_to_add if coord.item_id in precollected_ids]
    startable_coords: list[CoordData] = [coord for coord in Items.STARTABLE_COORDS if coord not in starting_coords]
    world.multiworld.random.shuffle(startable_coords)
    for coord in startable_coords[:max(3 - len(starting_coords), 0)]:
        starting_coords.append(coord)
        world.multiworld.push_precollected(world.create_item(coord.name))

    coords_to_add = [coord for coord in coords_to_add if coord not in starting_coords]

    return [world.create_item(coord.name) for coord in coords_to_add]


def create_equipment(world: "Rac2World") -> list["Item"]:
    equipment_to_add: list[EquipmentData] = list(Items.EQUIPMENT) + [Items.SHEEPINATOR, Items.SPIDERBOT_GLOVE]
    precollected_ids: list[int] = [item.code for item in world.multiworld.precollected_items[world.player]]
    equipment_to_add = [equipment for equipment in equipment_to_add if equipment.item_id not in precollected_ids]

    return [world.create_item(equipment.name) for equipment in equipment_to_add]


def create_collectables(world: "Rac2World") -> list["Item"]:
    collectable_items: list["Item"] = []

    precollected_platinum_bolts: int = len([
        item for item in world.multiworld.precollected_items[world.player]
        if item.code == Items.PLATINUM_BOLT.item_id
    ])
    for _ in range(Items.PLATINUM_BOLT.max_capacity - precollected_platinum_bolts):
        collectable_items.append(world.create_item(Items.PLATINUM_BOLT.name))

    precollected_nanotech_boosts: int = len([
        item for item in world.multiworld.precollected_items[world.player]
        if item.code == Items.NANOTECH_BOOST.item_id
    ])
    assert precollected_nanotech_boosts <= Items.NANOTECH_BOOST.max_capacity, "Added to many Nanotech Boosts to Start Inventory"
    for _ in range(Items.NANOTECH_BOOST.max_capacity - precollected_nanotech_boosts):
        collectable_items.append(world.create_item(Items.NANOTECH_BOOST.name))

    precollected_hypnomatic_parts: int = len([
        item for item in world.multiworld.precollected_items[world.player]
        if item.code == Items.HYPNOMATIC_PART.item_id
    ])
    assert precollected_hypnomatic_parts <= Items.HYPNOMATIC_PART.max_capacity, "Added to many Hypnomatic Parts to Start Inventory"
    for _ in range(Items.HYPNOMATIC_PART.max_capacity - precollected_hypnomatic_parts):
        collectable_items.append(world.create_item(Items.HYPNOMATIC_PART.name))

    return collectable_items


def create_upgrades(world: "Rac2World") -> list["Item"]:
    upgrades_to_add: list[ProgressiveUpgradeData] = list(Items.UPGRADES)
    # There are two wrench upgrades, add one more
    upgrades_to_add.append(Items.WRENCH_UPGRADE)

    # Remove the armor upgrade from the pool, as it currently is only for debug purpose
    # TODO: Remove this line once armor locations get implemented
    upgrades_to_add.remove(Items.ARMOR_UPGRADE)

    return [world.create_item(upgrade.name) for upgrade in upgrades_to_add]
