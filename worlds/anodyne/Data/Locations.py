from typing import NamedTuple, List, Dict

from . import Regions
from ..Options import CellGate, SuburbGate


class LocationData(NamedTuple):
    name: str
    region_name: str
    reqs: List[str] = []
    health_cicada: bool = False
    small_key: bool = False
    big_key: bool = False
    tentacle: bool = False
    nexus_gate: bool = False
    dust: bool = False

    def postgame(self,secret_paths:bool):
        return ("SwapOrSecret" in self.reqs and not secret_paths) or "Progressive Swap:2" in self.reqs or self.region_name in Regions.postgame_regions or (not secret_paths and self.region_name in Regions.postgame_without_secret_paths)


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
    LocationData("Beach - Secret Chest", "Beach Gauntlet", ["Progressive Swap:2"]),
    LocationData("Beach - Out-of-bounds Chest", "Beach", ["Progressive Swap:2"]),
    # 40DE36CF-9238-F8B0-7A57-C6C8CA465CC2
    LocationData("Temple of the Seeing One - Entrance Chest", "Bedroom entrance", small_key=True),
    LocationData("Temple of the Seeing One - Shieldy Room Chest", "Bedroom shieldy room", []),
    LocationData("Temple of the Seeing One - Rock-Surrounded Chest", "Bedroom core", []),
    LocationData("Temple of the Seeing One - Boss Chest", "Bedroom exit", []),
    # D41F2750-E3C7-BBB4-D650-FAFC190EBD32
    LocationData("Temple of the Seeing One - After Statue Left Chest", "Bedroom after statue", [], small_key=True),
    LocationData("Temple of the Seeing One - After Statue Right Chest", "Bedroom after statue", []),
    # 401939A4-41BA-E07E-3BA2-DC22513DCC5C
    LocationData("Temple of the Seeing One - Dark Room Chest", "Bedroom core", [], small_key=True),
    LocationData("Blank - Card Chest", "Blank windmill"),
    LocationData("Cell - Top Left Chest", "Cell", ["Jump Shoes"]),
    LocationData("Cell - Chaser Gauntlet Chest", "Cell", ["Progressive Swap:2", "Combat", "Jump Shoes"]),
    # 75C2D434-4AE8-BCD0-DBEB-8E6CDA67BF45
    LocationData("Circus - Rat Maze Chest", "Circus entry gauntlets", [], small_key=True),
    LocationData("Circus - Clowns Chest", "Circus entry gauntlets", []),
    LocationData("Circus - Fire Pillar Chest", "Circus circlejump gauntlets", []),
    # 69E8FBD6-2DA3-D25E-446F-6A59AC3E9FC2
    LocationData("Circus - Arthur Chest", "Circus entry gauntlets", [], small_key=True),
    # 6A95EB2F-75FD-8649-5E07-3ED37C69A9FB
    LocationData("Circus - Javiera Chest", "Circus circlejump gauntlets", [], small_key=True),
    # A2479A02-9B0D-751F-71A4-DB15C4982DF5
    LocationData("Circus - Lion Chest", "Circus third key gauntlet", [], small_key=True),
    LocationData("Circus - Double Clowns Chest", "Circus north gauntlet", []),
    LocationData("Circus - Boss Chest", "Circus boss gauntlet", ["Defeat Servants"]),
    LocationData("Cliffs - Upper Chest", "Cliff post windmill"),
    LocationData("Cliffs - Lower Chest", "Cliff post windmill"),
    LocationData("Mountain Cavern - 2F Crowded Ledge Chest", "Crowd floor 2 gauntlets",
                 ["Small Key (Mountain Cavern):4"]),
    # BE2FB96B-1D5F-FCD1-3F58-D158DB982C21
    LocationData("Mountain Cavern - 2F Four Enemies Chest", "Crowd floor 2", ["Combat"], small_key=True),
    # 5743A883-D209-2518-70D7-869D14925B77
    LocationData("Mountain Cavern - 2F Entrance Chest", "Crowd floor 2 gauntlets", small_key=True),
    # 21EE2D01-54FB-F145-9464-4C2CC8725EB3
    LocationData("Mountain Cavern - 2F Frogs and Dog Chest", "Crowd floor 2 gauntlets", small_key=True),
    LocationData("Mountain Cavern - 3F Roller Chest", "Crowd floor 3 center", []),
    LocationData("Mountain Cavern - Boss Chest", "Crowd exit", []),
    LocationData("Mountain Cavern - Extend Upgrade Chest", "Crowd jump challenge", ["Combat", "Jump Shoes"]),
    # 868736EF-EC8B-74C9-ACAB-B7BC56A44394
    LocationData("Mountain Cavern - 2F Frogs and Rotators Chest", "Crowd floor 2 gauntlets", small_key=True),
    LocationData("Debug - River Puzzles Chest", "Debug", ["Combat", "Jump Shoes"]),
    LocationData("Debug - Upper Prison Chest", "Debug"),
    LocationData("Debug - Lower Prison Chest", "Debug"),
    LocationData("Debug - Jumping Chest", "Debug"),
    LocationData("Debug - Maze Chest", "Debug", ["Jump Shoes"]),
    LocationData("Drawer - Game Over Chest", "Drawer", ["Progressive Swap:2"]),
    LocationData("Drawer - Brown Area Chest", "Drawer"),
    LocationData("Fields - Island Chest", "Fields Lake", ["Combat", "Jump Shoes"]),
    LocationData("Fields - Gauntlet Chest", "Fields Lake", ["Combat", "Jump Shoes"]),
    LocationData("Fields - Goldman's Cave Chest", "Fields", ["Combat"]),
    LocationData("Fields - Blocked River Chest", "Fields", ["Progressive Swap:2", "Jump Shoes"]),
    LocationData("Fields - Cardboard Box", "Fields"),
    LocationData("Fields - Shopkeeper Trade", "Fields", ["Cardboard Box"]),
    LocationData("Fields - Mitra Trade", "Fields", ["Biking Shoes"]),
    # Hidden path
    LocationData("Fields - Near Overworld Secret Chest", "Fields North Secret Area"),
    # Hidden path
    LocationData("Fields - Secluded Glen Chest", "Fields", ["SwapOrSecret"]),
    # Hidden path
    # Logically, this is in Terminal, because it is separated from the rest of Fields in the same way Terminal is.
    LocationData("Fields - Near Terminal Secret Chest", "Terminal", ["SwapOrSecret"]),
    LocationData("Deep Forest - Inlet Chest", "Forest", ["Combat"]),
    # This is the one that takes 2 hours
    LocationData("Deep Forest - Bunny Chest", "Forest", ["Progressive Swap:2"]),
    LocationData("GO - Swap Upgrade Chest", "Go bottom"),
    LocationData("GO - Secret Color Puzzle Chest", "Go bottom", ["Progressive Swap:2"]),
    # 6C8870D4-7600-6FFD-B425-2D951E65E160
    LocationData("Hotel - 4F Annoyers Chest", "Hotel floor 4", ["Combat", "Jump Shoes"], small_key=True),
    LocationData("Hotel - 4F Dust Blower Maze Chest", "Hotel floor 4", ["Combat", "Jump Shoes", "Small Key (Hotel):1"]),
    LocationData("Hotel - 3F Dashers Chest", "Hotel floor 3", ["Small Key (Hotel):6"]),
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
    LocationData("Hotel - Roof Chest", "Hotel roof", ["Combat", "Progressive Swap:2"]),
    LocationData("Nexus - Isolated Chest", "Nexus top", ["Progressive Swap:2"]),
    LocationData("Overworld - Near Gate Chest", "Overworld"),
    LocationData("Overworld - After Temple Chest", "Overworld post windmill", ["Combat"]),
    LocationData("Red Cave - Top Cave Slasher Chest", "Red Cave top", ["Combat"]),
    # 72BAD10E-598F-F238-0103-60E1B36F6240
    LocationData("Red Cave - Middle Cave Right Chest", "Red Cave center", small_key=True),
    # AE87F1D5-57E0-1749-7E1E-1D0BCC1BCAB4
    LocationData("Red Cave - Middle Cave Left Chest", "Red Cave center", ["Combat"], small_key=True),
    LocationData("Red Cave - Middle Cave Middle Chest", "Red Cave center", ["Small Key (Red Cave):6"]),
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
    LocationData("Red Sea - Out-of-bounds Chest", "Red Sea", ["Progressive Swap:2"]),
    LocationData("Young Town - Stab Reward Chest", "Suburb card house"),
    LocationData("Young Town - Killers Chest", "Suburb", ["Combat", "Progressive Swap:2"]),
    LocationData("Space - Left Chest", "Space"),
    LocationData("Space - Right Chest", "Space"),
    LocationData("Space - Challenge Area Chest", "Space Gauntlet"),
    # Wiggle glitch available
    LocationData("Space - Hidden Chest", "Space"),
    # 3307AA58-CCF1-FB0D-1450-5AF0A0C458F7
    LocationData("Street - Key Chest", "Street", ["Combat"], small_key=True),
    LocationData("Street - Broom Chest", "Street"),
    LocationData("Street - Secret Chest", "Street", ["Progressive Swap:2"]),
    LocationData("Terminal - Broken Bridge Chest", "Terminal"),
    LocationData("Windmill - Chest", "Windmill", []),
    LocationData("Windmill - Activation", "Windmill", []),
    LocationData("Boss Rush - Reward Chest", "Boss Rush"),
    # Health Cicadas
    LocationData("Apartment - Health Cicada", "Apartment floor 3", ["Defeat Watcher"], health_cicada=True),
    LocationData("Beach - Health Cicada", "Beach Gauntlet", [], health_cicada=True),
    LocationData("Temple of the Seeing One - Health Cicada", "Bedroom exit", ["Defeat Seer"], health_cicada=True),
    # Has to be frame 4
    LocationData("Cell - Health Cicada", "Cell", [CellGate.typename(), "Jump Shoes"], health_cicada=True),
    LocationData("Circus - Health Cicada", "Circus boss gauntlet", ["Defeat Servants"], health_cicada=True),
    LocationData("Mountain Cavern - Health Cicada", "Crowd floor 1", ["Defeat The Wall"], health_cicada=True),
    LocationData("Hotel - Health Cicada", "Hotel floor 1", ["Defeat Manager"], health_cicada=True),
    LocationData("Overworld - Health Cicada", "Overworld Gauntlet", [], health_cicada=True),
    LocationData("Red Cave - Health Cicada", "Red Cave top", ["Defeat Rogue"], health_cicada=True),
    LocationData("Young Town - Health Cicada", "Suburb", [SuburbGate.typename()], health_cicada=True),
    LocationData("Temple of the Seeing One - Green Key", "Bedroom exit", [], big_key=True),
    LocationData("Red Cave - Red Key", "Red Cave exit", [], big_key=True),
    LocationData("Mountain Cavern - Blue Key", "Crowd exit", [], big_key=True),
    LocationData("Red Cave - Middle Cave Left Tentacle", "Red Cave center", ["Combat"], tentacle=True),
    LocationData("Red Cave - Middle Cave Right Tentacle", "Red Cave center", [], tentacle=True),
    LocationData("Red Cave - Left Cave Tentacle", "Red Cave left", ["Small Key (Red Cave):6"], tentacle=True),
    LocationData("Red Cave - Right Cave Tentacle", "Red Cave right", ["Small Key (Red Cave):6"], tentacle=True),
    LocationData("GO - Defeat Briar", "Go top", ["Combat", "Jump Shoes"]),
    # Nexus portals
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
    # Dust locations
    LocationData("Apartment - 1F Shortcut Room Dust 1", "Apartment floor 1", ["Jump Shoes"], dust=True),
    LocationData("Apartment - 2F Switch Pillar Rat Maze Dust", "Apartment floor 2", ["Jump Shoes", "Small Key (Apartment):3"], dust=True),
    LocationData("Apartment - 2F Dash Trap Rat Maze Dust", "Apartment floor 2", ["Jump Shoes", "Small Key (Apartment):3"], dust=True),
    LocationData("Apartment - 2F Flooded Room Dust", "Apartment floor 2", ["Jump Shoes"], dust=True),
    LocationData("Apartment - 1F Couches Dust", "Apartment floor 1 top left", ["Jump Shoes"], dust=True),
    LocationData("Apartment - 1F Shortcut Room Dust 2", "Apartment floor 1", dust=True),
    LocationData("Apartment - 1F Rat Maze Chest Dust 1", "Apartment floor 1", dust=True),
    LocationData("Apartment - 1F Rat Maze Chest Dust 2", "Apartment floor 1", dust=True),
    LocationData("Apartment - 1F Rat Maze Chest Dust 3", "Apartment floor 1", dust=True),
    LocationData("Apartment - 1F Entrance Dust", "Apartment floor 1", dust=True),
    LocationData("Apartment - 1F Flooded Room Dust", "Apartment floor 1", dust=True),
    LocationData("Apartment - 1F Flooded Library Dust", "Apartment floor 1", dust=True),
    LocationData("Temple of the Seeing One - Laser Room Dust 1", "Bedroom core", dust=True),
    LocationData("Temple of the Seeing One - Laser Room Dust 2", "Bedroom core", dust=True),
    LocationData("Temple of the Seeing One - Room With Holes Dust 1", "Bedroom core", dust=True),
    LocationData("Temple of the Seeing One - Room With Holes Dust 2", "Bedroom core", dust=True),
    LocationData("Temple of the Seeing One - Past Shieldy Puzzle Dust 1", "Bedroom core", dust=True),
    LocationData("Temple of the Seeing One - Before Boss Dust 1", "Bedroom core", dust=True),
    LocationData("Temple of the Seeing One - Past Shieldy Puzzle Dust 2", "Bedroom core", dust=True),
    LocationData("Temple of the Seeing One - Shieldy Room Dust 1", "Bedroom shieldy room", dust=True),
    LocationData("Temple of the Seeing One - Shieldy Room Dust 2", "Bedroom shieldy room", dust=True),
    LocationData("Temple of the Seeing One - Laser Room Dust 3", "Bedroom core", dust=True),
    LocationData("Temple of the Seeing One - Entrance Dust 1", "Bedroom entrance", dust=True),
    LocationData("Temple of the Seeing One - Entrance Dust 2", "Bedroom entrance", dust=True),
    LocationData("Temple of the Seeing One - Before Boss Dust 2", "Bedroom core", dust=True),
    LocationData("Temple of the Seeing One - Laser Room Dust 4", "Bedroom core", dust=True),
    LocationData("Blue - Laser Room Dust", "Blue", ["Jump Shoes"], dust=True),
    LocationData("Circus - Dash Trap Dust", "Circus entry gauntlets", dust=True),
    LocationData("Circus - Fire Pillars in Water Dust 3", "Circus third key gauntlet", dust=True),
    LocationData("Circus - Lion Dust 1", "Circus third key gauntlet", dust=True),
    LocationData("Circus - Lion Dust 2", "Circus third key gauntlet", dust=True),
    LocationData("Circus - Fire Pillars in Water Dust 2", "Circus third key gauntlet", dust=True),
    LocationData("Circus - Fire Pillars in Water Dust 1", "Circus third key gauntlet", dust=True),
    # Overlaps with Fire Pillars in Water Dust 3
    LocationData("Circus - Fire Pillars in Water Dust 4", "Circus third key gauntlet", dust=True),
    LocationData("Circus - Dog Room Dust", "Circus boss gauntlet", dust=True),
    LocationData("Circus - Javiera Dust 2", "Circus circlejump gauntlets", dust=True),
    LocationData("Circus - Javiera Dust 1", "Circus circlejump gauntlets", dust=True),
    LocationData("Circus - Slime and Fire Pillar Dust", "Circus past entrance lake", dust=True),
    LocationData("Circus - Small Contort Room Dust", "Circus third key gauntlet", dust=True),
    LocationData("Circus - Save Point Dust", "Circus third key gauntlet", dust=True),
    LocationData("Circus - Clown Dust 1", "Circus entry gauntlets", dust=True),
    LocationData("Circus - Clown Dust 2", "Circus entry gauntlets", dust=True),
    LocationData("Circus - Spike Dust", "Circus boss gauntlet", dust=True),
    LocationData("Circus - Dash Pad over Hole Dust", "Circus entrance lake", dust=True),
    LocationData("Circus - Lion and Dash Pad Dust", "Circus past entrance lake", dust=True),
    LocationData("Circus - Spike Roller in Water Dust", "Circus entrance lake", dust=True),
    LocationData("Circus - Entrance Dust", "Circus", dust=True),
    LocationData("Mountain Cavern - 3F Top Center Moving Platform Dust", "Crowd floor 3", dust=True),
    LocationData("Mountain Cavern - 3F Top Right Moving Platform Dust", "Crowd floor 3", ["Jump Shoes"], dust=True),
    LocationData("Mountain Cavern - 3F Roller Dust", "Crowd floor 3 center", dust=True),
    LocationData("Mountain Cavern - 2F Frogs and Annoyers Dust", "Crowd floor 2 gauntlets", dust=True),
    LocationData("Mountain Cavern - 2F Rotators and Annoyers Dust 1", "Crowd floor 2 gauntlets", dust=True),
    LocationData("Mountain Cavern - 2F Rotators and Annoyers Dust 2", "Crowd floor 2 gauntlets", dust=True),
    LocationData("Mountain Cavern - 2F Circular Hole Dust 1", "Crowd floor 2 gauntlets", dust=True),
    LocationData("Mountain Cavern - 2F Circular Hole Dust 2", "Crowd floor 2 gauntlets", dust=True),
    LocationData("Mountain Cavern - 2F Crossing Moving Platforms Dust 1", "Crowd floor 2 gauntlets", dust=True),
    LocationData("Mountain Cavern - 2F Crossing Moving Platforms Dust 2", "Crowd floor 2 gauntlets", dust=True),
    LocationData("Mountain Cavern - 2F Moving Platform Crossroad Dust 1", "Crowd floor 2 gauntlets", dust=True),
    LocationData("Mountain Cavern - 2F Moving Platform Crossroad Dust 2", "Crowd floor 2 gauntlets", dust=True),
    LocationData("Mountain Cavern - 2F Moving Platform Crossroad Dust 3", "Crowd floor 2 gauntlets", dust=True),
    LocationData("Debug - Moving Platform Dust", "Debug", dust=True),
    LocationData("Debug - Whirlpool Room Dust 1", "Debug", dust=True),
    LocationData("Debug - Whirlpool Room Dust 2", "Debug", dust=True),
    LocationData("Debug - Sound Test Console Dust", "Debug", dust=True),
    LocationData("Fields - Goldman's Cave Dust 1", "Fields", dust=True),
    LocationData("Fields - Goldman's Cave Dust 2", "Fields", dust=True),
    LocationData("Fields - Goldman's Cave Dust 3", "Fields", dust=True),
    LocationData("Fields - Goldman's Cave Dust 4", "Fields", dust=True),
    LocationData("Fields - Goldman's Cave Dust 5", "Fields", dust=True),
    LocationData("Fields - Goldman's Cave Dust 6", "Fields", dust=True),
    LocationData("Fields - Goldman's Cave Dust 7", "Fields", dust=True),
    LocationData("Fields - Goldman's Cave Dust 8", "Fields", dust=True),
    LocationData("Fields - Goldman's Cave Dust 9", "Fields", dust=True),
    LocationData("Fields - Lake After Spikes Dust", "Fields Lake", dust=True),
    LocationData("Fields - North River Dust", "Fields", dust=True),
    LocationData("Fields - Lake After Holes Floating Dust", "Fields Lake", dust=True),
    LocationData("Fields - South East of Lake Dust", "Fields Lake", dust=True),
    LocationData("Fields - Lake Near Windmill Dust", "Fields Lake", dust=True),
    LocationData("Fields - North of Lake Rapids Dust", "Fields", dust=True),
    LocationData("Fields - North East of Lake Dust", "Fields", dust=True),
    LocationData("Fields - Before Annoyer Maze Dust", "Fields", dust=True),
    LocationData("Fields - Mitra House Dust", "Fields", dust=True),
    LocationData("Fields - Near Red Gate Dust", "Fields", dust=True),
    LocationData("Fields - After Red Gate Dust", "Fields Past Gate", dust=True),
    LocationData("Fields - Near Terminal Dust", "Fields Past Gate", dust=True),
    LocationData("Fields - North West of Lake Dust", "Fields", dust=True),
    LocationData("Fields - Near Beach Dust", "Fields", dust=True),
    LocationData("Fields - South West Corner Dust", "Fields Lake", dust=True),
    LocationData("Fields - South East of Gauntlet Dust", "Fields Lake", dust=True),
    LocationData("Fields - Before Gauntlet Dust", "Fields Lake", dust=True),
    LocationData("Fields - Island Chest Dust", "Fields Lake", dust=True),
    LocationData("Fields - Island Start Dust", "Fields Lake", dust=True),
    LocationData("Fields - Post Whirlpool Dust", "Fields Lake", dust=True),
    LocationData("Fields - Olive Dust", "Fields Lake", dust=True),
    LocationData("Deep Forest - Relaxation Pond Dust", "Forest", dust=True),
    LocationData("Deep Forest - Near Cliff Dust", "Forest", dust=True),
    LocationData("Deep Forest - Floating Dust", "Forest", dust=True),
    LocationData("Deep Forest - Thorax Dust", "Forest", dust=True),
    LocationData("Deep Forest - Carved Rock Dust", "Forest", dust=True),
    LocationData("Deep Forest - Tiny Island Dust", "Forest", dust=True),
    LocationData("Deep Forest - Inlet Dust", "Forest", dust=True),
    LocationData("Deep Forest - Before Inlet Chest Dust", "Forest", dust=True),
    LocationData("Happy - Final Room Dust", "Happy gauntlet", [], dust=True),
    LocationData("Happy - Dustmaid Dust", "Happy gauntlet", [], dust=True),
    LocationData("Hotel - 1F Floating Dustmaid Dust", "Hotel floor 1", ["Small Key (Hotel):4", "Jump Shoes"], dust=True),
    LocationData("Hotel - 3F Hallway Dustmaid Dust 2", "Hotel floor 3", ["Small Key (Hotel):1", "Jump Shoes"], dust=True),
    LocationData("Hotel - 3F Hallway Dustmaid Dust 1", "Hotel floor 3", ["Small Key (Hotel):1", "Jump Shoes"], dust=True),
    LocationData("Hotel - 4F Moving Platform Crossroad 1", "Hotel floor 4", ["Jump Shoes"], dust=True),
    LocationData("Hotel - 1F Boss Dust", "Hotel floor 1", ["Small Key (Hotel):6","Jump Shoes"], dust=True),
    LocationData("Hotel - 1F Gasguy Dust", "Hotel floor 1", ["Small Key (Hotel):6", "Jump Shoes"], dust=True),
    LocationData("Hotel - 1F Dustmaid and Steampipe Dust 3", "Hotel floor 1", ["Small Key (Hotel):6", "Jump Shoes"], dust=True),
    LocationData("Hotel - 1F Dustmaid and Steampipe Dust 2", "Hotel floor 1", ["Small Key (Hotel):6", "Jump Shoes"], dust=True),
    LocationData("Hotel - 1F Dustmaid and Steampipe Dust 1", "Hotel floor 1", ["Small Key (Hotel):6", "Jump Shoes"], dust=True),
    LocationData("Hotel - 1F Dustmaid and Steampipe Dust 4", "Hotel floor 1", ["Small Key (Hotel):6", "Jump Shoes"], dust=True),
    LocationData("Hotel - 2F Steampipe Dust 2", "Hotel floor 2", ["Jump Shoes"], dust=True),
    LocationData("Hotel - 2F Steampipe Dust 1", "Hotel floor 2", ["Jump Shoes"], dust=True),
    LocationData("Hotel - 1F Locked Dust", "Hotel floor 1", ["Small Key (Hotel):6", "Jump Shoes"], dust=True),
    LocationData("Hotel - 2F Dustmaid and Steampipe Dust 3", "Hotel floor 2", ["Small Key (Hotel):4", "Jump Shoes"], dust=True),
    LocationData("Hotel - 2F Dustmaid and Steampipe Dust 1", "Hotel floor 2", ["Small Key (Hotel):4", "Jump Shoes"], dust=True),
    LocationData("Hotel - 2F Dustmaid and Steampipe Dust 2", "Hotel floor 2", ["Small Key (Hotel):4", "Jump Shoes"], dust=True),
    LocationData("Hotel - 2F Dustmaid Hallway Dust", "Hotel floor 2", ["Small Key (Hotel):4", "Jump Shoes"], dust=True),
    LocationData("Hotel - 3F Stream Dustmaid Dust", "Hotel floor 3", ["Small Key (Hotel):4", "Jump Shoes"], dust=True),
    LocationData("Hotel - 3F Bedroom Dust", "Hotel floor 3", ["Small Key (Hotel):4", "Jump Shoes"], dust=True),
    LocationData("Hotel - 4F Slime Dust 2", "Hotel floor 4", ["Jump Shoes"], dust=True),
    LocationData("Hotel - 4F Slime Dust 1", "Hotel floor 4", ["Jump Shoes"], dust=True),
    LocationData("Hotel - 4F Moving Platform Crossroad 2", "Hotel floor 4", ["Jump Shoes"], dust=True),
    LocationData("Hotel - 4F Dustmaid Dust", "Hotel floor 4", ["Jump Shoes"], dust=True),
    LocationData("Hotel - 4F Near Elevator Dust", "Hotel floor 4", ["Jump Shoes"], dust=True),
    LocationData("Hotel - 4F Spring Puzzle Dust", "Hotel floor 4", ["Small Key (Hotel):1", "Jump Shoes"], dust=True),
    LocationData("Hotel - 4F Moving Platform Puzzle Dust", "Hotel floor 4", ["Small Key (Hotel):1", "Jump Shoes"], dust=True),
    LocationData("Red Cave - Top Cave Boss Dust 1", "Red Cave top", dust=True),
    LocationData("Red Cave - Top Cave Boss Dust 2", "Red Cave top", dust=True),
    LocationData("Red Cave - Top Cave Before Boss Dust", "Red Cave top", dust=True),
    LocationData("Red Cave - Top Cave Slasher Dust", "Red Cave top", dust=True),
    LocationData("Red Cave - Top Cave Before Slasher Dust", "Red Cave top", dust=True),
    LocationData("Red Cave - Top Cave Boss Dust 3", "Red Cave top", dust=True),
    LocationData("Red Cave - Top Cave Boss Dust 4", "Red Cave top", dust=True),
    LocationData("Red Cave - Left Cave Rapids Dust 1", "Red Cave left", dust=True),
    LocationData("Red Cave - Left Cave Rapids Dust 2", "Red Cave left", dust=True),
    LocationData("Red Cave - Right Cave Before Slasher Dust", "Red Cave right", dust=True),
    LocationData("Red Cave - Right Cave Whirlpool Dust 1", "Red Cave right", dust=True),
    LocationData("Red Cave - Left Cave Whirlpool Dust 1", "Red Cave left", dust=True),
    LocationData("Red Cave - Left Cave Whirlpool Dust 2", "Red Cave left", dust=True),
    LocationData("Red Cave - Right Cave Whirlpool Dust 2", "Red Cave right", dust=True),
    LocationData("Space - Challenge Area Dustmaid Dust 1", "Space Gauntlet", dust=True),
    LocationData("Space - Challenge Area Dustmaid Dust 2", "Space Gauntlet", dust=True),
    LocationData("Space - Challenge Area Lion Dust 1", "Space Gauntlet", dust=True),
    LocationData("Space - Challenge Area Lion Dust 2", "Space Gauntlet", dust=True),
    LocationData("Street - After Bridge Dust 1", "Street", ["Small Key (Street):1"], dust=True),
    LocationData("Street - After Bridge Dust 2", "Street", ["Small Key (Street):1"], dust=True),
    LocationData("Boss Rush - Before Red Boss Dust", "Boss Rush", dust=True),
    LocationData("Boss Rush - Red Boss Dust 1", "Boss Rush", dust=True),
    LocationData("Boss Rush - Red Boss Dust 2", "Boss Rush", dust=True),
    LocationData("Boss Rush - Red Boss Dust 3", "Boss Rush", dust=True),
    LocationData("Boss Rush - Red Boss Dust 4", "Boss Rush", dust=True),
    LocationData("Boss Rush - Manager Phase 1 Dust", "Boss Rush", dust=True),
    LocationData("Boss Rush - Manager Phase 2 Dust", "Boss Rush", dust=True)
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
