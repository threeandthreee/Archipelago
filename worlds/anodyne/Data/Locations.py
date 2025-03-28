from typing import NamedTuple, List, Dict

from . import Regions


class LocationData(NamedTuple):
    name: str
    region_name: str
    reqs: List[str] = []
    health_cicada: bool = False
    small_key: bool = False
    big_key: bool = False
    tentacle: bool = False
    nexus_gate: bool = False

    def postgame(self):
        return "Swap:2" in self.reqs or self.region_name in Regions.postgame_regions


# This array must maintain a consistent order because the IDs are generated from it.
all_locations: List[LocationData] = [
    # 0AC41F72-EE1D-0D32-8F5D-8F25796B6396
    LocationData("Apartment - 1F Ledge Chest", "Apartment floor 1", ["Combat"], small_key=True),
    # DE415E2A-06EE-83AC-F1A3-5DCA1FA44735
    LocationData("Apartment - 1F Rat Maze Chest", "Apartment floor 1", ["Combat"], small_key=True),
    LocationData("Apartment - 1F Exterior Chest", "Apartment floor 1", ["Combat", "Jump Shoes"]),
    LocationData("Apartment - 1F Couches Chest", "Apartment floor 1 top left", ["Combat", "Jump Shoes"]),
    # 5B55A264-3FCD-CF38-175C-141B2D093029
    LocationData("Apartment - 2F Rat Maze Chest", "Apartment floor 2", ["Combat", "Jump Shoes"], small_key=True),
    # 2BBF01C8-8267-7E71-5BD4-325001DBC0BA
    LocationData("Apartment - 3F Gauntlet Chest", "Apartment floor 3", ["Combat"], small_key=True),
    LocationData("Apartment - Boss Chest", "Apartment floor 3", ["Defeat Watcher"]),
    LocationData("Beach - Dock Chest", "Beach"),
    LocationData("Beach - Secret Chest", "Beach", ["Swap:2", "Cards:8", "Combat"]),
    LocationData("Beach - Out-of-bounds Chest", "Beach", ["Swap:2"]),
    # 40DE36CF-9238-F8B0-7A57-C6C8CA465CC2
    LocationData("Temple of the Seeing One - Entrance Chest", "Bedroom", small_key=True),
    LocationData("Temple of the Seeing One - Shieldy Room Chest", "Bedroom",
                 ["Combat", "Keys:Temple of the Seeing One:3"]),
    LocationData("Temple of the Seeing One - Rock-Surrounded Chest", "Bedroom", ["Combat"]),
    LocationData("Temple of the Seeing One - Boss Chest", "Bedroom exit", []),
    # D41F2750-E3C7-BBB4-D650-FAFC190EBD32
    LocationData("Temple of the Seeing One - After Statue Left Chest", "Bedroom exit",
                 ["Combat", "Temple of the Seeing One Statue"], small_key=True),
    LocationData("Temple of the Seeing One - After Statue Right Chest", "Bedroom exit",
                 ["Combat", "Temple of the Seeing One Statue"]),
    # 401939A4-41BA-E07E-3BA2-DC22513DCC5C
    LocationData("Temple of the Seeing One - Dark Room Chest", "Bedroom", ["Combat"], small_key=True),
    LocationData("Blank - Card Chest", "Blank windmill"),
    LocationData("Cell - Top Left Chest", "Cell", ["Jump Shoes"]),
    LocationData("Cell - Chaser Gauntlet Chest", "Cell", ["Swap:2", "Combat", "Jump Shoes"]),
    # 75C2D434-4AE8-BCD0-DBEB-8E6CDA67BF45
    LocationData("Circus - Rat Maze Chest", "Circus", ["Combat", "Jump Shoes"], small_key=True),
    LocationData("Circus - Clowns Chest", "Circus", ["Combat", "Jump Shoes"]),
    LocationData("Circus - Fire Pillar Chest", "Circus 2", ["Combat", "Jump Shoes"]),
    # 69E8FBD6-2DA3-D25E-446F-6A59AC3E9FC2
    LocationData("Circus - Arthur Chest", "Circus", ["Combat", "Jump Shoes"], small_key=True),
    # 6A95EB2F-75FD-8649-5E07-3ED37C69A9FB
    LocationData("Circus - Javiera Chest", "Circus 2", ["Combat", "Jump Shoes"], small_key=True),
    # A2479A02-9B0D-751F-71A4-DB15C4982DF5
    LocationData("Circus - Lion Chest", "Circus 3", ["Combat", "Jump Shoes"], small_key=True),
    LocationData("Circus - Double Clowns Chest", "Circus 4", ["Combat", "Jump Shoes", "Keys:Circus:4"]),
    LocationData("Circus - Boss Chest", "Circus 4", ["Defeat Servants", "Combat", "Jump Shoes"]),
    LocationData("Cliffs - Upper Chest", "Cliff post windmill"),
    LocationData("Cliffs - Lower Chest", "Cliff post windmill"),
    LocationData("Mountain Cavern - 2F Crowded Ledge Chest", "Crowd floor 2",
                 ["Combat", "Jump Shoes", "Keys:Mountain Cavern:4"]),
    # BE2FB96B-1D5F-FCD1-3F58-D158DB982C21
    LocationData("Mountain Cavern - 2F Four Enemies Chest", "Crowd floor 2", ["Combat"], small_key=True),
    # 5743A883-D209-2518-70D7-869D14925B77
    LocationData("Mountain Cavern - 2F Entrance Chest", "Crowd floor 2", ["Combat", "Jump Shoes"], small_key=True),
    # 21EE2D01-54FB-F145-9464-4C2CC8725EB3
    LocationData("Mountain Cavern - 2F Frogs and Dog Chest", "Crowd floor 2", ["Combat", "Jump Shoes"], small_key=True),
    LocationData("Mountain Cavern - 3F Roller Chest", "Crowd floor 3",
                 ["Combat", "Jump Shoes", "Keys:Mountain Cavern:4"]),
    LocationData("Mountain Cavern - Boss Chest", "Crowd exit", []),
    LocationData("Mountain Cavern - Extend Upgrade Chest", "Crowd jump challenge", ["Combat", "Jump Shoes"]),
    # 868736EF-EC8B-74C9-ACAB-B7BC56A44394
    LocationData("Mountain Cavern - 2F Frogs and Rotators Chest", "Crowd floor 2", ["Combat", "Jump Shoes"],
                 small_key=True),
    LocationData("Debug - River Puzzles Chest", "Debug", ["Combat", "Jump Shoes"]),
    LocationData("Debug - Upper Prison Chest", "Debug"),
    LocationData("Debug - Lower Prison Chest", "Debug"),
    LocationData("Debug - Jumping Chest", "Debug"),
    LocationData("Debug - Maze Chest", "Debug", ["Jump Shoes"]),
    LocationData("Drawer - Game Over Chest", "Drawer", ["Swap:2"]),
    LocationData("Drawer - Brown Area Chest", "Drawer"),
    LocationData("Fields - Island Chest", "Fields", ["Combat", "Jump Shoes"]),
    LocationData("Fields - Gauntlet Chest", "Fields", ["Combat", "Jump Shoes"]),
    LocationData("Fields - Goldman's Cave Chest", "Fields", ["Combat"]),
    LocationData("Fields - Blocked River Chest", "Fields", ["Swap:2", "Jump Shoes"]),
    LocationData("Fields - Cardboard Box", "Fields"),
    LocationData("Fields - Shopkeeper Trade", "Fields", ["Cardboard Box"]),
    LocationData("Fields - Mitra Trade", "Fields", ["Biking Shoes"]),
    # Hidden path
    LocationData("Fields - Near Overworld Secret Chest", "Fields", ["Swap:2"]),
    # Hidden path
    LocationData("Fields - Secluded Glen Chest", "Fields", ["Swap:2"]),
    # Hidden path
    # Logically, this is in Terminal, because it is separated from the rest of Fields in the same way Terminal is.
    LocationData("Fields - Near Terminal Secret Chest", "Terminal", ["Swap:2"]),
    LocationData("Deep Forest - Inlet Chest", "Forest", ["Combat"]),
    # This is the one that takes 2 hours
    LocationData("Deep Forest - Bunny Chest", "Forest", ["Swap:2"]),
    LocationData("GO - Swap Upgrade Chest", "Go bottom"),
    LocationData("GO - Secret Color Puzzle Chest", "Go bottom", ["Swap:2"]),
    # 6C8870D4-7600-6FFD-B425-2D951E65E160
    LocationData("Hotel - 4F Annoyers Chest", "Hotel floor 4", ["Combat", "Jump Shoes"], small_key=True),
    LocationData("Hotel - 4F Dust Blower Maze Chest", "Hotel floor 4", ["Combat", "Jump Shoes", "Keys:Hotel:1"]),
    LocationData("Hotel - 3F Dashers Chest", "Hotel floor 3", ["Keys:Hotel:6"]),
    # 64EE884F-EA96-FB09-8A9E-F75ABDB6DC0D
    LocationData("Hotel - 3F Gasguy Chest", "Hotel floor 3", ["Combat"], small_key=True),
    # 075E6024-FE2D-9C4A-1D2B-D627655FD31A
    LocationData("Hotel - 3F Rotators Chest", "Hotel floor 3", ["Combat"], small_key=True),
    LocationData("Hotel - 2F Dog Chest", "Hotel floor 2 right", ["Combat"]),
    # 1990B3A2-DBF8-85DA-C372-ADAFAA75744C
    LocationData("Hotel - 2F Crevice Right Chest", "Hotel floor 2 right", small_key=True),
    # D2392D8D-0633-2640-09FA-4B921720BFC4
    LocationData("Hotel - 2F Backrooms Chest", "Hotel floor 2", ["Combat"], small_key=True),
    # 019CBC29-3614-9302-6848-DDAEDC7C49E5
    LocationData("Hotel - 1F Burst Flowers Chest", "Hotel floor 1", small_key=True),
    # 9D6FDA36-0CC6-BACC-3844-AEFB6C5C6290
    LocationData("Hotel - 2F Crevice Left Chest", "Hotel floor 2", ["Jump Shoes"], small_key=True),
    LocationData("Hotel - Boss Chest", "Hotel floor 1", ["Defeat Manager"]),
    LocationData("Hotel - Roof Chest", "Hotel roof", ["Swap:2"]),
    LocationData("Nexus - Isolated Chest", "Nexus top", ["Swap:2"]),
    LocationData("Overworld - Near Gate Chest", "Overworld"),
    LocationData("Overworld - After Temple Chest", "Overworld post windmill", ["Combat"]),
    LocationData("Red Cave - Top Cave Slasher Chest", "Red Cave top", ["Combat"]),
    # 72BAD10E-598F-F238-0103-60E1B36F6240
    LocationData("Red Cave - Middle Cave Right Chest", "Red Cave center", small_key=True),
    # AE87F1D5-57E0-1749-7E1E-1D0BCC1BCAB4
    LocationData("Red Cave - Middle Cave Left Chest", "Red Cave center", ["Combat"], small_key=True),
    LocationData("Red Cave - Middle Cave Middle Chest", "Red Cave center", ["Keys:Red Cave:6"]),
    LocationData("Red Cave - Boss Chest", "Red Cave exit", []),
    # 4A9DC50D-8739-9AD8-2CB1-82ECE29D3B6F
    LocationData("Red Cave - Left Cave Rapids Chest", "Red Cave left", ["Combat"], small_key=True),
    # A7672339-F3FB-C49E-33CE-42A49D7E4533
    LocationData("Red Cave - Right Cave Slasher Chest", "Red Cave right", ["Combat"], small_key=True),
    # 83286BFB-FFDA-237E-BA57-CA2E532E1DC7
    LocationData("Red Cave - Right Cave Four Shooter Chest", "Red Cave right", ["Combat"], small_key=True),
    # CDA1FF45-0F88-4855-B0EC-A9B42376C33F
    LocationData("Red Cave - Left Cave Sticky Chest", "Red Cave left", ["Combat"], small_key=True),
    LocationData("Red Cave - Widen Upgrade Chest", "Red Cave bottom"),
    LocationData("Red Cave - Isaac Dungeon Chest", "Red Cave Isaac", ["Combat"]),
    LocationData("Red Sea - Lonely Chest", "Red Sea"),
    LocationData("Red Sea - Out-of-bounds Chest", "Red Sea", ["Swap:2"]),
    LocationData("Young Town - Stab Reward Chest", "Suburb card house"),
    LocationData("Young Town - Killers Chest", "Suburb", ["Combat", "Swap:2"]),
    LocationData("Space - Left Chest", "Space"),
    LocationData("Space - Right Chest", "Space"),
    LocationData("Space - Challenge Area Chest", "Space", ["Combat", "Jump Shoes", "Swap:2"]),
    # Wiggle glitch available
    LocationData("Space - Hidden Chest", "Space"),
    # 3307AA58-CCF1-FB0D-1450-5AF0A0C458F7
    LocationData("Street - Key Chest", "Street", ["Combat"], small_key=True),
    LocationData("Street - Broom Chest", "Street"),
    LocationData("Street - Secret Chest", "Street", ["Swap:2"]),
    LocationData("Terminal - Broken Bridge Chest", "Terminal"),
    LocationData("Windmill - Chest", "Windmill", []),
    LocationData("Windmill - Activation", "Windmill", []),
    LocationData("Boss Rush - Reward Chest", "Boss Rush", ["Combat"]),
    LocationData("Apartment - Health Cicada", "Apartment floor 3", ["Defeat Watcher"], health_cicada=True),
    LocationData("Beach - Health Cicada", "Beach", ["Cards:8", "Combat"], health_cicada=True),
    LocationData("Temple of the Seeing One - Health Cicada", "Bedroom exit", ["Combat"], health_cicada=True),
    # Has to be frame 4
    LocationData("Cell - Health Cicada", "Cell", ["Cards:24"], health_cicada=True),
    LocationData("Circus - Health Cicada", "Circus 4", ["Defeat Servants"], health_cicada=True),
    LocationData("Mountain Cavern - Health Cicada", "Crowd floor 1", ["Defeat The Wall"], health_cicada=True),
    LocationData("Hotel - Health Cicada", "Hotel floor 1", ["Defeat Manager"], health_cicada=True),
    LocationData("Overworld - Health Cicada", "Overworld", ["Combat", "Cards:4"], health_cicada=True),
    LocationData("Red Cave - Health Cicada", "Red Cave top", ["Defeat Rogue"], health_cicada=True),
    LocationData("Young Town - Health Cicada", "Suburb", ["Combat", "Cards:16"], health_cicada=True),
    LocationData("Temple of the Seeing One - Green Key", "Bedroom exit", [], big_key=True),
    LocationData("Red Cave - Red Key", "Red Cave exit", [], big_key=True),
    LocationData("Mountain Cavern - Blue Key", "Crowd exit", [], big_key=True),
    LocationData("Red Cave - Middle Cave Left Tentacle", "Red Cave center", ["Combat"], tentacle=True),
    LocationData("Red Cave - Middle Cave Right Tentacle", "Red Cave center", [], tentacle=True),
    LocationData("Red Cave - Left Cave Tentacle", "Red Cave left", ["Keys:Red Cave:6"], tentacle=True),
    LocationData("Red Cave - Right Cave Tentacle", "Red Cave right", ["Keys:Red Cave:6"], tentacle=True),
    LocationData("GO - Defeat Briar", "Go top", ["Combat", "Jump Shoes"]),
    LocationData("Apartment - Warp Pad", "Apartment floor 1", nexus_gate=True),
    LocationData("Beach - Warp Pad", "Beach", nexus_gate=True),
    LocationData("Temple of the Seeing One - Warp Pad", "Bedroom exit", nexus_gate=True),
    LocationData("Blue - Warp Pad", "Blue", nexus_gate=True),
    LocationData("Cell - Warp Pad", "Cell", nexus_gate=True),
    LocationData("Cliffs - Warp Pad", "Cliff", nexus_gate=True),
    LocationData("Circus - Warp Pad", "Circus", nexus_gate=True),
    LocationData("Mountain Cavern - Warp Pad", "Crowd exit", nexus_gate=True),
    LocationData("Fields - Warp Pad", "Fields", nexus_gate=True),
    LocationData("Deep Forest - Warp Pad", "Forest", nexus_gate=True),
    LocationData("GO - Warp Pad", "Go bottom", nexus_gate=True),
    LocationData("Happy - Warp Pad", "Happy", nexus_gate=True),
    LocationData("Hotel - Warp Pad", "Hotel floor 4", nexus_gate=True),
    LocationData("Overworld - Warp Pad", "Overworld", nexus_gate=True),
    LocationData("Red Cave - Warp Pad", "Red Cave exit", nexus_gate=True),
    LocationData("Red Sea - Warp Pad", "Red Sea", nexus_gate=True),
    LocationData("Young Town - Warp Pad", "Suburb", nexus_gate=True),
    LocationData("Space - Warp Pad", "Space", nexus_gate=True),
    LocationData("Terminal - Warp Pad", "Terminal", nexus_gate=True),
    LocationData("Windmill - Warp Pad", "Windmill entrance", nexus_gate=True),
]

locations_by_name: Dict[str, LocationData] = {location.name: location for location in all_locations}


def build_locations_by_region_dict():
    result: Dict[str, List[LocationData]] = {}
    for location in all_locations:
        result.setdefault(location.region_name, []).append(location)
    return result


locations_by_region: Dict[str, List[LocationData]] = build_locations_by_region_dict()

location_groups = {
    "Warp Pads": [location.name for location in all_locations if location.nexus_gate],
}
