events_by_region = {
    "Bedroom exit": {
        "Defeat Seer": ["Combat"],
        "Green Key": []
    },
    "Crowd floor 1": {
        "Defeat The Wall": ["Combat", "Jump Shoes"],
        "Blue Key": ["Defeat The Wall"]
    },
    "Windmill": {
        "Windmill activated": [],
    },
    "Hotel floor 1": {
        "Defeat Manager": ["Keys:Hotel:6", "Combat"],
    },
    "Circus 4": {
        "Defeat Servants": ["Combat", "Jump Shoes"],
    },
    "Apartment floor 3": {
        "Defeat Watcher": ["Combat", "Keys:Apartment:4"],
    },
    "Terminal": {
        "Defeat Sage": ["Combat", "Cards:36"],
    },
    "Go top": {
        "Defeat Briar": ["Jump Shoes", "Combat"],
    },
    "Nexus top": {
        "Open 49 card gate": ["Cards:49"],
    },
    "Red Cave center": {
        "Center left tentacle hit": ["Combat"],
        "Center right tentacle hit": ["Combat"],
    },
    "Red Cave left": {
        "Left tentacle hit": ["Combat", "Keys:Red Cave:6"],
    },
    "Red Cave right": {
        "Right tentacle hit": ["Combat", "Keys:Red Cave:6"],
    },
    "Red Cave top": {
        "Defeat Rogue": ["Combat"],
        "Red Key": ["Defeat Rogue"]
    },
}

all_events = [event_name for events in events_by_region.values() for event_name in events.keys()]
