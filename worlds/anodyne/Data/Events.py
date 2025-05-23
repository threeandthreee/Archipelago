from worlds.anodyne.Options import EndgameRequirement, PostgameEnd

events_by_region = {
    "Bedroom exit": {
        "Defeat Seer": ["Combat"],
        "Grab Green Key": []
    },
    "Crowd floor 1": {
        "Defeat The Wall": ["Combat", "Jump Shoes"],
        "Grab Blue Key": ["Defeat The Wall"]
    },
    "Windmill": {
        "Windmill activated": [],
    },
    "Hotel floor 1": {
        "Defeat Manager": ["Small Key (Hotel):6", "Combat"],
    },
    "Circus boss gauntlet": {
        "Defeat Servants": ["Combat", "Jump Shoes"],
    },
    "Apartment floor 3": {
        "Defeat Watcher": ["Combat", "Small Key (Apartment):4"],
    },
    "Terminal top": {
        "Defeat Sage": ["Combat", "Jump Shoes"],
    },
    "Go top": {
        "Defeat Briar": ["Jump Shoes", "Combat"],
    },
    "Nexus top": {
        "Open final gate": [PostgameEnd.typename()],
    },
    "Red Cave center": {
        "Center left tentacle hit": ["Combat"],
        "Center right tentacle hit": ["Combat"],
    },
    "Red Cave left": {
        "Left tentacle hit": ["Combat", "Small Key (Red Cave):6"],
    },
    "Red Cave right": {
        "Right tentacle hit": ["Combat", "Small Key (Red Cave):6"],
    },
    "Red Cave top": {
        "Defeat Rogue": ["Combat"],
        "Grab Red Key": ["Defeat Rogue"]
    },
}

all_events = [event_name for events in events_by_region.values() for event_name in events.keys()]
