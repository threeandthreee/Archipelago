import re
from enum import Enum, auto
from typing import List

SADX_BASE_ID = 543800000


def pascal_to_space(s):
    return re.sub(r'(?<!^)(?=[A-Z0-9])', ' ', s)


class Goal:
    Levels = 0
    Emblems = 1
    EmeraldHunt = 2
    LevelsAndEmeraldHunt = 3
    EmblemsAndEmeraldHunt = 4
    Missions = 5
    MissionsAndEmeraldHunt = 6


class Character(Enum):
    Sonic = 1
    Tails = auto()
    Knuckles = auto()
    Amy = auto()
    Big = auto()
    Gamma = auto()


def remove_character_suffix(string: str) -> str:
    for character in Character:
        if string.endswith(f" ({character.name})"):
            return re.sub(rf" \({character.name}\)$", "", string)
    return string


EVERYONE: List[Character] = [Character.Sonic, Character.Tails, Character.Knuckles,
                             Character.Amy, Character.Big, Character.Gamma]
SONIC_TAILS: List[Character] = [Character.Sonic, Character.Tails]
FLYERS: List[Character] = [Character.Tails, Character.Knuckles]


class Upgrade(Enum):
    LightShoes = auto()
    CrystalRing = auto()
    AncientLight = auto()
    JetAnkle = auto()
    RhythmBadge = auto()
    ShovelClaw = auto()
    FightingGloves = auto()
    LongHammer = auto()
    WarriorFeather = auto()
    JetBooster = auto()
    LaserBlaster = auto()
    LifeBelt = auto()
    PowerRod = auto()
    Lure1 = auto()
    Lure2 = auto()
    Lure3 = auto()
    Lure4 = auto()


class SubLevelMission(Enum):
    B = 0
    A = auto()


class LevelMission(Enum):
    C = 0
    B = auto()
    A = auto()


class SubLevel(Enum):
    SandHill = auto()
    TwinkleCircuit = auto()
    SkyChaseAct1 = auto()
    SkyChaseAct2 = auto()


class AdventureField(Enum):
    StationSquare = auto()
    MysticRuins = auto()
    EggCarrier = auto()
    Past = auto()


class Area(Enum):
    StationSquareMain = 0
    Station = auto()
    Hotel = auto()
    Casino = auto()
    TwinkleParkLobby = auto()
    MysticRuinsMain = auto()
    AngelIsland = auto()
    Jungle = auto()
    EggCarrierMain = auto()
    EmeraldCoast = auto()
    WindyValley = auto()
    Casinopolis = auto()
    IceCap = auto()
    TwinklePark = auto()
    SpeedHighway = auto()
    RedMountain = auto()
    SkyDeck = auto()
    LostWorld = auto()
    FinalEgg = auto()
    HotShelter = auto()


level_areas = [
    Area.EmeraldCoast,
    Area.WindyValley,
    Area.Casinopolis,
    Area.IceCap,
    Area.TwinklePark,
    Area.SpeedHighway,
    Area.RedMountain,
    Area.SkyDeck,
    Area.LostWorld,
    Area.FinalEgg,
    Area.HotShelter
]
