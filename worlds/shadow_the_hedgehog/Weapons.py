from dataclasses import dataclass

from . import Levels


@dataclass
class WeaponInfo:
    game_id: int
    name: str
    available_stages: []
    
    def __init__(self, id, name, stages, attributes):
        self.game_id = id
        self.name = "Weapon:"+name
        self.available_stages = stages
        self.attributes = attributes
        
    
class WeaponAttributes:
    SHOT = 1
    LONG_RANGE = 2
    VACUUM = 4
    TORCH = 8
    NOT_AIMABLE = 16
    HEAL = 32
    SPECIAL = 64
    SHADOW_RIFLE = 128


def GetAnyShadowBoxRegions():
    return [
        Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_GLYPHIC_CANYON,
        Levels.STAGE_LETHAL_HIGHWAY, (Levels.STAGE_CRYPTIC_CASTLE, 1), (Levels.STAGE_PRISON_ISLAND, 1),
        Levels.STAGE_CIRCUS_PARK, Levels.STAGE_CENTRAL_CITY, Levels.STAGE_THE_DOOM,
        Levels.STAGE_SKY_TROOPS, (Levels.STAGE_MAD_MATRIX, 1), Levels.STAGE_DEATH_RUINS,
        (Levels.STAGE_THE_ARK,1), Levels.STAGE_AIR_FLEET, Levels.STAGE_IRON_JUNGLE,
        Levels.STAGE_SPACE_GADGET, Levels.STAGE_LOST_IMPACT, Levels.STAGE_GUN_FORTRESS,
        (Levels.STAGE_BLACK_COMET,1), Levels.STAGE_LAVA_SHELTER, Levels.STAGE_COSMIC_FALL,
        Levels.STAGE_FINAL_HAUNT, Levels.STAGE_THE_LAST_WAY
    ]

def GetRuleByWeaponRequirement(player, req, stage, regions):
    if regions is not None:
        for i in range(0, len(regions)):
            if max(regions) > i:
                regions.append(i)
    elif stage is not None:
        p_regions = [ l.regionIndex for l in Levels.INDIVIDUAL_LEVEL_REGIONS if l.stageId == stage]
        if len(p_regions) == 0:
            regions = []
        else:
            regions = p_regions

    matches_items = [ w for w in WEAPON_INFO if (
            (req is None and len(w.attributes) > 0)
            or req in w.attributes or req == w.name) and
                len([ a for a in w.available_stages
                  if (stage is not None and type(a) is tuple and a[0] == stage and a[1] in regions)
                  or
                      (stage is None)
                  or
                      (stage is not None and type(a) is not tuple and a == stage)
                ]) > 0
                ]

    matches_groups = [ group[0] for group in WeaponGroups.items() if len([ x for x in group[1] if x in
                                                                           [m.game_id for m in matches_items]]) > 0]
    matches = []
    matches.extend([ x.name for x in matches_items])
    matches.extend(matches_groups)

    #print(stage, regions, matches)

    if len(matches) == 0:
        print("Something wrong here with", req, stage, regions)

    return lambda state, reqs=matches: state.has_any([m for m in reqs],player)


class WEAPONS:
    PISTOL = 0x1
    SUB_MACHINE_GUN = 0x2
    SEMI_AUTOMATIC_RIFLE = 0x3
    HEAVY_MACHINE_GUN = 0x4
    GATLING_GUN = 0x5
    EGG_GUN = 0x7
    LIGHT_SHOT = 0x8
    FLASH_SHOT = 0x9
    RING_SHOT = 0xA
    HEAVY_SHOT = 0xB
    GRENADE_LAUNCHER = 0xC
    BAZOOKA = 0xD
    TANK_CANNON = 0xE
    BLACK_BARREL = 0xF
    BIG_BARREL = 0x10
    EGG_BAZOOKA = 0x11
    RPG = 0x12
    FOUR_SHOT_RPG = 0x13
    EIGHT_SHOT_RPG = 0x14
    WORM_SHOOTER = 0x15
    WIDE_WORM_SHOOTER = 0x16
    BIG_WORM_SHOOTER = 0x17
    VACUUM_POD = 0x18
    LASER_RIFLE = 0x19
    SPLITTER = 0x1A
    REFRACTOR = 0x1B
    SURVIVAL_KNIFE = 0x1E
    BLACK_SWORD = 0x1F
    DARK_HAMMER = 0x20
    EGG_SPEAR = 0x21
    SPEED_LIMIT_SIGN = 0x22
    DIGITAL_POLE = 0x23
    CANYON_POLE = 0x24
    LETHAL_POLE = 0x25
    CRYPTIC_TORCH = 0x26
    PRISON_BRANCH = 0x27
    CIRCUS_POLE = 0x28
    STOP_SIGN = 0x29
    DOOM_POLE = 0x2A
    SKY_POLE = 0x2B
    MATRIX_POLE = 0x2C
    RUINS_BRANCH = 0x2D
    FLEET_POLE = 0x2F
    IRON_POLE = 0x30
    GADGET_POLE = 0x31
    IMPACT_POLE = 0x32
    FORTRESS_POLE = 0x33
    LAVA_SHOVEL = 0x35
    COSMIC_POLE = 0x36
    HAUNT_POLE = 0x37
    LAST_POLE = 0x38
    SAMURAI_BLADE = 0x3A
    SATELLITE_GUN = 0x3C
    EGG_VACUUM = 0x3E
    OMOCHAO_GUN = 0x40
    HEAL_CANNON = 0x42
    SHADOW_RIFLE = 0x43


WEAPON_INFO = [
    WeaponInfo(0x1, "Pistol",
               [Levels.STAGE_WESTOPOLIS,Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_PRISON_ISLAND,
                Levels.STAGE_CENTRAL_CITY, Levels.STAGE_THE_DOOM, Levels.STAGE_DEATH_RUINS,
                Levels.STAGE_LOST_IMPACT, Levels.BOSS_BLACK_BULL_DR, Levels.BOSS_DIABLON_GF],
               [WeaponAttributes.SHOT]),
    WeaponInfo(0x2, "Sub Machine Gun",
               [Levels.STAGE_WESTOPOLIS,
                Levels.STAGE_DIGITAL_CIRCUIT,Levels.STAGE_GLYPHIC_CANYON,Levels.STAGE_LETHAL_HIGHWAY,
                Levels.STAGE_PRISON_ISLAND, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_CENTRAL_CITY,
                Levels.STAGE_THE_DOOM, Levels.STAGE_DEATH_RUINS,
                Levels.STAGE_LOST_IMPACT, Levels.BOSS_BLUE_FALCON,
                Levels.BOSS_BLACK_DOOM_GF, Levels.BOSS_BLACK_DOOM_CF],
               [WeaponAttributes.SHOT, WeaponAttributes.LONG_RANGE]),
    WeaponInfo(0x3, "Semi Automatic Rifle",
               [Levels.STAGE_LETHAL_HIGHWAY,
                    Levels.STAGE_PRISON_ISLAND, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_CENTRAL_CITY,
                    Levels.STAGE_THE_DOOM, Levels.STAGE_DEATH_RUINS,
                    Levels.STAGE_THE_ARK, Levels.STAGE_AIR_FLEET, Levels.STAGE_IRON_JUNGLE, Levels.STAGE_SPACE_GADGET, Levels.STAGE_LOST_IMPACT,
                    Levels.STAGE_GUN_FORTRESS, Levels.STAGE_COSMIC_FALL,
                Levels.BOSS_BLACK_DOOM_CF],
               [WeaponAttributes.SHOT, WeaponAttributes.LONG_RANGE]),
    WeaponInfo(0x4, "Heavy Machine Gun",
               [Levels.STAGE_CIRCUS_PARK, (Levels.STAGE_CENTRAL_CITY,1), Levels.STAGE_THE_DOOM, Levels.STAGE_IRON_JUNGLE,
                (Levels.STAGE_THE_ARK,1),Levels.STAGE_AIR_FLEET,Levels.STAGE_SPACE_GADGET,
                Levels.STAGE_GUN_FORTRESS,(Levels.STAGE_BLACK_COMET,1),Levels.STAGE_COSMIC_FALL,
                Levels.BOSS_EGG_BREAKER_IJ],
               [WeaponAttributes.SHOT, WeaponAttributes.LONG_RANGE]),
    WeaponInfo(0x5, "Gatling Gun",
               [(Levels.STAGE_LETHAL_HIGHWAY, 1),
                   (Levels.STAGE_THE_ARK,1),Levels.STAGE_IRON_JUNGLE, Levels.STAGE_GUN_FORTRESS,
                (Levels.STAGE_BLACK_COMET,1)],
               [WeaponAttributes.SHOT, WeaponAttributes.LONG_RANGE]),
    WeaponInfo(0x7, "Egg Gun",
               [(Levels.STAGE_CRYPTIC_CASTLE,1), Levels.STAGE_CIRCUS_PARK, Levels.STAGE_SKY_TROOPS,
                Levels.STAGE_MAD_MATRIX, Levels.STAGE_IRON_JUNGLE, Levels.STAGE_LAVA_SHELTER,
                Levels.BOSS_EGG_BREAKER_CC, Levels.BOSS_EGG_BREAKER_MM,
                Levels.BOSS_EGG_BREAKER_IJ, Levels.BOSS_EGG_DEALER_BC,
                Levels.BOSS_EGG_DEALER_LS, Levels.BOSS_EGG_DEALER_CF],
        [WeaponAttributes.SHOT, WeaponAttributes.LONG_RANGE]),
    WeaponInfo(0x8, "Light Shot",
                [Levels.STAGE_WESTOPOLIS,
                Levels.STAGE_DIGITAL_CIRCUIT,Levels.STAGE_LETHAL_HIGHWAY,
                 (Levels.STAGE_CRYPTIC_CASTLE,2), Levels.STAGE_PRISON_ISLAND,
                Levels.STAGE_CENTRAL_CITY, Levels.STAGE_DEATH_RUINS,
                 Levels.STAGE_SPACE_GADGET,
                 Levels.BOSS_BLACK_BULL_LH, Levels.BOSS_BLACK_BULL_DR, Levels.BOSS_DIABLON_BC],
            [WeaponAttributes.SHOT]),
    WeaponInfo(0x9, "Flash Shot",
               [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON,
                Levels.STAGE_LETHAL_HIGHWAY, (Levels.STAGE_CRYPTIC_CASTLE,1),
                Levels.STAGE_PRISON_ISLAND, Levels.STAGE_CENTRAL_CITY,
                Levels.STAGE_DEATH_RUINS, Levels.STAGE_SPACE_GADGET,
                Levels.STAGE_BLACK_COMET, Levels.BOSS_DIABLON_BC, Levels.BOSS_BLACK_BULL_LH,
               Levels.BOSS_DIABLON_FH, Levels.BOSS_BLACK_DOOM_FH],
               [WeaponAttributes.SHOT]),
    WeaponInfo(0xA, "Ring Shot",
           [Levels.STAGE_SKY_TROOPS, Levels.STAGE_SPACE_GADGET,
                Levels.STAGE_FINAL_HAUNT, Levels.BOSS_DIABLON_BC,
            Levels.BOSS_DIABLON_FH, Levels.BOSS_BLACK_DOOM_FH,
            Levels.STAGE_THE_LAST_WAY],
[WeaponAttributes.SHOT]),
    WeaponInfo(0xB, "Heavy Shot",
               [(Levels.STAGE_FINAL_HAUNT,1),
                (Levels.STAGE_THE_LAST_WAY,1)],
               [WeaponAttributes.SHOT]),
    WeaponInfo(0xC, "Grenade Launcher",
               [Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_THE_DOOM,Levels.STAGE_DEATH_RUINS,
                (Levels.STAGE_SPACE_GADGET,1), Levels.STAGE_LOST_IMPACT, Levels.BOSS_BLACK_DOOM_GF],
    [WeaponAttributes.NOT_AIMABLE]),
    WeaponInfo(0xD, "Bazooka",
               [Levels.STAGE_CENTRAL_CITY, Levels.STAGE_DEATH_RUINS,
                (Levels.STAGE_BLACK_COMET, 1), Levels.STAGE_COSMIC_FALL,
                Levels.BOSS_BLACK_DOOM_CF],
[WeaponAttributes.NOT_AIMABLE]),
    WeaponInfo(0xE, "Tank Cannon",
               [(Levels.STAGE_PRISON_ISLAND, 2), (Levels.STAGE_IRON_JUNGLE,1),
                (Levels.STAGE_BLACK_COMET, 2)],
[WeaponAttributes.NOT_AIMABLE]),
    WeaponInfo(0xF, "Black Barrel",
               [Levels.STAGE_SKY_TROOPS, (Levels.STAGE_SPACE_GADGET, 1),
    (Levels.STAGE_BLACK_COMET,1), Levels.STAGE_FINAL_HAUNT,Levels.STAGE_THE_LAST_WAY],
[WeaponAttributes.NOT_AIMABLE]),
    WeaponInfo(0x10, "Big Barrel",
               [Levels.STAGE_COSMIC_FALL,(Levels.STAGE_FINAL_HAUNT,1),
                Levels.BOSS_BLACK_DOOM_FH,Levels.STAGE_THE_LAST_WAY],
[WeaponAttributes.NOT_AIMABLE]),
    WeaponInfo(0x11, "Egg Bazooka",
               [(Levels.STAGE_CRYPTIC_CASTLE, 1), Levels.STAGE_CIRCUS_PARK, Levels.STAGE_SKY_TROOPS,
                (Levels.STAGE_MAD_MATRIX,1), Levels.STAGE_IRON_JUNGLE, Levels.STAGE_LAVA_SHELTER,
                Levels.BOSS_EGG_BREAKER_MM, Levels.BOSS_EGG_BREAKER_IJ,
                Levels.BOSS_EGG_DEALER_BC, Levels.BOSS_EGG_DEALER_LS, Levels.BOSS_EGG_DEALER_CF],
[WeaponAttributes.NOT_AIMABLE]),
    WeaponInfo(0x12, "RPG",
               [Levels.STAGE_THE_DOOM,
                Levels.STAGE_THE_ARK,
                Levels.STAGE_GUN_FORTRESS],
[WeaponAttributes.NOT_AIMABLE]),
    WeaponInfo(0x13, "4-Shot RPG",
               [(Levels.STAGE_THE_ARK,1), Levels.STAGE_IRON_JUNGLE, Levels.STAGE_SPACE_GADGET,
                Levels.BOSS_HEAVY_DOG, Levels.BOSS_BLUE_FALCON,
                Levels.BOSS_BLACK_DOOM_GF, Levels.BOSS_BLACK_DOOM_CF],
[WeaponAttributes.NOT_AIMABLE]),
    WeaponInfo(0x14, "8-Shot RPG",
               [Levels.STAGE_GUN_FORTRESS, (Levels.STAGE_BLACK_COMET,1)],
[WeaponAttributes.NOT_AIMABLE]),
    WeaponInfo(0x15, "Worm Shooter",
               [Levels.STAGE_DIGITAL_CIRCUIT,Levels.STAGE_GLYPHIC_CANYON,
                (Levels.STAGE_PRISON_ISLAND,1), (Levels.STAGE_MAD_MATRIX, 1), Levels.STAGE_DEATH_RUINS,
                (Levels.STAGE_SPACE_GADGET, 1)],
[WeaponAttributes.NOT_AIMABLE]),
    WeaponInfo(0x16, "Wide Worm Shooter",
               [(Levels.STAGE_MAD_MATRIX, 1), (Levels.STAGE_BLACK_COMET,1),
                Levels.STAGE_THE_LAST_WAY],
[WeaponAttributes.NOT_AIMABLE]),
    WeaponInfo(0x17, "Big Worm Shooter",
               [(Levels.STAGE_BLACK_COMET,1),
                (Levels.STAGE_THE_LAST_WAY,1)],
[WeaponAttributes.NOT_AIMABLE]),
    WeaponInfo(0x18, "Vacuum Pod",
               [Levels.STAGE_CENTRAL_CITY, (Levels.STAGE_SPACE_GADGET,1), Levels.STAGE_FINAL_HAUNT],
[WeaponAttributes.VACUUM]),
    WeaponInfo(0x19, "Laser Rifle",
               [(Levels.STAGE_BLACK_COMET,1)],
[WeaponAttributes.SHOT, WeaponAttributes.LONG_RANGE]),
    WeaponInfo(0x1A, "Splitter",
               [Levels.STAGE_DEATH_RUINS, Levels.STAGE_AIR_FLEET,(Levels.STAGE_SPACE_GADGET, 1), Levels.STAGE_GUN_FORTRESS],
[WeaponAttributes.SHOT]),
    WeaponInfo(0x1B, "Refractor",
               [(Levels.STAGE_BLACK_COMET,1),Levels.STAGE_FINAL_HAUNT,
                Levels.BOSS_BLACK_DOOM_FH, Levels.STAGE_THE_LAST_WAY],
[WeaponAttributes.SHOT, WeaponAttributes.LONG_RANGE]),
    WeaponInfo(0x1E, "Survival Knife",
               [Levels.STAGE_THE_DOOM],
[]),
    WeaponInfo(0x1F, "Black Sword",
               [Levels.STAGE_DIGITAL_CIRCUIT,Levels.STAGE_GLYPHIC_CANYON,
                (Levels.STAGE_CRYPTIC_CASTLE,1),(Levels.STAGE_PRISON_ISLAND,1), Levels.STAGE_CENTRAL_CITY,
                Levels.STAGE_SKY_TROOPS, Levels.STAGE_AIR_FLEET,
                Levels.STAGE_FINAL_HAUNT, Levels.STAGE_THE_LAST_WAY],
[]),
    WeaponInfo(0x20, "Dark Hammer",
               [Levels.STAGE_FINAL_HAUNT,
                (Levels.STAGE_THE_LAST_WAY,1)],
[]),
    WeaponInfo(0x21, "Egg Spear",
               [Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_CIRCUS_PARK, (Levels.STAGE_SKY_TROOPS,1),
                Levels.STAGE_MAD_MATRIX, Levels.STAGE_IRON_JUNGLE, Levels.STAGE_LAVA_SHELTER,
                Levels.BOSS_EGG_DEALER_BC, Levels.BOSS_EGG_DEALER_LS,
                Levels.BOSS_EGG_DEALER_CF],
[]),

    WeaponInfo(0x22, "Speed Limit Sign",
                   [Levels.STAGE_WESTOPOLIS],
    []),

    WeaponInfo(0x23, "Digital Pole",
               [Levels.STAGE_DIGITAL_CIRCUIT],
[]),
    WeaponInfo(0x24, "Canyon Pole",
               [Levels.STAGE_GLYPHIC_CANYON],
[]),

    WeaponInfo(0x25, "Lethal Pole",
               [Levels.STAGE_LETHAL_HIGHWAY],
[]),

    WeaponInfo(0x26, "Cryptic Torch",
               [Levels.STAGE_CRYPTIC_CASTLE],
            [WeaponAttributes.TORCH]),
    WeaponInfo(0x27, "Prison Branch",
               [Levels.STAGE_PRISON_ISLAND],
[]),
    WeaponInfo(0x28, "Circus Pole",
               [Levels.STAGE_CIRCUS_PARK],
[]),

 WeaponInfo(0x29, "Stop Sign",
               [Levels.STAGE_CENTRAL_CITY],
[]),

    WeaponInfo(0x2A, "Doom Pole",
               [Levels.STAGE_THE_DOOM],
[]),

    WeaponInfo(0x2B, "Sky Pole",
               [Levels.STAGE_SKY_TROOPS],
[]),

    WeaponInfo(0x2C, "Matrix Pole",
               [(Levels.STAGE_MAD_MATRIX, 1)], []),

    WeaponInfo(0x2D, "Ruins Branch",
               [Levels.STAGE_DEATH_RUINS],
[]),
    WeaponInfo(0x2F, "Fleet Pole",
               [Levels.STAGE_AIR_FLEET],
[]),
    WeaponInfo(0x30, "Iron Pole",
               [Levels.STAGE_IRON_JUNGLE],
[]),
    WeaponInfo(0x31, "Gadget Pole",
               [Levels.STAGE_SPACE_GADGET],
[]),
    WeaponInfo(0x32, "Impact Pole",
               [Levels.STAGE_LOST_IMPACT],
[]),
    WeaponInfo(0x33, "Fortress Pole",
               [Levels.STAGE_GUN_FORTRESS],
[]),

    WeaponInfo(0x35, "Lava Shovel",
               [Levels.STAGE_LAVA_SHELTER],
[]),
    WeaponInfo(0x36, "Cosmic Pole",
               [Levels.STAGE_COSMIC_FALL],
[]),
    WeaponInfo(0x37, "Haunt Pole",
               [Levels.STAGE_FINAL_HAUNT],
[]),
    WeaponInfo(0x38, "Last Pole",
               [Levels.STAGE_THE_LAST_WAY],
[]),

    WeaponInfo(0x3A, "Samurai Blade",
               GetAnyShadowBoxRegions(),
[WeaponAttributes.SPECIAL]),
    WeaponInfo(0x3C, "Satellite Gun",
               GetAnyShadowBoxRegions(),
[WeaponAttributes.SPECIAL, WeaponAttributes.NOT_AIMABLE]),
    WeaponInfo(0x3E, "Egg Vacuum",
               GetAnyShadowBoxRegions(),
[WeaponAttributes.SPECIAL, WeaponAttributes.VACUUM]),
    WeaponInfo(0x40, "Omochao Gun",
               GetAnyShadowBoxRegions(),
[WeaponAttributes.SPECIAL, WeaponAttributes.SHOT, WeaponAttributes.LONG_RANGE]),
    WeaponInfo(0x42, "Heal Cannon",
               GetAnyShadowBoxRegions(),
[WeaponAttributes.SPECIAL, WeaponAttributes.HEAL]),
    WeaponInfo(0x43, "Shadow Rifle",
               GetAnyShadowBoxRegions(),
[WeaponAttributes.SPECIAL, WeaponAttributes.SHOT, WeaponAttributes.LONG_RANGE, WeaponAttributes.SHADOW_RIFLE])
]

def GetWeaponDict():
    weapon_dict = {}
    for weapon in WEAPON_INFO:
        weapon_dict[weapon.name] = weapon

    return weapon_dict

def GetWeaponDictById():
    weapon_dict = {}
    for weapon in WEAPON_INFO:
        weapon_dict[weapon.game_id] = weapon

    return weapon_dict

def GetWeaponGroupsDict():
    weapons = GetWeaponDictById()
    weapon_groups_dict = {}
    for group in WeaponGroups.items():
        weapon_groups_dict[group[0]] = []
        for item in group[1]:
            weapon_item = weapons[item]
            weapon_groups_dict[group[0]].append(weapon_item)

    return weapon_groups_dict


def GetWeaponByStageDict():
    stages_dict = {}
    for Weapon in WEAPON_INFO:
        for stage in Weapon.available_stages:
            stage_n = stage if type(stage) is int else stage[0]
            if stage_n not in stages_dict:
                stages_dict[stage_n] = []
            if WeaponAttributes.SPECIAL in Weapon.attributes:
                continue
            stages_dict[stage_n].append(Weapon.game_id)

    return stages_dict

def WeaponInfoByWeapon():
    stages_dict = {}
    for Weapon in WEAPON_INFO:
        print("###", Weapon.name.replace("Weapon:", ""), ":", Weapon.game_id, "\n * ",
              "\n * ".join([ Levels.LEVEL_ID_TO_LEVEL[x] if type(x) is int else Levels.LEVEL_ID_TO_LEVEL[x[0]]+"-"+str(x[1])
                for x in Weapon.available_stages]), "\n\n")
        for stage in Weapon.available_stages:
            stage_n = Levels.LEVEL_ID_TO_LEVEL[stage] if type(stage) is int else Levels.LEVEL_ID_TO_LEVEL[stage[0]]+"-"+str(stage[1])
            if stage_n not in stages_dict:
                stages_dict[stage_n] = []
            if WeaponAttributes.SPECIAL in Weapon.attributes:
                continue
            stages_dict[stage_n].append(Weapon)

    to_order = []
    for stage,weapons in stages_dict.items():
        to_order.append((stage, weapons))

    inv_map = {v: k for k, v in Levels.LEVEL_ID_TO_LEVEL.items()}
    to_order.sort(key= lambda x: inv_map[x[0].split("-")[0]])

    for stage,weapons in to_order:
        print("### ", stage, "\n *", "\n * ".join([w.name.replace("Weapon:", "") for w in weapons]), "\n\n")


    pass

#WeaponInfoByWeapon()

def GetWeaponByName(name):
    weapon = [ w for w in WEAPON_INFO if w.name == name]
    if len(weapon)  == 0:
        return None

    return weapon[0]

WeaponGroups = {

    "Stage Melee Weapons": [WEAPONS.SPEED_LIMIT_SIGN, WEAPONS.DIGITAL_POLE, WEAPONS.CANYON_POLE, WEAPONS.LETHAL_POLE,
                    WEAPONS.PRISON_BRANCH, WEAPONS.CIRCUS_POLE, WEAPONS.STOP_SIGN, WEAPONS.DOOM_POLE,
                    WEAPONS.SKY_POLE, WEAPONS.MATRIX_POLE, WEAPONS.RUINS_BRANCH, WEAPONS.FLEET_POLE,
                    WEAPONS.IRON_POLE, WEAPONS.GADGET_POLE, WEAPONS.IMPACT_POLE, WEAPONS.FORTRESS_POLE,
                    WEAPONS.LAVA_SHOVEL, WEAPONS.COSMIC_POLE, WEAPONS.HAUNT_POLE, WEAPONS.LAST_POLE],

    "Environment Weapons": [WEAPONS.SPEED_LIMIT_SIGN, WEAPONS.DIGITAL_POLE, WEAPONS.CANYON_POLE, WEAPONS.LETHAL_POLE,
                    WEAPONS.PRISON_BRANCH, WEAPONS.CIRCUS_POLE, WEAPONS.STOP_SIGN, WEAPONS.DOOM_POLE,
                    WEAPONS.SKY_POLE, WEAPONS.MATRIX_POLE, WEAPONS.RUINS_BRANCH, WEAPONS.FLEET_POLE,
                    WEAPONS.IRON_POLE, WEAPONS.GADGET_POLE, WEAPONS.IMPACT_POLE, WEAPONS.FORTRESS_POLE,
                    WEAPONS.LAVA_SHOVEL, WEAPONS.COSMIC_POLE, WEAPONS.HAUNT_POLE, WEAPONS.LAST_POLE, WEAPONS.CRYPTIC_TORCH],

    "Egg Pawn Weapons": [WEAPONS.EGG_GUN, WEAPONS.EGG_SPEAR, WEAPONS.EGG_BAZOOKA],

    "GUN Launcher Weapons": [WEAPONS.RPG, WEAPONS.FOUR_SHOT_RPG, WEAPONS.EIGHT_SHOT_RPG, WEAPONS.BAZOOKA,
                             WEAPONS.TANK_CANNON],

    "Black Warrior Weapons": [WEAPONS.FLASH_SHOT, WEAPONS.LIGHT_SHOT, WEAPONS.HEAVY_SHOT, WEAPONS.RING_SHOT,
                              WEAPONS.BLACK_SWORD],

    "Black Oak Weapons": [WEAPONS.BLACK_SWORD, WEAPONS.BLACK_BARREL, WEAPONS.BIG_BARREL,
                          WEAPONS.DARK_HAMMER],

    "Worm Weapons": [WEAPONS.WORM_SHOOTER, WEAPONS.WIDE_WORM_SHOOTER, WEAPONS.BIG_WORM_SHOOTER],

    "Gun Solider Weapons": [WEAPONS.PISTOL, WEAPONS.GRENADE_LAUNCHER, WEAPONS.SURVIVAL_KNIFE,
                            WEAPONS.SUB_MACHINE_GUN],

    "Gun Mech Weapons": [WEAPONS.SEMI_AUTOMATIC_RIFLE, WEAPONS.LASER_RIFLE, WEAPONS.HEAVY_MACHINE_GUN,
                         WEAPONS.SUB_MACHINE_GUN, WEAPONS.GATLING_GUN],

    "Laser Weapons": [WEAPONS.REFRACTOR, WEAPONS.LASER_RIFLE, WEAPONS.SPLITTER, WEAPONS.RING_SHOT],

    "Standard Melee Weapons": [WEAPONS.SURVIVAL_KNIFE, WEAPONS.BLACK_SWORD, WEAPONS.DARK_HAMMER],

    "All Melee Weapons": [WEAPONS.SPEED_LIMIT_SIGN, WEAPONS.DIGITAL_POLE, WEAPONS.CANYON_POLE, WEAPONS.LETHAL_POLE,
                    WEAPONS.PRISON_BRANCH, WEAPONS.CIRCUS_POLE, WEAPONS.STOP_SIGN, WEAPONS.DOOM_POLE,
                    WEAPONS.SKY_POLE, WEAPONS.MATRIX_POLE, WEAPONS.RUINS_BRANCH, WEAPONS.FLEET_POLE,
                    WEAPONS.IRON_POLE, WEAPONS.GADGET_POLE, WEAPONS.IMPACT_POLE, WEAPONS.FORTRESS_POLE,
                    WEAPONS.LAVA_SHOVEL, WEAPONS.COSMIC_POLE, WEAPONS.HAUNT_POLE, WEAPONS.LAST_POLE, WEAPONS.CRYPTIC_TORCH,
                          WEAPONS.SURVIVAL_KNIFE, WEAPONS.BLACK_SWORD, WEAPONS.DARK_HAMMER]




}
