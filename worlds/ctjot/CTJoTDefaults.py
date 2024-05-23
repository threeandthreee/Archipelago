# A set of default values for use with AP unit test or other cases where
# values are not provided for items/locations/victory conditions
# These correspond to a standard race seed with no additional settings

DEFAULT_LOCATIONS = [
    {
        "name": "Taban Key",
        "classification": "default"
    },
    {
        "name": "Mt Woe Key",
        "classification": "default"
    },
    {
        "name": "Fiona Key",
        "classification": "default"
    },
    {
        "name": "Reptite Lair Key",
        "classification": "default"
    },
    {
        "name": "Melchior Key",
        "classification": "default"
    },
    {
        "name": "Lazy Carpenter",
        "classification": "default"
    },
    {
        "name": "Sun Palace Key",
        "classification": "default"
    },
    {
        "name": "Kings Trial Key",
        "classification": "default"
    },
    {
        "name": "Denadoro Mts Key",
        "classification": "default"
    },
    {
        "name": "Geno Dome Key",
        "classification": "default"
    },
    {
        "name": "Arris Dome Key",
        "classification": "default"
    },
    {
        "name": "Giants Claw Key",
        "classification": "default"
    },
    {
        "name": "Zenan Bridge Key",
        "classification": "default"
    },
    {
        "name": "Snail Stop Key",
        "classification": "default"
    },
    {
        "name": "Frogs Burrow Left",
        "classification": "default"
    },
    {
        "name": "Starter 1",
        "classification": "event",
        "character": "Robo"
    },
    {
        "name": "Starter 2",
        "classification": "event",
        "character": "Crono"
    },
    {
        "name": "Cathedral",
        "classification": "event",
        "character": "Frog"
    },
    {
        "name": "Castle",
        "classification": "event",
        "character": "Ayla"
    },
    {
        "name": "Frogs Burrow",
        "classification": "event",
        "character": "Lucca"
    },
    {
        "name": "Dactyl Nest",
        "classification": "event",
        "character": "Marle"
    },
    {
        "name": "Proto Dome",
        "classification": "event",
        "character": "Magus"
    }
]

DEFAULT_ITEMS = [
    {
        "name": "Ruby Knife",
        "id": 224,
        "classification": "progression"
    },
    {
        "name": "Grand Leon",
        "id": 66,
        "classification": "progression"
    },
    {
        "name": "Toma's Pop",
        "id": 227,
        "classification": "progression"
    },
    {
        "name": "Clone",
        "id": 226,
        "classification": "progression"
    },
    {
        "name": "Bent Sword",
        "id": 80,
        "classification": "progression"
    },
    {
        "name": "Bent Hilt",
        "id": 81,
        "classification": "progression"
    },
    {
        "name": "Hero Medal",
        "id": 179,
        "classification": "progression"
    },
    {
        "name": "Robo's Rbn",
        "id": 184,
        "classification": "progression"
    },
    {
        "name": "Pendant",
        "id": 214,
        "classification": "progression"
    },
    {
        "name": "Gate Key",
        "id": 215,
        "classification": "progression"
    },
    {
        "name": "PrismShard",
        "id": 216,
        "classification": "progression"
    },
    {
        "name": "C. Trigger",
        "id": 217,
        "classification": "progression"
    },
    {
        "name": "Jerky",
        "id": 219,
        "classification": "progression"
    },
    {
        "name": "Dreamstone",
        "id": 220,
        "classification": "progression"
    },
    {
        "name": "Moon Stone",
        "id": 222,
        "classification": "progression"
    }
]

DEFAULT_RULES = {
    "Taban Key": [],
    "Mt Woe Key": [
        [
            "Gate Key"
        ],
        [
            "Pendant"
        ]
    ],
    "Fiona Key": [
        [
            "Robo"
        ]
    ],
    "Reptite Lair Key": [
        [
            "Gate Key"
        ]
    ],
    "Melchior Key": [
        [
            "Moon Stone",
            "PrismShard",
            "Gate Key",
            "Pendant",
            "Marle"
        ]
    ],
    "Lazy Carpenter": [],
    "Sun Palace Key": [
        [
            "Pendant"
        ]
    ],
    "Kings Trial Key": [
        [
            "PrismShard",
            "Marle"
        ]
    ],
    "Denadoro Mts Key": [],
    "Geno Dome Key": [
        [
            "Pendant"
        ]
    ],
    "Arris Dome Key": [
        [
            "Pendant"
        ]
    ],
    "Giants Claw Key": [
        [
            "Toma's Pop"
        ]
    ],
    "Zenan Bridge Key": [],
    "Snail Stop Key": [],
    "Frogs Burrow Left": [
        [
            "Hero Medal"
        ]
    ],
    "Starter 1": [],
    "Starter 2": [],
    "Cathedral": [],
    "Castle": [],
    "Frogs Burrow": [
        [
            "Bent Hilt",
            "Bent Sword"
        ]
    ],
    "Dactyl Nest": [
        [
            "Gate Key"
        ]
    ],
    "Proto Dome": [
        [
            "Pendant"
        ]
    ]
}

DEFAULT_VICTORY = [
    [
        "Gate Key",
        "Dreamstone",
        "Ruby Knife"
    ],
    [
        "Pendant",
        "Clone",
        "C. Trigger"
    ],
    [
        "Bent Sword",
        "Bent Hilt",
        "Frog"
    ]
]
