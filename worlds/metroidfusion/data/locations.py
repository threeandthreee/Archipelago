from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from worlds.metroidfusion import MetroidFusionOptions

level_1_e_tanks = 3
level_2_e_tanks = 5
level_3_e_tanks = 7
level_4_e_tanks = 10

class Requirement:
    """
    Defines a set of requirements for a Connection or Location.
    """
    items_needed: list[str] = []
    other_requirements: list["Requirement"] = []
    energy_tanks_needed: int = 0

    def __init__(self, items_needed, other_requirements, energy_tanks_needed = 0):
        """
        Creates a new Requirement object. The parameters are unpacked into a series of OR requirements where everything
        in ``items_required`` and one of the entries in ``other_requirements``
        must be met for the Requirement to be passed.

        :param items_needed: A list of items that are all required to be had.
        :param other_requirements: A list of Requirement objects.
            If not empty, one of these must be fulfilled in addition to the ``items_needed``.
        :param energy_tanks_needed: The number of energy tanks required.
        """
        self.items_needed = items_needed
        self.other_requirements = other_requirements
        self.energy_tanks_needed = energy_tanks_needed

    def __repr__(self):
        return_string = f"{self.__class__}\n"
        return_string += f"ItemsNeeded: [{', '.join(self.items_needed)}]\n"
        return_string += (f"OtherRequirements: "
                          f"[{', '.join([str(requirement) for requirement in self.other_requirements])}]\n")
        return_string += f"EnergyTanks: {self.energy_tanks_needed}"
        return return_string

    def __str__(self):
        return self.__repr__()

    @staticmethod
    def check_option_enabled(options: "MetroidFusionOptions") -> bool:
        return True

class FusionLocation:
    name: str
    major: bool
    requirements: list[Requirement]

    def __init__(self, name, major, requirements):
        self.name = name
        self.major = major
        self.requirements = requirements

class Connection:
    destination: "FusionRegion"
    requirements: list[Requirement]
    one_way: bool

    def __init__(self, destination, requirements, one_way=False):
        self.destination = destination
        self.requirements = requirements
        self.one_way = one_way

    def determine_destination(
            self,
            options: "MetroidFusionOptions",
            region_map: dict["FusionRegion", "FusionRegion"]):
        pass

class VariableConnection(Connection):
    def determine_destination(
            self,
            options: "MetroidFusionOptions",
            region_map: dict["FusionRegion", "FusionRegion"]):
        if self.destination in region_map.keys():
            origin = full_default_region_map[self.destination]
            self.destination = region_map[origin]

class FusionRegion:
    name: str
    connections: list[Connection] = []
    locations: list[FusionLocation] = []

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.__repr__()

# Requirements

#region Individual Item Requirements
class HasMorph(Requirement):
    items_needed = ["Morph Ball"]

class HasVaria(Requirement):
    items_needed = ["Varia Suit"]

class HasGravity(Requirement):
    items_needed = ["Gravity Suit"]

class HasHiJump(Requirement):
    items_needed = ["Hi-Jump"]

class HasSpaceJump(Requirement):
    items_needed = ["Space Jump"]

class HasSpeedBooster(Requirement):
    items_needed = ["Speed Booster"]

class HasScrewAttack(Requirement):
    items_needed = ["Screw Attack"]

class HasMissile(Requirement):
    items_needed = ["Missile Data"]

class HasChargeBeam(Requirement):
    items_needed = ["Charge Beam"]

class HasWaveBeam(Requirement):
    items_needed = ["Wave Beam"]

#endregion

# region Optional Requirements
class CanDoTrickyShinespark(Requirement):
    items_needed = ["Speed Booster"]

    @staticmethod
    def check_option_enabled(options: "MetroidFusionOptions") -> bool:
        return bool(options.TrickyShinesparksInRegionLogic.value)


class CanDoSimpleWallJump(Requirement):
    items_needed = []

    @staticmethod
    def check_option_enabled(options: "MetroidFusionOptions") -> bool:
        return bool(options.SimpleWallJumpsInRegionLogic.value)

class CanDoSimpleWallJumpWithHiJump(Requirement):
    items_needed = ["Hi-Jump"]

    @staticmethod
    def check_option_enabled(options: "MetroidFusionOptions") -> bool:
        return bool(options.SimpleWallJumpsInRegionLogic.value)

class CanDoSimpleWallJumpWithScrewAttack(Requirement):
    items_needed = ["Screw Attack"]

    @staticmethod
    def check_option_enabled(options: "MetroidFusionOptions") -> bool:
        return bool(options.SimpleWallJumpsInRegionLogic.value)


class SectorHubLevel1KeycardRequirement(Requirement):
    items_needed = ["Level 1 Keycard"]
    energy_tanks_needed = level_1_e_tanks

    @staticmethod
    def check_option_enabled(options: "MetroidFusionOptions"):
        return options.GameMode == options.GameMode.option_vanilla


class SectorHubLevel1And2KeycardRequirement(Requirement):
    items_needed = ["Level 1 Keycard", "Level 2 Keycard"]
    energy_tanks_needed = level_2_e_tanks

    @staticmethod
    def check_option_enabled(options: "MetroidFusionOptions"):
        return options.GameMode == options.GameMode.option_vanilla


# endregion

#region Keycard Requirements
class HasKeycard1(Requirement):
    energy_tanks_needed = level_1_e_tanks
    items_needed = ["Level 1 Keycard"]

class HasKeycard2(Requirement):
    energy_tanks_needed = level_2_e_tanks
    items_needed = ["Level 2 Keycard"]

class HasKeycard1And2(Requirement):
    energy_tanks_needed = level_2_e_tanks
    items_needed = ["Level 1 Keycard", "Level 2 Keycard"]

class HasKeycard3(Requirement):
    energy_tanks_needed = level_3_e_tanks
    items_needed = ["Level 3 Keycard"]

class HasKeycard4(Requirement):
    energy_tanks_needed = level_4_e_tanks
    items_needed = ["Level 4 Keycard"]

class Level1KeycardRequirement(Requirement):
    def __init__(self, items_needed, other_requirements, energy_tanks_needed=3):
        super().__init__(items_needed, other_requirements, energy_tanks_needed)
        self.items_needed.append("Level 1 Keycard")

class Level2KeycardRequirement(Requirement):
    def __init__(self, items_needed, other_requirements, energy_tanks_needed=5):
        super().__init__(items_needed, other_requirements, energy_tanks_needed)
        self.items_needed.append("Level 2 Keycard")

class Level1And2KeycardRequirement(Requirement):
    def __init__(self, items_needed, other_requirements, energy_tanks_needed=5):
        super().__init__(items_needed, other_requirements, energy_tanks_needed)
        self.items_needed.append("Level 1 Keycard")
        self.items_needed.append("Level 2 Keycard")

class Level3KeycardRequirement(Requirement):
    def __init__(self, items_needed, other_requirements, energy_tanks_needed=7):
        super().__init__(items_needed, other_requirements, energy_tanks_needed)
        self.items_needed.append("Level 3 Keycard")

class Level4KeycardRequirement(Requirement):
    def __init__(self, items_needed, other_requirements, energy_tanks_needed=10):
        super().__init__(items_needed, other_requirements, energy_tanks_needed)
        self.items_needed.append("Level 4 Keycard")
#endregion

#region Combined Item Requirements
class CanJumpHigh(Requirement):
    other_requirements = [
        Requirement(["Hi-Jump"], []),
        Requirement(["Space Jump"], [])
    ]

class CanLavaDive(Requirement):
    items_needed = ["Varia Suit", "Gravity Suit"]

class CanBomb(Requirement):
    items_needed = ["Morph Ball", "Bomb Data"]

class CanPowerBomb(Requirement):
    items_needed = ["Morph Ball", "Power Bomb Data"]

class CanBombOrPowerBomb(Requirement):
    other_requirements = [CanBomb, CanPowerBomb]

class CanPowerBombAndJumpHigh(Requirement):
    items_needed = ["Morph Ball", "Power Bomb Data"]
    other_requirements = [CanJumpHigh]

class CanBallJump(Requirement):
    items_needed = ["Morph Ball"]
    other_requirements = [
        Requirement(["Bomb Data"], []),
        Requirement(["Hi-Jump"], [])
    ]

class CanBallJumpAndBomb(Requirement):
    other_requirements = [
        Requirement(["Morph Ball", "Bomb Data"], []),
        Requirement(["Hi-Jump"], [CanPowerBomb])
    ]

class CanScrewAttackAndSpaceJump(Requirement):
    items_needed = ["Screw Attack", "Space Jump"]

class CanJumpHighUnderwater(Requirement):
    items_needed = ["Gravity Suit"]
    other_requirements = [CanJumpHigh]

class CanSpeedBoosterUnderwater(Requirement):
    items_needed = ["Gravity Suit", "Speed Booster"]

class CanFreezeEnemies(Requirement):
    other_requirements = [
        Requirement(["Ice Missile"], [HasMissile]),
        Requirement(["Diffusion Missile"], [HasMissile]),
        Requirement(["Ice Beam"], [])
    ]

class CanActivatePillar(Requirement):
    other_requirements = [CanBombOrPowerBomb, HasWaveBeam]

class CanDiffusionMissile(Requirement):
    items_needed = ["Missile Data", "Diffusion Missile"]

class CanDestroyBombBlocks(Requirement):
    other_requirements = [CanBomb, CanPowerBomb, Requirement(["Screw Attack"], [])]

#endregion

#region Enemy Requirements
class CanDefeatSmallGeron(Requirement):
    other_requirements = [
        Requirement(["Missile Data"], []),
        CanPowerBomb,
        Requirement(["Screw Attack"], [])
    ]

class CanDefeatMediumGeron(Requirement):
    other_requirements = [
        Requirement(["Missile Data", "Super Missile"], []),
        CanPowerBomb,
        Requirement(["Screw Attack"], [])
    ]

class CanDefeatLargeGeron(Requirement):
    other_requirements = [
        CanPowerBomb,
        Requirement(["Screw Attack"], [])
    ]

class CanBeatToughEnemy(Requirement):
    other_requirements = [HasChargeBeam, HasMissile]

class CanBeatToughEnemyAndJumpHigh(Requirement):
    other_requirements = [
        Requirement(["Hi-Jump"], [CanBeatToughEnemy]),
        Requirement(["Space Jump"], [CanBeatToughEnemy])
    ]

class CanDefeatStabilizer(Requirement):
    other_requirements = [
        Requirement(["Screw Attack"], []),
        Requirement(["Charge Beam"], []),
        Requirement(["Missile Data"], []),
        CanPowerBomb
    ]

#endregion

#region Boss Requirements
class CanFightBeginnerBoss(Requirement):
    items_needed = ["Missile Data"]

class CanFightBoss(Requirement):
    energy_tanks_needed = level_1_e_tanks
    items_needed = ["Missile Data", "Charge Beam"]

class CanFightMidgameBoss(Requirement):
    energy_tanks_needed = level_2_e_tanks
    items_needed = ["Super Missile"]
    other_requirements = [CanFightBoss]

class CanFightLateGameBoss(Requirement):
    energy_tanks_needed = level_3_e_tanks
    items_needed = ["Plasma Beam", "Space Jump"]
    other_requirements = [CanFightMidgameBoss]

#endregion

#region Individual Location Requirements
class CanReachAnimals(Requirement):
    items_needed = ["Speed Booster"]
    other_requirements = [
        Requirement(["Hi-Jump"], [CanFreezeEnemies]),
        HasSpaceJump
    ]

class CanReachGenesisSpeedway(Requirement):
    items_needed = ["Morph Ball", "Power Bomb Data"]
    other_requirements = [CanBallJump]

class CanCrossFromReactorToSector2(Requirement):
    items_needed = ["Space Jump", "Missile Data"]
    other_requirements = [CanBombOrPowerBomb]

class CanReachAnimorphs(Requirement):
    items_needed = ["Space Jump", "Charge Beam", "Wave Beam", "Missile Data", "Super Missile"]

class CanReachOasisStorage(Requirement):
    other_requirements = [
        CanPowerBomb,
        Requirement(["Hi-Jump"], [CanBombOrPowerBomb]),
        Requirement(["Morph Ball", "Screw Attack"], [CanJumpHighUnderwater])
    ]

class CanAscendBOXRoom(Requirement):
    items_needed = ["Charge Beam", "Missile Data"]
    other_requirements = [CanJumpHigh]

class CanNavigateLavaMaze(Requirement):
    items_needed = ["Morph Ball", "Power Bomb Data"]
    other_requirements = [CanLavaDive]

class CanAccessL2SecurityRoom(Requirement):
    items_needed = ["Speed Booster"]
    other_requirements = [CanBallJumpAndBomb]

class CanDrainAQA(Requirement):
    items_needed = ["Speed Booster", "Level 1 Keycard"]
    other_requirements = [CanBombOrPowerBomb]

class CanAscendCheddarBay(Requirement):
    items_needed = ["Missile Data"]
    other_requirements = [CanBombOrPowerBomb]

class CanAccessReservoirVault(Requirement):
    other_requirements = [
        Requirement(["Hi-Jump"], [CanBombOrPowerBomb]),
        Requirement(["Space Jump"], [CanBallJumpAndBomb])
    ]

class CanAccessSanctuaryCache(Requirement):
    other_requirements = [
        Requirement(["Wave Beam", "Charge Beam"], [CanDoSimpleWallJump, HasSpaceJump]),
        Requirement(
            ["Wave Beam", "Missile Data", "Morph Ball"],
            [CanDoSimpleWallJump, HasSpaceJump]
        ),
        Requirement(
            ["Power Bomb Data", "Missile Data", "Morph Ball"],
            [CanDoSimpleWallJump, HasSpaceJump]
        ),
        Requirement(
            ["Power Bomb Data", "Charge Beam", "Morph Ball"],
            [CanDoSimpleWallJump, HasSpaceJump]
        ),
    ]

class CanEscapeNightmareRoom(Requirement):
    items_needed = ["Gravity Suit", "Speed Booster"]
    other_requirements = [CanFightLateGameBoss]

class CanAccessRipperRoad(Requirement):
    items_needed = ["Morph Ball", "Hi-Jump"]
    other_requirements = [
        Requirement(["Bomb Data", "Screw Attack"], [CanFreezeEnemies]),
        Requirement(["Power Bomb Data"], [CanFreezeEnemies]),
    ]

class CanAccessRipperTreasure(Requirement):
    items_needed = ["Power Bomb Data"]
    other_requirements = [
        HasSpaceJump,
        Requirement(["Hi-Jump"], [CanFreezeEnemies])
    ]

class CanAccessFieryStorage(Requirement):
    items_needed = ["Varia Suit"]
    other_requirements = [
        CanBeatToughEnemy,
        CanLavaDive
    ]

class CanAccessFieryStorageUpper(Requirement):
    items_needed = ["Varia Suit", "Speed Booster"]
    other_requirements = [
        Requirement(
            ["Charge Beam", "Morph Ball", "Bomb Data"],
            [CanActivatePillar, HasSpaceJump]
        ),
        Requirement(
            ["Missile Data", "Morph Ball", "Bomb Data"],
            [CanActivatePillar, HasSpaceJump]
        ),
        Requirement(
            ["Gravity Suit", "Morph Ball", "Bomb Data"],
            [CanActivatePillar, HasSpaceJump]
        ),
        Requirement(
            ["Charge Beam", "Morph Ball", "Power Bomb Data"],
            [CanActivatePillar, HasSpaceJump]
        ),
        Requirement(
            ["Missile Data", "Morph Ball", "Power Bomb Data"],
            [CanActivatePillar, HasSpaceJump]
        ),
        Requirement(
            ["Gravity Suit", "Morph Ball", "Power Bomb Data"],
            [CanActivatePillar, HasSpaceJump]
        ),
        Requirement(["Charge Beam", "Screw Attack"], [CanActivatePillar, HasSpaceJump]),
        Requirement(["Missile Data", "Screw Attack"], [CanActivatePillar, HasSpaceJump]),
        Requirement(["Gravity Suit", "Screw Attack"], [CanActivatePillar, HasSpaceJump]),
    ]

class CanAccessGlassTubeItem(Requirement):
    other_requirements = [
        Requirement(["Hi-Jump"], [CanBomb]),
        CanPowerBomb,
        Requirement(["Screw Attack"], []),
    ]

class CanAccessGarbageChute(Requirement):
    items_needed = ["Screw Attack", "Speed Booster"]
    other_requirements = [
        CanLavaDive
    ]

class CanAccessWallJumpTutorialWithSpaceJump(Requirement):
    items_needed = ["Space Jump"]
    other_requirements = [CanBallJump]

class CanAccessWallJumpTutorialWithWallJump(Requirement):
    other_requirements = [
        Requirement(["Morph Ball", "Hi-Jump"], [CanDoSimpleWallJump]),
        Requirement(["Morph Ball", "Bomb Data"], [CanDoSimpleWallJump]),
    ]

class CanAccessZazabiSpeedway(Requirement):
    items_needed = [
        "Charge Beam",
        "Missile Data",
        "Space Jump",
        "Speed Booster",
        "Screw Attack"
    ]

class CanAccessWateringHole(Requirement):
    items_needed = ["Gravity Suit", "Speed Booster"]
    other_requirements = [
        Requirement(["Charge Beam"], [CanBallJump]),
        Requirement(["Plasma Beam"], [CanBallJump]),
        Requirement(["Missile Data"], [CanBallJump])

    ]

class CanBacktrackToCultivationStation(Requirement):
    other_requirements = [
        Requirement(["Hi-Jump"], [CanBombOrPowerBomb]),
        Requirement(["Space Jump"], [CanBombOrPowerBomb])
    ]

class CanAccessYakuza(Requirement):
    other_requirements = [
        Requirement(["Morph Ball", "Bomb Data"], [CanBeatToughEnemy]),
        Requirement(["Morph Ball", "Power Bomb Data"], [CanBeatToughEnemy]),
        Requirement(["Morph Ball", "Wave Beam"], [CanBeatToughEnemy]),
        Requirement(
            ["Morph Ball", "Missile Data", "Diffusion Missile"],
            [CanBeatToughEnemy]
        )
    ]

class CanCrossSector4RightWaterCorner(Requirement):
    items_needed = ["Missile Data", "Morph Ball", "Gravity Suit"]
    other_requirements = [
        CanFreezeEnemies,
        Requirement(["Space Jump"], []),
    ]

class CanCrossSector4LowerSecurityToRightWaterZone(Requirement):
    items_needed = ["Morph Ball", "Level 4 Keycard"]
    other_requirements = [
        Requirement(["Speed Booster"], [CanFreezeEnemies]),
        HasScrewAttack
    ]
    energy_tanks_needed = level_4_e_tanks

class CanAccessSector3LowerAlcove(Requirement):
    items_needed = ["Morph Ball"]
    other_requirements = [
        CanBombOrPowerBomb,
        Requirement(["Screw Attack"], [CanActivatePillar, HasSpeedBooster, CanJumpHigh])
    ]
#endregion

#region Event Requirements
class CanDrainAQARequirement(Requirement):
    def __init__(self, items_needed, other_requirements, energy_tanks_needed=3):
        super().__init__(items_needed, other_requirements, energy_tanks_needed)
        self.items_needed.append("Pump Control Activated")
#endregion

#region Region Definitions

#region Main Deck Regions

class MainDeckHub(FusionRegion):
    name = "Main Deck Hub"

class LowerArachnusArena(FusionRegion):
    name = "Lower Arachnus Arena"

class VentilationZone(FusionRegion):
    name = "Ventilation Zone"

class UpperArachnusArena(FusionRegion):
    name = "Upper Arachnus Arena"

class OperationsDeckElevatorBottom(FusionRegion):
    name = "Operations Deck Elevator Bottom"

class OperationsDeck(FusionRegion):
    name = "Operations Deck"

class OperationsDeckElevatorTop(FusionRegion):
    name = "Operations Deck Elevator Top"

class HabitationDeckElevatorBottom(FusionRegion):
    name = "Habitation Deck Elevator Bottom"

class HabitationDeckElevatorTop(FusionRegion):
    name = "Habitation Deck Elevator Top"

class HabitationDeck(FusionRegion):
    name = "Habitation Deck"

class SectorHubElevatorTop(FusionRegion):
    name = "Sector Hub Elevator Top"

class SectorHubElevatorBottom(FusionRegion):
    name = "Sector Hub Elevator Bottom"

class SectorHubElevator1Top(FusionRegion):
    name = "Sector Hub Elevator 1 Top"

class SectorHubElevator2Top(FusionRegion):
    name = "Sector Hub Elevator 2 Top"

class SectorHubElevator3Top(FusionRegion):
    name = "Sector Hub Elevator 3 Top"

class SectorHubElevator4Top(FusionRegion):
    name = "Sector Hub Elevator 4 Top"

class SectorHubElevator5Top(FusionRegion):
    name = "Sector Hub Elevator 5 Top"

class SectorHubElevator6Top(FusionRegion):
    name = "Sector Hub Elevator 6 Top"

class ReactorZone(FusionRegion):
    name = "Reactor Zone"

class YakuzaZone(FusionRegion):
    name = "Yakuza Zone"

class AuxiliaryReactor(FusionRegion):
    name = "Auxiliary Reactor"

class NexusStorage(FusionRegion):
    name = "Nexus Storage"

#endregion

#region Sector 1 Regions

class Sector1Hub(FusionRegion):
    name = "Sector 1 Hub"

class Sector1TubeRight(FusionRegion):
    name = "Sector 1 Tube Right"

class Sector1TubeLeft(FusionRegion):
    name = "Sector 1 Tube Left"

class Sector1Antechamber(FusionRegion):
    name = "Sector 1 Antechamber"

class Sector1FirstStabilizerZone(FusionRegion):
    name = "Sector 1 First Stabilizer Zone"

class Sector1SecondStabilizerZone(FusionRegion):
    name = "Sector 1 Second Stabilizer Zone"

class Sector1ChargeCoreZone(FusionRegion):
    name = "Sector 1 Charge Core Zone"

class Sector1AfterChargeCoreZone(FusionRegion):
    name = "Sector 1 After Charge Core Zone"

class Sector1TourianExit(FusionRegion):
    name = "Sector 1 Tourian Exit"

class Sector1TourianHub(FusionRegion):
    name = "Sector 1 Tourian Hub"

class Sector1TourianHubElevatorTop(FusionRegion):
    name = "Sector 1 Tourian Hub Elevator Top"
#endregion

#region Sector 2 Regions

class Sector2Hub(FusionRegion):
    name = "Sector 2 Hub"

class Sector2TubeLeft(FusionRegion):
    name = "Sector 2 Tube Left"

class Sector2TubeRight(FusionRegion):
    name = "Sector 2 Tube Right"

class Sector2LeftSide(FusionRegion):
    name = "Sector 2 Left Side"

class Sector2ZazabiZone(FusionRegion):
    name = "Sector 2 Zazabi Zone"

class Sector2ZazabiZoneUpper(FusionRegion):
    name = "Sector 2 Zazabi Zone Upper"

class Sector2NettoriZone(FusionRegion):
    name = "Sector 2 Nettori Zone"

#endregion

#region Sector 3 Regions

class Sector3Hub(FusionRegion):
    name = "Sector 3 Hub"

class Sector3TubeLeft(FusionRegion):
    name = "Sector 3 Tube Left"

class Sector3TubeRight(FusionRegion):
    name = "Sector 3 Tube Right"

class Sector3SecurityZone(FusionRegion):
    name = "Sector 3 Security Zone"

class Sector3MainShaft(FusionRegion):
    name = "Sector 3 Main Shaft"

class Sector3BoilerZone(FusionRegion):
    name = "Sector 3 Boiler Zone"

class Sector3BobZone(FusionRegion):
    name = "Sector 3 Bob Zone"

class Sector3BOXZone(FusionRegion):
    name = "Sector 3 BOX Zone"

class Sector3Attic(FusionRegion):
    name = "Sector 3 Attic"

class Sector3SovaProcessing(FusionRegion):
    name = "Sector 3 Sova Processing"

#endregion

#region Sector 4 Regions

class Sector4Hub(FusionRegion):
    name = "Sector 4 Hub"

class Sector4TubeLeft(FusionRegion):
    name = "Sector 4 Tube Left"

class Sector4TubeRight(FusionRegion):
    name = "Sector 4 Tube Right"

class Sector4UpperZone(FusionRegion):
    name = "Sector 4 Upper Zone"

class Sector4SerrisZone(FusionRegion):
    name = "Sector 4 Serris Zone"

class Sector4PumpControl(FusionRegion):
    name = "Sector 4 Pump Control"

class Sector4UpperWaterZone(FusionRegion):
    name = "Sector 4 Upper Water Zone"

class Sector4SecurityZone(FusionRegion):
    name = "Sector 4 Security Zone"

class Sector4LowerSecurityZone(FusionRegion):
    name = "Sector 4 Lower Security Zone"

class Sector4SecurityRoom(FusionRegion):
    name = "Sector 4 Security Room"

class Sector4RightWaterZone(FusionRegion):
    name = "Sector 4 Right Water Zone"

class Sector4DataZone(FusionRegion):
    name = "Sector 4 Data Zone"

class Sector4RightDataZone(FusionRegion):
    name = "Sector 4 Right Data Zone"

#endregion

#region Sector 5 Regions

class Sector5Hub(FusionRegion):
    name = "Sector 5 Hub"

class Sector5TubeLeft(FusionRegion):
    name = "Sector 5 Tube Left"

class Sector5TubeRight(FusionRegion):
    name = "Sector 5 Tube Right"

class Sector5MagicBox(FusionRegion):
    name = "Sector 5 Magic Box"

class Sector5BigRoom(FusionRegion):
    name = "Sector 5 Big Room"

class Sector5FrozenHub(FusionRegion):
    name = "Sector 5 Frozen Hub"

class Sector5SecurityZone(FusionRegion):
    name = "Sector 5 Security Zone"

class Sector5DataRoom(FusionRegion):
    name = "Sector 5 Data Room"

class Sector5BeforeNightmareHub(FusionRegion):
    name = "Sector 5 Before Nightmare Hub"

class Sector5NightmareHub(FusionRegion):
    name = "Sector 5 Nightmare Hub"

class Sector5NightmareZoneUpper(FusionRegion):
    name = "Sector 5 Nightmare Zone Upper"

class Sector5NightmareZoneArena(FusionRegion):
    name = "Sector 5 Nightmare Zone Arena"

#endregion

#region Sector 6 Regions

class Sector6Hub(FusionRegion):
    name = "Sector 6 Hub"

class Sector6TubeLeft(FusionRegion):
    name = "Sector 6 Tube Left"

class Sector6TubeRight(FusionRegion):
    name = "Sector 6 Tube Right"

class Sector6Crossroads(FusionRegion):
    name = "Sector 6 Crossroads"

class Sector6BeforeXBOXZone(FusionRegion):
    name = "Sector 6 Before X-BOX Zone"

class Sector6XBOXZone(FusionRegion):
    name = "Sector 6 X-BOX Zone"

class Sector6AfterXBOXZone(FusionRegion):
    name = "Sector 6 After X-BOX Zone"

class Sector6RestrictedZone(FusionRegion):
    name = "Sector 6 Restricted Zone"

class Sector6RestrictedZoneElevatorToTourian(FusionRegion):
    name = "Sector 6 Restricted Zone Elevator To Tourian Bottom"

class Sector6BeforeVariaCoreXZone(FusionRegion):
    name = "Sector 6 Before Varia Core-X Zone"

class Sector6VariaCoreXZone(FusionRegion):
    name = "Sector 6 Varia Core-X Zone"

class Sector6AfterVariaCoreXZone(FusionRegion):
    name = "Sector 6 After Varia Core-X Zone"

#endregion

#endregion

#region Topologies
#region Main Deck Topology
MainDeckHub.connections = [
    Connection(OperationsDeckElevatorBottom, []),
    Connection(VentilationZone, [CanDefeatSmallGeron]),
    Connection(LowerArachnusArena, [HasMorph]),
    Connection(UpperArachnusArena, [
        Requirement(["Morph Ball", "Space Jump", "Screw Attack"], [])
    ]),
    Connection(HabitationDeckElevatorBottom, [HasKeycard2]),
    Connection(SectorHubElevatorTop, [HasMorph, CanDoTrickyShinespark], one_way=True),
    Connection(ReactorZone, [
        Requirement(["Morph Ball"], [HasKeycard4, CanPowerBomb], 5)
    ]),
    Connection(NexusStorage, [
        Level2KeycardRequirement([], [CanDefeatLargeGeron])
    ])
]

VentilationZone.connections = [
    Connection(UpperArachnusArena, [CanFightBeginnerBoss])
]

OperationsDeckElevatorBottom.connections = [
    VariableConnection(OperationsDeckElevatorTop, [])
]

OperationsDeckElevatorTop.connections = [
    VariableConnection(OperationsDeckElevatorBottom, []),
    Connection(OperationsDeck, [])
]

OperationsDeck.connections = [
    Connection(LowerArachnusArena, [HasMissile], one_way=True)
]

HabitationDeckElevatorBottom.connections = [
    VariableConnection(HabitationDeckElevatorTop, [])
]

HabitationDeckElevatorTop.connections = [
    VariableConnection(HabitationDeckElevatorBottom, []),
    Connection(HabitationDeck, [HasKeycard2])
]

ReactorZone.connections = [
    Connection(YakuzaZone, [CanAccessYakuza]),
    Connection(AuxiliaryReactor, [HasWaveBeam], one_way=True),
    Connection(Sector2NettoriZone, [CanCrossFromReactorToSector2], one_way=True)
]

AuxiliaryReactor.connections = [
    Connection(ReactorZone, [], one_way=True)
]

YakuzaZone.connections = [
    Connection(AuxiliaryReactor, [HasSpaceJump])
]

SectorHubElevatorTop.connections = [
    Connection(MainDeckHub, [HasMorph, HasSpeedBooster], one_way=True),
    VariableConnection(SectorHubElevatorBottom, [])
]

SectorHubElevatorBottom.connections = [
    VariableConnection(SectorHubElevatorTop, []),
    Connection(SectorHubElevator1Top, []),
    Connection(SectorHubElevator2Top, []),
    Connection(SectorHubElevator3Top, [SectorHubLevel1KeycardRequirement]),
    Connection(SectorHubElevator4Top, [SectorHubLevel1KeycardRequirement]),
    Connection(SectorHubElevator5Top, [SectorHubLevel1And2KeycardRequirement]),
    Connection(SectorHubElevator6Top, [SectorHubLevel1And2KeycardRequirement])
]

SectorHubElevator1Top.connections = [
    VariableConnection(Sector1Hub, [])
]

SectorHubElevator2Top.connections = [
    VariableConnection(Sector2Hub, [])
]

SectorHubElevator3Top.connections = [
    VariableConnection(Sector3Hub, [])
]

SectorHubElevator4Top.connections = [
    VariableConnection(Sector4Hub, [])
]

SectorHubElevator5Top.connections = [
    VariableConnection(Sector5Hub, [])
]

SectorHubElevator6Top.connections = [
    VariableConnection(Sector6Hub, [])
]

MainDeckHub.locations = [
    FusionLocation("Main Deck -- Cubby Hole", False, [HasMorph]),
    FusionLocation("Main Deck -- Genesis Speedway", False, [CanReachGenesisSpeedway]),
    FusionLocation("Main Deck -- Quarantine Bay", False, []),
    FusionLocation("Main Deck -- Station Entrance", False, [CanPowerBomb]),
    FusionLocation("Main Deck -- Sub-Zero Containment", False, [
        Level3KeycardRequirement([], [HasVaria])
    ])
]

OperationsDeck.locations = [
    FusionLocation("Main Deck -- Operations Deck Data Room", True, [])
]

VentilationZone.locations = [
    FusionLocation("Main Deck -- Operations Ventilation", False, []),
    FusionLocation("Main Deck -- Operations Ventilation Storage", False, [])
]

UpperArachnusArena.locations = [
    FusionLocation("Main Deck -- Arachnus Arena -- Upper Item", False, []),
    FusionLocation("Main Deck -- Attic", False, [HasMissile]),
]

LowerArachnusArena.locations = [
    FusionLocation("Main Deck -- Arachnus Arena -- Core X", True, [CanFightBeginnerBoss])
]

HabitationDeck.locations = [
    FusionLocation("Main Deck -- Habitation Deck -- Animals", True, [
        Level2KeycardRequirement([], [CanReachAnimals])
    ]),
    FusionLocation("Main Deck -- Habitation Deck -- Lower Item", False, [
        Level2KeycardRequirement([], [CanReachAnimals, HasWaveBeam])
    ])
]

ReactorZone.locations = [
    FusionLocation("Main Deck -- Silo Catwalk", False, [CanBeatToughEnemy]),
    FusionLocation("Main Deck -- Silo Scaffolding", False, [CanBeatToughEnemy])
]

YakuzaZone.locations = [
    FusionLocation("Main Deck -- Yakuza Arena", True, [CanFightMidgameBoss])
]

AuxiliaryReactor.locations = [
    FusionLocation("Main Deck -- Auxiliary Power Station", True, [])
]

SectorHubElevatorTop.locations = [
    FusionLocation("Main Deck -- Main Elevator Cache", False, [HasSpeedBooster])
]

NexusStorage.locations = [
    FusionLocation("Main Deck -- Nexus Storage", False, [CanBallJumpAndBomb])
]

#endregion

#region Sector 1 Topology
Sector1Hub.connections = [
    VariableConnection(SectorHubElevator1Top, []),
    Connection(Sector1Antechamber, [
        Level2KeycardRequirement([], [CanScrewAttackAndSpaceJump])
    ]),
    Connection(Sector1TubeLeft, [
        Level1KeycardRequirement(["Morph Ball", "Screw Attack"], [])
    ]),
    Connection(Sector1FirstStabilizerZone, [
        CanDefeatSmallGeron,
        Level1And2KeycardRequirement([], [CanLavaDive]),
        CanDoTrickyShinespark
    ]),
]

Sector1Antechamber.connections = [
    Connection(Sector1Hub, [
        Level2KeycardRequirement([], [HasScrewAttack])
    ], one_way=True),
    Connection(Sector1TubeRight, [HasMorph], one_way=True)
]

Sector1TubeRight.connections = [
    Connection(Sector1Antechamber, [CanBallJump]),
    VariableConnection(Sector2TubeLeft, [])
]

Sector1TubeLeft.connections = [
    VariableConnection(Sector3TubeRight, [])
]

Sector1FirstStabilizerZone.connections = [
    Connection(Sector1SecondStabilizerZone, [CanDefeatStabilizer]),
    Connection(Sector1AfterChargeCoreZone, [HasWaveBeam], one_way=True),
]

Sector1SecondStabilizerZone.connections = [
    Connection(Sector1ChargeCoreZone, [HasMorph], one_way=True),
    Connection(Sector1TourianExit, [
        Requirement(["Screw Attack"], [])
    ], one_way=True)
]

Sector1ChargeCoreZone.connections = [
    Connection(Sector1AfterChargeCoreZone, [CanFightBeginnerBoss])
]

Sector1AfterChargeCoreZone.connections = [
    Connection(Sector1FirstStabilizerZone, [], one_way=True)
]

Sector1TourianExit.connections = [
    Connection(Sector1SecondStabilizerZone, [CanScrewAttackAndSpaceJump]),
    Connection(Sector1TourianHub, [
        Requirement(
            ["Missile Data", "Morph Ball"], [CanScrewAttackAndSpaceJump], level_4_e_tanks)
    ], one_way=True)
]

Sector1TourianHub.connections = [
    Connection(Sector1TourianExit, [
        Requirement(
            ["Screw Attack", "Morph Ball", "Wave Beam"],
            [HasMissile],
            level_4_e_tanks)
    ])
]

Sector1TourianHubElevatorTop.connections = [
    VariableConnection(Sector6RestrictedZoneElevatorToTourian, []),
    Connection(Sector1TourianHub, [Requirement([], [], level_4_e_tanks)])
]

Sector1Antechamber.locations = [
    FusionLocation("Sector 1 (SRX) -- Antechamber", False, [])
]

Sector1FirstStabilizerZone.locations = [
    FusionLocation("Sector 1 (SRX) -- Atmospheric Stabilizer Northeast", False, []),
    FusionLocation("Sector 1 (SRX) -- Hornoad Hole", False, [HasMorph]),
    FusionLocation("Sector 1 (SRX) -- Wall Jump Tutorial", False, [
        CanAccessWallJumpTutorialWithSpaceJump,
        CanAccessWallJumpTutorialWithWallJump
    ])
]

Sector1SecondStabilizerZone.locations = [
    FusionLocation("Sector 1 (SRX) -- Lava Lake -- Lower Item", False, [CanLavaDive]),
    FusionLocation("Sector 1 (SRX) -- Lava Lake -- Upper Left Item", False, [
        HasSpaceJump,
        CanDoTrickyShinespark
    ]),
    FusionLocation("Sector 1 (SRX) -- Lava Lake -- Upper Right Item", False, []),
    FusionLocation("Sector 1 (SRX) -- Stabilizer Storage", False, []),
]

Sector1ChargeCoreZone.locations = [
    FusionLocation("Sector 1 (SRX) -- Charge Core Arena -- Core X", True, [
        CanFightBeginnerBoss
    ]),
    FusionLocation("Sector 1 (SRX) -- Charge Core Arena -- Upper Item", False, [
        Requirement(["Speed Booster"], [CanFightBeginnerBoss])
    ]),
    FusionLocation("Sector 1 (SRX) -- Watering Hole", False, [CanAccessWateringHole])
]

Sector1AfterChargeCoreZone.locations = [
    FusionLocation("Sector 1 (SRX) -- Crab Rave", False, [
        Requirement(["Morph Ball", "Missile Data"], [])
    ])
]

Sector1TourianHub.locations = [
    FusionLocation("Sector 1 (SRX) -- Animorphs Cache", False, [CanReachAnimorphs]),
    FusionLocation("Sector 1 (SRX) -- Ridley Arena", True, [CanFightLateGameBoss]),
    FusionLocation("Sector 1 (SRX) -- Ripper Maze", False, [CanDiffusionMissile])
]

#endregion

#region Sector 2 Topology
Sector2Hub.connections = [
    VariableConnection(SectorHubElevator2Top, []),
    Connection(Sector2TubeLeft, [HasScrewAttack]),
    Connection(Sector2TubeRight, [HasScrewAttack]),
    Connection(Sector2LeftSide, [CanBombOrPowerBomb]),
    Connection(Sector2ZazabiZoneUpper, [CanBombOrPowerBomb]),
    Connection(Sector2NettoriZone, [
        CanPowerBombAndJumpHigh,
        Requirement(["Morph Ball", "Power Bomb Data"], [CanDoSimpleWallJump])
    ])
]

Sector2TubeLeft.connections = [
    VariableConnection(Sector1TubeRight, [])
]

Sector2TubeRight.connections = [
    VariableConnection(Sector4TubeLeft, [])
]

Sector2LeftSide.connections = [
    Connection(Sector2ZazabiZone, [CanBombOrPowerBomb], one_way=True)
]

Sector2ZazabiZone.connections = [
    Connection(Sector2LeftSide, [
        Requirement(["Space Jump"], [CanBombOrPowerBomb])
    ]),
    Connection(Sector2NettoriZone, [HasSpaceJump]),
    Connection(Sector2ZazabiZoneUpper, [CanAccessZazabiSpeedway, HasSpaceJump])
]

Sector2ZazabiZoneUpper.connections = [
    Connection(Sector2ZazabiZone, [], one_way=True)
]

Sector2Hub.locations = [
    FusionLocation("Sector 2 (TRO) -- Crumble City -- Lower Item", False, [
        CanScrewAttackAndSpaceJump
    ]),
    FusionLocation("Sector 2 (TRO) -- Crumble City -- Upper Item", False, [
        CanScrewAttackAndSpaceJump
    ]),
    FusionLocation("Sector 2 (TRO) -- Data Courtyard", False, [CanBombOrPowerBomb]),
    FusionLocation("Sector 2 (TRO) -- Data Room", True, [HasKeycard1]),
    FusionLocation("Sector 2 (TRO) -- Kago Room", False, [CanJumpHigh, HasScrewAttack]),
    FusionLocation("Sector 2 (TRO) -- Level 1 Security Room", True, []),
    FusionLocation("Sector 2 (TRO) -- Lobby Cache", False, [
        Level1KeycardRequirement([], [CanBombOrPowerBomb])
    ]),
]

Sector2LeftSide.locations = [
    FusionLocation("Sector 2 (TRO) -- Zoro Zig-Zag", False, [
        Requirement(["Morph Ball"], [CanActivatePillar, CanJumpHigh])
    ])
]

Sector2ZazabiZone.locations = [
    FusionLocation("Sector 2 (TRO) -- Cultivation Station", False, [
        CanBacktrackToCultivationStation
    ]),
    FusionLocation("Sector 2 (TRO) -- Oasis", False, [CanJumpHigh]),
    FusionLocation("Sector 2 (TRO) -- Oasis Storage", False, [CanReachOasisStorage]),
    FusionLocation("Sector 2 (TRO) -- Ripper Tower -- Lower Item", False, [
        Requirement(["Morph Ball"], [CanFreezeEnemies])
    ]),
    FusionLocation("Sector 2 (TRO) -- Ripper Tower -- Upper Item", False, [
        Requirement(["Morph Ball"], [CanFreezeEnemies])
    ]),
    FusionLocation("Sector 2 (TRO) -- Zazabi Arena", True, [CanFightBoss]),
    FusionLocation("Sector 2 (TRO) -- Zazabi Arena Access", False, []),
    FusionLocation("Sector 2 (TRO) -- Zazabi Speedway -- Lower Item", False, [
        CanAccessZazabiSpeedway
    ]),
    FusionLocation("Sector 2 (TRO) -- Zazabi Speedway -- Upper Item", False, [
        CanAccessZazabiSpeedway
    ])
]

Sector2ZazabiZoneUpper.locations = [
    FusionLocation("Sector 2 (TRO) -- Dessgeega Dorm", False, [CanBombOrPowerBomb])
]

Sector2NettoriZone.locations = [
    FusionLocation("Sector 2 (TRO) -- Nettori Arena", True, [CanFightMidgameBoss]),
    FusionLocation("Sector 2 (TRO) -- Overgrown Cache", False, [HasMorph]),
    FusionLocation("Sector 2 (TRO) -- Puyo Palace", False, [])
]


#endregion

#region Sector 3 Topology
Sector3Hub.connections = [
    VariableConnection(SectorHubElevator3Top, []),
    Connection(Sector3TubeLeft, [Requirement(["Screw Attack"], [
        CanAccessFieryStorage
    ])], one_way=True),
    Connection(Sector3SecurityZone, [HasSpeedBooster]),
    Connection(Sector3MainShaft, [
        Requirement(["Morph Ball", "Speed Booster"], [])
    ]),
    Connection(Sector3BobZone, [
        Level2KeycardRequirement([], [CanDefeatMediumGeron])
    ]),
    Connection(Sector3Attic, [
        Requirement(["Screw Attack", "Space Jump"], [HasMorph, HasMissile])
    ])
]

Sector3TubeLeft.connections = [
    VariableConnection(Sector5TubeRight, []),
    Connection(Sector3Hub, [
        Requirement(["Screw Attack"], [CanJumpHigh])
    ], one_way=True)
]

Sector3TubeRight.connections = [
    VariableConnection(Sector1TubeLeft, []),
    Connection(Sector3Attic, [HasScrewAttack], one_way=True)
]

Sector3MainShaft.connections = [
    Connection(Sector3BoilerZone, [Level2KeycardRequirement([], [HasVaria])]),
    Connection(Sector3BobZone, [Requirement([], [CanBallJumpAndBomb])]),
    Connection(Sector3SovaProcessing, [
        Level2KeycardRequirement(
            ["Varia Suit", "Morph Ball", "Bomb Data"],
            [HasSpaceJump, HasWaveBeam]
        ),
        Level2KeycardRequirement(
            ["Varia Suit", "Morph Ball", "Power Bomb Data"],
            [HasSpaceJump, HasWaveBeam]),
        Level2KeycardRequirement(
            ["Varia Suit", "Screw Attack"],
            [HasSpaceJump, HasWaveBeam]),
    ])
]

Sector3BobZone.connections = [
    Connection(Sector3BOXZone, [Requirement(["Morph Ball"], [HasKeycard2])]),
    Connection(Sector3Hub, [], one_way=True)
]

Sector3BOXZone.connections = [
    Connection(Sector3Attic, [CanAscendBOXRoom])
]

Sector3Attic.connections = [
    Connection(Sector3Hub, [CanBombOrPowerBomb], one_way=True),
    Connection(Sector3BOXZone, [CanFightBoss], one_way=True),
    Connection(Sector3TubeRight, [CanScrewAttackAndSpaceJump])
]

Sector3SovaProcessing.connections = [
    Connection(Sector3Attic, [CanAccessGarbageChute], one_way=True)
]

Sector3Hub.locations = [
    FusionLocation("Sector 3 (PYR) -- Fiery Storage -- Lower Item", False, [
        CanAccessFieryStorage
    ]),
    FusionLocation("Sector 3 (PYR) -- Fiery Storage -- Upper Item", False, [
        CanAccessFieryStorageUpper
    ])
]

Sector3TubeLeft.locations = [
    FusionLocation("Sector 3 (PYR) -- Glass Tube to Sector 5 (ARC)", False, [
        CanAccessGlassTubeItem
    ])
]

Sector3SecurityZone.locations = [
    FusionLocation("Sector 3 (PYR) -- Level 2 Security Room", True, [
        HasKeycard2,
        CanAccessL2SecurityRoom
    ]),
    FusionLocation("Sector 3 (PYR) -- Security Access", False, [CanBeatToughEnemyAndJumpHigh])
]

Sector3MainShaft.locations = [
    FusionLocation("Sector 3 (PYR) -- Namihe's Lair", False, [CanPowerBombAndJumpHigh]),
    FusionLocation("Sector 3 (PYR) -- Processing Access", False, [
        Level2KeycardRequirement([], [])
    ]),
]

Sector3BoilerZone.locations = [
    FusionLocation("Sector 3 (PYR) -- Lava Maze", False, [
        Requirement([], [CanNavigateLavaMaze])
    ]),
    FusionLocation("Sector 3 (PYR) -- Main Boiler Control Room -- Boiler", True, [
        Requirement(["Missile Data"], [HasSpaceJump, CanFreezeEnemies])
    ]),
    FusionLocation("Sector 3 (PYR) -- Main Boiler Control Room -- Core X", True, [
        Requirement(["Missile Data"], [HasSpaceJump, CanFreezeEnemies])
    ]),
]

Sector3BobZone.locations = [
    FusionLocation("Sector 3 (PYR) -- Bob's Abode", False, [CanBallJump]),
]

Sector3BOXZone.locations = [
    FusionLocation("Sector 3 (PYR) -- Data Room", True, [
        Level2KeycardRequirement([], [CanFightBoss])
    ]),
    FusionLocation("Sector 3 (PYR) -- Geron's Treasure", False, [CanDefeatMediumGeron])
]

Sector3Attic.locations = [
    FusionLocation("Sector 3 (PYR) -- Alcove -- Lower Item", False, [
        CanAccessSector3LowerAlcove
    ]),
    FusionLocation("Sector 3 (PYR) -- Alcove -- Upper Item", False, [
        Requirement(["Speed Booster"], [CanPowerBomb])
    ]),
    FusionLocation("Sector 3 (PYR) -- Deserted Runway", False, [HasSpeedBooster]),
]

Sector3SovaProcessing.locations = [
    FusionLocation("Sector 3 (PYR) -- Sova Processing -- Left Item", False, [
        Requirement(["Morph Ball"], [HasSpaceJump, CanFreezeEnemies])
    ]),
    FusionLocation("Sector 3 (PYR) -- Sova Processing -- Right Item", False, [
        Requirement(["Morph Ball"], [HasSpaceJump, CanFreezeEnemies])
    ]),
    FusionLocation("Sector 3 (PYR) -- Garbage Chute -- Lower Item", False, [
        CanAccessGarbageChute
    ]),
    FusionLocation("Sector 3 (PYR) -- Garbage Chute -- Upper Item", False, [
        CanAccessGarbageChute
    ])
]

#endregion

#region Sector 4 Topology
Sector4Hub.connections = [
    VariableConnection(SectorHubElevator4Top, []),
    Connection(Sector4UpperZone, [CanBombOrPowerBomb], one_way=True),
    Connection(Sector4DataZone, [
        CanDrainAQARequirement(["Missile Data", "Diffusion Missile"], []),
        CanDrainAQARequirement(["Ice Beam", "Wave Beam"], [])
    ]),
    Connection(Sector4RightWaterZone, [
        CanDrainAQARequirement(
            ["Missile Data", "Diffusion Missile", "Gravity Suit"],
            [CanBombOrPowerBomb]
        ),
        CanDrainAQARequirement(
            ["Ice Beam", "Wave Beam", "Gravity Suit"],
            [CanBombOrPowerBomb]
        )
    ])
]

Sector4TubeRight.connections = [
    VariableConnection(Sector6TubeLeft, [HasScrewAttack]),
    Connection(Sector4RightDataZone, [
        Requirement(["Morph Ball"], [HasMissile])
    ]),
]

Sector4TubeLeft.connections = [
    VariableConnection(Sector2TubeRight, []),
    Connection(Sector4RightWaterZone, [
        Requirement(["Gravity Suit"], [CanScrewAttackAndSpaceJump])
    ])
]

Sector4UpperZone.connections = [
    Connection(Sector4Hub, [CanDrainAQARequirement([], [])], one_way=True),
    Connection(Sector4PumpControl, [
        Level1KeycardRequirement([], [HasSpeedBooster])
    ], one_way=True),
    Connection(Sector4UpperWaterZone, [
        CanDrainAQARequirement(["Gravity Suit"], [HasKeycard4])
    ]),
    Connection(Sector4SerrisZone, [
        Requirement(["Hi-Jump"] ,[CanBombOrPowerBomb])
    ], one_way=True)
]

Sector4SerrisZone.connections = [
    Connection(Sector4UpperZone, [HasSpeedBooster], one_way=True)
]

Sector4PumpControl.connections = [
    Connection(Sector4UpperZone, [CanBallJump], one_way=True)
]

Sector4UpperWaterZone.connections = [
    Connection(Sector5NightmareHub, [
        Requirement(["Hi-Jump", "Gravity Suit"], [HasSpeedBooster])
    ]),
    Connection(Sector4SecurityZone, [HasSpeedBooster, HasScrewAttack]),
]

Sector4SecurityZone.connections = [
    Connection(Sector4RightWaterZone, [CanCrossSector4LowerSecurityToRightWaterZone]),
    Connection(Sector4LowerSecurityZone, [HasKeycard4, CanAscendCheddarBay]),
    Connection(Sector4SecurityRoom, [CanAscendCheddarBay], one_way=True),
]

Sector4LowerSecurityZone.connections = [
    Connection(Sector4SecurityRoom, [HasKeycard4])
]

Sector4RightWaterZone.connections = [
    Connection(Sector4RightDataZone, [
        Requirement(["Gravity Suit"], [CanCrossSector4RightWaterCorner])
    ]),
    Connection(Sector4TubeLeft, [
        Requirement(["Gravity Suit"] ,[HasScrewAttack])
    ], one_way=True)
]

Sector4DataZone.connections = [
    Connection(Sector4RightDataZone, [
        Level4KeycardRequirement([], [CanBombOrPowerBomb])
    ])
]

Sector4RightDataZone.connections = [
    Connection(Sector4RightWaterZone, [
        Requirement(["Morph Ball"], [CanDiffusionMissile])
    ], one_way=True)
]

Sector4Hub.locations = [
    FusionLocation("Sector 4 (AQA) -- Drain Pipe", False, [
        CanDrainAQARequirement(["Morph Ball"], [CanDefeatLargeGeron]),
        CanDrainAQARequirement(["Morph Ball"], [HasWaveBeam]),

    ]),
    FusionLocation("Sector 4 (AQA) -- Reservoir East", False, [
        CanDrainAQARequirement([], [CanPowerBomb])
    ])
]

Sector4PumpControl.locations = [
    FusionLocation("Sector 4 (AQA) -- Pump Control Unit", False, [HasMorph])
]

Sector4UpperZone.locations = [
    FusionLocation("Sector 4 (AQA) -- Broken Bridge", False, []),
    FusionLocation("Sector 4 (AQA) -- C-Cache", False, []),
    FusionLocation("Sector 4 (AQA) -- Reservoir Vault -- Lower Item", False, [
        Requirement(["Missile Data"], [CanAccessReservoirVault])
    ]),
    FusionLocation("Sector 4 (AQA) -- Reservoir Vault -- Upper Item", False, [
        CanAccessReservoirVault
    ]),
    FusionLocation("Sector 4 (AQA) -- Waterway", False, [
        CanDrainAQARequirement([], [HasMorph])
    ]),
]

Sector4SerrisZone.locations = [
    FusionLocation("Sector 4 (AQA) -- Serris Arena", True, [
        Requirement(["Hi-Jump"], [CanFightBoss])
    ])
]

Sector4UpperWaterZone.locations = [
    FusionLocation("Sector 4 (AQA) -- Cargo Hold to Sector 5 (ARC)", False, [
        HasScrewAttack,
        HasSpeedBooster
    ]),
    FusionLocation("Sector 4 (AQA) -- Aquarium Pirate Tank", False, [CanPowerBomb]),
]

Sector4SecurityZone.locations = [
    FusionLocation("Sector 4 (AQA) -- Cheddar Bay", False, [CanAscendCheddarBay]),
    FusionLocation("Sector 4 (AQA) -- Yard Firing Range", False, [])
]

Sector4LowerSecurityZone.locations = [
    FusionLocation("Sector 4 (AQA) -- Sanctuary Cache", False, [
        Requirement(["Morph Ball", "Bomb Data"], [CanAccessSanctuaryCache]),
        Requirement(["Morph Ball", "Hi-Jump"], [CanAccessSanctuaryCache])
    ])
]

Sector4SecurityRoom.locations = [
    FusionLocation("Sector 4 (AQA) -- Level 4 Security Room", True, [
        Requirement(["Space Jump"], [HasKeycard4, CanAscendCheddarBay])
    ]),
]

Sector4RightWaterZone.locations = [
    FusionLocation("Sector 4 (AQA) -- Aquarium Kago Storage -- Left Item", False, [
        HasSpeedBooster,
        HasScrewAttack
    ]),
    FusionLocation("Sector 4 (AQA) -- Aquarium Kago Storage -- Right Item", False, [
        HasSpeedBooster
    ])
]

Sector4DataZone.locations = [
    FusionLocation("Sector 4 (AQA) -- Data Room", True, [
        CanDrainAQARequirement([], [HasKeycard4])
    ])
]

#endregion

#region Sector 5 Topology
Sector5Hub.connections = [
    VariableConnection(SectorHubElevator5Top, []),
    Connection(Sector5MagicBox, [
        Level3KeycardRequirement([], [])
    ]),
    Connection(Sector5BigRoom, [
        HasKeycard3,
        Requirement(["Morph Ball"], [HasMissile])
    ])
]

Sector5TubeLeft.connections = [
    VariableConnection(Sector6TubeRight, []),
    Connection(Sector5MagicBox, [HasScrewAttack])
]

Sector5TubeRight.connections = [
    VariableConnection(Sector3TubeLeft, []),
    Connection(Sector5BeforeNightmareHub, [], one_way=True)
]

Sector5BigRoom.connections = [
    Connection(Sector5FrozenHub, [HasVaria])
]

Sector5FrozenHub.connections = [
    Connection(Sector5DataRoom, [HasKeycard3], one_way=True),
    Connection(Sector5BeforeNightmareHub, [
        Level3KeycardRequirement([], [HasVaria])
    ]),
    Connection(Sector5SecurityZone, [
        Requirement(["Speed Booster"], [CanBombOrPowerBomb]),
        Level3KeycardRequirement([], [HasWaveBeam])
    ], one_way=True),

]

Sector5SecurityZone.connections = [
    Connection(Sector5DataRoom, [Requirement(["Space Jump"], [HasKeycard3])]),
    Connection(Sector5FrozenHub, [
        HasKeycard3,
        Requirement(["Space Jump"], [CanBombOrPowerBomb])
    ], one_way=True)
]

Sector5DataRoom.connections = [
    Connection(Sector5FrozenHub, [
        Level3KeycardRequirement([], [HasWaveBeam])
    ]),
    Connection(Sector5SecurityZone, [], one_way=True)
]

Sector5BeforeNightmareHub.connections = [
    Connection(Sector5TubeRight, [CanJumpHigh]),
    Connection(Sector5NightmareHub, [
        Requirement(["Hi-Jump"], [CanBeatToughEnemy])
    ], one_way=True)
]

Sector5NightmareHub.connections = [
    Connection(Sector5BeforeNightmareHub, [
        Requirement(["Gravity Suit"], [CanScrewAttackAndSpaceJump])
    ]),
    Connection(Sector5NightmareZoneArena, [CanSpeedBoosterUnderwater], one_way=True),
    Connection(Sector4UpperWaterZone, [CanSpeedBoosterUnderwater]),
    Connection(Sector5NightmareZoneUpper, [CanFightBoss])
]

Sector5NightmareZoneUpper.connections = [
    Connection(Sector5NightmareZoneArena, [])
]

Sector5NightmareZoneArena.connections = [
    Connection(Sector5NightmareHub, [CanEscapeNightmareRoom])
]

Sector5Hub.locations = [
    FusionLocation("Sector 5 (ARC) -- Gerubus Gully", False, [
        Level3KeycardRequirement([], [CanPowerBomb]),
        Level3KeycardRequirement(["Morph Ball", "Bomb Data"], [HasScrewAttack])
    ]),
]

Sector5MagicBox.locations = [
    FusionLocation("Sector 5 (ARC) -- Magic Box", False, [])
]

Sector5BigRoom.locations = [
    FusionLocation("Sector 5 (ARC) -- Training Aerie -- Left Item", False, [
        Requirement(["Speed Booster"], [HasSpaceJump, CanFreezeEnemies])
    ]),
    FusionLocation("Sector 5 (ARC) -- Training Aerie -- Right Item", False, [
        HasSpaceJump,
        CanFreezeEnemies
    ])
]

Sector5FrozenHub.locations = [
    FusionLocation("Sector 5 (ARC) -- Ripper Road", False, [CanAccessRipperRoad])
]

Sector5BeforeNightmareHub.locations = [
    FusionLocation("Sector 5 (ARC) -- Crow's Nest", False, [
        Requirement(["Morph Ball", "Power Bomb Data"], [HasSpaceJump]),
        Requirement(["Morph Ball"], [CanScrewAttackAndSpaceJump]),
        Requirement(["Morph Ball", "Power Bomb Data"], [CanDoSimpleWallJumpWithHiJump]),
        Requirement(["Morph Ball"], [CanDoSimpleWallJumpWithScrewAttack]),
    ])
]

Sector5DataRoom.locations = [
    FusionLocation("Sector 5 (ARC) -- Data Room", True, [])
]

Sector5SecurityZone.locations = [
    FusionLocation("Sector 5 (ARC) -- E-Tank Mimic Den", False, [
        Level3KeycardRequirement(
            ["Morph Ball", "Bomb Data"],
            [CanFreezeEnemies, HasSpaceJump]
        ),
        Level3KeycardRequirement(
            ["Morph Ball", "Power Bomb Data"],
            [CanFreezeEnemies, HasSpaceJump]
        ),
        Level3KeycardRequirement(
            ["Morph Ball", "Screw Attack"],
            [CanFreezeEnemies, HasSpaceJump]
        ),
    ]),
    FusionLocation("Sector 5 (ARC) -- Level 3 Security Room", True, []),
    FusionLocation("Sector 5 (ARC) -- Ripper's Treasure", False, [CanAccessRipperTreasure]),
    FusionLocation("Sector 5 (ARC) -- Security Shaft East", False, [CanPowerBomb]),
    FusionLocation("Sector 5 (ARC) -- Transmutation Trial", False, [
        Level3KeycardRequirement(["Hi-Jump"], [HasSpaceJump, CanFreezeEnemies])
    ])
]

Sector5NightmareHub.locations = [
    FusionLocation("Sector 5 (ARC) -- Flooded Airlock to Sector 4 (AQA)", False, [
        CanSpeedBoosterUnderwater
    ]),
    FusionLocation("Sector 5 (ARC) -- Mini-Fridge", False, [
        Requirement(["Missile Data", "Varia Suit", "Gravity Suit"], [CanBallJump])
    ]),
    FusionLocation("Sector 5 (ARC) -- Nightmare Hub", False, [
        Requirement(["Power Bomb Data"], [CanBallJump])
    ]),
    FusionLocation("Sector 5 (ARC) -- Ruined Break Room", False, [CanPowerBomb])
]

Sector5NightmareZoneUpper.locations = [
    FusionLocation("Sector 5 (ARC) -- Nightmare Nook", False, [CanBallJumpAndBomb])
]

Sector5NightmareZoneArena.locations = [
    FusionLocation("Sector 5 (ARC) -- Nightmare Arena", True, [CanFightLateGameBoss])
]
#endregion

#region Sector 6 Topology
Sector6Hub.connections = [
    VariableConnection(SectorHubElevator6Top, []),
    Connection(Sector6Crossroads, [CanDefeatMediumGeron]),
    Connection(Sector6TubeLeft, [HasScrewAttack])
]

Sector6TubeLeft.connections = [
    VariableConnection(Sector4TubeRight, [])
]

Sector6TubeRight.connections = [
    VariableConnection(Sector5TubeLeft, []),
    Connection(Sector6Crossroads, [HasScrewAttack])
]

Sector6Crossroads.connections = [
    Connection(Sector6BeforeXBOXZone, [
        Level4KeycardRequirement(["Varia Suit"], [CanPowerBomb])
    ]),
    Connection(Sector6BeforeVariaCoreXZone, [
        Requirement(["Speed Booster"], [CanBombOrPowerBomb])
    ]),
    Connection(Sector6AfterVariaCoreXZone, [
        Requirement(["Morph Ball", "Varia Suit"], [HasScrewAttack])
    ])
]

Sector6BeforeXBOXZone.connections = [
    Connection(Sector6XBOXZone, [], one_way=True)
]

Sector6XBOXZone.connections = [
    Connection(Sector6AfterXBOXZone, [CanFightLateGameBoss])
]

Sector6AfterXBOXZone.connections = [
    Connection(Sector6BeforeXBOXZone, [CanScrewAttackAndSpaceJump], one_way=True),
    Connection(Sector6RestrictedZone, [HasWaveBeam])
]

Sector6RestrictedZone.connections = [
    Connection(Sector6RestrictedZoneElevatorToTourian, [HasSpeedBooster], one_way=True)
]

Sector6RestrictedZoneElevatorToTourian.connections = [
    VariableConnection(Sector1TourianHubElevatorTop, [HasKeycard4])
]

Sector6BeforeVariaCoreXZone.connections = [
    Connection(Sector6VariaCoreXZone, [
        Level2KeycardRequirement([], [CanFightBoss])
    ])
]

Sector6VariaCoreXZone.connections = [
    Connection(Sector6AfterVariaCoreXZone, [
        Requirement(["Varia Suit"], [CanFightBoss])
    ])
]

Sector6AfterVariaCoreXZone.connections = [
    Connection(Sector6Crossroads, [HasMorph], one_way=True)
]

Sector6Hub.locations = [
    FusionLocation("Sector 6 (NOC) -- Entrance Lobby", False, [
        Requirement(["Screw Attack"], [CanBallJump]),
        Requirement([], [CanBallJumpAndBomb])
    ])
]

Sector6Crossroads.locations = [
    FusionLocation("Sector 6 (NOC) -- Catacombs", False, [HasSpeedBooster]),
    FusionLocation("Sector 6 (NOC) -- Missile Mimic Lodge", False, [
        Requirement(["Varia Suit"], [CanBombOrPowerBomb])
    ]),
    FusionLocation("Sector 6 (NOC) -- Pillar Highway", False, [
        Requirement(
            ["Screw Attack", "Speed Booster", "Varia Suit"],
            [CanBomb, HasWaveBeam]
        )
    ]),
    FusionLocation("Sector 6 (NOC) -- Vault", False, [CanBallJumpAndBomb])
]

Sector6BeforeXBOXZone.locations = [
    FusionLocation("Sector 6 (NOC) -- Spaceboost Alley -- Lower Item", False, [
        Requirement(["Hi-Jump", "Space Jump", "Screw Attack"], [HasSpeedBooster])
    ]),
    FusionLocation("Sector 6 (NOC) -- Spaceboost Alley -- Upper Item", False, [
        Requirement(["Screw Attack"], [HasSpeedBooster])
    ])
]

Sector6XBOXZone.locations = [
    FusionLocation("Sector 6 (NOC) -- X-B.O.X. Arena", True, [CanFightLateGameBoss])
]

Sector6AfterXBOXZone.locations = [
    FusionLocation("Sector 6 (NOC) -- X-B.O.X. Garage -- Lower Item", False, [HasWaveBeam]),
    FusionLocation("Sector 6 (NOC) -- X-B.O.X. Garage -- Upper Item", False, [
        Requirement(["Morph Ball", "Bomb Data"], [CanScrewAttackAndSpaceJump]),
    ])
]

Sector6RestrictedZone.locations = [
    FusionLocation("Main Deck -- Restricted Airlock", False, [HasSpeedBooster])
]

Sector6BeforeVariaCoreXZone.locations = [
    FusionLocation("Sector 6 (NOC) -- Zozoro Wine Cellar", False, [
        Requirement(["Morph Ball", "Bomb Data"], [CanJumpHigh]),
        Requirement(["Morph Ball", "Power Bomb Data"], [CanJumpHigh]),
    ])
]

Sector6VariaCoreXZone.locations = [
    FusionLocation("Sector 6 (NOC) -- Varia Core-X Arena", True, [CanFightBoss])
]

Sector6AfterVariaCoreXZone.locations = [
    FusionLocation("Sector 6 (NOC) -- Twin Caverns West -- Lower Item", False, [
        Requirement(["Morph Ball"], [CanJumpHigh])
    ]),
    FusionLocation("Sector 6 (NOC) -- Twin Caverns West -- Upper Item", False, [])
]

#endregion

#endregion

fusion_regions: list[FusionRegion] = [
    MainDeckHub,
    VentilationZone,
    UpperArachnusArena,
    LowerArachnusArena,
    OperationsDeckElevatorBottom,
    OperationsDeckElevatorTop,
    OperationsDeck,
    HabitationDeckElevatorBottom,
    HabitationDeckElevatorTop,
    HabitationDeck,
    SectorHubElevatorTop,
    SectorHubElevatorBottom,
    SectorHubElevator1Top,
    SectorHubElevator2Top,
    SectorHubElevator3Top,
    SectorHubElevator4Top,
    SectorHubElevator5Top,
    SectorHubElevator6Top,
    ReactorZone,
    YakuzaZone,
    AuxiliaryReactor,
    NexusStorage,
    Sector1Hub,
    Sector1TubeLeft,
    Sector1TubeRight,
    Sector1Antechamber,
    Sector1FirstStabilizerZone,
    Sector1SecondStabilizerZone,
    Sector1ChargeCoreZone,
    Sector1AfterChargeCoreZone,
    Sector1TourianExit,
    Sector1TourianHub,
    Sector1TourianHubElevatorTop,
    Sector2Hub,
    Sector2TubeLeft,
    Sector2TubeRight,
    Sector2LeftSide,
    Sector2ZazabiZone,
    Sector2ZazabiZoneUpper,
    Sector2NettoriZone,
    Sector3Hub,
    Sector3TubeLeft,
    Sector3TubeRight,
    Sector3SecurityZone,
    Sector3MainShaft,
    Sector3BoilerZone,
    Sector3BobZone,
    Sector3BOXZone,
    Sector3Attic,
    Sector3SovaProcessing,
    Sector4Hub,
    Sector4TubeLeft,
    Sector4TubeRight,
    Sector4UpperZone,
    Sector4SerrisZone,
    Sector4PumpControl,
    Sector4UpperWaterZone,
    Sector4SecurityZone,
    Sector4LowerSecurityZone,
    Sector4SecurityRoom,
    Sector4RightWaterZone,
    Sector4DataZone,
    Sector4RightDataZone,
    Sector5Hub,
    Sector5TubeLeft,
    Sector5TubeRight,
    Sector5MagicBox,
    Sector5BigRoom,
    Sector5FrozenHub,
    Sector5SecurityZone,
    Sector5DataRoom,
    Sector5BeforeNightmareHub,
    Sector5NightmareHub,
    Sector5NightmareZoneUpper,
    Sector5NightmareZoneArena,
    Sector6Hub,
    Sector6TubeLeft,
    Sector6TubeRight,
    Sector6Crossroads,
    Sector6BeforeXBOXZone,
    Sector6XBOXZone,
    Sector6AfterXBOXZone,
    Sector6RestrictedZone,
    Sector6RestrictedZoneElevatorToTourian,
    Sector6BeforeVariaCoreXZone,
    Sector6VariaCoreXZone,
    Sector6AfterVariaCoreXZone,
]

left_tubes = [
    Sector1TubeLeft,
    Sector2TubeLeft,
    Sector3TubeLeft,
    Sector4TubeLeft,
    Sector5TubeLeft,
    Sector6TubeLeft
]

right_tubes = [
    Sector3TubeRight,
    Sector1TubeRight,
    Sector5TubeRight,
    Sector2TubeRight,
    Sector6TubeRight,
    Sector4TubeRight
]

sector_elevator_tops = [
    SectorHubElevator1Top,
    SectorHubElevator2Top,
    SectorHubElevator3Top,
    SectorHubElevator4Top,
    SectorHubElevator5Top,
    SectorHubElevator6Top
]

sector_elevator_bottoms = [
    Sector1Hub,
    Sector2Hub,
    Sector3Hub,
    Sector4Hub,
    Sector5Hub,
    Sector6Hub
]

sector_elevators = [
    *sector_elevator_tops,
    *sector_elevator_bottoms
]

other_elevator_tops = [
    OperationsDeckElevatorTop,
    HabitationDeckElevatorTop,
    SectorHubElevatorTop,
    Sector1TourianHubElevatorTop,
]

other_elevator_bottoms = [
    OperationsDeckElevatorBottom,
    HabitationDeckElevatorBottom,
    SectorHubElevatorBottom,
    Sector6RestrictedZoneElevatorToTourian,
]

other_elevators = [
    *other_elevator_tops,
    *other_elevator_bottoms
]

default_region_map = {
    Sector1TubeLeft: Sector3TubeRight,
    Sector2TubeLeft: Sector1TubeRight,
    Sector3TubeLeft: Sector5TubeRight,
    Sector4TubeLeft: Sector2TubeRight,
    Sector5TubeLeft: Sector6TubeRight,
    Sector6TubeLeft: Sector4TubeRight,
    SectorHubElevator1Top: Sector1Hub,
    SectorHubElevator2Top: Sector2Hub,
    SectorHubElevator3Top: Sector3Hub,
    SectorHubElevator4Top: Sector4Hub,
    SectorHubElevator5Top: Sector5Hub,
    SectorHubElevator6Top: Sector6Hub,
    OperationsDeckElevatorTop: OperationsDeckElevatorBottom,
    HabitationDeckElevatorTop: HabitationDeckElevatorBottom,
    SectorHubElevatorTop: SectorHubElevatorBottom,
    Sector1TourianHubElevatorTop: Sector6RestrictedZoneElevatorToTourian
}

reverse_region_map = {v: k for k, v in default_region_map.items()}

full_default_region_map = {
    **default_region_map,
    **reverse_region_map
}

sector_tube_id_lookups = {
    Sector1TubeLeft.name: 1,
    Sector1TubeRight.name: 1,
    Sector2TubeLeft.name: 2,
    Sector2TubeRight.name: 2,
    Sector3TubeLeft.name: 3,
    Sector3TubeRight.name: 3,
    Sector4TubeLeft.name: 4,
    Sector4TubeRight.name: 4,
    Sector5TubeLeft.name: 5,
    Sector5TubeRight.name: 5,
    Sector6TubeLeft.name: 6,
    Sector6TubeRight.name: 6
}

elevator_id_lookups = {
    OperationsDeckElevatorTop.name: "OperationsDeckTop",
    SectorHubElevator1Top.name: "MainHubToSector1",
    SectorHubElevator2Top.name: "MainHubToSector2",
    SectorHubElevator3Top.name: "MainHubToSector3",
    SectorHubElevator4Top.name: "MainHubToSector4",
    SectorHubElevator5Top.name: "MainHubToSector5",
    SectorHubElevator6Top.name: "MainHubToSector6",
    SectorHubElevatorTop.name: "MainHubTop",
    HabitationDeckElevatorTop.name: "HabitationDeckTop",
    Sector1TourianHubElevatorTop.name: "Sector1ToRestrictedLab",
    OperationsDeckElevatorBottom.name: "OperationsDeckBottom",
    SectorHubElevatorBottom.name: "MainHubBottom",
    Sector6RestrictedZoneElevatorToTourian.name: "RestrictedLabToSector1",
    HabitationDeckElevatorBottom.name: "HabitationDeckBottom",
    Sector1Hub.name: "Sector1ToMainHub",
    Sector2Hub.name: "Sector2ToMainHub",
    Sector3Hub.name: "Sector3ToMainHub",
    Sector4Hub.name: "Sector4ToMainHub",
    Sector5Hub.name: "Sector5ToMainHub",
    Sector6Hub.name: "Sector6ToMainHub"
}