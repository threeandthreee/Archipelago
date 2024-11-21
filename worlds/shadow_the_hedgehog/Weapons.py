from dataclasses import dataclass

from . import Levels, Regions


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


def GetAnyShadowBoxRegions():
    return [
        Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_GLYPHIC_CANYON,
        Levels.STAGE_LETHAL_HIGHWAY, (Levels.STAGE_CRYPTIC_CASTLE, 1), (Levels.STAGE_PRISON_ISLAND, 1),
        Levels.STAGE_CIRCUS_PARK, Levels.STAGE_CENTRAL_CITY, Levels.STAGE_THE_DOOM,
        Levels.STAGE_SKY_TROOPS, (Levels.STAGE_MAD_MATRIX, 1), Levels.STAGE_DEATH_RUINS,
        (Levels.STAGE_THE_ARK,1), Levels.STAGE_AIR_FLEET, Levels.STAGE_IRON_JUNGLE,
        Levels.STAGE_SPACE_GADGET, Levels.STAGE_LOST_IMPACT, Levels.STAGE_GUN_FORTRESS,
        (Levels.STAGE_BLACK_COMET,1), Levels.STAGE_LAVA_SHELTER, Levels.STAGE_COSMIC_FALL,
        Levels.STAGE_FINAL_HAUNT
    ]

def GetRuleByWeaponRequirement(player, req, stage, regions):
    if regions is not None:
        for i in range(0, len(regions)):
            if max(regions) > i:
                regions.append(i)
    else:
        p_regions = [ l.regionIndex for l in Levels.INDIVIDUAL_LEVEL_REGIONS if l.stageId == stage]
        if len(p_regions) == 0:
            regions = []
        else:
            regions = p_regions

    matches = [ w for w in WEAPON_INFO if req in w.attributes and
                len([ a for a in w.available_stages
                  if (type(a) is tuple and a[0] == stage and a[1] in regions)
                  or
                  a == stage
                ]) > 0
                ]

    if len(matches) == 0:
        print("Something wrong here with", req, stage, regions)

    return lambda state, match=matches: state.has_any([m.name for m in matches],player)



WEAPON_INFO = [
    WeaponInfo(0x1, "Pistol",
               [Levels.STAGE_WESTOPOLIS,Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_CENTRAL_CITY,
                Levels.STAGE_THE_DOOM, Levels.STAGE_DEATH_RUINS,
                Levels.STAGE_IRON_JUNGLE],
               [WeaponAttributes.SHOT]),
    WeaponInfo(0x2, "Sub Machine Gun",
               [Levels.STAGE_WESTOPOLIS,
                Levels.STAGE_DIGITAL_CIRCUIT,Levels.STAGE_GLYPHIC_CANYON,Levels.STAGE_LETHAL_HIGHWAY,
                Levels.STAGE_PRISON_ISLAND, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_CENTRAL_CITY,
                Levels.STAGE_THE_DOOM, Levels.STAGE_DEATH_RUINS,
                Levels.STAGE_LOST_IMPACT],
               [WeaponAttributes.SHOT, WeaponAttributes.LONG_RANGE]),
    WeaponInfo(0x3, "Semi Automatic Rifle",
               [Levels.STAGE_LETHAL_HIGHWAY,
                    Levels.STAGE_PRISON_ISLAND, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_CENTRAL_CITY,
                    Levels.STAGE_THE_DOOM, Levels.STAGE_DEATH_RUINS,
                    Levels.STAGE_THE_ARK, Levels.STAGE_AIR_FLEET,Levels.STAGE_SPACE_GADGET, Levels.STAGE_LOST_IMPACT,
                    Levels.STAGE_GUN_FORTRESS, Levels.STAGE_COSMIC_FALL],
               [WeaponAttributes.SHOT, WeaponAttributes.LONG_RANGE]),
    WeaponInfo(0x4, "Heavy Machine Gun",
               [Levels.STAGE_CIRCUS_PARK, (Levels.STAGE_CENTRAL_CITY,1), Levels.STAGE_THE_DOOM, Levels.STAGE_IRON_JUNGLE,
                (Levels.STAGE_THE_ARK,1),Levels.STAGE_AIR_FLEET,Levels.STAGE_SPACE_GADGET,
                Levels.STAGE_GUN_FORTRESS,(Levels.STAGE_BLACK_COMET,1),Levels.STAGE_COSMIC_FALL],
               [WeaponAttributes.SHOT, WeaponAttributes.LONG_RANGE]),
    WeaponInfo(0x5, "Gatling Gun",
               [(Levels.STAGE_LETHAL_HIGHWAY, 1),
                   (Levels.STAGE_THE_ARK,1),Levels.STAGE_IRON_JUNGLE, Levels.STAGE_GUN_FORTRESS],
               [WeaponAttributes.SHOT, WeaponAttributes.LONG_RANGE]),
    WeaponInfo(0x7, "Egg Gun",
               [(Levels.STAGE_CRYPTIC_CASTLE,1), Levels.STAGE_CIRCUS_PARK, Levels.STAGE_SKY_TROOPS,
                Levels.STAGE_MAD_MATRIX, Levels.STAGE_IRON_JUNGLE, Levels.STAGE_LAVA_SHELTER],
        [WeaponAttributes.SHOT, WeaponAttributes.LONG_RANGE]),
    WeaponInfo(0x8, "Light Shot",
                [Levels.STAGE_WESTOPOLIS,
                Levels.STAGE_DIGITAL_CIRCUIT,Levels.STAGE_LETHAL_HIGHWAY,
                 (Levels.STAGE_CRYPTIC_CASTLE,2), Levels.STAGE_PRISON_ISLAND,
                Levels.STAGE_CENTRAL_CITY, Levels.STAGE_DEATH_RUINS,
                 Levels.STAGE_SPACE_GADGET],
            [WeaponAttributes.SHOT]),
    WeaponInfo(0x9, "Flash Shot",
               [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON,
                Levels.STAGE_LETHAL_HIGHWAY,Levels.STAGE_PRISON_ISLAND, Levels.STAGE_CENTRAL_CITY,
                Levels.STAGE_DEATH_RUINS, Levels.STAGE_SPACE_GADGET,
                Levels.STAGE_BLACK_COMET],
[WeaponAttributes.SHOT]),
    WeaponInfo(0xA, "Ring Shot",
           [Levels.STAGE_SKY_TROOPS, Levels.STAGE_SPACE_GADGET,
                Levels.STAGE_FINAL_HAUNT],
[WeaponAttributes.SHOT]),
    WeaponInfo(0xB, "Heavy Shot",
               [(Levels.STAGE_FINAL_HAUNT,1)],[WeaponAttributes.SHOT]),
    WeaponInfo(0xC, "Grenade Launcher",
               [Levels.STAGE_GLYPHIC_CANYON, Levels.STAGE_THE_DOOM,Levels.STAGE_DEATH_RUINS,
                (Levels.STAGE_SPACE_GADGET,1), Levels.STAGE_LOST_IMPACT],
    [WeaponAttributes.NOT_AIMABLE]),
    WeaponInfo(0xD, "Bazooka",
               [Levels.STAGE_CENTRAL_CITY, Levels.STAGE_DEATH_RUINS,
                (Levels.STAGE_BLACK_COMET, 1), Levels.STAGE_COSMIC_FALL],
[WeaponAttributes.NOT_AIMABLE]),
    WeaponInfo(0xE, "Tank Cannon",
               [(Levels.STAGE_PRISON_ISLAND, 2), (Levels.STAGE_IRON_JUNGLE,1),
                (Levels.STAGE_BLACK_COMET, 2)],
[WeaponAttributes.NOT_AIMABLE]),
    WeaponInfo(0xF, "Black Barrel",
               [Levels.STAGE_SKY_TROOPS,(Levels.STAGE_BLACK_COMET,1), Levels.STAGE_FINAL_HAUNT,],
[WeaponAttributes.NOT_AIMABLE]),
    WeaponInfo(0x10, "Big Barrel",
               [Levels.STAGE_COSMIC_FALL,(Levels.STAGE_FINAL_HAUNT,1)],
[WeaponAttributes.NOT_AIMABLE]),
    WeaponInfo(0x11, "Egg Bazooka",
               [(Levels.STAGE_CRYPTIC_CASTLE, 1), Levels.STAGE_CIRCUS_PARK, Levels.STAGE_SKY_TROOPS,
                Levels.STAGE_MAD_MATRIX, Levels.STAGE_IRON_JUNGLE, Levels.STAGE_LAVA_SHELTER],
[WeaponAttributes.NOT_AIMABLE]),
    WeaponInfo(0x12, "RPG",
               [Levels.STAGE_THE_DOOM, Levels.STAGE_THE_ARK, Levels.STAGE_GUN_FORTRESS],
[WeaponAttributes.NOT_AIMABLE]),
    WeaponInfo(0x13, "4-Shot RPG",
               [(Levels.STAGE_THE_ARK,1), Levels.STAGE_IRON_JUNGLE, Levels.STAGE_SPACE_GADGET],
[WeaponAttributes.NOT_AIMABLE]),
    WeaponInfo(0x14, "8-Shot RPG",
               [Levels.STAGE_GUN_FORTRESS, (Levels.STAGE_BLACK_COMET,1)],
[WeaponAttributes.NOT_AIMABLE]),
    WeaponInfo(0x15, "Worm Shooter",
               [Levels.STAGE_DIGITAL_CIRCUIT,Levels.STAGE_GLYPHIC_CANYON,
                (Levels.STAGE_PRISON_ISLAND,1), Levels.STAGE_DEATH_RUINS],
[WeaponAttributes.NOT_AIMABLE]),
    WeaponInfo(0x16, "Wide Worm Shooter",
               [(Levels.STAGE_MAD_MATRIX, 1), (Levels.STAGE_BLACK_COMET,1)],
[WeaponAttributes.NOT_AIMABLE]),
    WeaponInfo(0x17, "Big Worm Shooter",
               [(Levels.STAGE_BLACK_COMET,1)],
[WeaponAttributes.NOT_AIMABLE]),
    WeaponInfo(0x18, "Vacuum Pod",
               [Levels.STAGE_CENTRAL_CITY, (Levels.STAGE_SPACE_GADGET,1), Levels.STAGE_FINAL_HAUNT],
[WeaponAttributes.VACUUM]),
    WeaponInfo(0x19, "Laser Rifle",
               [(Levels.STAGE_BLACK_COMET,1)],
[WeaponAttributes.SHOT, WeaponAttributes.LONG_RANGE]),
    WeaponInfo(0x1A, "Splitter",
               [Levels.STAGE_AIR_FLEET,Levels.STAGE_GUN_FORTRESS],
[WeaponAttributes.SHOT]),
    WeaponInfo(0x1B, "Refractor",
               [(Levels.STAGE_BLACK_COMET,1),Levels.STAGE_FINAL_HAUNT],
[WeaponAttributes.SHOT, WeaponAttributes.LONG_RANGE]),
    WeaponInfo(0x1E, "Survival Knife",
               [Levels.STAGE_THE_DOOM],
[]),
    WeaponInfo(0x1F, "Black Sword",
               [Levels.STAGE_DIGITAL_CIRCUIT,Levels.STAGE_GLYPHIC_CANYON,
                (Levels.STAGE_CRYPTIC_CASTLE,1),(Levels.STAGE_PRISON_ISLAND,1), Levels.STAGE_CENTRAL_CITY,
                Levels.STAGE_SKY_TROOPS, Levels.STAGE_AIR_FLEET,
                Levels.STAGE_FINAL_HAUNT],
[]),
    WeaponInfo(0x20, "Dark Hammer",
               [Levels.STAGE_FINAL_HAUNT],
[]),
    WeaponInfo(0x21, "Egg Spear",
               [Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_CIRCUS_PARK, Levels.STAGE_SKY_TROOPS,
                Levels.STAGE_MAD_MATRIX, Levels.STAGE_IRON_JUNGLE, Levels.STAGE_LAVA_SHELTER],
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

    WeaponInfo(0x35, "Lava Pole",
               [Levels.STAGE_LAVA_SHELTER],
[]),
    WeaponInfo(0x36, "Cosmic Pole",
               [Levels.STAGE_COSMIC_FALL],
[]),
    WeaponInfo(0x37, "Haunt Pole",
               [Levels.STAGE_FINAL_HAUNT],
[]),
    WeaponInfo(0x38, "Last Pole",
               [],
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
[WeaponAttributes.SPECIAL, WeaponAttributes.SHOT, WeaponAttributes.LONG_RANGE])
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