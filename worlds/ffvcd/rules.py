from worlds.generic.Rules import add_rule, set_rule, forbid_item

def set_rules(ffvcdworld):
    world = ffvcdworld.multiworld
    player = ffvcdworld.player
    world.completion_condition[player] = lambda state: state.has("Victory", player)    
    
    # set_rule(world.get_location("Kelb - CornaJar at Kelb (CornaJar)", ffvcdworld.player),
    #       lambda state: state.has("Catch Ability", ffvcdworld.player) or
    #                     state.has("Trainer Crystal", ffvcdworld.player))
    
