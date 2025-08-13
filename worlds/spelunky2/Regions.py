from typing import Optional, List, NamedTuple


class Spelunky2RegionData(NamedTuple):
    exits: Optional[List[str]] = None


region_data_table = {
    "Menu": Spelunky2RegionData(["Dwelling"]),  # Add connections to Olmec's Lair and Ice Caves when shortcuts are added
    "Dwelling": Spelunky2RegionData(["Jungle", "Volcana"]),
    "Jungle": Spelunky2RegionData(["Olmec's Lair"]),
    "Volcana": Spelunky2RegionData(["Olmec's Lair"]),
    "Olmec's Lair": Spelunky2RegionData(["Tide Pool", "Temple"]),
    "Tide Pool": Spelunky2RegionData(["Ice Caves"]),
    "Temple": Spelunky2RegionData(["Ice Caves"]),
    "Ice Caves": Spelunky2RegionData(["Neo Babylon"]),
    "Neo Babylon": Spelunky2RegionData(["Sunken City"]),
    "Sunken City": Spelunky2RegionData(["Cosmic Ocean"]),
    "Cosmic Ocean": Spelunky2RegionData(),
}
