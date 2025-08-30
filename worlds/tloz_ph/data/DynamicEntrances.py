from .Entrances import ENTRANCES
from .Constants import LOCATION_GROUPS

def create_scene_id(entrance):
    e_stage, e_room, e_entrance = entrance
    return e_stage * 0x100 + e_room

DYNAMIC_ENTRANCES = {
    # Dungeon Shortcuts
    "Shortcut to TotOK": {
        "entrance": "Mercay SE Tuzi",
        "destination": "TotOK Lobby Entrance",
        "has_slot_data": [("dungeon_shortcuts", 1)],
        "any_has_locations": ["TotOK Phantom Hourglass",
                          "TotOK 1F Linebeck Key"],
    },
    "Shortcut to Temple of Fire": {
        "entrance": "Ember Port House",
        "destination": "ToF Entrance",
        "has_slot_data": [("dungeon_shortcuts", 1)],
        "any_has_locations": ["Temple of Fire 1F Keese Chest",
                              "Temple of Fire 1F Maze Chest"],
    },
    "Shortcut to Temple of Wind": {
        "entrance": "Ocean NW Isle of Gust",
        "destination": "ToW Entrance",
        "has_slot_data": [("dungeon_shortcuts", 1)],
        "has_locations": LOCATION_GROUPS["Isle of Gust"],
    },
    "Shortcut to Temple of Wind no digging": {
        "entrance": "Ocean NW Isle of Gust",
        "destination": "ToW Entrance",
        "has_slot_data": [("dungeon_shortcuts", 1), ("randomize_digs", 0)],
        "has_locations": [
            "Isle of Gust Hideout Chest",
            "Isle of Gust Miblin Cave North Chest",
            "Isle of Gust Miblin Cave South Chest",
            "Isle of Gust West Cliff Chest",
            "Isle of Gust Sandworm Chest",
        ],
    },
    "Shortcut to Temple of Courage": {
        "entrance": "Molida Port House",
        "destination": "ToC Entrance",
        "has_slot_data": [("dungeon_shortcuts", 1)],
        "any_has_locations": ["Temple of Courage 1F Bomb Alcove Chest",
                          "Temple of Courage 1F Raised Platform Chest"],
    },
    "Shortcut to Goron Temple": {
        "entrance": "Goron Port House",
        "destination": "GT Entrance",
        "has_slot_data": [("dungeon_shortcuts", 1)],
        "any_has_locations": ["Goron Temple 1F Switch Chest",
                              "Goron Temple 1F Bow Chest",
                              "Goron Temple B1 Bombchu Bag Chest"],
    },
    "Shortcut to Temple of Ice": {
        "entrance": "Frost Smart House",
        "destination": "ToI Entrance",
        "has_slot_data": [("dungeon_shortcuts", 1)],
        "any_has_locations": ["Temple of Ice 3F Corner Chest",
                              "Temple of Ice B1 Entrance Chest"],
    },
    "Shortcut to Mutoh's Temple": {
        "entrance": "Ruins Port Cave",
        "destination": "MT Entrance",
        "has_slot_data": [("dungeon_shortcuts", 1)],
        "any_has_locations": ["Mutoh's Temple 2F Like-Like Maze Chest",
                              "Mutoh's Temple 3F Hammer Chest",
                              "Mutoh's Temple B2 Spike Roller Chest",
                              "Mutoh's Temple B2 Ledge Chest",
                              "Mutoh's Temple B1 Lower Water Chest",
                              "Mutoh's Temple B1 Push Boulder Chest",
                              "Mutoh's Temple B1 Boss Key Chest"],
    },
    # Ending blue warps take you inside dungeon, to save ER hassles
    "Blaaz warp": {
        "entrance": "ToF Blaaz Warp",
        "destination": "ToF Entrance",
        "has_slot_data": [("shuffle_dungeon_entrances", 1)],
    },
    "Cyclok warp": {
        "entrance": "ToW Cyclok Warp",
        "destination": "ToW Entrance",
        "has_slot_data": [("shuffle_dungeon_entrances", 1)],
    },
    "Crayk warp": {
        "entrance": "ToC Crayk Warp",
        "destination": "ToC Entrance",
        "has_slot_data": [("shuffle_dungeon_entrances", 1)],
    },
    "Dongo warp": {
        "entrance": "GT Dongo Warp",
        "destination": "GT Entrance",
        "has_slot_data": [("shuffle_dungeon_entrances", 1)],
    },
    "Gleeok warp": {
        "entrance": "ToI Gleeok Warp",
        "destination": "ToI Entrance",
        "has_slot_data": [("shuffle_dungeon_entrances", 1)],
    },
    "Eox warp": {
        "entrance": "MT Eox Warp",
        "destination": "MT Entrance",
        "has_slot_data": [("shuffle_dungeon_entrances", 1)],
    },
}

DYNAMIC_ENTRANCES_BY_SCENE = {}
for name, data in DYNAMIC_ENTRANCES.items():
    data["name"] = name
    entrance_data = ENTRANCES[data["entrance"]]
    destination_data = ENTRANCES[data["destination"]]

    entrance_scene = create_scene_id(entrance_data["entrance"])
    detect_scene = create_scene_id(entrance_data["exit"])

    link_coords = entrance_data.get("coords", None)

    # Handle extra data
    extra_data = {"y": link_coords[1]} if link_coords else {}  # Ensure that the y value is always checked
    extra_data |= entrance_data.get("extra_data", {})  # Contains additional boundaries and stuff
    extra_data = tuple(extra_data.items()) if extra_data else None
    coords = list(link_coords) if link_coords else [None]

    # Values for Client.er_in_scene
    exit_data = list(destination_data["entrance"]) + coords
    detect_data = tuple(list(entrance_data["exit"]) + [extra_data])



    # Save er_in_scene values in data
    data["detect_data"] = detect_data
    data["exit_data"] = exit_data
    DYNAMIC_ENTRANCES_BY_SCENE.setdefault(entrance_scene, dict())
    DYNAMIC_ENTRANCES_BY_SCENE[entrance_scene][name] = data
