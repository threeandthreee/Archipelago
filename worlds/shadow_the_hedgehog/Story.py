from dataclasses import dataclass

from . import Levels

@dataclass
class PathInfo:
    start_stage_id: int
    alignment_id: int
    end_stage_id: int
    cutscenes: []
    boss = None

    def __init__(self, o_id, alignment, n_id, cutscenes):
        self.start_stage_id = o_id
        self.alignment_id = alignment
        self.end_stage_id = n_id
        self.cutscenes = cutscenes

    def via_boss(self, boss):
        self.boss = boss
        return self


StoryMode = \
[
    PathInfo(None, None, Levels.STAGE_WESTOPOLIS, []),

    PathInfo(Levels.STAGE_WESTOPOLIS, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_DIGITAL_CIRCUIT, []),
    PathInfo(Levels.STAGE_WESTOPOLIS, Levels.MISSION_ALIGNMENT_NEUTRAL, Levels.STAGE_GLYPHIC_CANYON, []),
    PathInfo(Levels.STAGE_WESTOPOLIS, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_LETHAL_HIGHWAY, [])
    ,
    PathInfo(Levels.STAGE_DIGITAL_CIRCUIT, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_CRYPTIC_CASTLE, []),
    PathInfo(Levels.STAGE_DIGITAL_CIRCUIT, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_PRISON_ISLAND, []),

    PathInfo(Levels.STAGE_GLYPHIC_CANYON, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_CRYPTIC_CASTLE, []),
    PathInfo(Levels.STAGE_GLYPHIC_CANYON, Levels.MISSION_ALIGNMENT_NEUTRAL, Levels.STAGE_PRISON_ISLAND, []),
    PathInfo(Levels.STAGE_GLYPHIC_CANYON, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_CIRCUS_PARK, []),

    PathInfo(Levels.STAGE_LETHAL_HIGHWAY, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_PRISON_ISLAND, [])
        .via_boss(Levels.BOSS_BLACK_BULL_LH),
    PathInfo(Levels.STAGE_LETHAL_HIGHWAY, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_CIRCUS_PARK, [])
        .via_boss(Levels.BOSS_BLACK_BULL_LH),

    PathInfo(Levels.STAGE_CRYPTIC_CASTLE, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_CENTRAL_CITY, [])
        .via_boss(Levels.BOSS_EGG_BREAKER_CC),
    PathInfo(Levels.STAGE_CRYPTIC_CASTLE, Levels.MISSION_ALIGNMENT_NEUTRAL, Levels.STAGE_THE_DOOM, [])
        .via_boss(Levels.BOSS_EGG_BREAKER_CC),
    PathInfo(Levels.STAGE_CRYPTIC_CASTLE, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_SKY_TROOPS, [])
        .via_boss(Levels.BOSS_EGG_BREAKER_CC),

    PathInfo(Levels.STAGE_PRISON_ISLAND, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_THE_DOOM, []),
    PathInfo(Levels.STAGE_PRISON_ISLAND, Levels.MISSION_ALIGNMENT_NEUTRAL, Levels.STAGE_SKY_TROOPS, []),
    PathInfo(Levels.STAGE_PRISON_ISLAND, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_MAD_MATRIX, []),

    PathInfo(Levels.STAGE_CIRCUS_PARK, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_SKY_TROOPS, []),
    PathInfo(Levels.STAGE_CIRCUS_PARK, Levels.MISSION_ALIGNMENT_NEUTRAL, Levels.STAGE_MAD_MATRIX, []),
    PathInfo(Levels.STAGE_CIRCUS_PARK, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_DEATH_RUINS, []),

    PathInfo(Levels.STAGE_CENTRAL_CITY, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_THE_ARK, []),
    PathInfo(Levels.STAGE_CENTRAL_CITY, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_AIR_FLEET, []),

    PathInfo(Levels.STAGE_THE_DOOM, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_THE_ARK, [])
        .via_boss(Levels.BOSS_HEAVY_DOG),
    PathInfo(Levels.STAGE_THE_DOOM, Levels.MISSION_ALIGNMENT_NEUTRAL, Levels.STAGE_AIR_FLEET, [])
        .via_boss(Levels.BOSS_HEAVY_DOG),
    PathInfo(Levels.STAGE_THE_DOOM, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_IRON_JUNGLE, [])
        .via_boss(Levels.BOSS_HEAVY_DOG),

    PathInfo(Levels.STAGE_SKY_TROOPS, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_AIR_FLEET, []),
    PathInfo(Levels.STAGE_SKY_TROOPS, Levels.MISSION_ALIGNMENT_NEUTRAL, Levels.STAGE_IRON_JUNGLE, []),
    PathInfo(Levels.STAGE_SKY_TROOPS, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_SPACE_GADGET, []),

    PathInfo(Levels.STAGE_MAD_MATRIX, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_IRON_JUNGLE, [])
        .via_boss(Levels.BOSS_EGG_BREAKER_MM),
    PathInfo(Levels.STAGE_MAD_MATRIX, Levels.MISSION_ALIGNMENT_NEUTRAL, Levels.STAGE_SPACE_GADGET, [])
        .via_boss(Levels.BOSS_EGG_BREAKER_MM),
    PathInfo(Levels.STAGE_MAD_MATRIX, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_LOST_IMPACT, [])
        .via_boss(Levels.BOSS_EGG_BREAKER_MM),

    PathInfo(Levels.STAGE_DEATH_RUINS, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_SPACE_GADGET, [])
        .via_boss(Levels.BOSS_BLACK_BULL_DR),
    PathInfo(Levels.STAGE_DEATH_RUINS, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_LOST_IMPACT, [])
        .via_boss(Levels.BOSS_BLACK_BULL_DR),

    PathInfo(Levels.STAGE_THE_ARK, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_GUN_FORTRESS, [])
        .via_boss(Levels.BOSS_BLUE_FALCON),
    PathInfo(Levels.STAGE_THE_ARK, Levels.MISSION_ALIGNMENT_NEUTRAL, Levels.STAGE_BLACK_COMET, [])
        .via_boss(Levels.BOSS_BLUE_FALCON),

    PathInfo(Levels.STAGE_AIR_FLEET, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_GUN_FORTRESS, []),
    PathInfo(Levels.STAGE_AIR_FLEET, Levels.MISSION_ALIGNMENT_NEUTRAL, Levels.STAGE_BLACK_COMET, []),
    PathInfo(Levels.STAGE_AIR_FLEET, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_LAVA_SHELTER, []),

    PathInfo(Levels.STAGE_IRON_JUNGLE, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_BLACK_COMET, [])
        .via_boss(Levels.BOSS_EGG_BREAKER_IJ),
    PathInfo(Levels.STAGE_IRON_JUNGLE, Levels.MISSION_ALIGNMENT_NEUTRAL, Levels.STAGE_LAVA_SHELTER, [])
        .via_boss(Levels.BOSS_EGG_BREAKER_IJ),
    PathInfo(Levels.STAGE_IRON_JUNGLE, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_COSMIC_FALL, [])
        .via_boss(Levels.BOSS_EGG_BREAKER_IJ),

    PathInfo(Levels.STAGE_SPACE_GADGET, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_LAVA_SHELTER, []),
    PathInfo(Levels.STAGE_SPACE_GADGET, Levels.MISSION_ALIGNMENT_NEUTRAL, Levels.STAGE_COSMIC_FALL, []),
    PathInfo(Levels.STAGE_SPACE_GADGET, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_FINAL_HAUNT, []),

    PathInfo(Levels.STAGE_LOST_IMPACT, Levels.MISSION_ALIGNMENT_NEUTRAL, Levels.STAGE_COSMIC_FALL, []),
    PathInfo(Levels.STAGE_LOST_IMPACT, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_FINAL_HAUNT, []),

    PathInfo(Levels.STAGE_GUN_FORTRESS, Levels.MISSION_ALIGNMENT_DARK, None, [])
        .via_boss(Levels.BOSS_DIABLON_GF),
    PathInfo(Levels.STAGE_GUN_FORTRESS, Levels.MISSION_ALIGNMENT_HERO, None, [])
        .via_boss(Levels.BOSS_BLACK_DOOM_GF),

    PathInfo(Levels.STAGE_BLACK_COMET, Levels.MISSION_ALIGNMENT_DARK, None, [])
        .via_boss(Levels.BOSS_DIABLON_BC),
    PathInfo(Levels.STAGE_BLACK_COMET, Levels.MISSION_ALIGNMENT_HERO, None, [])
        .via_boss(Levels.BOSS_EGG_DEALER_BC),

    PathInfo(Levels.STAGE_LAVA_SHELTER, Levels.MISSION_ALIGNMENT_DARK, None, [])
        .via_boss(Levels.BOSS_EGG_DEALER_LS),
    PathInfo(Levels.STAGE_LAVA_SHELTER, Levels.MISSION_ALIGNMENT_HERO, None, [])
        .via_boss(Levels.BOSS_EGG_DEALER_LS),

    PathInfo(Levels.STAGE_COSMIC_FALL, Levels.MISSION_ALIGNMENT_DARK, None, [])
        .via_boss(Levels.BOSS_EGG_DEALER_CF),
    PathInfo(Levels.STAGE_COSMIC_FALL, Levels.MISSION_ALIGNMENT_HERO, None, [])
        .via_boss(Levels.BOSS_BLACK_DOOM_CF),

    PathInfo(Levels.STAGE_FINAL_HAUNT, Levels.MISSION_ALIGNMENT_DARK, None, [])
        .via_boss(Levels.BOSS_DIABLON_FH),
    PathInfo(Levels.STAGE_FINAL_HAUNT, Levels.MISSION_ALIGNMENT_HERO, None, [])
        .via_boss(Levels.BOSS_BLACK_DOOM_FH),

]