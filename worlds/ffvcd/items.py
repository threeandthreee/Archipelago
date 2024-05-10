import os, sys
from BaseClasses import ItemClassification, Item
arch_item_offset = 352000000



EXDEATH_ITEM_ID = 1200
WORLD2_ACCESS_ITEM_ID = 1201
WORLD3_ACCESS_ITEM_ID = 1202
EXDEATH_W2_ITEM_ID = 1203


# I tried making these integers for better performance
# but AutoWorld.py method get_data_package_data()
# tries to sort this list, and cannot because "Everything" is a group name

# So I changed them back to strings...

ITEM_CODE_UNIQUE = '1'
ITEM_CODE_ABILITIES = '2'
ITEM_CODE_CRYSTALS = '3'
ITEM_CODE_FUNGIBLE = '4'
ITEM_CODE_GIL = '5'
ITEM_CODE_ITEM = '6'
ITEM_CODE_KEY_ITEMS = '7'
ITEM_CODE_MAGIC = '8'
ITEM_CODE_VICTORY = '9'
ITEM_CODE_MIB_REWARD = '10'
ITEM_CODE_EXDEATH_W2 = '11'

class ItemData:
    def __init__(self, item_id, classification, groups):
        self.groups = groups
        self.classification = classification
        self.id = None if item_id is None else item_id + arch_item_offset


def create_item(name: str, classification, item_data_id, player, groups) -> Item:
    return FFVCDItem(name, classification, item_data_id, player, groups)



def create_world_items(world, trapped_chests_flag = False, chosen_mib_locations = None):
    
    mib_items_to_place = []
    mib_item_pool = []



    
    # add victory first, manually update location and item table
    exdeath = world.multiworld.get_location("ExDeath", world.player)    
    new_item = create_item("Victory",  
                                ItemClassification.progression, 
                                EXDEATH_ITEM_ID + arch_item_offset, 
                                world.player, [ITEM_CODE_VICTORY])
    exdeath.place_locked_item(new_item)


    
    ##################
    # trapped chest items handling
    ##################
    
    if trapped_chests_flag and chosen_mib_locations:
        
        mib_item_data = dict({(i, item_table[i]) for i in item_table if '10' in item_table[i].groups})
        sorted_list = sorted(mib_item_data.items())
        sorted_dict = {}
        for key, value in sorted_list:
            sorted_dict[key] = value
        mib_item_data = sorted_dict
        for k, v in mib_item_data.items():
            mib_item_pool.append(create_item(k, v.classification, v.id, world.player, v.groups))
            
        mib_items_to_place = world.multiworld.per_slot_randoms[world.player].choices(mib_item_pool, k=len(chosen_mib_locations))
            
    
    ##################    
    # add progression items
    ##################
    placed_items = []
    for key_item_name in [i for i in item_table if ITEM_CODE_KEY_ITEMS in item_table[i].groups]:
        item_data = item_table[key_item_name]
        if item_data.classification == ItemClassification.progression:
            new_item = create_item(key_item_name, item_data.classification, item_data.id, \
                                   world.player, item_data.groups)
            placed_items.append(new_item)


            
    ###############
    # FOUR JOB ENABLED
    # do not add abilities/crystals to pool if four job enabled
    ###############
    if world.options.four_job:
        starting_crystals = world.multiworld.random.sample([i for i in item_table \
                                                            if ITEM_CODE_CRYSTALS in item_table[i].groups],4)       
        for item_name in [i for i in item_table\
                              if ITEM_CODE_MAGIC in item_table[i].groups or ITEM_CODE_GIL in item_table[i].groups]:
            
            if item_name not in starting_crystals:
                
                item_data = item_table[item_name]
                new_item = create_item(item_name, item_data.classification, item_data.id, \
                                       world.player, item_data.groups)
                placed_items.append(new_item)



    ###############
    # FOUR JOB DISABLED
    # add crystals only if four job not enabled
    ###############
    else:
        
        # first choose starting crystal
        starting_crystals = [world.multiworld.random.choice([i for i in item_table \
                                                             if ITEM_CODE_CRYSTALS in item_table[i].groups])]

        for item_name in [i for i in item_table if ITEM_CODE_CRYSTALS in item_table[i].groups or \
                              ITEM_CODE_ABILITIES in item_table[i].groups or ITEM_CODE_MAGIC in item_table[i].groups\
                                  or ITEM_CODE_GIL in item_table[i].groups]:
            if item_name not in starting_crystals:
                item_data = item_table[item_name]
                new_item = create_item(item_name, item_data.classification, item_data.id, \
                                       world.player, item_data.groups)
                placed_items.append(new_item)

        


    
    # then calculate remaining    
    locations_this_world = [i for i in world.multiworld.get_locations(world.player)]
    # this has a minus 1 at the end to accommodate special locations like "ExDeath" at the end
    
    item_count_to_place = len(locations_this_world) - len(mib_items_to_place) - len(placed_items) - 1
    
    # get mib item names, if any
    mib_already_chosen_items = [i.name for i in mib_items_to_place]
    
    for item_name in world.multiworld.random.sample([i for i in item_table if ITEM_CODE_FUNGIBLE in \
                                                     item_table[i].groups and i not in mib_already_chosen_items
                                                     ], item_count_to_place):
        item_data = item_table[item_name]
        new_item = create_item(item_name, item_data.classification, item_data.id, \
                                                   world.player, item_data.groups)
            
        placed_items.append(new_item)

    world.random.shuffle(placed_items)
    # add remaining to itempool
    for new_item in placed_items:
        world.multiworld.itempool.append(new_item)
        
        
    return starting_crystals, placed_items, mib_items_to_place

item_table = {
    "Knight Crystal" : ItemData(100, ItemClassification.useful, [ITEM_CODE_UNIQUE, ITEM_CODE_CRYSTALS]),
    "Monk Crystal" : ItemData(101, ItemClassification.useful, [ITEM_CODE_UNIQUE, ITEM_CODE_CRYSTALS]),
    "Thief Crystal" : ItemData(102, ItemClassification.useful, [ITEM_CODE_UNIQUE, ITEM_CODE_CRYSTALS]),
    "Dragoon Crystal" : ItemData(103, ItemClassification.useful, [ITEM_CODE_UNIQUE, ITEM_CODE_CRYSTALS]),
    "Ninja Crystal" : ItemData(104, ItemClassification.useful, [ITEM_CODE_UNIQUE, ITEM_CODE_CRYSTALS]),
    "Samurai Crystal" : ItemData(105, ItemClassification.useful, [ITEM_CODE_UNIQUE, ITEM_CODE_CRYSTALS]),
    "Berserker Crystal" : ItemData(106, ItemClassification.useful, [ITEM_CODE_UNIQUE, ITEM_CODE_CRYSTALS]),
    "Hunter Crystal" : ItemData(107, ItemClassification.useful, [ITEM_CODE_UNIQUE, ITEM_CODE_CRYSTALS]),
    "MysticKnight Crystal" : ItemData(108, ItemClassification.useful, [ITEM_CODE_UNIQUE, ITEM_CODE_CRYSTALS]),
    "WhiteMage Crystal" : ItemData(109, ItemClassification.useful, [ITEM_CODE_UNIQUE, ITEM_CODE_CRYSTALS]),
    "BlackMage Crystal" : ItemData(110, ItemClassification.useful, [ITEM_CODE_UNIQUE, ITEM_CODE_CRYSTALS]),
    "TimeMage Crystal" : ItemData(111, ItemClassification.useful, [ITEM_CODE_UNIQUE, ITEM_CODE_CRYSTALS]),
    "Summoner Crystal" : ItemData(112, ItemClassification.useful, [ITEM_CODE_UNIQUE, ITEM_CODE_CRYSTALS]),
    "BlueMage Crystal" : ItemData(113, ItemClassification.useful, [ITEM_CODE_UNIQUE, ITEM_CODE_CRYSTALS]),
    "RedMage Crystal" : ItemData(114, ItemClassification.useful, [ITEM_CODE_UNIQUE, ITEM_CODE_CRYSTALS]),
    "Trainer Crystal" : ItemData(115, ItemClassification.useful, [ITEM_CODE_UNIQUE, ITEM_CODE_CRYSTALS]),
    "Chemist Crystal" : ItemData(116, ItemClassification.useful, [ITEM_CODE_UNIQUE, ITEM_CODE_CRYSTALS]),
    "Geomancer Crystal" : ItemData(117, ItemClassification.useful, [ITEM_CODE_UNIQUE, ITEM_CODE_CRYSTALS]),
    "Bard Crystal" : ItemData(118, ItemClassification.useful, [ITEM_CODE_UNIQUE, ITEM_CODE_CRYSTALS]),
    "Dancer Crystal" : ItemData(119, ItemClassification.useful, [ITEM_CODE_UNIQUE, ITEM_CODE_CRYSTALS]),
    "Mimic Crystal" : ItemData(120, ItemClassification.useful, [ITEM_CODE_UNIQUE, ITEM_CODE_CRYSTALS]),
    "Freelancer Crystal" : ItemData(121, ItemClassification.useful, [ITEM_CODE_UNIQUE, ITEM_CODE_CRYSTALS]),
        
    "Ice Sword Magic" : ItemData(201, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Bolt Sword Magic" : ItemData(202, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Venom Sword Magic" : ItemData(203, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Mute Sword Magic" : ItemData(204, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Sleep Sword Magic" : ItemData(205, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Fire2 Sword Magic" : ItemData(206, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Ice2 Sword Magic" : ItemData(207, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Bolt2 Sword Magic" : ItemData(208, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Drain Sword Magic" : ItemData(209, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Break Sword Magic" : ItemData(210, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Bio Sword Magic" : ItemData(211, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Fire3 Sword Magic" : ItemData(212, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Ice3 Sword Magic" : ItemData(213, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Bolt3 Sword Magic" : ItemData(214, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Holy Sword Magic" : ItemData(215, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Flare Sword Magic" : ItemData(216, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Psych Sword Magic" : ItemData(217, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Cure White Magic" : ItemData(218, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Scan White Magic" : ItemData(219, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Antdt White Magic" : ItemData(220, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Mute White Magic" : ItemData(221, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Armor White Magic" : ItemData(222, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Size White Magic" : ItemData(223, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Cure2 White Magic" : ItemData(224, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Life White Magic" : ItemData(225, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Charm White Magic" : ItemData(226, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Image White Magic" : ItemData(227, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Shell White Magic" : ItemData(228, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Heal White Magic" : ItemData(229, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Cure3 White Magic" : ItemData(230, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Wall White Magic" : ItemData(231, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Bersk White Magic" : ItemData(232, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Life2 White Magic" : ItemData(233, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Holy White Magic" : ItemData(234, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Dispel White Magic" : ItemData(235, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Fire Black Magic" : ItemData(236, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Ice Black Magic" : ItemData(237, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Bolt Black Magic" : ItemData(238, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Venom Black Magic" : ItemData(239, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Sleep Black Magic" : ItemData(240, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Toad Black Magic" : ItemData(241, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Fire2 Black Magic" : ItemData(242, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Ice2 Black Magic" : ItemData(243, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Bolt2 Black Magic" : ItemData(244, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Drain Black Magic" : ItemData(245, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Break Black Magic" : ItemData(246, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Bio Black Magic" : ItemData(247, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Fire3 Black Magic" : ItemData(248, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Ice3 Black Magic" : ItemData(249, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Bolt3 Black Magic" : ItemData(250, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Flare Black Magic" : ItemData(251, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Doom Black Magic" : ItemData(252, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Psych Black Magic" : ItemData(253, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Slow Time Magic" : ItemData(255, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Regen Time Magic" : ItemData(256, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Void Time Magic" : ItemData(257, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Haste Time Magic" : ItemData(258, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Float Time Magic" : ItemData(259, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Demi Time Magic" : ItemData(260, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Stop Time Magic" : ItemData(261, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Comet Time Magic" : ItemData(263, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Slow2 Time Magic" : ItemData(264, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Reset Time Magic" : ItemData(265, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Qrter Time Magic" : ItemData(266, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Hast2 Time Magic" : ItemData(267, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Old Time Magic" : ItemData(268, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Meteo Time Magic" : ItemData(269, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Quick Time Magic" : ItemData(270, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Xzone Time Magic" : ItemData(271, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Chocob Esper Magic" : ItemData(272, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Sylph Esper Magic" : ItemData(273, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Remora Esper Magic" : ItemData(274, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Shiva Esper Magic" : ItemData(275, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Ramuh Esper Magic" : ItemData(276, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Ifrit Esper Magic" : ItemData(277, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Titan Esper Magic" : ItemData(278, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Golem Esper Magic" : ItemData(279, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Shoat Esper Magic" : ItemData(280, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Crbnkl Esper Magic" : ItemData(281, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Syldra Esper Magic" : ItemData(282, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Odin Esper Magic" : ItemData(283, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Phenix Esper Magic" : ItemData(284, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Levia Esper Magic" : ItemData(285, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Bahmut Esper Magic" : ItemData(286, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Power Song Magic" : ItemData(287, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Speed Song Magic" : ItemData(288, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Vitality Song Magic" : ItemData(289, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Magic Song Magic" : ItemData(290, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Hero Song Magic" : ItemData(291, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Requiem Song Magic" : ItemData(292, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Love Song Magic" : ItemData(293, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Charm Song Magic" : ItemData(294, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Condemn Blue Magic" : ItemData(295, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Roulette Blue Magic" : ItemData(296, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "AquaRake Blue Magic" : ItemData(297, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "L5 Doom Blue Magic" : ItemData(298, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "L4 Qrter Blue Magic" : ItemData(299, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "L2 Old Blue Magic" : ItemData(300, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "L3 Flare Blue Magic" : ItemData(301, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "FrogSong Blue Magic" : ItemData(302, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "TinySong Blue Magic" : ItemData(303, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Flash Blue Magic" : ItemData(304, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Time Slip Blue Magic" : ItemData(305, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "MoonFlut Blue Magic" : ItemData(306, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "DethClaw Blue Magic" : ItemData(307, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Aero Blue Magic" : ItemData(308, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Aero 2 Blue Magic" : ItemData(309, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Aero 3 Blue Magic" : ItemData(310, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Emission Blue Magic" : ItemData(311, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "GblinPnch Blue Magic" : ItemData(312, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "DrkShock Blue Magic" : ItemData(313, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "GuardOff Blue Magic" : ItemData(314, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Fusion Blue Magic" : ItemData(315, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "MindBlst Blue Magic" : ItemData(316, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Vampire Blue Magic" : ItemData(317, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Hammer Blue Magic" : ItemData(318, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "BigGuard Blue Magic" : ItemData(319, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Exploder Blue Magic" : ItemData(320, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "???? Blue Magic" : ItemData(321, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Blowfish Blue Magic" : ItemData(322, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "WhiteWind Blue Magic" : ItemData(323, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
    "Missile Blue Magic" : ItemData(324, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC]),
        
    "Kick Ability" : ItemData(400, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "BuildUp Ability" : ItemData(401, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Mantra Ability" : ItemData(402, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Escape Ability" : ItemData(403, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Steal Ability" : ItemData(404, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Mug Ability" : ItemData(405, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Jump Ability" : ItemData(406, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "DrgnSwd Ability" : ItemData(407, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Smoke Ability" : ItemData(408, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Image Ability" : ItemData(409, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Throw Ability" : ItemData(410, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "SwdSlap Ability" : ItemData(411, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "GilToss Ability" : ItemData(412, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Slash Ability" : ItemData(413, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Animals Ability" : ItemData(414, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Aim Ability" : ItemData(415, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "X-Fight Ability" : ItemData(416, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Conjure Ability" : ItemData(417, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Observe Ability" : ItemData(418, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Analyze Ability" : ItemData(419, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Tame Ability" : ItemData(420, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Control Ability" : ItemData(421, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Catch Ability" : ItemData(422, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Mix Ability" : ItemData(423, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Drink Ability" : ItemData(424, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Pray Ability" : ItemData(425, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Revive Ability" : ItemData(426, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Terrain Ability" : ItemData(427, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Hide Ability" : ItemData(428, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Sing Ability" : ItemData(429, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Flirt Ability" : ItemData(430, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Dance Ability" : ItemData(431, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Mimic Ability" : ItemData(432, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "MgcSwrd Lv.1 Ability" : ItemData(433, ItemClassification.filler, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "MgcSwrd Lv.2 Ability" : ItemData(434, ItemClassification.filler, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "MgcSwrd Lv.3 Ability" : ItemData(435, ItemClassification.filler, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "MgcSwrd Lv.4 Ability" : ItemData(436, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "MgcSwrd Lv.5 Ability" : ItemData(437, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "MgcSwrd Lv.6 Ability" : ItemData(438, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "White Lv.1 Ability" : ItemData(439, ItemClassification.filler, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "White Lv.2 Ability" : ItemData(440, ItemClassification.filler, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "White Lv.3 Ability" : ItemData(441, ItemClassification.filler, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "White Lv.4 Ability" : ItemData(442, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "White Lv.5 Ability" : ItemData(443, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "White Lv.6 Ability" : ItemData(444, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Black Lv.1 Ability" : ItemData(445, ItemClassification.filler, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Black Lv.2 Ability" : ItemData(446, ItemClassification.filler, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Black Lv.3 Ability" : ItemData(447, ItemClassification.filler, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Black Lv.4 Ability" : ItemData(448, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Black Lv.5 Ability" : ItemData(449, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Black Lv.6 Ability" : ItemData(450, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Time Lv.1 Ability" : ItemData(451, ItemClassification.filler, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Time Lv.2 Ability" : ItemData(452, ItemClassification.filler, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Time Lv.3 Ability" : ItemData(453, ItemClassification.filler, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Time Lv.4 Ability" : ItemData(454, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Time Lv.5 Ability" : ItemData(455, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Time Lv.6 Ability" : ItemData(456, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Summon Lv.1 Ability" : ItemData(457, ItemClassification.filler, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Summon Lv.2 Ability" : ItemData(458, ItemClassification.filler, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Summon Lv.3 Ability" : ItemData(459, ItemClassification.filler, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Summon Lv.4 Ability" : ItemData(460, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Summon Lv.5 Ability" : ItemData(461, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Red Lv.1 Ability" : ItemData(462, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Red Lv.2 Ability" : ItemData(463, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Red Lv.3 Ability" : ItemData(464, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "X-Magic Ability" : ItemData(465, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Blue Ability" : ItemData(466, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Equip Shield Ability" : ItemData(467, ItemClassification.filler, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Equip Armors Ability" : ItemData(468, ItemClassification.filler, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Equip Ribbon Ability" : ItemData(469, ItemClassification.filler, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Equip Swords Ability" : ItemData(470, ItemClassification.filler, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Equip Spears Ability" : ItemData(471, ItemClassification.filler, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Equip Katana Ability" : ItemData(472, ItemClassification.filler, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Equip Axes Ability" : ItemData(473, ItemClassification.filler, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Equip Bows Ability" : ItemData(474, ItemClassification.filler, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Equip Whips Ability" : ItemData(475, ItemClassification.filler, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Equip Harps Ability" : ItemData(476, ItemClassification.filler, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Agility Ability" : ItemData(477, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "HP +10% Ability" : ItemData(478, ItemClassification.filler, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "HP +20% Ability" : ItemData(479, ItemClassification.filler, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "HP +30% Ability" : ItemData(480, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "MP +10% Ability" : ItemData(481, ItemClassification.filler, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "MP +30% Ability" : ItemData(482, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Brawl Ability" : ItemData(483, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Dbl Grip Ability" : ItemData(484, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "2-Wield Ability" : ItemData(485, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Medicine Ability" : ItemData(486, ItemClassification.filler, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Cover Ability" : ItemData(487, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Counter Ability" : ItemData(488, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Evade Ability" : ItemData(489, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Barrier Ability" : ItemData(490, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Berserk Ability" : ItemData(491, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Caution Ability" : ItemData(492, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Preemptive Ability" : ItemData(493, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "DmgFloor Ability" : ItemData(494, ItemClassification.filler, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    "Equip Rods Ability" : ItemData(495, ItemClassification.filler, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES]),
    
        
    "Knife Item" : ItemData(600, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Dagger Item" : ItemData(601, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Mythril Knife Item" : ItemData(602, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Kunai Item" : ItemData(603, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Mage Masher Item" : ItemData(604, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Guardian Item" : ItemData(605, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Kodachi Item" : ItemData(606, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Orialcon Item" : ItemData(607, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Air Knife Item" : ItemData(608, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Assassin Item" : ItemData(609, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Hardened Dagger Item" : ItemData(610, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Broadsword Item" : ItemData(611, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "RegalCut Item" : ItemData(612, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Mythril Sword Item" : ItemData(613, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Coral Sword Item" : ItemData(614, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Ancient Sword Item" : ItemData(615, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Epee Sword Item" : ItemData(616, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Slumber Sword Item" : ItemData(617, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Defender Sword Item" : ItemData(618, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Excalibur Item" : ItemData(619, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Ragnarok Item" : ItemData(620, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Javelin Item" : ItemData(621, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Spear Item" : ItemData(622, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Mythril Spear Item" : ItemData(623, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Trident Item" : ItemData(624, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Wind Spear Item" : ItemData(625, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Partisan Item" : ItemData(626, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Heavy Spear Item" : ItemData(627, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "DblLance Item" : ItemData(628, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Holy Lance Item" : ItemData(629, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Dragoon Lance Item" : ItemData(630, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Battle Axe Item" : ItemData(631, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Mythril Hammer Item" : ItemData(632, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Ogre Killer Item" : ItemData(633, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "War Hammer Item" : ItemData(634, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Venom Axe Item" : ItemData(635, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Earth Hammer Item" : ItemData(636, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Rune Axe Item" : ItemData(637, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Thor Hammer Item" : ItemData(638, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Katana Item" : ItemData(639, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Air Blade Item" : ItemData(640, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Kotetsu Item" : ItemData(641, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Bizen Item" : ItemData(642, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Forged Item" : ItemData(643, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Murasume Item" : ItemData(644, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Masamune Item" : ItemData(645, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Tempest Item" : ItemData(646, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Rod Item" : ItemData(647, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Fire Rod Item" : ItemData(648, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Ice Rod Item" : ItemData(649, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Thunder Rod Item" : ItemData(650, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Venom Rod Item" : ItemData(651, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Lillith Rod Item" : ItemData(652, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Wizard Rod Item" : ItemData(653, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Staff Item" : ItemData(654, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Mythril Staff Item" : ItemData(655, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Power Staff Item" : ItemData(656, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Healing Staff Item" : ItemData(657, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Staff of Light Item" : ItemData(658, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Sage's Staff Item" : ItemData(659, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Judgement Staff Item" : ItemData(660, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Fire Bow Item" : ItemData(661, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Ice Bow Item" : ItemData(662, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Thunder Bow Item" : ItemData(663, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Darkness Bow Item" : ItemData(664, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Killer Bow Item" : ItemData(665, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Elven Bow Item" : ItemData(666, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Yoichi Bow Item" : ItemData(667, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Artemis Bow Item" : ItemData(668, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Silver Harp Item" : ItemData(669, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Dream Harp Item" : ItemData(670, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Lamia's Harp Item" : ItemData(671, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Apollo's Harp Item" : ItemData(672, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Whip Item" : ItemData(673, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Chain Whip Item" : ItemData(674, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Thunder Whip Item" : ItemData(675, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Flame Whip Item" : ItemData(676, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Dragon's Whisker Item" : ItemData(677, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Giyaman Item" : ItemData(678, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Earth Bell Item" : ItemData(679, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Rune Chime Item" : ItemData(680, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Tinkerbell Item" : ItemData(681, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Drain Sword Item" : ItemData(682, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "RuneEdge Item" : ItemData(683, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Flametongue Item" : ItemData(684, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "IceBrand Item" : ItemData(685, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Full Moon Item" : ItemData(686, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Shuriken Item" : ItemData(687, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Pinwheel Item" : ItemData(688, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Excailbur Item" : ItemData(689, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "BeastKiller Item" : ItemData(690, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Flail Item" : ItemData(691, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Morning Star Item" : ItemData(692, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Wonder Wand Item" : ItemData(693, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Brave Blade Item" : ItemData(694, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Soot Item" : ItemData(695, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Chicken Knife Item" : ItemData(696, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "RisingSun Item" : ItemData(697, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Silver Bow Item" : ItemData(698, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Gale Bow Item" : ItemData(699, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "AntiMagic Bow Item" : ItemData(700, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Avis Killer Item" : ItemData(701, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "DoomCut Item" : ItemData(702, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Giant's Axe Item" : ItemData(703, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "ManEater Item" : ItemData(704, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Thief Knife Item" : ItemData(705, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Dancing Dagger Item" : ItemData(706, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Enhancer Item" : ItemData(707, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Leather Shield Item" : ItemData(708, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Bronze Shield Item" : ItemData(709, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Iron Shield Item" : ItemData(710, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Mythril Shield Item" : ItemData(711, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Golden Shield Item" : ItemData(712, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Aegis Shield Item" : ItemData(713, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Diamond Shield Item" : ItemData(714, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Crystal Shield Item" : ItemData(715, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Leather Cap Item" : ItemData(716, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Bronze Helm Item" : ItemData(717, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Iron Helm Item" : ItemData(718, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Mythril Helm Item" : ItemData(719, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Golden Helm Item" : ItemData(720, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Diamond Helm Item" : ItemData(721, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Crystal Helm Item" : ItemData(722, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Plumed Hat Item" : ItemData(723, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Tricorn Hat Item" : ItemData(724, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Magus Item" : ItemData(725, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Circlet Item" : ItemData(726, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Gold Hairpin Item" : ItemData(727, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Ribbon Item" : ItemData(728, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Bandana Item" : ItemData(729, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "GrnBeret Item" : ItemData(730, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "DarkHood Item" : ItemData(731, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Lamia's Tiara Item" : ItemData(732, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Leather Armor Item" : ItemData(733, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Bronze Armor Item" : ItemData(734, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Iron Armor Item" : ItemData(735, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Mythril Armor Item" : ItemData(736, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Golden Armor Item" : ItemData(737, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Diamond Armor Item" : ItemData(738, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Crystal Armor Item" : ItemData(739, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "CopperPlt Item" : ItemData(740, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Training Suit Item" : ItemData(741, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Silver Plate Item" : ItemData(742, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Stealth Suit Item" : ItemData(743, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "DiamndPlt Item" : ItemData(744, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "DarkSuit Item" : ItemData(745, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Cotton Robe Item" : ItemData(746, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Silk robe Item" : ItemData(747, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Gaia Gear Item" : ItemData(748, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Bard's Surplice Item" : ItemData(749, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Lumina Robe Item" : ItemData(750, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Black Robe Item" : ItemData(751, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "White Robe Item" : ItemData(752, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Mirage Vest Item" : ItemData(753, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Guard Ring Item" : ItemData(754, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Thief's Glove Item" : ItemData(755, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Giant's Gloves Item" : ItemData(756, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Elf Cape Item" : ItemData(757, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Cursed Ring Item" : ItemData(758, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Glasses Item" : ItemData(759, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Running Shoes Item" : ItemData(760, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Mythril Glove Item" : ItemData(761, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Silver Armlet Item" : ItemData(762, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Diamond Armlet Item" : ItemData(763, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Strength Item" : ItemData(764, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Power Wrist Item" : ItemData(765, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Angel Gwn Item" : ItemData(766, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Angel Ring Item" : ItemData(767, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Flame Ring Item" : ItemData(768, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Coral Ring Item" : ItemData(769, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Bone Mail Item" : ItemData(770, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Leather Shoes Item" : ItemData(771, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Kaiser Knuckles Item" : ItemData(772, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Gauntlets Item" : ItemData(773, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Tiger Mask Item" : ItemData(774, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Flame Shield Item" : ItemData(775, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "CornaJar Item" : ItemData(776, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Genji Shield Item" : ItemData(777, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Genji Helm Item" : ItemData(778, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Genji Armor Item" : ItemData(779, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Genji Gloves Item" : ItemData(780, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Wall Ring Item" : ItemData(781, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Hypno Helm Item" : ItemData(782, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Thornlet Item" : ItemData(783, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Ice Shield Item" : ItemData(784, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Cursed Shield Item" : ItemData(785, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Rainbow Dress Item" : ItemData(786, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Red Shoes Item" : ItemData(787, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Potion Item" : ItemData(788, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "HiPotion Item" : ItemData(789, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Ether Item" : ItemData(790, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Elixir Item" : ItemData(791, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Phoenix Down Item" : ItemData(792, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Maiden's Kiss Item" : ItemData(793, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Revivify Item" : ItemData(794, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "TurtleShell Item" : ItemData(795, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Antidote Item" : ItemData(796, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Eyedrop Item" : ItemData(797, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "DragonFang Item" : ItemData(798, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "DarkMatter Item" : ItemData(799, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Soft Item" : ItemData(800, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "LuckMallet Item" : ItemData(801, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Magic Lamp Item" : ItemData(802, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Tent Item" : ItemData(803, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Cabin Item" : ItemData(804, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Giant Drink Item" : ItemData(805, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Power Drink Item" : ItemData(806, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Speed Drink Item" : ItemData(807, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Protect Drink Item" : ItemData(808, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Hero Drink Item" : ItemData(809, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Ramuh Item" : ItemData(810, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Shoat Item" : ItemData(811, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Golem Item" : ItemData(812, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Flame Scroll Item" : ItemData(813, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Water Scroll Item" : ItemData(814, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Thunder Scroll Item" : ItemData(815, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    
    "100 Gil" : ItemData(900, ItemClassification.filler, [ITEM_CODE_GIL, ITEM_CODE_ITEM]),
    "300 Gil" : ItemData(901, ItemClassification.filler, [ITEM_CODE_GIL, ITEM_CODE_ITEM]),
    "1000 Gil" : ItemData(902, ItemClassification.useful, [ITEM_CODE_GIL, ITEM_CODE_ITEM]),
    "5000 Gil (#1)" : ItemData(903, ItemClassification.useful, [ITEM_CODE_GIL, ITEM_CODE_ITEM]),
    "9900 Gil" : ItemData(904, ItemClassification.useful, [ITEM_CODE_GIL, ITEM_CODE_ITEM]),
    "8000 Gil (#1)" : ItemData(905, ItemClassification.useful, [ITEM_CODE_GIL, ITEM_CODE_ITEM]),
    "4400 Gil" : ItemData(906, ItemClassification.useful, [ITEM_CODE_GIL, ITEM_CODE_ITEM]),
    "10000 Gil (#1)" : ItemData(907, ItemClassification.useful, [ITEM_CODE_GIL, ITEM_CODE_ITEM]),
    "5000 Gil (#2)" : ItemData(908, ItemClassification.useful, [ITEM_CODE_GIL, ITEM_CODE_ITEM]),
    "8000 Gil (#2)" : ItemData(909, ItemClassification.useful, [ITEM_CODE_GIL, ITEM_CODE_ITEM]),
    "5000 Gil (#3)" : ItemData(910, ItemClassification.useful, [ITEM_CODE_GIL, ITEM_CODE_ITEM]),
    "9000 Gil (#1)" : ItemData(911, ItemClassification.useful, [ITEM_CODE_GIL, ITEM_CODE_ITEM]),
    "18000 Gil" : ItemData(912, ItemClassification.useful, [ITEM_CODE_GIL, ITEM_CODE_ITEM]),
    "2500 Gil" : ItemData(913, ItemClassification.useful, [ITEM_CODE_GIL, ITEM_CODE_ITEM]),
    "4900 Gil" : ItemData(914, ItemClassification.useful, [ITEM_CODE_GIL, ITEM_CODE_ITEM]),
    "9500 Gil" : ItemData(915, ItemClassification.useful, [ITEM_CODE_GIL, ITEM_CODE_ITEM]),
    "9000 Gil (#2)" : ItemData(916, ItemClassification.useful, [ITEM_CODE_GIL, ITEM_CODE_ITEM]),
    "8000 Gil (#3)" : ItemData(917, ItemClassification.useful, [ITEM_CODE_GIL, ITEM_CODE_ITEM]),
    "10000 Gil (#2)" : ItemData(918, ItemClassification.useful, [ITEM_CODE_GIL, ITEM_CODE_ITEM]),
    "12000 Gil (#1)" : ItemData(919, ItemClassification.useful, [ITEM_CODE_GIL, ITEM_CODE_ITEM]),
    "12000 Gil (#2)" : ItemData(920, ItemClassification.useful, [ITEM_CODE_GIL, ITEM_CODE_ITEM]),
    "9000 Gil (#3)" : ItemData(921, ItemClassification.useful, [ITEM_CODE_GIL, ITEM_CODE_ITEM]),
    "12000 Gil (#3)" : ItemData(922, ItemClassification.useful, [ITEM_CODE_GIL, ITEM_CODE_ITEM]),
    "5000 Gil (#4)" : ItemData(923, ItemClassification.useful, [ITEM_CODE_GIL, ITEM_CODE_ITEM]),
    "15000 Gil" : ItemData(924, ItemClassification.useful, [ITEM_CODE_GIL, ITEM_CODE_ITEM]),
    "20000 Gil" : ItemData(925, ItemClassification.useful, [ITEM_CODE_GIL, ITEM_CODE_ITEM]),
    "25000 Gil" : ItemData(926, ItemClassification.useful, [ITEM_CODE_GIL, ITEM_CODE_ITEM]),


    "Walse Tower Key" : ItemData(1000, ItemClassification.progression, [ITEM_CODE_UNIQUE, ITEM_CODE_KEY_ITEMS]),
    "Steamship Key" : ItemData(1001, ItemClassification.progression, [ITEM_CODE_UNIQUE, ITEM_CODE_KEY_ITEMS]),
    "Ifrit's Fire" : ItemData(1002, ItemClassification.progression, [ITEM_CODE_UNIQUE, ITEM_CODE_KEY_ITEMS]),
    "SandwormBait" : ItemData(1003, ItemClassification.progression, [ITEM_CODE_UNIQUE, ITEM_CODE_KEY_ITEMS]),
    "Big Bridge Key" : ItemData(1004, ItemClassification.progression, [ITEM_CODE_UNIQUE, ITEM_CODE_KEY_ITEMS]),
    "Hiryuu Call" : ItemData(1005, ItemClassification.progression, [ITEM_CODE_UNIQUE, ITEM_CODE_KEY_ITEMS]),
    "Submarine Key" : ItemData(1006, ItemClassification.progression, [ITEM_CODE_UNIQUE, ITEM_CODE_KEY_ITEMS]),
    "Anti Barrier" : ItemData(1007, ItemClassification.progression, [ITEM_CODE_UNIQUE, ITEM_CODE_KEY_ITEMS]),
    "Bracelet" : ItemData(1008, ItemClassification.progression, [ITEM_CODE_UNIQUE, ITEM_CODE_KEY_ITEMS]),
    "Pyramid Page" : ItemData(1009, ItemClassification.progression, [ITEM_CODE_UNIQUE, ITEM_CODE_KEY_ITEMS]),
    "Shrine Page" : ItemData(1010, ItemClassification.progression, [ITEM_CODE_UNIQUE, ITEM_CODE_KEY_ITEMS]),
    "Trench Page" : ItemData(1011, ItemClassification.progression, [ITEM_CODE_UNIQUE, ITEM_CODE_KEY_ITEMS]),
    "Falls Page" : ItemData(1012, ItemClassification.progression, [ITEM_CODE_UNIQUE, ITEM_CODE_KEY_ITEMS]),
    "Mirage Radar" : ItemData(1013, ItemClassification.progression, [ITEM_CODE_UNIQUE, ITEM_CODE_KEY_ITEMS]),
    "Adamantite" : ItemData(1014, ItemClassification.progression, [ITEM_CODE_UNIQUE, ITEM_CODE_KEY_ITEMS]),
    "Moogle Suit" : ItemData(1015, ItemClassification.progression, [ITEM_CODE_UNIQUE, ITEM_CODE_KEY_ITEMS]),
    "Elder Branch" : ItemData(1016, ItemClassification.progression, [ITEM_CODE_UNIQUE, ITEM_CODE_KEY_ITEMS]),
    "1st Tablet" : ItemData(1017, ItemClassification.progression, [ITEM_CODE_UNIQUE, ITEM_CODE_KEY_ITEMS]),
    "2nd Tablet" : ItemData(1018, ItemClassification.progression, [ITEM_CODE_UNIQUE, ITEM_CODE_KEY_ITEMS]),
    "3rd Tablet" : ItemData(1019, ItemClassification.progression, [ITEM_CODE_UNIQUE, ITEM_CODE_KEY_ITEMS]),
    "4th Tablet" : ItemData(1020, ItemClassification.progression, [ITEM_CODE_UNIQUE, ITEM_CODE_KEY_ITEMS]),

    "Victory" : ItemData(1200, ItemClassification.progression, [ITEM_CODE_VICTORY]),
    "Exdeath in World 2" : ItemData(1203, ItemClassification.progression, [ITEM_CODE_EXDEATH_W2]),

}

item_groups = {}
for item, data in item_table.items():
    for group in data.groups:
        item_groups[group] = item_groups.get(group, []) + [item]


class FFVCDItem(Item):
    game = "ffvcd"
    def __init__(self, name, classification, item_data_id, player, groups):
        super().__init__(name, classification, item_data_id, player)
        self.groups = groups

