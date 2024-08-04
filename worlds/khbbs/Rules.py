from BaseClasses import CollectionState, MultiWorld

def can_glide(state, player):
    return state.has("Glide", player) or state.has("Superglide", player) or state.has("Fire Glide", player)

def can_airslide(state, player):
    return state.has("Air Slide", player) or state.has("Ice Slide", player)

def set_rules(khbbsworld):
    multiworld = khbbsworld.multiworld
    player     = khbbsworld.player
    options    = khbbsworld.options
    # Location Rules
    if options.character == 2:
        multiworld.get_location("(T) The Land of Departure Defeat Eraqus Max HP Increase"       , player).access_rule = lambda state: state.has_all({"Wayfinder Ventus", "Wayfinder Aqua", "Wayfinder Terra"}, player)
        multiworld.get_location("(T) The Land of Departure Defeat Eraqus Chaos Ripper"          , player).access_rule = lambda state: state.has_all({"Wayfinder Ventus", "Wayfinder Aqua", "Wayfinder Terra"}, player)
        multiworld.get_location("(T) The Land of Departure Defeat Eraqus Xehanort's Report 8"   , player).access_rule = lambda state: state.has_all({"Wayfinder Ventus", "Wayfinder Aqua", "Wayfinder Terra"}, player)
       #multiworld.get_location("(T) The Land of Departure Defeat Unknown No Name"              , player).access_rule = lambda state: state.has_all({"Wayfinder Ventus", "Wayfinder Aqua", "Wayfinder Terra"}, player)
        multiworld.get_location("(T) Dwarf Woodlands Vault Flame Salvo Chest"                   , player).access_rule = lambda state: state.has("High Jump", player) or can_airslide(state, player)
        multiworld.get_location("(T) Castle of Dreams Passage Flying Balloon Sticker"           , player).access_rule = lambda state: state.has("High Jump", player)
        multiworld.get_location("(T) Radiant Garden Fountain Court Dale Sticker"                , player).access_rule = lambda state: state.has("High Jump", player)
        multiworld.get_location("(T) Radiant Garden Outer Gardens Airplane Sticker"             , player).access_rule = lambda state: state.has("High Jump", player)
        multiworld.get_location("(T) Olympus Coliseum Coliseum Gates Balloon Sticker"           , player).access_rule = lambda state: state.has("High Jump", player)
        multiworld.get_location("(T) Deep Space Machinery Bay Access Mine Square Chest"         , player).access_rule = lambda state: state.has("High Jump", player)
        multiworld.get_location("(T) Never Land Rainbow Falls: Base Rainbow Sticker"            , player).access_rule = lambda state: state.has("High Jump", player)
        multiworld.get_location("(T) Never Land Cliff Path Mega-Potion Chest"                   , player).access_rule = lambda state: can_airslide(state, player)
        multiworld.get_location("(T) Never Land Skull Rock: Cavern Megalixir Chest"             , player).access_rule = lambda state: state.has("High Jump", player)
        multiworld.get_location("(T) Never Land Skull Rock: Entrance Chip Sticker"              , player).access_rule = lambda state: state.has("High Jump", player)
        multiworld.get_location("(T) Never Land Skull Rock: Cavern Ars Solum Chest"             , player).access_rule = lambda state: state.has("High Jump", player)
        multiworld.get_location("(T) Never Land Skull Rock: Cavern Chaos Crystal Chest"         , player).access_rule = lambda state: state.has("High Jump", player)
        multiworld.get_location("(T) Disney Town Pete's Rec Room Aerial Slam Chest"             , player).access_rule = lambda state: can_airslide(state, player)
        multiworld.get_location("(T) Disney Town Pete's Rec Room Break Time Chest"              , player).access_rule = lambda state: can_airslide(state, player)
        multiworld.get_location("(T) Disney Town Raceway Traffic Cone Sticker"                  , player).access_rule = lambda state: state.has("High Jump", player) and can_airslide(state, player)
        multiworld.get_location("(T) The Keyblade Graveyard Twister Trench Traffic Cone Sticker", player).access_rule = lambda state: state.has("High Jump", player)
    if options.character == 1:
        multiworld.get_location("(A) The Land of Departure World Sealed Brightcrest"            , player).access_rule = lambda state: state.has_all({"Wayfinder Ventus", "Wayfinder Aqua", "Wayfinder Terra"}, player)
       #multiworld.get_location("(A) The Land of Departure Defeat Unknown No Name"              , player).access_rule = lambda state: state.has_all({"Wayfinder Ventus", "Wayfinder Aqua", "Wayfinder Terra"}, player)
        multiworld.get_location("(A) Dwarf Woodlands Vault Magnet Chest"                        , player).access_rule = lambda state: state.has("High Jump", player) or state.has("Doubleflight", player)
        multiworld.get_location("(A) Dwarf Woodlands Vault Bubble Sticker"                      , player).access_rule = lambda state: state.has("High Jump", player) and state.has("Doubleflight", player)
        multiworld.get_location("(A) Enchanted Dominion Dungeon Horace Sticker"                 , player).access_rule = lambda state: state.has("High Jump", player) or state.has("Doubleflight", player)
        multiworld.get_location("(A) Radiant Garden Aqueduct Donut Sticker"                     , player).access_rule = lambda state: state.has("High Jump", player) or state.has("Doubleflight", player)
        multiworld.get_location("(A) Radiant Garden Defeat Final Terra-Xehanort II"             , player).access_rule = lambda state: state.has_all({"Wayfinder Ventus", "Wayfinder Aqua", "Wayfinder Terra"}, player)
        multiworld.get_location("(A) Olympus Coliseum Coliseum Gates Fireworks Sticker"         , player).access_rule = lambda state: state.has("High Jump", player) and (can_airslide(state, player) or state.has("Doubleflight", player))
        multiworld.get_location("(A) Never Land Mermaid Lagoon Rainbow Sticker"                 , player).access_rule = lambda state: can_airslide(state, player)
        multiworld.get_location("(A) Never Land Jungle Clearing Fireworks Sticker"              , player).access_rule = lambda state: state.has("Doubleflight", player)
        multiworld.get_location("(A) Disney Town Raceway Daisy Sticker"                         , player).access_rule = lambda state: can_airslide(state, player)
        multiworld.get_location("(A) Disney Town Main Plaza Minnie Sticker"                     , player).access_rule = lambda state: state.has("Doubleflight", player)
        multiworld.get_location("(A) The Keyblade Graveyard Seat of War Flower Sticker"         , player).access_rule = lambda state: state.has("Doubleflight", player)
        multiworld.get_location("(A) The Keyblade Graveyard Fissure Bubble Sticker"             , player).access_rule = lambda state: state.has("Doubleflight", player)
    if options.character == 0:
       #multiworld.get_location("(V) The Land of Departure Defeat Unknown No Name"              , player).access_rule = lambda state: state.has_all({"Wayfinder Ventus", "Wayfinder Aqua", "Wayfinder Terra"}, player)
        multiworld.get_location("(V) Enchanted Dominion Audience Chamber Dewey Sticker"         , player).access_rule = lambda state: state.has("High Jump", player) and can_glide(state, player)
        multiworld.get_location("(V) Radiant Garden Front Doors Fireworks Sticker"              , player).access_rule = lambda state: state.has("High Jump", player)
        multiworld.get_location("(V) Never Land Rainbow Falls: Base Rainbow Sticker"            , player).access_rule = lambda state: state.has("High Jump", player) and can_glide(state, player)
        multiworld.get_location("(V) Disney Town Raceway Superglide Chest"                      , player).access_rule = lambda state: can_glide(state, player)
        multiworld.get_location("(V) The Keyblade Graveyard Seat of War Ice Cream Sticker"      , player).access_rule = lambda state: state.has("High Jump", player)
    
    # Region rules.
    multiworld.get_entrance("Dwarf Woodlands"                                                   , player).access_rule = lambda state: state.has("Dwarf Woodlands",      player)
    multiworld.get_entrance("Castle of Dreams"                                                  , player).access_rule = lambda state: state.has("Castle of Dreams",     player)
    multiworld.get_entrance("Enchanted Dominion"                                                , player).access_rule = lambda state: state.has("Enchanted Dominion",   player)
    multiworld.get_entrance("The Mysterious Tower"                                              , player).access_rule = lambda state: state.has("The Mysterious Tower", player)
    multiworld.get_entrance("Radiant Garden"                                                    , player).access_rule = lambda state: state.has("Radiant Garden",       player)
    multiworld.get_entrance("Olympus Coliseum"                                                  , player).access_rule = lambda state: state.has("Olympus Coliseum",     player)
    multiworld.get_entrance("Deep Space"                                                        , player).access_rule = lambda state: state.has("Deep Space",           player)
   #multiworld.get_entrance("Destiny Islands"                                                   , player).access_rule = lambda state: state.has("Destiny Islands",      player)
    multiworld.get_entrance("Never Land"                                                        , player).access_rule = lambda state: state.has("Never Land",           player)
    multiworld.get_entrance("Disney Town"                                                       , player).access_rule = lambda state: state.has("Disney Town",          player)
    multiworld.get_entrance("The Keyblade Graveyard"                                            , player).access_rule = lambda state: state.has_all({"Wayfinder Ventus", "Wayfinder Aqua", "Wayfinder Terra"}, player)
    multiworld.get_entrance("Realm of Darkness"                                                 , player).access_rule = lambda state: state.has_all({"Wayfinder Ventus", "Wayfinder Aqua", "Wayfinder Terra"}, player) and state.has("Realm of Darkness", player)

    # Win condition.
    multiworld.completion_condition[player] = lambda state: state.has("Victory", player)
    