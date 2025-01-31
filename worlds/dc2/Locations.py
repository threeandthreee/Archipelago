from enum import IntEnum
from typing import Optional, NamedTuple, Dict

from BaseClasses import Location, Region


class DC2LocationCategory(IntEnum):
    FLOOR = 0
    DUNGEON = 1
    RECRUIT = 2
    GEORAMA = 3
    MIRACLE_CHEST = 4
    BOSS = 5
    MISC = 6
    GEOSTONE = 7
    EVENT = 8
    SKIP = 9


class DC2LocationData(NamedTuple):
    name: str
    default_item: str
    category: DC2LocationCategory


class DarkCloud2Location(Location):
    game: str = "Dark Cloud 2"
    category: DC2LocationCategory
    default_item_name: str

    def __init__(
            self,
            player: int,
            name: str,
            category: DC2LocationCategory,
            default_item_name: str,
            address: Optional[int] = None,
            parent: Optional[Region] = None):
        super().__init__(player, name, address, parent)
        self.default_item_name = default_item_name
        self.category = category

    @staticmethod
    def get_name_to_id() -> dict:
        base_id = 694201000
        table_offset = 1000

        table_order = [
            "Palm Brinks",
            "Underground Water Channel",
            "Sindain",
            "Rainbow Butterfly Wood"
        ]

        output = {}
        for i, region_name in enumerate(table_order):
            if len(location_tables[region_name]) > table_offset:
                raise Exception("A location table has {} entries, that is more than {} entries (table #{})".format(len(location_tables[region_name]), table_offset, i))

            output.update({location_data.name: id for id, location_data in enumerate(location_tables[region_name], base_id + (table_offset * i))})

        return output


location_tables = {
    "Palm Brinks": [
        DC2LocationData("PB: Miracle chest 1",                      "Fruit of Eden",                    DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData("PB: Miracle chest 2",                      "Potato Pie",                       DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData("PB: Miracle chest 3",                      "Fruit of Eden",                    DC2LocationCategory.MIRACLE_CHEST),
    ],
    "Underground Water Channel": [
        DC2LocationData("UWC: Floor 1",                             "null",       DC2LocationCategory.FLOOR),        
        DC2LocationData("UWC: Floor 2",                             "null",       DC2LocationCategory.FLOOR),         
        DC2LocationData("UWC: Floor 3",                             "null",       DC2LocationCategory.FLOOR),    
        DC2LocationData("UWC: Pump Room",                           "null",       DC2LocationCategory.FLOOR),         
        DC2LocationData("UWC: Linda",                               "null",       DC2LocationCategory.BOSS),   
        DC2LocationData("UWC: Floor 4",                             "null",       DC2LocationCategory.FLOOR),
        DC2LocationData("UWC: Floor 5",                             "null",       DC2LocationCategory.FLOOR),
        DC2LocationData("UWC: Halloween",                           "null",       DC2LocationCategory.BOSS),
        DC2LocationData("UWC: Chapter 1 Complete",                  "null",       DC2LocationCategory.EVENT),
    ],
    "Sindain": [    
        DC2LocationData("S: Miracle chest 1",                      "Fruit of Eden",                    DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData("S: Miracle chest 2",                      "Potato Pie",                       DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData("S: Miracle chest 3",                      "Fruit of Eden",                    DC2LocationCategory.MIRACLE_CHEST),        
        DC2LocationData("S: Miracle chest 4",                      "Fruit of Eden",                    DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData("S: Miracle chest 5",                      "Potato Pie",                       DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData("S: Miracle chest 6",                      "Fruit of Eden",                    DC2LocationCategory.MIRACLE_CHEST),        
        DC2LocationData("S: Miracle chest 7",                      "Fruit of Eden",                    DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData("S: Miracle chest 8",                      "Potato Pie",                       DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData("S: Miracle chest 9",                      "Fruit of Eden",                    DC2LocationCategory.MIRACLE_CHEST),        
        DC2LocationData("S: Miracle chest 10",                      "Fruit of Eden",                    DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData("S: Miracle chest 11",                      "Potato Pie",                       DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData("S: Miracle chest 12",                      "Fruit of Eden",                    DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData("S: Miracle chest 13",                      "Fruit of Eden",                    DC2LocationCategory.MIRACLE_CHEST),        
        DC2LocationData("S: Miracle chest 14",                      "Fruit of Eden",                    DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData("S: Miracle chest 15",                      "Potato Pie",                       DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData("S: Miracle chest 16",                      "Fruit of Eden",                    DC2LocationCategory.MIRACLE_CHEST),
        
        DC2LocationData("S: Grape Juice",                           "Grape Juice",                      DC2LocationCategory.MISC),
    ],
    "Rainbow Butterfly Wood": [    
        DC2LocationData("RBW: Floor 1",                             "null",       DC2LocationCategory.FLOOR),   
        DC2LocationData("RBW: Floor 2",                             "null",       DC2LocationCategory.FLOOR),   
        DC2LocationData("RBW: Floor 3",                             "null",       DC2LocationCategory.FLOOR),   
        DC2LocationData("RBW: Floor 4",                             "null",       DC2LocationCategory.FLOOR),   
        DC2LocationData("RBW: Floor 5",                             "null",       DC2LocationCategory.FLOOR),   
        DC2LocationData("RBW: Chapter 2 Complete",                  "null",               DC2LocationCategory.EVENT),
    ],
    
}

location_dictionary: Dict[str, DC2LocationData] = {}
for location_table in location_tables.values():
    location_dictionary.update({location_data.name: location_data for location_data in location_table})
