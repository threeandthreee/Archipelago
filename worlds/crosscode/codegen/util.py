import json
import os
import typing
import pkgutil

from BaseClasses import ItemClassification

from .merge import merge

BASE_ID = 3235824000

# I reserve some item IDs at the beginning of our slot for elements
# and other items that don't map to CrossCode items
RESERVED_ITEM_IDS = 100

SP_UPGRADE_ID_OFFSET = 4
SP_UPGRADE_NAME = "SP Upgrade"

CIRCUIT_OVERRIDE = 428

GENERATED_COMMENT = """WARNING: THIS FILE HAS BEEN GENERATED!
Modifications to this file will not be kept.
If you need to change something here, check out codegen.py and the templates directory.
"""

def get_json_object(package, filename: str):
    return json.loads(pkgutil.get_data(package, filename).decode())


def load_json_with_includes(package, filename: str) -> typing.Dict[str, typing.Any]:
    master = get_json_object(package, filename)
    dirname = os.path.dirname(filename)

    if not isinstance(master, dict):
        raise RuntimeError(f"error loading file '{filename}': root should be an object")
    if "includes" not in master:
        return master

    includes = master.pop("includes")
    for subfilename in includes:
        subfile = load_json_with_includes(package, os.path.join(dirname, subfilename))

        master = merge(master, subfile, apply_diffs=False)

    return master


def load_world_json(package, filename: str, zipped=False) -> tuple[dict[str, typing.Any], dict[str, dict[str, typing.Any]]]:
    master = load_json_with_includes(package, filename)
    dirname = os.path.dirname(filename)

    if "addons" not in master:
        return (master, {})

    addons = master.pop("addons")
    loaded_addons = {}
    for addon_name in addons:
        subfile = load_json_with_includes(
            package,
            os.path.join(dirname, "addons", addon_name, "master.json")
        )

        loaded_addons[addon_name] = subfile

    return master, loaded_addons

def get_item_classification(item: dict) -> ItemClassification:
    """Deduce the classification of an item based on its item-database entry"""
    if item["type"] == "CONS" or item["type"] == "TRADE":
        return ItemClassification.filler
    elif item["type"] == "KEY":
        return ItemClassification.progression
    elif item["type"] == "EQUIP":
        return ItemClassification.useful
    elif item["type"] == "TOGGLE":
        if "Booster" in item["name"]["en_US"]:
            return ItemClassification.progression
        else:
            return ItemClassification.filler
    else:
        raise RuntimeError(f"I don't know how to classify this item: {item['name']}")
