from .Locations import prices_ints

from .Constants import *

def can_play_song(song, state, player):
    return state.has(song, player) and state.has("Ocarina of Time", player)

def can_get_magic_beans(state, player):
    return state.has("Magic Bean", player) and state.has("Deku Mask", player) and state.can_reach("Deku Palace", 'Region', player)

def has_bombchus(state, player):
    return state.has("Progressive Bombchu Bag", player)

def has_explosives(state, player):
    return state.has("Progressive Bomb Bag", player) or has_bombchus(state, player) or state.has("Blast Mask", player)

def has_hard_projectiles(state, player):
    return state.has("Progressive Bow", player) or state.has("Zora Mask", player) or state.has("Hookshot", player)

def has_projectiles(state, player):
    return (state.has("Deku Mask", player) and state.has("Progressive Magic", player)) or has_hard_projectiles(state, player)

def can_smack_hard(state, player):
    return state.has("Progressive Sword", player) or state.has("Fierce Deity's Mask", player) or state.has("Great Fairy Sword", player) or state.has("Goron Mask", player) or state.has("Zora Mask", player)

def can_smack(state, player):
    return can_smack_hard(state, player) or state.has("Deku Mask", player)

def can_clear_woodfall(state, player):
    return state.can_reach("Woodfall Temple Odolwa's Remains", 'Location', player)
    
def can_clear_snowhead(state, player):
    return state.can_reach("Snowhead Temple Goht's Remains", 'Location', player)
    
def can_clear_greatbay(state, player):
    return state.can_reach("Great Bay Temple Gyorg's Remains", 'Location', player)
    
def can_clear_stonetower(state, player):
    return state.can_reach("Stone Tower Temple Inverted Twinmold's Remains", 'Location', player)

def has_paper(state, player):
    return state.has("Land Title Deed", player) or state.has("Swamp Title Deed", player) or state.has("Mountain Title Deed", player) or state.has("Ocean Title Deed", player) or state.has("Letter to Kafei", player) or state.has("Priority Mail", player)

def can_get_cow_milk(state, player):
    return has_bottle(state, player) and can_play_song("Epona's Song", state, player) and (has_explosives(state, player) or can_use_powder_keg(state, player) or state.has("Hookshot", player) or (state.has("Gibdo Mask", player) and has_bottle(state, player) and can_plant_beans(state, player) and state.can_reach("Twin Islands Hot Water Grotto Chest", 'Location', player) or can_use_light_arrows(state, player) and (state.can_reach("Twin Islands Hot Water Grotto Chest", 'Location', player) or (state.has("Goron Mask", player) and state.can_reach("Mountain Village Invisible Ladder Cave Healing Invisible Goron", 'Location', player)) or state.can_reach("Ikana Well Invisible Chest", 'Location', player))))

def has_bottle(state, player, need_count=1):
    bottle_count = 0
    if state.has("Bottle", player, 2):
        bottle_count += 2
    elif state.has("Bottle", player):
        bottle_count += 1
    if state.has("Bottle of Milk", player):
        bottle_count += 1
    if state.has("Bottle of Chateau Romani", player):
        bottle_count += 1
    if state.has("Bottle of Red Potion", player):
        bottle_count += 1
    return bottle_count >= need_count

def can_plant_beans(state, player):
    return can_get_magic_beans(state, player) and (has_bottle(state, player) or can_play_song("Song of Storms", state, player))

def can_use_powder_keg(state, player):
    return state.has("Powder Keg", player) and state.has("Goron Mask", player)

def can_use_magic_arrow(item, state, player):
    return state.has(item, player) and state.has("Progressive Bow", player) and state.has("Progressive Magic", player)

def can_use_fire_arrows(state, player):
    return can_use_magic_arrow("Fire Arrow", state, player)

def can_use_ice_arrows(state, player):
    return can_use_magic_arrow("Ice Arrow", state, player)

def can_use_light_arrows(state, player):
    return can_use_magic_arrow("Light Arrow", state, player)

def has_gilded_sword(state, player):
    return state.has("Progressive Sword", player, 3)

def has_mirror_shield(state, player):
    return state.has("Progressive Shield", player, 2)

def can_use_lens(state, player):
    return state.has("Lens of Truth", player) and state.has("Progressive Magic", player)

def can_bring_to_player(state, player):
    return state.has("Hookshot", player) or state.has("Zora Mask", player)

def can_reach_scarecrow(state, player):
    return state.can_reach("Astral Observatory", 'Region', player) or state.can_reach("Trading Post", 'Region', player),

def can_reach_seahorse(state, player):
    return state.can_reach("Fisherman's House", 'Region', player) and state.has("Zora Mask", player) and state.has("Pictograph Box", player) and (state.has("Hookshot", player) or state.has("Goron Mask", player))

def can_afford_price(state, player, price):
    if price > 200:
        return state.has("Progressive Wallet", player, 2)
    elif price > 99:
        return state.has("Progressive Wallet", player)
    return True

def can_purchase(state, player, price_index):
    price = prices_ints[price_index]
    if price > 200:
        return state.has("Progressive Wallet", player, 2)
    elif price > 99:
        return state.has("Progressive Wallet", player)
    return True

def has_enough_remains(state, player, need_count):
    remains_count = 0
    if state.has("Odolwa's Remains", player):
        remains_count += 1
    if state.has("Goht's Remains", player):
        remains_count += 1
    if state.has("Gyorg's Remains", player):
        remains_count += 1
    if state.has("Twinmold's Remains", player):
        remains_count += 1
    return remains_count >= need_count

def get_region_rules(player, options):
    return {
        "Clock Town -> The Moon":
            lambda state: state.has("Ocarina of Time", player) and state.has("Oath to Order", player) and has_enough_remains(state, player, options.moon_remains_required.value),
        "Southern Swamp -> Southern Swamp (Deku Palace)":
            lambda state: state.has("Bottle of Red Potion", player) or (has_hard_projectiles(state, player) and state.has("Deku Mask", player)) or (state.has("Pictograph Box", player) and state.has("Deku Mask", player)),
        "Southern Swamp (Deku Palace) -> Swamp Spider House":
            lambda state: state.has("Deku Mask", player),
        "Southern Swamp (Deku Palace) -> Deku Palace":
            lambda state: state.has("Deku Mask", player),
        "Southern Swamp (Deku Palace) -> Woodfall":
            lambda state: state.has("Deku Mask", player),
        "Woodfall -> Woodfall Temple":
            lambda state: can_play_song("Sonata of Awakening", state, player),
        "Termina Field -> Path to Mountain Village":
            lambda state: state.has("Progressive Bow", player),
        "Path to Mountain Village -> Mountain Village":
            lambda state: state.has("Goron Mask", player) or (has_explosives(state, player)) or (can_use_fire_arrows(state, player)),
        "Path to Snowhead -> Snowhead Temple":
            lambda state: state.has("Goron Mask", player) and can_play_song("Goron Lullaby", state, player) and state.has("Progressive Magic", player),
        "Termina Field -> Great Bay":
            lambda state: can_play_song("Epona's Song", state, player),
        "Great Bay -> Ocean Spider House":
            lambda state: has_explosives(state, player),
        "Great Bay -> Pirates' Fortress":
            lambda state: state.has("Zora Mask", player),
        "Pirates' Fortress -> Pirates' Fortress Sewers":
            lambda state: state.has("Goron Mask", player) or state.has("Hookshot", player),
        "Pirates' Fortress Sewers -> Pirates' Fortress (Interior)":
            lambda state: True,
        "Zora Cape -> Zora Hall":
            lambda state: state.has("Zora Mask", player),
        "Zora Cape -> Great Bay Temple":
            lambda state: can_play_song("New Wave Bossa Nova", state, player) and state.has("Hookshot", player) and state.has("Zora Mask", player),
        "Road to Ikana -> Ikana Graveyard":
            lambda state: can_play_song("Epona's Song", state, player),
        "Road to Ikana -> Ikana Canyon":
            lambda state: (state.has("Garo Mask", player) and can_play_song("Epona's Song", state, player) and state.has("Hookshot", player)) or (state.has("Gibdo Mask", player) and can_play_song("Epona's Song", state, player) and state.has("Hookshot", player)),
        "Ikana Canyon -> Secret Shrine":
            lambda state: can_use_light_arrows(state, player),
        "Ikana Canyon -> Beneath the Well":
            lambda state: can_use_ice_arrows(state, player) and state.has("Hookshot", player) and state.has("Gibdo Mask", player) and has_bottle(state, player),
        "Ikana Canyon -> Ikana Castle":
            lambda state: can_use_ice_arrows(state, player) and state.has("Hookshot", player) and (can_use_light_arrows(state, player) or has_mirror_shield(state, player)),
        "Stone Tower -> Stone Tower Temple":
            lambda state: can_use_ice_arrows(state, player) and can_play_song("Elegy of Emptiness", state, player) and state.has("Goron Mask", player) and state.has("Zora Mask", player),
        "Stone Tower -> Stone Tower (Inverted)":
            lambda state: state.can_reach("Stone Tower Temple", 'Region', player) and can_use_light_arrows(state, player) and can_play_song("Elegy of Emptiness", state, player),
    }

def get_location_rules(player, options):
    return {
        "Keaton Quiz":
            lambda state: state.has("Keaton Mask", player),
        "Clock Tower Happy Mask Salesman #1":
            lambda state: True,
        "Clock Tower Happy Mask Salesman #2":
            lambda state: True,
        "Clock Town Postbox":
            lambda state: state.has("Postman's Hat", player),
        "Clock Town Hide-and-Seek":
            lambda state: has_projectiles(state, player),
        "Clock Town Trading Post Shop Item 1":
            lambda state: can_purchase(state, player, SHOP_ID_TRADING_POST_1),
        "Clock Town Trading Post Shop Item 2":
            lambda state: can_purchase(state, player, SHOP_ID_TRADING_POST_2),
        "Clock Town Trading Post Shop Item 3":
            lambda state: can_purchase(state, player, SHOP_ID_TRADING_POST_3),
        "Clock Town Trading Post Shop Item 4":
            lambda state: can_purchase(state, player, SHOP_ID_TRADING_POST_4),
        "Clock Town Trading Post Shop Item 5":
            lambda state: can_purchase(state, player, SHOP_ID_TRADING_POST_5),
        "Clock Town Trading Post Shop Item 6":
            lambda state: can_purchase(state, player, SHOP_ID_TRADING_POST_6),
        "Clock Town Trading Post Shop Item 7":
            lambda state: can_purchase(state, player, SHOP_ID_TRADING_POST_7),
        "Clock Town Trading Post Shop Item 8":
            lambda state: can_purchase(state, player, SHOP_ID_TRADING_POST_8),
        "Clock Town Trading Post Shop (Night) Item 1":
            lambda state: can_purchase(state, player, SHOP_ID_TRADING_POST_NIGHT_1),
        "Clock Town Trading Post Shop (Night) Item 2":
            lambda state: can_purchase(state, player, SHOP_ID_TRADING_POST_NIGHT_2),
        "Clock Town Trading Post Shop (Night) Item 3":
            lambda state: can_purchase(state, player, SHOP_ID_TRADING_POST_NIGHT_3),
        "Clock Town Trading Post Shop (Night) Item 4":
            lambda state: can_purchase(state, player, SHOP_ID_TRADING_POST_NIGHT_4),
        "Clock Town Trading Post Shop (Night) Item 5":
            lambda state: can_purchase(state, player, SHOP_ID_TRADING_POST_NIGHT_5),
        "Clock Town Trading Post Shop (Night) Item 6":
            lambda state: can_purchase(state, player, SHOP_ID_TRADING_POST_NIGHT_6),
        "Clock Town Trading Post Shop (Night) Item 7":
            lambda state: can_purchase(state, player, SHOP_ID_TRADING_POST_NIGHT_7),
        "Clock Town Trading Post Shop (Night) Item 8":
            lambda state: can_purchase(state, player, SHOP_ID_TRADING_POST_NIGHT_8),
        "Clock Town Bomb Shop Item 1":
            lambda state: can_purchase(state, player, SHOP_ID_BOMB_SHOP_1),
        "Clock Town Bomb Shop Item 2":
            lambda state: can_purchase(state, player, SHOP_ID_BOMB_SHOP_2),
        "Clock Town Bomb Shop Item 3":
            lambda state: can_purchase(state, player, SHOP_ID_BOMB_SHOP_3),
        "Clock Town Bomb Shop Powder Keg Goron":
            lambda state: state.has("Goron Mask", player) and state.has("Powder Keg", player),
        "Clock Town Bomb Shop Item 3 (Stop Thief)":
            lambda state: state.can_reach("North Clock Town Save Old Lady", 'Location', player) and can_purchase(state, player, SHOP_ID_BOMB_SHOP_3_UPGRADE),
        "Curiosity Shop Blue Rupee Trade":
            lambda state: has_bottle(state, player) and (state.has("Mask of Scents", player) or can_get_cow_milk(state, player)),
        "Curiosity Shop Red Rupee Trade":
            lambda state: has_bottle(state, player),
        "Curiosity Shop Purple Rupee Trade":
            lambda state: has_bottle(state, player) and state.can_reach("Stone Tower Temple Inverted Death Armos Maze Chest", 'Location', player),
        "Curiosity Shop Gold Rupee Trade":
            lambda state: has_bottle(state, player) and ((state.can_reach("Graveyard Day 3 Dampe Big Poe Chest", 'Location', player) or (state.can_reach("Ikana Well Rightside Torch Chest", 'Location', player) and state.has("Progressive Bomb Bag", player))) or (state.has("Romani Mask", player) and can_afford_price(state, player, 200)) or state.can_reach("Goron Racetrack Prize", 'Location', player)),
        "Curiosity Shop Night 3 (Stop Thief)":
            lambda state: can_purchase(state, player, SHOP_ID_CURIOSITY_SHOP_MASK) and state.can_reach("North Clock Town Save Old Lady", 'Location', player),
        "Curiosity Shop Night 3 Thief Stolen Item":
            lambda state: can_purchase(state, player, SHOP_ID_CURIOSITY_SHOP_BOMB_BAG),
        "Laundry Pool Kafei's Request":
            lambda state: state.has("Letter to Kafei", player),
        "Laundry Pool Curiosity Shop Salesman #1":
            lambda state: state.has("Letter to Kafei", player),
        "Laundry Pool Curiosity Shop Salesman #2":
            lambda state: state.has("Letter to Kafei", player),
        "South Clock Town Moon's Tear Trade":
            lambda state: state.has("Moon's Tear", player),
        "South Clock Town Corner Chest":
            lambda state: state.has("Hookshot", player),
        "South Clock Town Final Day Tower Chest":
            lambda state: state.has("Hookshot", player) or (state.has("Deku Mask", player) and state.has("Moon's Tear", player)),
        "East Clock Town Couples Mask on Mayor":
            lambda state: state.has("Couple's Mask", player),
        "East Clock Town Shooting Gallery 40-49 Points":
            lambda state: state.has("Progressive Bow", player),
        "East Clock Town Shooting Gallery Perfect 50 Points":
            lambda state: state.has("Progressive Bow", player),
        "East Clock Town Honey and Darling Any Day":
            lambda state: state.has("Progressive Bow", player) or (state.has("Progressive Bomb Bag", player) or has_bombchus(state, player)) or (state.has("Deku Mask", player) and state.has("Progressive Magic", player)),
        "East Clock Town Honey and Darling All Days":
            lambda state: state.has("Progressive Bow", player) and state.has("Progressive Bomb Bag", player) and has_bombchus(state, player),
        "East Clock Town Treasure Game Chest (Human)":
            lambda state: True,
        "East Clock Town Treasure Game Chest (Deku)":
            lambda state: state.has("Deku Mask", player),
        "East Clock Town Treasure Game Chest (Goron)":
            lambda state: state.has("Goron Mask", player),
        "East Clock Town Treasure Game Chest (Zora)":
            lambda state: state.has("Zora Mask", player),
        "Bomber's Hideout Chest":
            lambda state: state.can_reach("Clock Town Hide-and-Seek", 'Location', player) and has_explosives(state, player),
        "Bomber's Hideout Astral Observatory":
            lambda state: has_projectiles(state, player),
        "North Clock Town Deku Playground Any Day":
            lambda state: state.has("Deku Mask", player),
        "North Clock Town Deku Playground All Days":
            lambda state: state.has("Deku Mask", player),
        "North Clock Town Save Old Lady":
            lambda state: state.has("Progressive Sword", player) or state.has("Great Fairy Sword", player) or state.has("Zora Mask", player) or state.has("Goron Mask", player),
        "North Clock Town Great Fairy Reward (Has Transformation Mask)":
            lambda state: (state.has("Stray Fairy (Clock Town)", player) and (state.has("Deku Mask", player) or state.has("Goron Mask", player) or state.has("Zora Mask", player))),
        "North Clock Town Great Fairy Reward":
            lambda state: state.has("Stray Fairy (Clock Town)", player),
        "Tingle Clock Town Map Purchase":
            lambda state: has_projectiles(state, player), # could also check for upper ikana, but you literally get this in clock town lmao
        "West Clock Town Swordsman Expert Course":
            lambda state: state.has("Progressive Sword", player),
        "West Clock Town Postman Counting":
            lambda state: state.has("Bunny Hood", player),
        "West Clock Town Dancing Sisters":
            lambda state: state.has("Kamaro Mask", player),
        "West Clock Town Bank 200 Rupees":
            lambda state: True,
        "West Clock Town Bank 500 Rupees":
            lambda state: state.has("Progressive Wallet", player),
        "West Clock Town Bank 1000 Rupees":
            lambda state: state.has("Progressive Wallet", player, 2),
        "West Clock Town Priority Mail to Postman":
            lambda state: state.has("Priority Mail", player),
        "Top of Clock Tower (Ocarina of Time)":
            lambda state: has_projectiles(state, player),
        "Top of Clock Tower (Song of Time)":
            lambda state: has_projectiles(state, player),
        "Stock Pot Inn Midnight Meeting":
            lambda state: (state.has("Kafei's Mask", player) and (state.has("Deku Mask", player) or state.has("Room Key", player))),
        "Stock Pot Inn Upstairs Middle Room Chest":
            lambda state: state.has("Room Key", player),
        "Stock Pot Inn Midnight Toilet Hand":
            lambda state: has_paper(state, player),
        "Stock Pot Inn Granny Story #1":
            lambda state: state.has("All-Night Mask", player),
        "Stock Pot Inn Granny Story #2":
            lambda state: state.has("All-Night Mask", player),
        "Stock Pot Inn Anju and Kafei":
            lambda state: (state.has("Kafei's Mask", player) and can_play_song("Epona's Song", state, player) and state.has("Letter to Kafei", player) and state.has("Pendant of Memories", player) and state.has("Hookshot", player) and (state.has("Garo Mask", player) or state.has("Gibdo Mask", player))),
        "Milk Bar Show":
            lambda state: state.has("Romani Mask", player) and state.has("Deku Mask", player) and state.has("Goron Mask", player) and state.has("Zora Mask", player) and state.has("Ocarina of Time", player),
        "Milk Bar Priority Mail to Aroma":
            lambda state: state.has("Romani Mask", player) and state.has("Kafei's Mask", player) and state.has("Priority Mail", player),
        "East Clock Town Milk Bar Milk Purchase":
            lambda state: state.has("Romani Mask", player) and can_afford_price(state, player, 40),
        "East Clock Town Milk Bar Chateau Romani Purchase":
            lambda state: state.has("Romani Mask", player) and can_afford_price(state, player, 200),

        "Termina Tall Grass Chest":
            lambda state: True,
        "Termina Tall Grass Grotto Chest":
            lambda state: True,
        "Termina Stump Chest":
            lambda state: state.has("Hookshot", player) or can_plant_beans(state, player),
        "Termina Underwater Chest":
            lambda state: state.has("Zora Mask", player),
        "Termina Peahat Grotto Chest":
            lambda state: True,
        "Termina Dodongo Grotto Chest":
            lambda state: True,
        "Termina Bio Baba Grotto HP":
            lambda state: (has_explosives(state, player) or state.has("Goron Mask", player)) and state.has("Zora Mask", player),
        "Termina Northern Midnight Dancer":
            lambda state: state.has("Ocarina of Time", player) and state.has("Song of Healing", player),
        "Termina Gossip Stones HP":
            lambda state: (has_explosives(state, player) or state.has("Goron Mask", player)) and ((state.has("Deku Mask", player) and can_play_song("Sonata of Awakening", state, player)) or (state.has("Goron Mask", player) and can_play_song("Goron Lullaby", state, player)) or (state.has("Zora Mask", player) and can_play_song("New Wave Bossa Nova", state, player))),
        "Termina Moon's Tear Scrub HP":
            lambda state: (state.can_reach("Bomber's Hideout Astral Observatory", 'Location', player) and state.has("Ocarina of Time", player) and can_afford_price(state, player, 100)) or (state.has("Deku Mask", player) and state.has("Ocarina of Time", player) and can_afford_price(state, player, 100)),
        "Termina Log Bombable Grotto Left Cow":
            lambda state: has_explosives(state, player) and can_play_song("Epona's Song", state, player),
        "Termina Log Bombable Grotto Right Cow":
            lambda state: has_explosives(state, player) and can_play_song("Epona's Song", state, player),
        "Milk Road Gorman Ranch Race":
            lambda state: state.has("Ocarina of Time", player) and state.has("Epona's Song", player),
        "Milk Road Gorman Ranch Purchase":
            lambda state: True,
        "Tingle Romani Ranch Map Purchase":
            lambda state: has_projectiles(state, player) or (state.can_reach("Milk Road", 'Region', player) or state.can_reach("Twin Islands", 'Region', player)),
        "Road to Swamp Tree HP":
            lambda state: has_projectiles(state, player),
        "Tingle Woodfall Map Purchase":
            lambda state: has_projectiles(state, player) or (state.can_reach("Southern Swamp", 'Region', player) or state.can_reach("Clock Town", 'Region', player)),
        "Swamp Shooting Gallery 2120 Points":
            lambda state: state.has("Progressive Bow", player),
        "Swamp Shooting Gallery 2180 Points":
            lambda state: state.has("Progressive Bow", player),


        "Southern Swamp Deku Scrub Purchase Beans":
            lambda state: (state.has("Deku Mask", player) and can_plant_beans(state, player)) or (state.has("Land Title Deed", player) and state.has("Moon's Tear", player) and can_plant_beans(state, player)),
        "Southern Swamp Deku Trade":
            lambda state: state.has("Land Title Deed", player),
        "Southern Swamp Deku Trade Freestanding HP":
            lambda state: state.has("Land Title Deed", player) and state.has("Deku Mask", player),
        "Southern Swamp Tour Witch Gift":
            lambda state: state.has("Bottle of Red Potion", player),
        "Southern Swamp Tour Guide Winning Picture":
            lambda state: state.has("Pictograph Box", player),
        "Southern Swamp Tour Guide Good Picture":
            lambda state: state.has("Pictograph Box", player),
        "Southern Swamp Tour Guide Okay Picture":
            lambda state: state.has("Pictograph Box", player),
        "Southern Swamp Near Swamp Spider House Grotto Chest":
            lambda state: state.has("Deku Mask", player),
        "Southern Swamp Song Tablet":
            lambda state: state.has("Deku Mask", player),
        "Southern Swamp Mystery Woods Day 2 Grotto Chest":
            lambda state: True,
        "Southern Swamp Witch Shop Item 1":
            lambda state: state.has("Mask of Scents", player) and has_bottle(state, player) and can_purchase(state, player, SHOP_ID_WITCH_POTION_1),
        "Southern Swamp Witch Shop Item 2":
            lambda state: can_purchase(state, player, SHOP_ID_WITCH_POTION_2),
        "Southern Swamp Witch Shop Item 3":
            lambda state: can_purchase(state, player, SHOP_ID_WITCH_POTION_3),


        "Swamp Spider House First Room Pot Near Entrance Token":
            lambda state: can_smack(state, player),
        "Swamp Spider House First Room Crawling In Water Token":
            lambda state: can_smack(state, player),
        "Swamp Spider House First Room Crawling Right Column Token":
            lambda state: can_smack(state, player),
        "Swamp Spider House First Room Crawling Left Column Token":
            lambda state: can_smack(state, player),
        "Swamp Spider House First Room Against Far Wall Token":
            lambda state: (can_bring_to_player(state, player) and has_projectiles(state, player)) or (state.has("Deku Mask", player) and state.has("Progressive Magic", player)) or (state.has("Deku Mask", player) and state.has("Progressive Bow", player)),
        "Swamp Spider House First Room Lower Left Bugpatch Token":
            lambda state: can_smack(state, player) and has_bottle(state, player),
        "Swamp Spider House First Room Lower Right Bugpatch Token":
            lambda state: can_smack(state, player) and has_bottle(state, player),
        "Swamp Spider House First Room Upper Right Bugpatch Token":
            lambda state: can_smack(state, player) and has_bottle(state, player),
        "Swamp Spider House Monument Room Left Crate Token":
            lambda state: can_smack(state, player),
        "Swamp Spider House Monument Room Right Crate Token":
            lambda state: can_smack(state, player),
        "Swamp Spider House Monument Room Crawling Wall Token":
            lambda state: can_bring_to_player(state, player) or (can_smack(state, player) and can_plant_beans(state, player) and (has_explosives(state, player) or state.has("Goron Mask", player))),
        "Swamp Spider House Monument Room Crawling On Monument Token":
            lambda state: can_smack(state, player) and can_bring_to_player(state, player) and has_projectiles(state, player),
        "Swamp Spider House Monument Room Behind Torch Token":
            lambda state: can_smack(state, player),
        "Swamp Spider House Pottery Room Beehive #1 Token":
            lambda state: can_smack(state, player) and has_projectiles(state, player),
        "Swamp Spider House Pottery Room Beehive #2 Token":
            lambda state: can_smack(state, player) and has_projectiles(state, player),
        "Swamp Spider House Pottery Room Small Pot Token":
            lambda state: can_smack(state, player),
        "Swamp Spider House Pottery Room Left Large Pot Token":
            lambda state: can_smack(state, player),
        "Swamp Spider House Pottery Room Right Large Pot Token":
            lambda state: can_smack(state, player),
        "Swamp Spider House Pottery Room Behind Vines Token":
            lambda state: state.has("Progressive Sword", player) or state.has("Great Fairy Sword", player) or state.has("Fierce Deity's Mask", player),
        "Swamp Spider House Pottery Room Upper Wall Token":
            lambda state: can_smack(state, player),
        "Swamp Spider House Golden Room Crawling Left Wall Token":
            lambda state: can_smack(state, player),
        "Swamp Spider House Golden Room Crawling Right Column Token":
            lambda state: can_smack(state, player),
        "Swamp Spider House Golden Room Against Far Wall Token":
            lambda state: can_smack(state, player) and (can_bring_to_player(state, player) or can_plant_beans(state, player)),
        "Swamp Spider House Golden Room Beehive Token":
            lambda state: can_smack(state, player) and has_projectiles(state, player),
        "Swamp Spider House Tree Room Tall Grass #1 Token":
            lambda state: can_smack(state, player),
        "Swamp Spider House Tree Room Tall Grass #2 Token":
            lambda state: can_smack(state, player),
        "Swamp Spider House Tree Room Tree #1 Token":
            lambda state: can_smack(state, player),
        "Swamp Spider House Tree Room Tree #2 Token":
            lambda state: can_smack(state, player),
        "Swamp Spider House Tree Room Tree #3 Token":
            lambda state: can_smack(state, player),
        "Swamp Spider House Tree Room Beehive Token":
            lambda state: can_smack(state, player) and has_projectiles(state, player),
        "Swamp Spider House Reward":
            lambda state: state.has("Swamp Skulltula Token", player, 30),


        "Deku Palace Bean Seller":
            lambda state: state.has("Deku Mask", player),
        "Deku Palace Bean Grotto Chest":
            lambda state: can_plant_beans(state, player) or state.has("Hookshot", player),
        "Deku Palace Monkey Song":
            lambda state: state.has("Ocarina of Time", player) and can_plant_beans(state, player) and state.has("Deku Mask", player),
        "Deku Palace Butler Race":
            lambda state: can_clear_woodfall(state, player) and has_bottle(state, player) and (state.has("Progressive Sword", player) or state.has("Great Fairy Sword", player) or state.has("Fierce Deity's Mask", player)),


        "Woodfall Great Fairy Reward":
            lambda state: state.has("Stray Fairy (Woodfall)", player, 15),
        "Woodfall Near Owl Statue Chest":
            lambda state: state.has("Deku Mask", player),
        "Woodfall After Great Fairy Cave Chest":
            lambda state: state.has("Deku Mask", player),
        "Woodfall Near Swamp Entrance Chest":
            lambda state: state.has("Deku Mask", player),


        "Woodfall Temple Dragonfly Chest":
            lambda state: state.has("Small Key (Woodfall)", player) or state.has("Progressive Bow", player),
        "Woodfall Temple Black Boe Room Chest":
            lambda state: state.has("Small Key (Woodfall)", player) or state.has("Progressive Bow", player),
        "Woodfall Temple Wooden Flower Switch Chest":
            lambda state: state.has("Progressive Bow", player),
        "Woodfall Temple Dinolfos Chest":
            lambda state: (state.has("Small Key (Woodfall)", player) and can_smack(state, player)) or state.has("Progressive Bow", player),
        "Woodfall Temple Boss Key Chest":
            lambda state: state.has("Progressive Bow", player) and can_smack(state, player),
        "Woodfall Temple Wooden Flower Bubble SF":
            lambda state: (state.has("Progressive Bow", player) and state.has("Great Fairy Mask", player)) or can_use_fire_arrows(state, player),
        "Woodfall Temple Moving Flower Platform Room Beehive SF":
            lambda state: (state.has("Progressive Bow", player) or (state.has("Deku Mask", player) and state.has("Progressive Magic", player))) or (state.has("Great Fairy Mask", player) and (state.has("Hookshot", player) or state.has("Zora Mask", player))),
        "Woodfall Temple Push Block Skulltula SF":
            lambda state: (state.has("Small Key (Woodfall)", player) and can_smack(state, player)) or state.has("Progressive Bow", player),
        "Woodfall Temple Push Block Bubble SF":
            lambda state: state.has("Great Fairy Mask", player) and ((state.has("Small Key (Woodfall)", player) and has_projectiles(state, player)) or state.has("Progressive Bow", player)),
        "Woodfall Temple Push Block Beehive SF":
            lambda state: state.has("Great Fairy Mask", player) and ((state.has("Small Key (Woodfall)", player) and has_projectiles(state, player)) or state.has("Progressive Bow", player)),
        "Woodfall Temple Final Room Right Lower Platform SF":
            lambda state: state.has("Progressive Bow", player) or can_use_fire_arrows(state, player),
        "Woodfall Temple Final Room Right Upper Platform SF":
            lambda state: state.has("Progressive Bow", player) or can_use_fire_arrows(state, player),
        "Woodfall Temple Final Room Left Upper Platform SF":
            lambda state: state.has("Progressive Bow", player) or can_use_fire_arrows(state, player),
        "Woodfall Temple Final Room Bubble SF":
            lambda state: state.has("Progressive Bow", player) or can_use_fire_arrows(state, player),
        "Woodfall Temple Heart Container":
            lambda state: can_smack(state, player) and state.has("Progressive Bow", player) and (state.has("Boss Key (Woodfall)", player) or (state.has("Odolwa's Remains", player) and options.remains_allow_boss_warps.value)),
        "Woodfall Temple Odolwa's Remains":
            lambda state: can_smack(state, player) and state.has("Progressive Bow", player) and (state.has("Boss Key (Woodfall)", player) or (state.has("Odolwa's Remains", player) and options.remains_allow_boss_warps.value)),
            
            
        "Tour Witch Target Shooting":
            lambda state: can_clear_woodfall(state, player) and has_bottle(state, player) and state.has("Progressive Bow", player),
            
            
        "Mountain Village Invisible Ladder Cave Healing Invisible Goron":
            lambda state: can_use_lens(state, player) and can_play_song("Song of Healing", state, player),
        "Mountain Village Feeding Freezing Goron":
            lambda state: state.has("Goron Mask", player) and state.has("Progressive Magic", player) and (can_play_song("Goron Lullaby", state, player) or can_use_fire_arrows(state, player)),
        "Mountain Village Spring Waterfall Chest":
            lambda state: can_clear_snowhead(state, player),
        "Mountain Village Spring Ramp Grotto":
            lambda state: can_clear_snowhead(state, player),
        "Don Gero Mask Frog Song HP":
            lambda state: state.has("Don Gero Mask", player) and can_clear_snowhead(state, player) and state.can_reach("Woodfall Temple Boss Key Chest", 'Location', player) and state.can_reach("Great Bay Temple", 'Region', player) and can_use_ice_arrows(state, player) and can_use_fire_arrows(state, player),
        "Mountain Village Smithy Upgrade":
            lambda state: can_afford_price(state, player, 100) and (can_use_fire_arrows(state, player) or state.can_reach("Twin Islands Hot Water Grotto Chest", 'Location', player) or can_clear_snowhead(state, player)),
        "Mountain Village Smithy Gold Dust Upgrade":
            # gold dust is not shuffled, so its received with "Goron Racetrack Prize"
            lambda state: state.can_reach("Mountain Village Smithy Upgrade", 'Location', player) and state.can_reach("Goron Racetrack Prize", 'Location', player) and has_bottle(state, player),
            
        "Tingle Snowhead Map Purchase":
            lambda state: has_projectiles(state, player) and (state.can_reach("Twin Islands", 'Region', player) or state.can_reach("Southern Swamp", 'Region', player)),
        "Twin Islands Ramp Grotto Chest":
            lambda state: has_explosives(state, player) and (state.has("Goron Mask", player) or state.has("Hookshot", player)),
        "Twin Islands Goron Elder Request":
            lambda state: state.has("Goron Mask", player) and (can_use_fire_arrows(state, player) or ((state.can_reach("Mountain Village Invisible Ladder Cave Healing Invisible Goron", 'Location', player) or (state.can_reach("Ikana Well Invisible Chest", 'Location', player) and can_play_song("Song of Soaring", state, player))) and has_bottle(state, player))),
        "Twin Islands Hot Water Grotto Chest":
            lambda state: (has_explosives(state, player) and can_use_fire_arrows(state, player)) or (state.can_reach("Mountain Village Invisible Ladder Cave Healing Invisible Goron", 'Location', player) and has_bottle(state, player) and state.has("Goron Mask", player) and has_explosives(state, player)) or (can_clear_snowhead(state, player) or (state.can_reach("Ikana Well Invisible Chest", 'Location', player) and can_play_song("Song of Soaring", state, player))),
        "Twin Islands Spring Underwater Cave Chest":
            lambda state: state.has("Zora Mask", player) and can_clear_snowhead(state, player),
        "Twin Islands Spring Underwater Near Ramp Chest":
            lambda state: state.has("Zora Mask", player) and can_clear_snowhead(state, player),
        "Goron Racetrack Prize":
            lambda state: (can_use_powder_keg(state, player) or state.can_reach("Powder Keg Goron Reward", 'Location', player)) and can_clear_snowhead(state, player),
            
            
        "Goron Village Lens Cave Rock Chest":
            lambda state: has_explosives(state, player),
        "Goron Village Lens Cave Invisible Chest":
            lambda state: True,
        "Goron Village Lens Cave Center Chest":
            lambda state: True,
        "Goron Village Deku Scrub Purchase Bomb Bag":
            lambda state: can_afford_price(state, player, 200) and (state.has("Goron Mask", player) or (state.can_reach("Goron Village Deku Trade Freestanding HP", 'Location', player) and state.can_reach("Southern Swamp Deku Trade Freestanding HP", 'Location', player) and state.has("Moon's Tear", player))),
        "Goron Village Deku Trade":
            lambda state: state.has("Deku Mask", player) and state.has("Swamp Title Deed", player),
        "Goron Village Deku Trade Freestanding HP":
            lambda state: state.can_reach("Goron Village Deku Trade", 'Location', player),
        "Powder Keg Goron Reward":
            lambda state: can_clear_snowhead(state, player) or (can_use_fire_arrows(state, player) and state.has("Goron Mask", player)),
        "Goron Village Baby Goron Lullaby":
            lambda state: state.has("Goron Mask", player) and can_play_song("Goron Lullaby", state, player),
        "Goron Village Shop Item 1":
            lambda state: state.has("Goron Mask", player) and can_purchase(state, player, SHOP_ID_GORON_SHOP_1),
        "Goron Village Shop Item 2":
            lambda state: state.has("Goron Mask", player) and can_purchase(state, player, SHOP_ID_GORON_SHOP_2),
        "Goron Village Shop Item 3":
            lambda state: state.has("Goron Mask", player) and can_purchase(state, player, SHOP_ID_GORON_SHOP_3),
        "Goron Village Shop (Spring) Item 1":
            lambda state: state.has("Goron Mask", player) and can_purchase(state, player, SHOP_ID_GORON_SHOP_SPRING_1) and can_clear_snowhead(state, player),
        "Goron Village Shop (Spring) Item 2":
            lambda state: state.has("Goron Mask", player) and can_purchase(state, player, SHOP_ID_GORON_SHOP_SPRING_2) and can_clear_snowhead(state, player),
        "Goron Village Shop (Spring) Item 3":
            lambda state: state.has("Goron Mask", player) and can_purchase(state, player, SHOP_ID_GORON_SHOP_SPRING_3) and can_clear_snowhead(state, player),
        "Goron Village Deku Trade Freestanding HP (Spring)":
            lambda state: can_clear_snowhead(state, player) and state.has("Deku Mask", player) and state.has("Swamp Title Deed", player),


        "Path to Snowhead Grotto Chest":
            lambda state: state.has("Goron Mask", player) and state.has("Progressive Magic", player) and has_explosives(state, player),
        "Path to Snowhead Scarecrow Pillar HP":
            lambda state: can_reach_scarecrow(state, player) and state.has("Goron Mask", player) and can_use_lens(state, player) and state.has("Hookshot", player),
            
            
        "Snowhead Great Fairy Reward":
            lambda state: state.has("Stray Fairy (Snowhead)", player, 15),
            
       # Snowhead has 3 small keys     
        "Snowhead Temple Initial Runway Under Platform Bubble SF":
            lambda state: state.has("Progressive Bow", player) and state.has("Great Fairy Mask", player),
        "Snowhead Temple Initial Runway Tower Bubble SF":
            lambda state: state.has("Progressive Bow", player) and state.has("Great Fairy Mask", player),
        "Snowhead Temple Grey Door Near Bombable Stairs Box SF":
            lambda state: (state.has("Small Key (Snowhead)", player) and state.has("Great Fairy Mask", player) and has_explosives(state, player)) or (state.has("Hookshot", player) and state.can_reach("Snowhead Temple Initial Runway Tower Bubble SF", 'Location', player) and has_explosives(state, player)),
        # "Snowhead Temple Timed Switch Room Bubble SF" needs 2 small keys following the 'vanilla path' \/
        "Snowhead Temple Timed Switch Room Bubble SF":
            lambda state: (state.has("Small Key (Snowhead)", player, 2) and state.has("Great Fairy Mask", player) and state.has("Progressive Bow", player) and can_use_lens(state, player) and has_explosives(state, player)) or (can_reach_scarecrow(state, player) and state.has("Hookshot", player) and state.has("Great Fairy Mask", player) and state.has("Progressive Bow", player) and can_use_lens(state, player)) or (can_use_fire_arrows(state, player) and state.has("Great Fairy's Mask", player) and can_use_lens(state, player)),
        # "Snowhead Temple Snowmen Bubble SF" needs 3 small keys following the 'vanilla' path' - this is the final small key too. \/
        "Snowhead Temple Snowmen Bubble SF":
            lambda state: state.has("Small Key (Snowhead)", player) and can_use_fire_arrows(state, player) and state.has("Great Fairy Mask", player),
        # Both Dinolfos checks require 3 small keys following vanilla path
        "Snowhead Temple Dinolfos Room First SF":
            lambda state: state.has("Small Key (Snowhead)", player) and can_use_fire_arrows(state, player),
        "Snowhead Temple Dinolfos Room Second SF":
            lambda state: state.has("Small Key (Snowhead)", player) and can_use_fire_arrows(state, player),
        "Snowhead Temple Initial Runway Ice Blowers Chest":
            lambda state: can_use_fire_arrows(state, player) or state.has("Hookshot", player),
        "Snowhead Temple Green Door Ice Blowers Chest":
            lambda state: can_use_fire_arrows(state, player),
        #  "Snowhead Temple Orange Door Upper Chest" only needs 1 small key
        "Snowhead Temple Orange Door Upper Chest":
            lambda state: state.has("Hookshot", player) or state.has("Small Key (Snowhead)", player) and can_use_fire_arrows(state, player),
        "Snowhead Temple Orange Door Behind Block Chest":
            lambda state: True,
        #  "Snowhead Temple Grey Door Center Chest" requires one key (either im colour blind or you are but that door is like, light blue)
        "Snowhead Temple Light Blue Door Center Chest":
            lambda state: state.has("Small Key (Snowhead)", player) or state.has("Hookshot", player),
        "Snowhead Temple Light Blue Door Upper Chest":
            lambda state: can_use_fire_arrows(state, player) and (state.has("Small Key (Snowhead)", player) or state.has("Hookshot", player)),
        "Snowhead Temple Upstairs 2F Icicle Room Hidden Chest":
            lambda state: can_use_lens(state, player) and has_explosives(state, player) and state.has("Progressive Bow", player) and (state.has("Small Key (Snowhead)", player) or state.has("Hookshot", player)),
        "Snowhead Temple Upstairs 2F Icicle Room Snowball Chest":
            lambda state: has_explosives(state, player) and (state.has("Small Key (Snowhead)", player) and state.has("Progressive Bow", player)) or state.has("Hookshot", player),
        "Snowhead Temple Elevator Room Invisible Platform Chest":
            lambda state: (can_use_lens(state, player) and state.has("Small Key (Snowhead)", player, 2) and has_explosives(state, player)) or (can_use_lens(state, player) and can_use_fire_arrows(state, player)) or (can_use_lens(state, player) and state.has("Hookshot", player)),
        "Snowhead Temple Elevator Room Lower Chest":
            lambda state: True,
        "Snowhead Temple 1st Wizzrobe Chest":
            lambda state: (state.has("Small Key (Snowhead)", player, 2) and has_explosives(state, player)) or can_use_fire_arrows(state, player),
        "Snowhead Temple Column Room 2F Hidden Chest":
            lambda state: (state.has("Small Key (Snowhead)", player, 3) and can_use_fire_arrows(state, player) and can_use_lens(state, player) and has_explosives(state, player) and state.has("Deku Mask", player)) or (can_use_fire_arrows(state, player) and can_reach_scarecrow(state, player) and state.has("Hookshot", player) and can_use_lens(state, player)),
        "Snowhead Temple 2nd Wizzrobe Chest":
            lambda state: (state.has("Small Key (Snowhead)", player, 3) and can_use_fire_arrows(state, player) and has_explosives(state, player)) or (state.has("Small Key (Snowhead)", player, 1) and can_use_fire_arrows(state, player) and state.has("Deku Mask", player)),
        "Snowhead Temple Heart Container":
            lambda state: can_use_fire_arrows(state, player) and ((state.has("Small Key (Snowhead)", player, 1) and state.has("Boss Key (Snowhead)", player)) or (state.has("Goht's Remains", player) and options.remains_allow_boss_warps.value)),
        "Snowhead Temple Goht's Remains":
            lambda state: can_use_fire_arrows(state, player) and ((state.has("Small Key (Snowhead)", player, 1) and state.has("Boss Key (Snowhead)", player)) or (state.has("Goht's Remains", player) and options.remains_allow_boss_warps.value)),


        "Romani Ranch Bremen Mask March Baby Cuccos":
            lambda state: state.has("Bremen Mask", player),
        "Romani Ranch Helping Cremia":
            lambda state: can_use_powder_keg(state, player) and state.has("Progressive Bow", player),
        "Romani Ranch Doggy Racetrack Rooftop Chest":
            lambda state: state.has("Hookshot", player) or can_plant_beans(state, player) or state.has("Zora Mask", player),
        "Romani Ranch Doggy Race":
            lambda state: state.has("Mask of Truth", player), # or state.has("Muervo Luck", player),
        "Romani Ranch Romani Game":
            lambda state: can_use_powder_keg(state, player) and state.has("Progressive Bow", player),
        "Romani Ranch Defended Against Aliens":
            lambda state: can_use_powder_keg(state, player) and state.has("Progressive Bow", player),
        "Romani Ranch Barn Free Cow":
            lambda state: can_use_powder_keg(state, player) and can_play_song("Epona's Song", state, player),
        "Romani Ranch Barn Stables Front Cow":
            lambda state: can_use_powder_keg(state, player) and can_play_song("Epona's Song", state, player),
        "Romani Ranch Barn Stables Back Cow":
            lambda state: can_use_powder_keg(state, player) and can_play_song("Epona's Song", state, player),


        "Great Bay Healing Zora":
            lambda state: can_play_song("Song of Healing", state, player),
        "Great Bay Scarecrow Ledge HP":
            lambda state: can_plant_beans(state, player) and can_reach_scarecrow(state, player) and state.has("Hookshot", player),
        "Tingle Great Bay Map Purchase":
            lambda state: has_projectiles(state, player) and (state.can_reach("Great Bay", 'Region', player) or state.can_reach("Milk Road", 'Region', player)),
        "Great Bay Ledge Grotto Left Cow":
            lambda state: state.has("Hookshot", player) and can_play_song("Epona's Song", state, player),
        "Great Bay Ledge Grotto Right Cow":
            lambda state: state.has("Hookshot", player) and can_play_song("Epona's Song", state, player),
        "Pinnacle Rock HP":
            lambda state: can_reach_seahorse(state, player) and has_bottle(state, player) and state.has("Zora Mask", player),
        "Pinnacle Rock Upper Eel Chest":
            lambda state: can_reach_seahorse(state, player) and has_bottle(state, player) and state.has("Zora Mask", player),
        "Pinnacle Rock Lower Eel Chest":
            lambda state: can_reach_seahorse(state, player) and has_bottle(state, player) and state.has("Zora Mask", player),
        # ~ maybe require 3 bottles for eggs
        "Great Bay Marine Research Lab Zora Egg Delivery Song":
            lambda state: can_reach_seahorse(state, player) and has_bottle(state, player, 3) and state.can_reach("Pirates' Fortress Leader's Room Chest", "Location", player),
        "Great Bay Marine Research Lab Feeding Fish":
            lambda state: has_bottle(state, player),
        "Great Bay (Cleared) Fisherman Island Game HP":
            lambda state: can_clear_greatbay(state, player),
        
            
        "Ocean Spider House Ramp Upper Token":
            lambda state: state.has("Hookshot", player),
        "Ocean Spider House Ramp Lower Token":
            lambda state: state.has("Hookshot", player),
        "Ocean Spider House Lobby Ceiling Token":
            lambda state: state.has("Hookshot", player) and can_use_fire_arrows(state, player),
        "Ocean Spider House First Room Rafter Token":
            lambda state: state.has("Hookshot", player),
        "Ocean Spider House First Room Open Pot #1 Token":
            lambda state: state.has("Hookshot", player),
        "Ocean Spider House First Room Open Pot #2 Token":
            lambda state: state.has("Hookshot", player) and can_use_fire_arrows(state, player),
        "Ocean Spider House First Room Wall Token":
            lambda state: state.has("Hookshot", player),
        "Ocean Spider House Library Top Bookcase Token":
            lambda state: state.has("Hookshot", player),
        "Ocean Spider House Library Passage Behind Bookcase Front Token":
            lambda state: state.has("Hookshot", player),
        "Ocean Spider House Library Passage Behind Bookcase Rear Token":
            lambda state: state.has("Hookshot", player),
        "Ocean Spider House Libary Painting #1 Token":
            lambda state: state.has("Hookshot", player),
        "Ocean Spider House Library Painting #2 Token":
            lambda state: state.has("Hookshot", player),
        "Ocean Spider House Library Rafter Token":
            lambda state: state.has("Hookshot", player),
        "Ocean Spider House Library Bookshelf Hole Token":
            lambda state: state.has("Hookshot", player),
        "Ocean Spider House First Room Downstairs Rafter Token":
            lambda state: state.has("Hookshot", player),
        "Ocean Spider House First Room Downstairs Open Pot Token":
            lambda state: state.has("Hookshot", player),
        "Ocean Spider House First Room Downstairs Behind Staircase Token":
            lambda state: state.has("Hookshot", player),
        "Ocean Spider House First Room Downstairs Crate Token":
            lambda state: state.has("Hookshot", player),
        "Ocean Spider House First Room Downstairs Wall Token":
            lambda state: state.has("Hookshot", player),
        "Ocean Spider House Dining Room Open Pot Token":
            lambda state: state.has("Hookshot", player),
        "Ocean Spider House Dining Room Painting Token":
            lambda state: state.has("Hookshot", player),
        "Ocean Spider House Dining Room Ceiling Token":
            lambda state: state.has("Hookshot", player),
        "Ocean Spider House Dining Room Chandelier #1 Token":
            lambda state: state.has("Hookshot", player),
        "Ocean Spider House Dining Room Chandelier #2 Token":
            lambda state: state.has("Hookshot", player),
        "Ocean Spider House Dining Room Chandelier #3 Token ":
            lambda state: state.has("Hookshot", player),
        "Ocean Spider House Storage Room Web Token":
            lambda state: state.has("Hookshot", player) and can_use_fire_arrows(state, player),
        "Ocean Spider House Storage Room North Wall Token":
            lambda state: state.has("Hookshot", player),
        "Ocean Spider House Storage Room Crate Token":
            lambda state: state.has("Hookshot", player),
        "Ocean Spider House Storage Room Hidden Hole Token":
            lambda state: state.has("Hookshot", player),
        "Ocean Spider House Storage Room Ceiling Pot Token":
            lambda state: state.has("Hookshot", player),
        "Ocean Spider House Coloured Mask Sequence HP":
            lambda state: state.has("Hookshot", player) and state.has("Captain's Hat", player) and state.has("Progressive Bow", player),
        "Ocean Spider House Reward":
            lambda state: state.has("Ocean Skulltula Token", player, 30),
        
        # I added these using the names in locations.py, might wanna double check they're functional since i'm a dummy - muervo.
        "Pirates' Fortress Exterior Underwater Log Chest":
            lambda state: state.has("Zora Mask", player),
        "Pirates' Fortress Exterior Underwater Near Entrance Chest":
            lambda state: state.has("Zora Mask", player),
        "Pirates' Fortress Exterior Underwater Corner Near Fortress Chest":
            lambda state: state.has("Zora Mask", player),
        
        "Pirates' Fortress Sewers Push Block Maze Chest":
            lambda state: state.has("Goron Mask", player),
        "Pirates' Fortress Sewers Cage HP":
            lambda state: state.has("Goron Mask", player),
        "Pirates' Fortress Sewers Underwater Upper Chest":
            lambda state: state.has("Goron Mask", player),
        "Pirates' Fortress Sewers Underwater Lower Chest":
            lambda state: state.has("Goron Mask", player),
        
        "Pirates' Fortress Hub Lower Chest":
            lambda state: True,
        "Pirates' Fortress Hub Upper Chest":
            lambda state: state.has("Hookshot", player),
        "Pirates' Fortress Leader's Room Chest":
            lambda state: (state.has("Hookshot", player) or state.has("Goron Mask", player)) and (state.has("Progressive Bow", player) or (state.has("Deku Mask", player) and state.has("Progressive Magic", player))),
        "Pirates' Fortress Near Egg Chest":
            lambda state: state.has("Hookshot", player) and can_smack_hard(state, player),
        "Pirates' Fortress Pirates Surrounding Chest":
            lambda state: state.has("Hookshot", player),
            
            
        "Zora Cape Near Great Fairy Grotto Chest":
            lambda state: state.has("Goron Mask", player) or has_explosives(state, player),
        "Zora Cape Underwater Chest":
            lambda state: state.has("Zora Mask", player),
        "Zora Cape Underwater Like-Like HP":
            lambda state: state.has("Zora Mask", player),
        "Zora Cape Pot Game Silver Rupee":
            lambda state: state.has("Zora Mask", player),
        "Zora Cape Upper Chest":
            lambda state: state.has("Hookshot", player),
        "Zora Cape Tree Chest":
            lambda state: state.has("Hookshot", player) and state.has("Deku Mask", player),
        # petition to rename this to 'pixel and muervo bottle reward
        "Beaver Bros. Race Bottle Reward":
            lambda state: state.has("Hookshot", player) and state.has("Zora Mask", player),
        # petition to rename this to 'pixel and muervo's love'
        "Beaver Bros. Race HP":
            lambda state: state.has("Hookshot", player) and state.has("Zora Mask", player),
            
            
        "Zora Hall Piano Zora Song":
            lambda state: state.has("Zora Mask", player),
        "Zora Hall Torches Reward":
            lambda state: state.has("Zora Mask", player) and can_use_fire_arrows(state, player),
        "Zora Hall Good Picture of Lulu":
           lambda state: state.has("Pictograph Box", player) and state.has("Zora Mask", player),
        "Zora Hall Bad Picture of Lulu":
           lambda state: state.has("Pictograph Box", player) and state.has("Zora Mask", player),
        "Zora Hall Deku Scrub Purchase Green Potion":
            lambda state: state.has("Zora Mask", player) and has_bottle(state, player),
        "Zora Hall Goron Scrub Trade":
            lambda state: state.has("Zora Mask", player) and state.has("Mountain Title Deed", player) and state.has("Goron Mask", player),
        "Zora Hall Goron Scrub Trade Freestanding HP":
            lambda state: state.has("Deku Mask", player) and state.can_reach("Zora Hall Goron Scrub Trade", 'Location', player),
        "Zora Hall Shop Item 1":
            lambda state: state.has("Zora Mask", player) and can_purchase(state, player, SHOP_ID_ZORA_SHOP_1),
        "Zora Hall Shop Item 2":
            lambda state: state.has("Zora Mask", player) and can_purchase(state, player, SHOP_ID_ZORA_SHOP_2),
        "Zora Hall Shop Item 3":
            lambda state: state.has("Zora Mask", player) and can_purchase(state, player, SHOP_ID_ZORA_SHOP_3),


        "Great Bay Great Fairy Reward":
            lambda state: state.has("Stray Fairy (Great Bay)", player, 15) and state.has("Hookshot", player),
            
            
        "Great Bay Temple Four Torches Chest":
            lambda state: True,
        "Great Bay Temple Waterwheel Room Skulltula SF":
            lambda state: can_smack_hard(state, player),
        "Great Bay Temple Waterwheel Room Bubble Under Platform SF":
            lambda state: state.has("Zora Mask", player) or (has_projectiles(state, player) and state.has("Great Fairy Mask", player)),
        "Great Bay Temple Blender Room Barrel SF":
            lambda state: True,
        "Great Bay Temple Pot At Bottom Of Blender SF":
            lambda state: True,
        "Great Bay Temple Red-Green Pipe First Room Chest":
            lambda state: can_use_ice_arrows(state, player),
        "Great Bay Temple Red-Green Pipe First Room Pot SF":
            lambda state: can_use_ice_arrows(state, player) or (has_projectiles(state, player) and state.has("Great Fairy Mask", player)) or state.has("Deku Mask", player),
        "Great Bay Temple Bio-Baba Hall Chest":
            lambda state: True,
        "Great Bay Temple Froggy Entrance Room Pot SF":
            lambda state: True,
        "Great Bay Temple Froggy Entrance Room Upper Chest":
            lambda state: True,
        "Great Bay Temple Froggy Entrance Room Caged Chest":
            lambda state: can_use_ice_arrows(state, player) and can_use_fire_arrows(state, player),
        "Great Bay Temple Froggy Entrance Room Underwater Chest":
            lambda state: True,
        "Great Bay Temple Behind Locked Door Chest":
            lambda state: (state.has("Small Key (Great Bay)", player) and can_smack_hard(state, player)) or (state.has("Small Key (Great Bay)", player) and has_explosives(state, player)) or (state.has("Small Key (Great Bay)", player) and state.has("Progressive Bow", player)),
        "Great Bay Temple Room Behind Waterfall Ceiling Chest":
            lambda state: can_use_ice_arrows(state, player),
        "Great Bay Temple Green Pipe Freezable Waterwheel Upper Chest":
            lambda state: can_use_ice_arrows(state, player) and can_use_fire_arrows(state, player),
        "Great Bay Temple Green Pipe Freezable Waterwheel Lower Chest":
            lambda state: can_use_ice_arrows(state, player) and can_use_fire_arrows(state, player),
        "Great Bay Temple Seesaw Room Underwater Barrel SF":
            lambda state: can_use_ice_arrows(state, player) and can_use_fire_arrows(state, player),
        "Great Bay Temple Seesaw Room Chest":
            lambda state: can_use_ice_arrows(state, player) and can_use_fire_arrows(state, player),
        "Great Bay Temple Before Boss Room Underneath Platform Bubble SF":
            lambda state: can_use_ice_arrows(state, player) and can_use_fire_arrows(state, player), # can just shoot ice arrows and stand on the platform
        "Great Bay Temple Before Boss Room Exit Tunnel Bubble SF":
            lambda state: state.can_reach("Great Bay Temple Before Boss Room Underneath Platform Bubble SF", 'Location', player),
        "Great Bay Temple Heart Container":
            lambda state: state.has("Hookshot", player) and ((state.can_reach("Great Bay Temple Before Boss Room Underneath Platform Bubble SF", 'Location', player) and state.has("Boss Key (Great Bay)", player)) or (state.has("Gyorg's Remains", player) and options.remains_allow_boss_warps.value)),
        "Great Bay Temple Gyorg's Remains":
            lambda state: state.has("Hookshot", player) and ((state.can_reach("Great Bay Temple Before Boss Room Underneath Platform Bubble SF", 'Location', player) and state.has("Boss Key (Great Bay)", player)) or (state.has("Gyorg's Remains", player) and options.remains_allow_boss_warps.value)),
        

        "Road to Ikana Pillar Chest":
            lambda state: state.has("Hookshot", player),
        "Road to Ikana Rock Grotto Chest":
            lambda state: state.has("Goron Mask", player),
        "Road to Ikana Invisible Soldier":
            lambda state: can_play_song("Epona's Song", state, player) and state.has("Bottle of Red Potion", player) and can_use_lens(state, player),
            
        
        "Ikana Graveyard Bombable Grotto Chest":
            lambda state: has_explosives(state, player),
        "Graveyard Day 1 Bats Chest":
            lambda state: state.has("Captain's Hat", player) and can_smack(state, player),
        "Graveyard Day 2 Dampe Bats":
            lambda state: has_projectiles(state, player), # has_explosives does work, but seems unintuitive
        "Graveyard Day 2 Iron Knuckle Chest":
            lambda state: state.has("Captain's Hat", player) and can_smack_hard(state, player) and has_explosives(state, player) and can_use_lens(state, player),
        "Graveyard Day 3 Dampe Big Poe Chest":
            lambda state: (state.has("Captain's Hat", player) and state.has("Progressive Bow", player)) or (state.has("Captain's Hat", player) and state.has("Zora Mask", player)),
        "Graveyard Sonata To Wake Sleeping Skeleton Chest":
            lambda state: can_play_song("Sonata of Awakening", state, player) and can_smack_hard(state, player),
        "Graveyard Day 1 Iron Knuckle Song":
            lambda state: state.has("Captain's Hat", player) and can_smack_hard(state, player),


        "Tingle Stone Tower Map Purchase":
            lambda state: has_projectiles(state, player) and ((state.can_reach("Ikana Canyon", 'Region', player) and can_use_ice_arrows(state, player) and state.has("Hookshot", player)) or state.can_reach("Great Bay", 'Region', player)),
        "Ikana Canyon Spirit House":
            lambda state: can_use_ice_arrows(state, player) and state.has("Hookshot", player),
        "Ikana Canyon Music Box Mummy":
            lambda state: can_use_ice_arrows(state, player) and can_play_song("Song of Healing", state, player) and can_play_song("Song of Storms", state, player),
        "Ikana Canyon Deku Scrub Purchase Blue Potion":
            lambda state: state.has("Zora Mask", player) and has_bottle(state, player) and can_afford_price(state, player, 100),
        "Ikana Canyon Zora Scrub Trade":
            lambda state: state.has("Zora Mask", player) and state.has("Ocean Title Deed", player),
        "Ikana Canyon Zora Trade Freestanding HP":
            lambda state: state.has("Deku Mask", player) and state.has("Zora Mask", player) and state.has("Ocean Title Deed", player),
        "Ikana Canyon Grotto Chest":
            lambda state: True,


        "Stone Tower Great Fairy Reward":
            lambda state: state.has("Stray Fairy (Stone Tower)", player, 15) and can_use_ice_arrows(state, player),
            
        
        "Secret Shrine Left Chest":
            lambda state: can_smack_hard(state, player) and can_use_light_arrows(state, player),
        "Secret Shrine Middle-Left Chest":
            lambda state: can_smack_hard(state, player) and can_use_light_arrows(state, player),
        "Secret Shrine Middle-Right Chest":
            lambda state: can_smack_hard(state, player) and can_use_light_arrows(state, player),
        "Secret Shrine Right Chest":
            lambda state: can_use_light_arrows(state, player) and can_smack_hard(state, player),
        "Secret Shrine Center Chest":
            lambda state: state.can_reach("Secret Shrine Left Chest", 'Location', player) and state.can_reach("Secret Shrine Middle-Left Chest", 'Location', player) and state.can_reach("Secret Shrine Middle-Right Chest", 'Location', player) and state.can_reach("Secret Shrine Right Chest", 'Location', player),
            
        # Recommend 2-3 bottles for Well in logic
        "Ikana Well Rightside Torch Chest":
            lambda state: state.has("Gibdo Mask", player) and has_bottle(state, player) and (can_plant_beans(state, player) or can_use_light_arrows(state, player)),
        "Ikana Well Invisible Chest":
            lambda state: state.has("Gibdo Mask", player) and has_bottle(state, player) and (can_afford_price(state, player, 100) or state.has("Mask of Scents", player)), # blue potion
        "Ikana Well Final Chest":
            lambda state: (state.has("Gibdo Mask", player) and has_bottle(state, player) and can_plant_beans(state, player) and (state.has("Progressive Bomb Bag", player) or (state.has("Captain's Hat", player) and state.has("Progressive Bow", player)))) or (can_use_light_arrows(state, player) and can_use_fire_arrows(state, player)),
        "Ikana Well Cow":
            lambda state: state.has("Gibdo Mask", player) and has_bottle(state, player) and (can_play_song("Epona's Song", state, player) and (can_plant_beans(state, player) or can_use_light_arrows(state, player)) and ((can_play_song("Song of Soaring", state, player) and ((state.can_reach("Twin Islands", 'Region', player) and can_use_fire_arrows(state, player)) or (state.can_reach("Mountain Village Invisible Ladder Cave Healing Invisible Goron", 'Location', player) and state.has("Goron Mask", player)))) or state.can_reach("Ikana Well Invisible Chest", 'Location', player))),
            
            
        "Ikana Castle Pillar Freestanding HP":
            lambda state: state.has("Deku Mask", player) and can_use_lens(state, player) and can_use_fire_arrows(state, player),
        "Ikana Castle King Song":
            lambda state: state.has("Deku Mask", player) and can_use_lens(state, player) and can_use_fire_arrows(state, player) and state.has("Powder Keg", player) and state.has("Goron Mask", player) and has_mirror_shield(state, player) or (can_use_fire_arrows(state, player) and has_mirror_shield(state, player) and can_use_light_arrows(state, player)),

        "Stone Tower Inverted Outside Left Chest":
            lambda state: can_plant_beans(state, player),
        "Stone Tower Inverted Outside Middle Chest":
            lambda state: can_plant_beans(state, player),
        "Stone Tower Inverted Outside Right Chest":
            lambda state: can_plant_beans(state, player),
        # Stone Tower region access rules require all 'heavy' transforms and hookshot, hence why they're removed from the rules.
        # Stone Tower has 4 keys total
        "Stone Tower Temple Entrance Room Eye Switch Chest":
            lambda state: state.has("Progressive Bow", player),
        "Stone Tower Temple Entrance Room Lower Chest":
            lambda state: state.has("Small Key (Stone Tower)", player, 4) and state.has("Deku Mask", player) and can_use_light_arrows(state, player),
        "Stone Tower Temple Armos Room Back Chest":
            lambda state: (has_explosives(state, player) and has_mirror_shield(state, player)) or can_use_light_arrows(state, player),
        "Stone Tower Temple Armos Room Upper Chest":
            lambda state: state.has("Hookshot", player),
        "Stone Tower Temple Armos Room Lava Chest":
            lambda state: (has_explosives(state, player) and has_mirror_shield(state, player)) or can_use_light_arrows(state, player),
        "Stone Tower Temple Eyegore Room Switch Chest":
            lambda state: can_use_light_arrows(state, player),
        # "Stone Tower Temple Eyegore Room Dexi Hand Ledge Chest" Vanilla route requires 1 small key
        "Stone Tower Temple Eyegore Room Dexi Hand Ledge Chest":
            lambda state: state.has("Small Key (Stone Tower)", player) or can_use_light_arrows(state, player),
        # "Stone Tower Temple Eastern Water Room Underwater Chest" involves inverting STT then uninverting in vanilla gameplay, the Ice arrows allow you to bypass this, original logic was a 'trick' method
        "Stone Tower Temple Eastern Water Room Underwater Chest":
            lambda state: can_use_light_arrows(state, player),
        # Vanilla route requires you to route left through STT and end in the water room, this applies to check above
        # could clean code up below here removing light arrow requirements and using the can_reach function to massively reduce length of lines.
        # Also following vanilla routing, all checks below here in Uninverted STT require a second key
        "Stone Tower Temple Eastern Water Room Sun Block Chest":
            lambda state: can_use_light_arrows(state, player) or (state.has("Small Key (Stone Tower)", player) and has_mirror_shield(state, player)),
        "Stone Tower Temple Mirror Room Sun Block Chest":
            lambda state: (state.has("Small Key (Stone Tower)", player, 2) and has_mirror_shield(state, player)) or (can_use_light_arrows(state, player) and state.has("Small Key (Stone Tower)", player, 1)),
        "Stone Tower Temple Mirror Room Sun Face Chest":
            lambda state: (state.has("Small Key (Stone Tower)", player, 2) and has_mirror_shield(state, player)) or (can_use_light_arrows(state, player) and state.has("Small Key (Stone Tower)", player, 1)),
        "Stone Tower Temple Air Gust Room Side Chest":
            lambda state: (state.has("Small Key (Stone Tower)", player, 2) and has_mirror_shield(state, player) and state.has("Deku Mask", player)) or (can_use_light_arrows(state, player) and state.has("Small Key (Stone Tower)", player, 1) and state.has("Deku Mask", player)),
        "Stone Tower Temple Air Gust Room Goron Switch Chest":
            lambda state: state.can_reach("Stone Tower Temple Mirror Room Sun Block Chest", 'Location', player) and state.has("Goron Mask", player),
        "Stone Tower Temple Garo Master Chest":
            lambda state: (state.has("Small Key (Stone Tower)", player, 2) and has_mirror_shield(state, player) and state.has("Deku Mask", player) and can_smack_hard(state, player)) or (can_use_light_arrows(state, player) and state.has("Small Key (Stone Tower)", player, 1) and can_smack_hard(state, player)),
        "Stone Tower Temple After Garo Upside Down Chest":
            lambda state: state.can_reach("Stone Tower Temple Inverted Eyegore Chest", 'Location', player),
        "Stone Tower Temple Eyegore Chest":
            lambda state: state.can_reach("Stone Tower Temple Garo Master Chest", 'Location', player),
        "Stone Tower Temple Inverted Entrance Room Sun Face Chest":
            lambda state: can_use_light_arrows(state, player),
        "Stone Tower Temple Inverted Eastern Air Gust Room Fire Chest":
            lambda state: state.has("Deku Mask", player) and can_use_light_arrows(state, player),
        "Stone Tower Temple Inverted Eastern Air Gust Room Ice Eye Switch Chest":
            lambda state: can_use_light_arrows(state, player) and state.has("Deku Mask", player) and can_use_fire_arrows(state, player),
        "Stone Tower Temple Inverted Eastern Air Gust Room Hall Floor Switch Chest":
            lambda state: can_use_light_arrows(state, player) and state.has("Deku Mask", player),
        # "Stone Tower Temple Inverted Wizzrobe Chest" This is where the third key would be getting used on its way to that check
        "Stone Tower Temple Inverted Wizzrobe Chest":
            lambda state: can_use_light_arrows(state, player) and state.has("Deku Mask", player) and state.has("Small Key (Stone Tower)", player, 3),
        "Stone Tower Temple Inverted Death Armos Maze Chest":
            lambda state:  state.can_reach("Stone Tower Temple Inverted Wizzrobe Chest", 'Location', player),
        "Stone Tower Temple Inverted Gomess Chest":
            lambda state: state.can_reach("Stone Tower Temple Inverted Wizzrobe Chest", 'Location', player) and can_use_light_arrows(state, player) and can_smack_hard(state, player),
        # "Stone Tower Temple Inverted Eyegore Chest" is where the fourth key would be getting used
        "Stone Tower Temple Inverted Eyegore Chest":
            lambda state: state.can_reach("Stone Tower Temple Inverted Wizzrobe Chest", 'Location', player) and state.has("Small Key (Stone Tower)", player, 4),
        "Stone Tower Temple Inverted Heart Container":
            lambda state: state.can_reach("Stone Tower Temple Inverted Eyegore Chest", 'Location', player) and (state.has("Progressive Bow", player) or state.has("Fierce Deity's Mask", player) or (state.has("Giant's Mask", player) and state.has("Progressive Magic", player) and state.has("Progressive Sword", player))) and (state.has("Boss Key (Stone Tower)", player) or (state.has("Twinmold's Remains", player) and options.remains_allow_boss_warps.value)),
        "Stone Tower Temple Inverted Twinmold's Remains":
            lambda state: state.can_reach("Stone Tower Temple Inverted Eyegore Chest", 'Location', player) and (state.has("Progressive Bow", player) or state.has("Fierce Deity's Mask", player) or (state.has("Giant's Mask", player) and state.has("Progressive Magic", player) and state.has("Progressive Sword", player))) and (state.has("Boss Key (Stone Tower)", player) or (state.has("Twinmold's Remains", player) and options.remains_allow_boss_warps.value)),

        "Oath to Order":
            lambda state: can_clear_woodfall(state, player) or can_clear_snowhead(state, player) or can_clear_greatbay(state, player) or can_clear_stonetower(state, player),

        "Moon Deku Trial HP":
            lambda state: state.has("Deku Mask", player),
        "Moon Goron Trial HP":
            lambda state: state.has("Goron Mask", player) and state.has("Progressive Magic", player),
        "Moon Zora Trial HP":
            lambda state: state.has("Zora Mask", player),
        "Moon Link Trial Garo Master Chest":
            lambda state: can_smack_hard(state, player) and state.has("Hookshot", player),
        "Moon Link Trial Iron Knuckle Lower Chest":
            lambda state: state.can_reach("Moon Link Trial Garo Master Chest", 'Location', player),
        "Moon Link Trial HP":
            lambda state: state.can_reach("Moon Link Trial Garo Master Chest", 'Location', player) and has_bombchus(state, player) and state.has("Progressive Bow", player),
        "Moon Trade All Masks":
            lambda state: state.can_reach("Moon Deku Trial HP", 'Location', player) and state.can_reach("Moon Goron Trial HP", 'Location', player) and state.can_reach("Moon Zora Trial HP", 'Location', player) and state.can_reach("Moon Link Trial HP", 'Location', player) and can_use_fire_arrows(state, player) and state.has("Captain's Hat", player) and state.has("Giant's Mask", player) and state.has("All-Night Mask", player) and state.has("Bunny Hood", player) and state.has("Keaton Mask", player) and state.has("Garo Mask", player) and state.has("Romani Mask", player) and state.has("Circus Leader's Mask", player) and state.has("Postman's Hat", player) and state.has("Couple's Mask", player) and state.has("Great Fairy Mask", player) and state.has("Gibdo Mask", player) and state.has("Don Gero Mask", player) and state.has("Kamaro Mask", player) and state.has("Mask of Truth", player) and state.has("Stone Mask", player) and state.has("Bremen Mask", player) and state.has("Blast Mask", player) and state.has("Mask of Scents", player) and state.has("Kafei's Mask", player),
        "Defeat Majora":
            lambda state: can_smack_hard(state, player) and (((state.has("Zora Mask", player) or has_mirror_shield(state, player)) and can_use_light_arrows(state, player)) or (state.has("Fierce Deity's Mask", player) and state.has("Progressive Magic", player))) and has_enough_remains(state, player, options.majora_remains_required.value),
    }
