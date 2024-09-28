from BaseClasses import CollectionState
from worlds.generic.Rules import add_rule

WORLDS = [
    "Dwarf Woodlands",
    "Castle of Dreams",
    "Enchanted Dominion",
    "The Mysterious Tower",
    "Radiant Garden",
    "Mirage Arena",
    "Olympus Coliseum",
    "Deep Space",
    "Realm of Darkness",
    "Never Land",
    "Disney Town"]

def can_glide(state, player):
    return state.has_any({
        "Glide",
        "Superglide",
        "Fire Glide"}, player)

def can_airslide(state, player):
    return state.has_any({
        "Air Slide",
        "Ice Slide"}, player)

def has_x_worlds(state, player, num_of_worlds):
    return state.has_from_list_unique(WORLDS, player, num_of_worlds)

def set_rules(khbbsworld):
    multiworld = khbbsworld.multiworld
    player     = khbbsworld.player
    options    = khbbsworld.options
    # Location Rules
    if options.character == 2:
        add_rule(khbbsworld.get_location("(T) The Land of Departure Defeat Eraqus Max HP Increase"),
            lambda state: (
                state.has_all({
                "Wayfinder Ventus",
                "Wayfinder Aqua",
                "Wayfinder Terra"}, player)
            ))
        add_rule(khbbsworld.get_location("(T) The Land of Departure Defeat Eraqus Chaos Ripper"),
            lambda state: (
                state.has_all({
                "Wayfinder Ventus",
                "Wayfinder Aqua",
                "Wayfinder Terra"}, player)
            ))
        add_rule(khbbsworld.get_location("(T) The Land of Departure Defeat Eraqus Xehanort's Report 8"),
            lambda state: (
                state.has_all({
                "Wayfinder Ventus",
                "Wayfinder Aqua",
                "Wayfinder Terra"}, player)
            ))
        add_rule(khbbsworld.get_location("(T) Dwarf Woodlands Vault Flame Salvo Chest"),
            lambda state: (
                state.has("High Jump", player)
                or can_airslide(state, player)
            ))
        add_rule(khbbsworld.get_location("(T) Castle of Dreams Passage Flying Balloon Sticker"),
            lambda state: state.has("High Jump", player))
        add_rule(khbbsworld.get_location("(T) Radiant Garden Fountain Court Dale Sticker"),
            lambda state: (
                state.has("High Jump", player)
                and can_airslide(state, player)
            ))
        add_rule(khbbsworld.get_location("(T) Radiant Garden Outer Gardens Airplane Sticker"),
            lambda state: state.has("High Jump", player))
        add_rule(khbbsworld.get_location("(T) Olympus Coliseum Coliseum Gates Balloon Sticker"),
            lambda state: state.has("High Jump", player))
        add_rule(khbbsworld.get_location("(T) Never Land Rainbow Falls: Base Rainbow Sticker"),
            lambda state: state.has("High Jump", player))
        add_rule(khbbsworld.get_location("(T) Never Land Cliff Path Mega-Potion Chest"),
            lambda state: can_airslide(state, player))
        add_rule(khbbsworld.get_location("(T) Never Land Skull Rock: Cavern Megalixir Chest"),
            lambda state: state.has("High Jump", player))
        add_rule(khbbsworld.get_location("(T) Never Land Skull Rock: Entrance Chip Sticker"),
            lambda state: (
                state.has("High Jump", player)
                and can_airslide(state, player)
            ))
        add_rule(khbbsworld.get_location("(T) Never Land Skull Rock: Cavern Ars Solum Chest"),
            lambda state: (
                state.has("High Jump", player)
                and can_airslide(state, player)
            ))
        add_rule(khbbsworld.get_location("(T) Never Land Skull Rock: Cavern Chaos Crystal Chest"),
            lambda state: (
                state.has("High Jump", player)
                and can_airslide(state, player)
            ))
        add_rule(khbbsworld.get_location("(T) Disney Town Pete's Rec Room Aerial Slam Chest"),
            lambda state: can_airslide(state, player))
        add_rule(khbbsworld.get_location("(T) Disney Town Pete's Rec Room Break Time Chest"),
            lambda state: can_airslide(state, player))
        add_rule(khbbsworld.get_location("(T) Disney Town Raceway Traffic Cone Sticker"),
            lambda state: (
                state.has("High Jump", player)
                and can_airslide(state, player)
            ))
        add_rule(khbbsworld.get_location("(T) The Keyblade Graveyard Twister Trench Traffic Cone Sticker"),
            lambda state: state.has("High Jump", player))
        if options.mirage_arena:
            if options.command_board:
                add_rule(khbbsworld.get_location("(T) Mirage Arena Win a Command Board game"),
                    lambda state: state.has_group_unique("Command Board", player, 1))
                add_rule(khbbsworld.get_location("(T) Mirage Arena Win 3 Command Board games"),
                    lambda state: state.has_group_unique("Command Board", player, 1))
                add_rule(khbbsworld.get_location("(T) Mirage Arena Win 5 Command Board games"),
                    lambda state: state.has_group_unique("Command Board", player, 1))
                add_rule(khbbsworld.get_location("(T) Mirage Arena Win 7 Command Board games"),
                    lambda state: state.has_group_unique("Command Board", player, 1))
            if options.super_bosses:
                add_rule(khbbsworld.get_location("(T) Mirage Arena Villains' Vendetta Ultima Weapon"),
                    lambda state: has_x_worlds(state, player, 10))
                add_rule(khbbsworld.get_location("(T) Mirage Arena Complete Villains' Vendetta"),
                    lambda state: has_x_worlds(state, player, 10))
                add_rule(khbbsworld.get_location("(T) Mirage Arena Light's Lessons Max HP Increase"),
                    lambda state: has_x_worlds(state, player, 10))
                add_rule(khbbsworld.get_location("(T) Mirage Arena Complete Light's Lessons"),
                    lambda state: has_x_worlds(state, player, 10))
                add_rule(khbbsworld.get_location("(T) Mirage Arena Peering into Darkness Royal Radiance"),
                    lambda state: has_x_worlds(state, player, 10))
                add_rule(khbbsworld.get_location("(T) Mirage Arena Complete Peering into Darkness"),
                    lambda state: has_x_worlds(state, player, 10))
            add_rule(khbbsworld.get_location("(T) Mirage Arena Complete Day of Reckoning"),
                lambda state: has_x_worlds(state, player, 2))
            add_rule(khbbsworld.get_location("(T) Mirage Arena Complete Wheels of Misfortune"),
                lambda state: has_x_worlds(state, player, 2))
            add_rule(khbbsworld.get_location("(T) Mirage Arena Complete Risky Riches"),
                lambda state: has_x_worlds(state, player, 2))
            add_rule(khbbsworld.get_location("(T) Mirage Arena Weaver Fever Max HP Increase"),
                lambda state: (
                    has_x_worlds(state, player, 4)
                    and state.has("Enchanted Dominion", player)
                ))
            add_rule(khbbsworld.get_location("(T) Mirage Arena Complete Weaver Fever"),
                lambda state: (
                    has_x_worlds(state, player, 4)
                    and state.has("Enchanted Dominion", player)
                ))
            add_rule(khbbsworld.get_location("(T) Mirage Arena Sinister Sentinel Xehanort's Report 5"),
                lambda state: has_x_worlds(state, player, 4))
            add_rule(khbbsworld.get_location("(T) Mirage Arena Complete Sinister Sentinel"),
                lambda state: has_x_worlds(state, player, 4))
            add_rule(khbbsworld.get_location("(T) Mirage Arena Dead Ringer Darkgnaw"),
                lambda state: has_x_worlds(state, player, 4))
            add_rule(khbbsworld.get_location("(T) Mirage Arena Complete Dead Ringer"),
                lambda state: has_x_worlds(state, player, 4))
            add_rule(khbbsworld.get_location("(T) Mirage Arena Complete Combined Threat"),
                lambda state: (
                    has_x_worlds(state, player, 6)
                    and state.has("Radiant Garden", player)
                ))
            add_rule(khbbsworld.get_location("(T) Mirage Arena Complete Treasure Tussle"),
                lambda state: has_x_worlds(state, player, 6))
            add_rule(khbbsworld.get_location("(T) Mirage Arena Complete Harsh Punishment"),
                lambda state: has_x_worlds(state, player, 6))
            add_rule(khbbsworld.get_location("(T) Mirage Arena Complete A Time to Chill"),
                lambda state: (
                    has_x_worlds(state, player, 8)
                    and state.has("Olympus Coliseum", player)
                ))
            add_rule(khbbsworld.get_location("(T) Mirage Arena Copycat Crisis Max HP Increase"),
                lambda state: has_x_worlds(state, player, 8))
            add_rule(khbbsworld.get_location("(T) Mirage Arena Complete Copycat Crisis"),
                lambda state: has_x_worlds(state, player, 8))
            add_rule(khbbsworld.get_location("(T) Mirage Arena Keepers of the Arena Ultima Cannon"),
                lambda state: has_x_worlds(state, player, 8))
            add_rule(khbbsworld.get_location("(T) Mirage Arena Complete Keepers of the Arena"),
                lambda state: has_x_worlds(state, player, 8))
            add_rule(khbbsworld.get_location("(T) Mirage Arena Monster of the Sea Mini"),
                lambda state: (
                    has_x_worlds(state, player, 8)
                    and state.has("Disney Town", player)
                ))
            add_rule(khbbsworld.get_location("(T) Mirage Arena Complete Monster of the Sea"),
                lambda state: (
                    has_x_worlds(state, player, 8)
                    and state.has("Disney Town", player)
                ))
            add_rule(khbbsworld.get_location("(T) Mirage Arena Country Chase: Finish 5 laps in 2:30"),
                lambda state: state.has("Disney Town", player))
            add_rule(khbbsworld.get_location("(T) Mirage Arena Disney Drive: Finish 5 laps in 5 minutes"),
                lambda state: state.has("Disney Town", player))
            add_rule(khbbsworld.get_location("(T) Mirage Arena Grand Spree: Finish 5 laps in 5 minutes"),
                lambda state: state.has("Disney Town", player))
            add_rule(khbbsworld.get_location("(T) Mirage Arena Castle Circuit: Finish 5 laps in 5:30"),
                lambda state: state.has("Disney Town", player))
        if options.super_bosses:
            add_rule(khbbsworld.get_location("(T) The Land of Departure Defeat Unknown No Name"),
                lambda state: has_x_worlds(state, player, 10))
            add_rule(khbbsworld.get_location("(T) The Keyblade Graveyard Defeat Vanitas Remnant Void Gear"),
                lambda state: has_x_worlds(state, player, 10))
    if options.character == 1:
        add_rule(khbbsworld.get_location("(A) The Land of Departure World Sealed Brightcrest"),
            lambda state: (
                state.has_all({
                    "Wayfinder Ventus",
                    "Wayfinder Aqua",
                    "Wayfinder Terra"}, player)
            ))
        add_rule(khbbsworld.get_location("(A) Dwarf Woodlands Vault Magnet Chest"),
            lambda state: (
                state.has_any({
                "High Jump",
                "Doubleflight"}, player)
            ))
        add_rule(khbbsworld.get_location("(A) Dwarf Woodlands Vault Bubble Sticker"),
            lambda state: (
                state.has_any({
                "High Jump",
                "Doubleflight"}, player)
            ))
        add_rule(khbbsworld.get_location("(A) Enchanted Dominion Dungeon Horace Sticker"),
            lambda state: (
                state.has_any({
                "High Jump",
                "Doubleflight"}, player)
            ))
        add_rule(khbbsworld.get_location("(A) Radiant Garden Front Doors Juice Sticker"),
            lambda state: (
                state.has_any({
                "High Jump",
                "Doubleflight"}, player)
            ))
        add_rule(khbbsworld.get_location("(A) Radiant Garden Aqueduct Donut Sticker"),
            lambda state: (
                state.has_any({
                "High Jump",
                "Doubleflight"}, player)
            ))
        add_rule(khbbsworld.get_location("(A) Radiant Garden Defeat Final Terra-Xehanort II"),
            lambda state: (
                state.has_all({
                    "Wayfinder Ventus",
                    "Wayfinder Aqua",
                    "Wayfinder Terra"}, player)
            ))
        add_rule(khbbsworld.get_location("(A) Olympus Coliseum Coliseum Gates Fireworks Sticker"),
            lambda state: (
                state.has_any({
                    "High Jump",
                    "Doubleflight"}, player)
                or can_airslide(state, player)
            ))
        add_rule(khbbsworld.get_location("(A) Never Land Mermaid Lagoon Rainbow Sticker"),
            lambda state: can_airslide(state, player))
        add_rule(khbbsworld.get_location("(A) Never Land Jungle Clearing Fireworks Sticker"),
            lambda state: state.has("Doubleflight", player))
        add_rule(khbbsworld.get_location("(A) Disney Town Raceway Daisy Sticker"),
            lambda state: can_airslide(state, player))
        add_rule(khbbsworld.get_location("(A) Disney Town Main Plaza Minnie Sticker"),
            lambda state: (
                state.has_all({
                    "High Jump",
                    "Doubleflight"}, player)
            ))
        add_rule(khbbsworld.get_location("(A) The Keyblade Graveyard Seat of War Flower Sticker"),
            lambda state: state.has("Doubleflight", player))
        add_rule(khbbsworld.get_location("(A) The Keyblade Graveyard Fissure Bubble Sticker"),
            lambda state: (
                state.has_all({
                    "High Jump",
                    "Doubleflight"}, player)
            ))
        if options.mirage_arena:
            if options.command_board:
                add_rule(khbbsworld.get_location("(A) Mirage Arena Win a Command Board game"),
                    lambda state: state.has_group_unique("Command Board", player, 1))
                add_rule(khbbsworld.get_location("(A) Mirage Arena Win 3 Command Board games"),
                    lambda state: state.has_group_unique("Command Board", player, 1))
                add_rule(khbbsworld.get_location("(A) Mirage Arena Win 5 Command Board games"),
                    lambda state: state.has_group_unique("Command Board", player, 1))
                add_rule(khbbsworld.get_location("(A) Mirage Arena Win 7 Command Board games"),
                    lambda state: state.has_group_unique("Command Board", player, 1))
            if options.super_bosses:
                add_rule(khbbsworld.get_location("(A) Mirage Arena Villains' Vendetta Ultima Weapon"),
                    lambda state: has_x_worlds(state, player, 10))
                add_rule(khbbsworld.get_location("(A) Mirage Arena Complete Villains' Vendetta"),
                    lambda state: has_x_worlds(state, player, 10))
                add_rule(khbbsworld.get_location("(A) Mirage Arena Light's Lessons Max HP Increase"),
                    lambda state: has_x_worlds(state, player, 10))
                add_rule(khbbsworld.get_location("(A) Mirage Arena Complete Light's Lessons"),
                    lambda state: has_x_worlds(state, player, 10))
                add_rule(khbbsworld.get_location("(A) Mirage Arena Peering into Darkness Royal Radiance"),
                    lambda state: has_x_worlds(state, player, 10))
                add_rule(khbbsworld.get_location("(A) Mirage Arena Complete Peering into Darkness"),
                    lambda state: has_x_worlds(state, player, 10))
            add_rule(khbbsworld.get_location("(A) Mirage Arena Complete Day of Reckoning"),
                lambda state: has_x_worlds(state, player, 2))
            add_rule(khbbsworld.get_location("(A) Mirage Arena Wheels of Misfortune Max HP Increase"),
                lambda state: has_x_worlds(state, player, 2))
            add_rule(khbbsworld.get_location("(A) Mirage Arena Complete Wheels of Misfortune"),
                lambda state: has_x_worlds(state, player, 2))
            add_rule(khbbsworld.get_location("(A) Mirage Arena Complete Risky Riches"),
                lambda state: has_x_worlds(state, player, 2))
            add_rule(khbbsworld.get_location("(A) Mirage Arena Complete Weaver Fever"),
                lambda state: (
                    has_x_worlds(state, player, 4)
                    and state.has("Enchanted Dominion", player)
                ))
            add_rule(khbbsworld.get_location("(A) Mirage Arena Complete Sinister Sentinel"),
                lambda state: has_x_worlds(state, player, 4))
            add_rule(khbbsworld.get_location("(A) Mirage Arena Complete Dead Ringer"),
                lambda state: has_x_worlds(state, player, 4))
            add_rule(khbbsworld.get_location("(A) Mirage Arena Combined Threat Sky Climber"),
                lambda state: (
                    has_x_worlds(state, player, 6)
                    and state.has("Radiant Garden", player)
                ))
            add_rule(khbbsworld.get_location("(A) Mirage Arena Complete Combined Threat"),
                lambda state: (
                    has_x_worlds(state, player, 6)
                    and state.has("Radiant Garden", player)
                ))
            add_rule(khbbsworld.get_location("(A) Mirage Arena Complete Treasure Tussle"),
                lambda state: has_x_worlds(state, player, 6))
            add_rule(khbbsworld.get_location("(A) Mirage Arena Complete Harsh Punishment"),
                lambda state: has_x_worlds(state, player, 6))
            add_rule(khbbsworld.get_location("(A) Mirage Arena A Time to Chill Max HP Increase"),
                lambda state: (
                    has_x_worlds(state, player, 8)
                    and state.has("Olympus Coliseum", player)
                ))
            add_rule(khbbsworld.get_location("(A) Mirage Arena Complete A Time to Chill"),
                lambda state: (
                    has_x_worlds(state, player, 8)
                    and state.has("Olympus Coliseum", player)
                ))
            add_rule(khbbsworld.get_location("(A) Mirage Arena Complete Copycat Crisis"),
                lambda state: has_x_worlds(state, player, 8))
            add_rule(khbbsworld.get_location("(A) Mirage Arena Keepers of the Arena Lightbloom"),
                lambda state: has_x_worlds(state, player, 8))
            add_rule(khbbsworld.get_location("(A) Mirage Arena Complete Keepers of the Arena"),
                lambda state: has_x_worlds(state, player, 8))
            add_rule(khbbsworld.get_location("(A) Mirage Arena Monster of the Sea Mini"),
                lambda state: (
                    has_x_worlds(state, player, 8)
                    and state.has("Disney Town", player)
                ))
            add_rule(khbbsworld.get_location("(A) Mirage Arena Complete Monster of the Sea"),
                lambda state: (
                    has_x_worlds(state, player, 8)
                    and state.has("Disney Town", player)
                ))
            add_rule(khbbsworld.get_location("(A) Mirage Arena Country Chase: Finish 5 laps in 2:30"),
                lambda state: state.has("Disney Town", player))
            add_rule(khbbsworld.get_location("(A) Mirage Arena Disney Drive: Finish 5 laps in 5 minutes"),
                lambda state: state.has("Disney Town", player))
            add_rule(khbbsworld.get_location("(A) Mirage Arena Grand Spree: Finish 5 laps in 5 minutes"),
                lambda state: state.has("Disney Town", player))
            add_rule(khbbsworld.get_location("(A) Mirage Arena Castle Circuit: Finish 5 laps in 5:30"),
                lambda state: state.has("Disney Town", player))
        if options.super_bosses:
            add_rule(khbbsworld.get_location("(A) The Land of Departure Defeat Unknown No Name"),
                lambda state: has_x_worlds(state, player, 10))
            add_rule(khbbsworld.get_location("(A) The Keyblade Graveyard Defeat Vanitas Remnant Void Gear"),
                lambda state: has_x_worlds(state, player, 10))
    if options.character == 0:
        add_rule(khbbsworld.get_location("(V) Enchanted Dominion Audience Chamber Dewey Sticker"),
            lambda state: (
                state.has("High Jump", player)
                and can_glide(state, player)
            ))
        add_rule(khbbsworld.get_location("(V) Radiant Garden Front Doors Fireworks Sticker"),
            lambda state: state.has("High Jump", player))
        add_rule(khbbsworld.get_location("(V) Never Land Rainbow Falls: Base Rainbow Sticker"),
            lambda state: (
                state.has("High Jump", player)
                and can_glide(state, player)
            ))
        add_rule(khbbsworld.get_location("(V) Disney Town Raceway Superglide Chest"),
            lambda state: can_glide(state, player))
        add_rule(khbbsworld.get_location("(V) The Keyblade Graveyard Seat of War Ice Cream Sticker"),
            lambda state: state.has("High Jump", player))
        if options.mirage_arena:
            if options.command_board:
                add_rule(khbbsworld.get_location("(V) Mirage Arena Win a Command Board game"),
                    lambda state: state.has_group_unique("Command Board", player, 1))
                add_rule(khbbsworld.get_location("(V) Mirage Arena Win 3 Command Board games"),
                    lambda state: state.has_group_unique("Command Board", player, 1))
                add_rule(khbbsworld.get_location("(V) Mirage Arena Win 5 Command Board games"),
                    lambda state: state.has_group_unique("Command Board", player, 1))
                add_rule(khbbsworld.get_location("(V) Mirage Arena Win 7 Command Board games"),
                    lambda state: state.has_group_unique("Command Board", player, 1))
            if options.super_bosses:
                add_rule(khbbsworld.get_location("(V) Mirage Arena Villains' Vendetta Ultima Weapon"),
                    lambda state: has_x_worlds(state, player, 10))
                add_rule(khbbsworld.get_location("(V) Mirage Arena Complete Villains' Vendetta"),
                    lambda state: has_x_worlds(state, player, 10))
                add_rule(khbbsworld.get_location("(V) Mirage Arena Light's Lessons Max HP Increase"),
                    lambda state: has_x_worlds(state, player, 10))
                add_rule(khbbsworld.get_location("(V) Mirage Arena Complete Light's Lessons"),
                    lambda state: has_x_worlds(state, player, 10))
                add_rule(khbbsworld.get_location("(V) Mirage Arena Peering into Darkness Royal Radiance"),
                    lambda state: has_x_worlds(state, player, 10))
                add_rule(khbbsworld.get_location("(V) Mirage Arena Complete Peering into Darkness"),
                    lambda state: has_x_worlds(state, player, 10))
            add_rule(khbbsworld.get_location("(V) Mirage Arena Complete Day of Reckoning"),
                lambda state: has_x_worlds(state, player, 2))
            add_rule(khbbsworld.get_location("(V) Mirage Arena Complete Wheels of Misfortune"),
                lambda state: has_x_worlds(state, player, 2))
            add_rule(khbbsworld.get_location("(V) Mirage Arena Complete Risky Riches"),
                lambda state: has_x_worlds(state, player, 2))
            add_rule(khbbsworld.get_location("(V) Mirage Arena Complete Weaver Fever"),
                lambda state: (
                    has_x_worlds(state, player, 4)
                    and state.has("Enchanted Dominion", player)
                ))
            add_rule(khbbsworld.get_location("(V) Mirage Arena Sinister Sentinel Sky Climber"),
                lambda state: has_x_worlds(state, player, 4))
            add_rule(khbbsworld.get_location("(V) Mirage Arena Complete Sinister Sentinel"),
                lambda state: has_x_worlds(state, player, 4))
            add_rule(khbbsworld.get_location("(V) Mirage Arena Dead Ringer Max HP Increase"),
                lambda state: has_x_worlds(state, player, 4))
            add_rule(khbbsworld.get_location("(V) Mirage Arena Complete Dead Ringer"),
                lambda state: has_x_worlds(state, player, 4))
            add_rule(khbbsworld.get_location("(V) Mirage Arena Complete Combined Threat"),
                lambda state: (
                    has_x_worlds(state, player, 6)
                    and state.has("Radiant Garden", player)
                ))
            add_rule(khbbsworld.get_location("(V) Mirage Arena Complete Treasure Tussle"),
                lambda state: has_x_worlds(state, player, 6))
            add_rule(khbbsworld.get_location("(V) Mirage Arena Complete Harsh Punishment"),
                lambda state: has_x_worlds(state, player, 6))
            add_rule(khbbsworld.get_location("(V) Mirage Arena A Time to Chill Max HP Increase"),
                lambda state: (
                    has_x_worlds(state, player, 8)
                    and state.has("Olympus Coliseum", player)
                ))
            add_rule(khbbsworld.get_location("(V) Mirage Arena Complete A Time to Chill"),
                lambda state: (
                    has_x_worlds(state, player, 8)
                    and state.has("Olympus Coliseum", player)
                ))
            add_rule(khbbsworld.get_location("(V) Mirage Arena Complete Copycat Crisis"),
                lambda state: has_x_worlds(state, player, 8))
            add_rule(khbbsworld.get_location("(V) Mirage Arena Keepers of the Arena Multivortex"),
                lambda state: has_x_worlds(state, player, 8))
            add_rule(khbbsworld.get_location("(V) Mirage Arena Complete Keepers of the Arena"),
                lambda state: has_x_worlds(state, player, 8))
            add_rule(khbbsworld.get_location("(V) Mirage Arena Monster of the Sea Mini"),
                lambda state: (
                    has_x_worlds(state, player, 8)
                    and state.has("Disney Town", player)
                ))
            add_rule(khbbsworld.get_location("(V) Mirage Arena Complete Monster of the Sea"),
                lambda state: (
                    has_x_worlds(state, player, 8)
                    and state.has("Disney Town", player)
                ))
            add_rule(khbbsworld.get_location("(V) Mirage Arena Country Chase: Finish 5 laps in 2:30"),
                lambda state: state.has("Disney Town", player))
            add_rule(khbbsworld.get_location("(V) Mirage Arena Disney Drive: Finish 5 laps in 5 minutes"),
                lambda state: state.has("Disney Town", player))
            add_rule(khbbsworld.get_location("(V) Mirage Arena Grand Spree: Finish 5 laps in 5 minutes"),
                lambda state: state.has("Disney Town", player))
            add_rule(khbbsworld.get_location("(V) Mirage Arena Castle Circuit: Finish 5 laps in 5:30"),
                lambda state: state.has("Disney Town", player))
        if options.super_bosses:
            add_rule(khbbsworld.get_location("(V) The Land of Departure Defeat Unknown No Name"),
                lambda state: has_x_worlds(state, player, 10))
            add_rule(khbbsworld.get_location("(V) The Keyblade Graveyard Defeat Vanitas Remnant Void Gear"),
                lambda state: has_x_worlds(state, player, 10))
        
    
    # Region rules.
    add_rule(khbbsworld.get_entrance("Dwarf Woodlands"),
        lambda state: state.has("Dwarf Woodlands", player))
    add_rule(khbbsworld.get_entrance("Castle of Dreams"),
        lambda state: state.has("Castle of Dreams", player))
    add_rule(khbbsworld.get_entrance("Enchanted Dominion"),
        lambda state: state.has("Enchanted Dominion", player))
    add_rule(khbbsworld.get_entrance("The Mysterious Tower"),
        lambda state: state.has("The Mysterious Tower", player))
    add_rule(khbbsworld.get_entrance("Radiant Garden"),
        lambda state: state.has("Radiant Garden", player))
    add_rule(khbbsworld.get_entrance("Olympus Coliseum"),
        lambda state: state.has("Olympus Coliseum", player))
    add_rule(khbbsworld.get_entrance("Deep Space"),
        lambda state: state.has("Deep Space", player))
   #add_rule(khbbsworld.get_entrance("Destiny Islands"),
   #     lambda state: state.has("Destiny Islands", player))
    add_rule(khbbsworld.get_entrance("Never Land"),
        lambda state: state.has("Never Land", player))
    add_rule(khbbsworld.get_entrance("Disney Town"),
        lambda state: state.has("Disney Town", player))
    add_rule(khbbsworld.get_entrance("Mirage Arena"),
        lambda state: state.has("Mirage Arena", player))
    add_rule(khbbsworld.get_entrance("The Keyblade Graveyard"),
        lambda state: (
            state.has_all({
                "Wayfinder Ventus",
                "Wayfinder Aqua",
                "Wayfinder Terra"}, player)
        ))
    add_rule(khbbsworld.get_entrance("Realm of Darkness"),
        lambda state: (
            state.has_all({
                "Wayfinder Ventus",
                "Wayfinder Aqua",
                "Wayfinder Terra",
                "Realm of Darkness"}, player)
            or
            (
                state.has("Realm of Darkness", player)
                and options.realm_of_darkness_early
            )
        ))

    # Win condition.
    multiworld.completion_condition[player] = lambda state: state.has("Victory", player)
    