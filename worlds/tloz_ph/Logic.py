from BaseClasses import MultiWorld, Item, Entrance, EntranceType
from .data import LOCATIONS_DATA
from .data.LogicPredicates import *
from .Options import PhantomHourglassOptions
from .data.Entrances import ENTRANCES

def make_overworld_logic():
    overworld_logic = [

        # ====== Mercay Island ==============

        ["mercay sw", "mercay dig spot", False, "shovel"],
        ["mercay island", "mercay zora cave", False, "explosives"],
        ["mercay zora cave", "mercay zora cave south", False, "bow"],
        ["mercay island", "mercay zora cave south", False, "sword_scroll_clip"],
        ["mercay island", "totok", True, None],
        ["mercay island", "mercay freedle island", False, "explosives"],
        ["mercay freedle island", "mercay freedle tunnel chest", False, "range"],
        ["mercay freedle island", "mercay freedle gift", False, "sea_chart", "SE"],
        ["mercay se", "mercay yellow guy", False, "courage_crest"],
        ["mercay oshus", "mercay oshus gem", False, "oshus_gem"],
        ["mercay oshus", "mercay oshus phantom blade", False, "can_make_phantom_sword"],
        ["mercay oshus phantom blade", "mercay oshus gem", False, None],
        ["mercay se", "sw ocean", False, "sea_chart", "SW"],

        # ER
        ["mercay island", "mercay sw", False, None],
        ["mercay sw", "mercay sw bridge", True, None],
        ["mercay sw", "mercay oshus", True, None],
        ["mercay sw", "mercay apricot", True, None],
        ["mercay sw", "mercay sword cave", True, None],

        ["mercay sw bridge", "mercay se", True, None],
        ["mercay se", "mercay tuzi", True, None],
        ["mercay se", "mercay milk bar", True, None],
        ["mercay se", "mercay shop", True, None],
        ["mercay se", "mercay shipyard", False, "has", "_beat_tof"],
        ["mercay shipyard", "mercay se", False, None],
        ["mercay se", "mercay treasure teller", False, "courage_crest"],
        ["mercay treasure teller", "mercay se", False, None],


        # ======== Mountain Passage =========

        ["mercay island", "mercay passage 1", False, "can_enter_mp"],
        ["mercay island", "mercay passage 2", False, "can_reach_mp2"],
        ["mercay passage 2", "mercay passage rat", False, "mp_rat"],

        # ========== TotOK ===================
        ["totok", "totok 1f", False, "totok_1f"],

        ["totok 1f", "totok 1f chest", False, "totok_1f_chest"],
        ["totok 1f", "totok 1f chart", False, "totok_1f_chart"],
        ["totok 1f", "totok b1", False, "totok_b1"],

        ["totok b1", "totok b1 key", False, "totok_b1_key"],
        ["totok b1", "totok b1 phantom", False, "totok_b1_phantom"],
        ["totok b1", "totok b1 bow", False, "totok_b1_bow"],
        ["totok b1", "totok b2", False, "totok_b2"],

        ["totok b2", "totok b2 key", False, "totok_b2_key"],
        ["totok b2", "totok b2 phantom", False, "totok_b2_phantom"],
        ["totok b2", "totok b2 chu", False, "totok_b2_chu"],
        ["totok b2", "totok b3", False, "totok_b3"],

        ["totok b3", "totok b3 nw", False, "totok_b3_nw"],
        ["totok b3", "totok b3 se", False, "totok_b3_se"],
        ["totok b3", "totok b3 sw", False, "totok_b3_sw"],
        ["totok b3", "totok b3 bow", False, "totok_b3_bow"],
        ["totok b3", "totok b3 key", False, "totok_b3_key"],
        ["totok b3", "totok b3 phantom", False, "totok_b3_phantom"],
        ["totok b3", "totok b35", False, "totok_b35"],

        ["totok b35", "totok b4", False, "totok_b4"],
        ["totok b4", "totok b4 key", False, "totok_b4_key"],
        ["totok b4", "totok b4 eyes", False, "totok_b4_eyes"],
        ["totok b4", "totok b4 phantom", False, "totok_b4_phantom"],
        ["totok b4", "totok b5", False, "totok_b5"],
        ["totok b4", "totok b5 alt", False, "totok_b5_alt"],

        ["totok b5", "totok b5 chest", False, "totok_b5_chest"],
        ["totok b5", "totok b6", False, "totok_b6"],
        ["totok b5 alt", "totok b5 alt chest", False, "totok_b5_alt_chest"],
        ["totok b5 alt", "totok b6", False, "totok_b6"],

        ["totok b6", "totok b6 bow", False, "totok_b6_bow"],
        ["totok b6", "totok b6 phantom", False, "totok_b6_phantom"],
        ["totok b6", "totok b6 crest", False, "totok_b6_crest"],
        ["totok b6", "totok midway", False, "totok_b7"],
        ["totok midway", "totok b7", False, "spirit", "Courage"],

        ["totok b7", "totok b7 crystal", False, "totok_b7_crystal"],
        ["totok b7", "totok b7 switch", False, "totok_b7_switch_chest"],
        ["totok b7", "totok b8", False, "totok_b8"],

        ["totok b8", "totok b8 phantom", False, "totok_b8_phantom"],
        ["totok b8", "totok b9", False, "totok_b9"],
        ["totok b8", "totok b8 2c chest", False, "totok_b8_2_crystal_chest"],
        ["totok b8", "totok b7 phantom", False, "totok_b7_phantom"],
        ["totok b8", "totok b9 corner chest", False, "totok_b9_corner_chest"],

        ["totok b9", "totok b9 phantom", False, "totok_b9_phantom"],
        ["totok b9", "totok b9 ghosts", False, "totok_b9_ghosts"],

        ["totok b9", "totok b10", False, "totok_b10"],

        ["totok b10", "totok b10 key", False, "totok_b10_key"],
        ["totok b10", "totok b10 phantom", False, "totok_b10_phantom"],
        ["totok b10", "totok b10 eye", False, "totok_b10_eye"],
        ["totok b10", "totok b10 hammer", False, "totok_b10_hammer"],
        ["totok b10", "totok b11", False, "totok_b11"],

        ["totok b11", "totok b11 phantom", False, "totok_b11_phantom"],
        ["totok b11", "totok b11 eyes", False, "totok_b11_eyes"],
        ["totok b11", "totok b12", False, "totok_b12"],

        ["totok b12", "totok b12 nw", False, "totok_b12_nw"],
        ["totok b12", "totok b12 ne", False, "totok_b12_ne"],
        ["totok b12", "totok b12 phantom", False, "totok_b12_phantom"],
        ["totok b12", "totok b12 ghost", False, "totok_b12_ghost"],
        ["totok b12", "totok b12 hammer", False, "totok_b12_hammer"],
        ["totok b12", "totok b13", False, "totok_b13"],

        ["totok b13", "totok b13 chest", False, "totok_b13_chest"],
        ["totok b13", "totok before bellum", False, "b13_door"],
        ["totok", "totok before bellum", False, "bellum_warp"],
        # Bellum
        ["totok before bellum", "bellum 1", False, "bellum_staircase"],
        ["bellum 1", "ghost ship fight", False, "can_beat_bellum"],
        ["ghost ship fight", "bellumbeck", False, "can_beat_ghost_ship_fight"],

        # ============ Shops ====================

        ["mercay island", "shop power gem", False, "can_buy_gem"],
        ["mercay island", "shop quiver", False, "can_buy_quiver"],
        ["mercay island", "shop bombchu bag", False, "can_buy_chu_bag"],
        ["mercay island", "shop heart container", False, "can_buy_heart"],

        ["sw ocean east", "beedle", False, None],
        ["beedle", "beedle gem", False, "beedle_shop", 500],
        ["beedle", "beedle bomb bag", False, "can_buy_bomb_bag"],
        ["beedle", "masked ship gem", False, "beedle_shop", 500],
        ["beedle", "masked ship hc", False, "beedle_shop", 500],

        ["beedle", "beedle bronze", False, "can_get_beedle_bronze"],
        ["beedle", "beedle silver", False, "has_beedle_points", 20],
        ["beedle", "beedle gold", False, "has_beedle_points", 50],
        ["beedle", "beedle plat", False, "has_beedle_points", 100],
        ["beedle", "beedle vip", False, "has_beedle_points", 200],


        # ============ SW Ocean =================

        ["mercay island", "sw ocean east", False, "boat_access"],
        ["sw ocean east", "cannon island", False, None],
        ["sw ocean east", "ember port", True, None],
        ["sw ocean east", "sw ocean crest salvage", False, "salvage_courage_crest"],
        ["sw ocean east", "sw ocean west", False, "ocean_sw_west"],
        ["sw ocean west", "molida island", False, None],
        ["sw ocean west", "spirit island", False, None],
        ["sw ocean west", "sw ocean nyave", False, "nyave_fight"],
        ["sw ocean nyave", "sw ocean nyave trade", False, "guard_notebook"],
        ["sw ocean west", "sw ocean frog phi", False, "cannon"],
        ["sw ocean east", "sw ocean frog x", False, "cannon"],

        # ============ Cannon Island ===============

        ["cannon island", "cannon island salvage arm", False, "courage_crest"],
        ["cannon island", "cannon island dig", False, "spade"],

        # =============== Isle of Ember ================

        # ER
        ["ember port", "ember astrid", True, None],
        ["ember astrid", "ember astrid basement", True, None],
        ["ember astrid basement", "ember astrid basement dig", False, "spade"],
        ["ember port", "ember kayo", True, None],
        ["ember port", "ember port house", True, None],
        ["ember astrid", "ember astrid post tof", False, "has", "_beat_tof"],

        ["ember port", "ember grapple", False, "ember_grapple"],
        ["ember grapple", "ember port", False, "grapple"],
        ["ember grapple", "ember coast north", True, "grapple"],

        ["ember coast north", "ember coast east", True, None],
        ["ember port", "ember coast east", True, None],
        ["ember climb west", "ember coast east", True, None],
        ["ember climb west", "ember outside tof", True, None],
        ["ember outside tof", "tof 1f", True, None],
        ["ember summit west", "ember outside tof", True, None],
        ["ember summit west", "ember summit east", True, None],
        ["ember outside tof", "ember outside tof dig", False, "shovel"],

        ["ember summit west", "ember climb west", False, None],
        ["ember summit east", "ember outside tof", False, None],
        ["ember climb west", "ember port", False, None],
        ["ember outside tof", "ember coast east", False, None],

        ["ember climb east", "ember coast east", True, None],
        ["ember summit north", "ember summit east", True, None],
        ["ember climb east", "ember port", True, None],
        ["ember summit north", "ember summit west", True, None],



        # =============== Temple of Fire =================

        ["tof 1f", "tof 1f keese", False, "can_kill_bat"],
        ["tof 1f", "tof 1f maze", False, "tof_maze"],
        ["tof 1f maze", "tof 2f", False, "can_hit_spin_switches"],
        # 2F
        ["tof 2f", "tof 1f west", False, "short_range"],
        ["tof 1f west", "tof 1f sw", False, "can_hit_spiral_wall_switches"],
        ["tof 1f sw", "tof 2f south", False, "can_kill_bubble"],
        ["tof 2f south", "tof 3f", False, "tof_3f"],
        # 3F
        ["tof 3f", "tof 3f key drop", False, "boomerang"],
        ["tof 3f key drop", "tof 3f boss key", False, "tof_3f_bk"],  # All 3F checks need boomerang, UT included
        ["tof 3f boss key", "tof blaaz", False, "tof_blaaz"],  # Includes UT
        ["tof blaaz", "post tof", False, None],

        # =========== Molida Island ===============

        ["molida island", "molida dig", False, "spade"],
        ["molida island", "molida port house", True, None],
        ["molida island", "molida grapple", False, "grapple"],
        ["molida island", "molida cave back", False, "cave_damage"],
        ["molida cave back", "molida cave back dig", False, "spade"],
        ["molida cave back dig", "molida cuccoo dig", False, "grapple"],
        ["molida dig", "molida north", False, "sun_key"],
        ["molida north", "molida north grapple", False, "grapple"],
        ["molida north", "toc gates", False, "enter_toc"],
        ["toc gates", "toc", True, None],
        ["toc crayk", "post toc", False, None],
        ["post toc", "molida archery", False, None],

        # =============== Temple of Courage ================

        ["toc", "toc bomb alcove", False, "boom"],
        ["toc", "toc b1", False, "toc_door_1"],
        ["toc", "toc hammer clips", False, "hammer_clip"],
        ["toc b1", "toc b1 grapple", False, "toc_grapple"],
        ["toc b1", "toc 1f west", False, "toc_1f_west"],
        ["toc b1 grapple", "toc 1f west", False, "bow"],
        ["toc hammer clips", "toc 1f west", False, None],
        ["toc 1f west", "toc map room", False, "boom"],
        ["toc 1f west", "toc 2f beamos", False, "toc_door_2"],
        ["toc 1f west", "toc b1 maze", False, "shape_crystal", "Temple of Courage", "Square"],
        ["toc 2f beamos", "toc b1 maze", False, "is_ut"],  # UT Crystal
        ["toc 2f beamos", "toc south 1f", False, "toc_beamos_ut"],  # UT Crystal South
        ["toc b1 grapple", "toc b1 maze", False, None],
        ["toc b1 maze", "toc south 1f", False, "toc_crystal_south"],

        ["toc south 1f", "toc 2f spike corridor", False, "boom"],
        ["toc 2f spike corridor", "toc 2f platforms", False, "toc_spike_corridor"],
        ["toc hammer clips", "toc 2f spike corridor", False, None],
        ["toc south 1f", "toc 2f platforms", False, "bow"],
        ["toc 2f spike corridor", "toc torches", False, "boomerang"],
        ["toc torches", "toc torches chest", False, "bow"],
        ["toc torches", "toc pols 2", False, "toc_switch_state"],
        ["toc pols 2", "toc bk room", False, "toc_door_3"],
        ["toc bk room", "toc bk chest", False, "bow"],
        ["toc bk room", "toc before boss", False, "boss_key", "Temple of Courage"],
        ["toc bk chest", "toc before boss", False, "simple_boss_key", "Temple of Courage"],
        ["toc before boss", "toc before boss chest", False, "boom"],
        ["toc before boss", "toc crayk", False, "bow"],

        # ================ Spirit Island =====================

        ["spirit island", "spirit island gauntlet", False, "grapple"],
        ["spirit island", "spirit power 1", False, "spirit_gems", "Power", 10],
        ["spirit island", "spirit power 2", False, "spirit_gems",  "Power", 20],
        ["spirit island", "spirit wisdom 1", False, "spirit_gems",  "Wisdom", 10],
        ["spirit island", "spirit wisdom 2", False, "spirit_gems",  "Wisdom", 20],
        ["spirit island", "spirit courage 1", False, "spirit_gems",  "Courage", 10],
        ["spirit island", "spirit courage 2", False, "spirit_gems",  "Courage", 20],

        # ============ Ocean NW ===============
        ["sw ocean west", "nw ocean", False, "sea_chart", "NW"],
        ["sw ocean east", "nw ocean", False, "frog_n"],
        ["nw ocean", "nw ocean frog n", False, "cannon"],
        ["nw ocean", "gust", True, None],
        ["nw ocean", "bannan", False, None],
        ["nw ocean", "zauz", False, None],
        ["nw ocean", "uncharted", False, None],
        ["nw ocean", "ghost ship", False, "ghost_ship"],
        ["nw ocean", "porl", False, None],
        ["porl", "porl item", False, "sword"],
        ["porl", "porl trade", False, "heroes_new_clothes"],

        # ================= Isle of Gust ====================

        ["gust", "gust combat", False, "cave_damage"],
        ["gust", "gust dig", False, "shovel"],
        ["gust dig", "tow", True, None],

        # ================= Temple of Wind ====================

        ["tow", "tow b1", False, "tow_b1"],
        ["tow b1", "tow b2", False, None],
        ["tow b2", "tow b2 dig", False, "shovel"],
        ["tow b2", "tow b2 bombs", False, "explosives"],
        ["tow b2", "tow b2 key", False, "tow_key"],
        ["tow b2", "tow bk chest", False, "bombs"],
        ["tow", "tow cyclok", False, "tow_cyclok"],
        ["tow cyclok", "post tow", False, None],

        # ================= Bannan Island ====================

        ["bannan", "bannan grapple", False, "grapple"],
        ["bannan", "bannan dig", False, "shovel"],
        ["bannan", "bannan east", False, "bombs"],
        ["bannan east", "bannan east grapple", False, "grapple"],
        ["bannan east grapple", "bannan east grapple dig", False, "shovel"],
        ["bannan east", "bannan cannon game", False, "cannon"],
        ["bannan", "bannan scroll", False, "bannan_scroll"],
        ["bannan", "bannan loovar", False, "loovar"],
        ["bannan", "bannan rsf", False, "rsf"],
        ["bannan", "bannan neptoona", False, "neptoona"],
        ["bannan", "bannan stowfish", False, "stowfish"],
        ["bannan", "bannan letter", False, "jolene_letter"],

        # ================= Zauz's Island ====================

        ["zauz", "zauz dig", False, "shovel"],
        ["zauz", "zauz blade", False, "has_zauz_required_metals"],
        ["ghost ship tetra", "zauz crest", False, None],

        # ================= Uncharted Island ====================

        ["uncharted", "uncharted dig", False, "shovel"],
        ["uncharted", "uncharted cave", False, "sword"],
        ["uncharted cave", "uncharted grapple", False, "grapple"],

        # ================= Ghost Ship ====================

        ["ghost ship", "ghost ship barrel", False, "gs_barrel"],
        ["ghost ship barrel", "ghost ship b2", False, "gs_triangle"],
        ["ghost ship b2", "ghost ship b3", False, None],
        ["ghost ship b3", "ghost ship cubus", False, "sword"],
        ["ghost ship b2", "ghost ship tetra", False, "ghost_key"],
        ["ghost ship tetra", "spawn pirate ambush", False, None],

        # ================= SE Ocean ====================

        ["sw ocean", "se ocean", False, "se_ocean"],
        ["se ocean", "se ocean frogs", False, "cannon"],
        ["se ocean", "goron", False, "can_pass_sea_monsters"],
        ["se ocean", "se ocean trade", False, "kaleidoscope"],
        ["se ocean", "iof", False, "can_pass_sea_monsters"],
        ["se ocean", "harrow", False, "sword"],
        ["se ocean", "ds", False, None],
        ["se ocean", "pirate ambush", False, "beat_gs"],

        # ================= Goron Island ====================

        ["goron", "goron port house", True, None],
        ["goron", "goron chus", False, "goron_chus"],
        ["goron", "goron grapple", False, "grapple"],
        ["goron chus", "goron quiz", False, None],
        ["goron", "goron north", False, None],
        ["goron north", "goron north bombchu", False, "bombchu_switches"],
        ["goron north", "goron outside temple", False, "explosives"],
        ["goron", "goron outside temple", False, "hammer_clip"],
        ["goron outside temple", "goron north", False, "bombs"],
        ["goron outside temple", "gt", True, None],
        ["gt dongo", "goron chief 2", False, "goron_chus"],

        # ================= Goron Temple ====================
        ["gt", "gt 2", False, "goron_entrance"],
        ["gt 2", "gt bow", False, "bow"],
        ["gt 2", "gt b1", False, "gt_b1"],
        ["gt b1", "gt b2", False, "bombchu_switches"],
        ["gt b2", "gt b3", False, None],
        ["gt b2", "gt b2 back", False, "gt_b2_back"],
        ["gt b2 back", "gt bk chest", False, "chus"],
        ["gt b2", "gt dongo", False, "gt_dongo"],

        # ================= Harrow Island ====================

        ["harrow", "harrow dig", False, "shovel"],
        ["harrow dig", "harrow dig 2", False, "sea_chart", "NE"],

        # ================= Dee Ess Island ====================

        ["ds", "ds dig", False, "shovel"],
        ["ds", "ds combat", False, "can_kill_eye_brute"],
        ["gt dongo", "ds race", False, None],

        # ================= Isle of Frost ====================

        ["iof", "iof grapple", False, "grapple"],
        ["iof", "iof smart house", True, None],
        ["iof", "iof dig", False, "shovel"],
        ["iof grapple", "iof grapple dig", False, "shovel"],
        ["iof", "iof yook", False, "damage"],
        ["iof yook", "toi", True, None],

        # ================= Ice Temple ====================

        ["toi", "toi 2f", False, "toi_2f"],
        ["toi 2f", "toi 3f", False, "toi_3f"],
        ["toi 3f", "toi 3f switch", False, "toi_3f_switch"],
        ["toi 3f switch", "toi 3f boomerang", False, "toi_3f_boomerang"],
        ["toi 3f boomerang", "toi 2f miniboss", False, "toi_miniboss"],
        ["toi 3f", "toi 2f miniboss", False, "toi_key_doors", 3, 1],
        ["toi 2f miniboss", "toi side path", False, "grapple"],
        ["toi", "toi side path", False, "toi_shortcut"],
        ["toi side path", "toi b1", False, "toi_b1"],
        ["toi b1", "toi b1 2", False, "explosives"],
        ["toi b1 2", "toi b1 key", False, "toi_key_door_2"],
        ["toi b1 2", "toi b2", False, "toi_b2"],
        ["toi b2", "toi bk chest", False, "hammer_clip"],
        ["toi b2", "toi b2 key", False, "toi_key_door_3"],
        ["toi b2 key", "toi bk chest", False, None],
        ["toi bk chest", "toi gleeok", False, "is_ut"],
        ["toi b2", "toi gleeok", False, "boss_key", "Temple of Ice"],

        # ================= NE Ocean ====================

        ["sw ocean", "ne ocean", False, "frog_square"],
        ["se ocean", "ne ocean", False, "sea_chart", "NE"],
        ["ne ocean", "ne ocean frog", False, "cannon"],
        ["ne ocean", "ne ocean combat", False, "can_kill_blue_chu"],
        ["ne ocean", "iotd", False, None],
        ["ne ocean", "maze", False, "sword"],
        ["ne ocean", "ruins port", False, "regal_necklace"],
        ["ne ocean", "pirate ambush", False, "beat_gs"],

        # ================= IotD ====================

        ["iotd", "iotd rupoor", False, "bombs"],
        ["iotd", "iotd dig", False, "shovel"],
        ["iotd dig", "iotd cave", False, "bombs"],

        # ================= Isle of Ruins ====================

        ["ruins port", "ruins cave", True, None],
        ["ruins cave", "ruins", True, "cave_damage"],
        ["ruins", "ruins dig", False, "shovel"],
        ["ruins", "ruins water", False, "kings_key"],
        ["ruins water", "mutoh", True, None],

        # ================= Mutoh's Temple ====================

        ["mutoh", "mutoh landing", False, "mutoh_entrance"],
        ["mutoh landing", "mutoh hammer", False, "hammer"],
        ["mutoh hammer", "mutoh water", False, "mutoh_water"],
        ["mutoh water", "mutoh bk chest", False, "mutoh_bk_chest"],
        ["mutoh water", "mutoh eox", False, "boss_key", "Mutoh's Temple"],
        ["mutoh bk chest", "mutoh eox", False, "is_ut"],

        # ================= Maze Island ====================

        ["maze", "maze east", False, "explosives"],
        ["maze", "maze normal", False, "bow"],
        ["maze normal", "maze expert", False, "grapple"],
        ["maze", "maze dig", False, "shovel"],

        # ========== Fishing ====================

        ["sw ocean", "fishing", False, "fishing_rod"],
        ["fishing", "fishing bcl", False, "big_catch_lure"],
        ["fishing", "fishing rsf", False, "can_catch_rsf"],
        ["fishing", "fishing shadows", False, "swordfish_shadows"],
        ["fishing", "fishing stowfish", False, "ut_can_stowfish"],

        # ========== Salvage ==============

        ["sw ocean west", "sw ocean west salvage", False, "salvage"],
        ["sw ocean east", "sw ocean east salvage", False, "salvage"],
        ["nw ocean", "nw ocean salvage", False, "salvage"],
        ["se ocean", "se ocean salvage", False, "salvage"],
        ["ne ocean", "ne ocean salvage", False, "salvage"],
        ["ne ocean", "ne ocean inner", False, "regal_necklace"],
        ["ne ocean inner", "ne ocean salvage inner", False, "salvage"],
        ["ne ocean", "nw ocean corner salvage", False, "salvage_behind_bannan"],

        ["sw ocean west salvage", "salvage 1", False, "treasure_map", 1],
        ["sw ocean east salvage", "salvage 2", False, "treasure_map", 2],
        ["nw ocean salvage", "salvage 3", False, "treasure_map", 3],
        ["nw ocean corner salvage", "salvage 4", False, "treasure_map", 4],
        ["sw ocean west salvage", "salvage 5", False, "treasure_map", 5],
        ["nw ocean salvage", "salvage 6", False, "treasure_map", 6],
        ["nw ocean salvage", "salvage 7", False, "treasure_map", 7],
        ["sw ocean east salvage", "salvage 8", False, "treasure_map", 8],
        ["sw ocean east salvage", "salvage 9", False, "treasure_map", 9],
        ["nw ocean salvage", "salvage 10", False, "treasure_map", 10],
        ["nw ocean salvage", "salvage 11", False, "treasure_map", 11],
        ["se ocean salvage", "salvage 12", False, "treasure_map", 12],
        ["se ocean salvage", "salvage 13", False, "treasure_map", 13],
        ["se ocean salvage", "salvage 14", False, "treasure_map", 14],
        ["se ocean salvage", "salvage 15", False, "treasure_map", 15],
        ["se ocean salvage", "salvage 16", False, "treasure_map", 16],
        ["se ocean salvage", "salvage 17", False, "treasure_map", 17],
        ["sw ocean east salvage", "salvage 18", False, "treasure_map", 18],
        ["nw ocean salvage", "salvage 19", False, "treasure_map", 19],
        ["nw ocean corner salvage", "salvage 20", False, "treasure_map", 20],
        ["sw ocean west salvage", "salvage 21", False, "treasure_map", 21],
        ["se ocean salvage", "salvage 22", False, "treasure_map", 22],
        ["se ocean salvage", "salvage 23", False, "treasure_map", 23],
        ["ne ocean salvage", "salvage 24", False, "treasure_map", 24],
        ["ne ocean salvage", "salvage 25", False, "treasure_map", 25],
        ["ne ocean salvage inner", "salvage 26", False, "treasure_map", 26],
        ["ne ocean salvage", "salvage 27", False, "treasure_map", 27],
        ["ne ocean salvage inner", "salvage 28", False, "treasure_map", 28],
        ["ne ocean salvage", "salvage 29", False, "treasure_map", 29],
        ["ne ocean salvage", "salvage 30", False, "treasure_map", 30],
        ["ne ocean salvage", "salvage 31", False, "treasure_map", 31],

        # Goal stuff
        ["sw ocean east", "bellumbeck", False, "bellumbeck_quick_finish"],
        ["bellumbeck", "beat bellumbeck", False, "can_beat_bellumbeck"],
        ["beat bellumbeck", "goal", False, None],
        ["totok midway", "goal", False, "goal_midway"],
        ["mercay island", "goal", False, "win_on_metals"],

    ]

    return overworld_logic


def is_item(item: Item, player: int, item_name: str):
    return item.player == player and item.name == item_name


def create_connections(multiworld: MultiWorld, player: int, origin_name: str, options):
    def create_entrance(r1, r2, *arguments):
        entrance_key = (r1.name, r2.name)
        if rule_lookup:
            rule_func = RULE_DICT[rule_lookup]
            entrance = r1.connect(r2, None, lambda state: rule_func(state, player, *arguments))
        else:
            entrance = r1.connect(r2, None, None)

        if entrance_key in test_entrances:
            # Set entrance data
            entrance_data = ENTRANCES[test_entrances[entrance_key]]
            rando_type_bool = entrance_data.get("two_way", True)
            entrance.randomization_type = EntranceType.TWO_WAY if rando_type_bool else EntranceType.ONE_WAY
            entrance.randomization_group = entrance_data["direction"] | (entrance_data["type"])
            entrance.name = test_entrances[entrance_key]
            multiworld.worlds[player].entrances[entrance.name] = entrance

    all_logic = [
        make_overworld_logic()
    ]

    test_entrances = {(e["entrance_region"], e["exit_region"]): name for name, e in ENTRANCES.items()}

    # Create connections
    for logic_array in all_logic:
        for entrance_desc in logic_array:
            reg1, reg2, is_two_way, rule_lookup, *args = entrance_desc
            region_1 = multiworld.get_region(reg1, player)
            region_2 = multiworld.get_region(reg2, player)

            create_entrance(region_1, region_2, *args)
            if is_two_way:
                create_entrance(region_2, region_1, *args)




