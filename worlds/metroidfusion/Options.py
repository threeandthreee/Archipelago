from dataclasses import dataclass

from Options import (Toggle, Range, Choice, PerGameCommonOptions, DefaultOnToggle, StartInventoryPool, OptionGroup,
                     OptionSet, Visibility)

class EarlyProgression(Choice):
    """Determines if an early progression item guaranteed in one of your first locations.
    Normal restricts the starting item pool to Morph Ball and Missiles.
    Advanced expands the pool to Screw Attack.
    If Tricky Shinessparks In Region Logic (below) is enabled, adds Speed Booster as well
    Option is in testing and may increase generation failures."""
    display_name = "Early Progression"
    option_none = 0
    option_normal = 1
    option_advanced = 2
    default = 1

class TrickyShinesparksInRegionLogic(Toggle):
    """Are difficult or risky shinesparks required to navigate around?
    Note that this does not exclude items that require shinesparking in vanilla to obtain.
    Use the ShinesparkLocations location group for that."""
    display_name = "Tricky Shinesparks in Region Logic"

class GameMode(Choice):
    """Determines starting location and accessibility.
    Vanilla starts you in the Docking Bay with no items.
    Open Sector Hub starts you in the Sector Hub with one E-Tank and one random item. All sector elevators will be open."""
    display_name = "Game Mode"
    option_vanilla = 0
    option_open_sector_hub = 1

class InfantMetroidsInPool(Range):
    """How many Infant Metroids will be in the item pool."""
    display_name = "Infant Metroids in Pool"
    range_start = 1
    range_end = 20
    default = 5

class InfantMetroidsRequired(Range):
    """How many Infant Metroids will be required to beat the game.
    If set to more than the number in the pool, will instead become however many are present."""
    display_name = "Infant Metroids Required"
    range_start = 1
    range_end = 20
    default = 5

class PaletteRandomization(Toggle):
    """Randomize the ingame palettes."""
    display_name = "Palette Randomization"

class EnableHints(DefaultOnToggle):
    """Enable ingame hints at Navigation Stations."""
    display_name = "Enable Hints"

class RevealHiddenBlocks(DefaultOnToggle):
    """Enables whether destructible blocks are revealed from the start."""
    display_name = "Reveal Hidden Blocks"

class FastDoorTransitions(DefaultOnToggle):
    """Enables fast door transitions between rooms."""
    display_name = "Fast Door Transitions"

class MissileDataAmmo(Range):
    """The amount of missiles provided by a Missile Data item."""
    display_name = "Missile Data Ammo"
    range_start = 5
    range_end = 100
    default = 10

class PowerBombDataAmmo(Range):
    """The amount of power bombs provided by a Power Bomb Data item."""
    display_name = "Power Bomb Data Ammo"
    range_start = 5
    range_end = 100
    default = 10

class MissileTankAmmo(Range):
    """The amount of missiles provided by a Missile Tank item."""
    display_name = "Missile Tank Ammo"
    range_start = 0
    range_end = 100
    default = 5

class PowerBombTankAmmo(Range):
    """The amount of power bombs provided by a Power Bomb Tank item."""
    display_name = "Power Bomb Tank Ammo"
    range_start = 0
    range_end = 100
    default = 2

@dataclass
class MetroidFusionOptions(PerGameCommonOptions):
    EarlyProgression: EarlyProgression
    TrickyShinesparksInRegionLogic: TrickyShinesparksInRegionLogic
    GameMode: GameMode
    InfantMetroidsInPool: InfantMetroidsInPool
    InfantMetroidsRequired: InfantMetroidsRequired
    PaletteRandomization: PaletteRandomization
    EnableHints: EnableHints
    RevealHiddenBlocks: RevealHiddenBlocks
    FastDoorTransitions: FastDoorTransitions
    MissileDataAmmo: MissileDataAmmo
    MissileTankAmmo: MissileTankAmmo
    PowerBombDataAmmo: PowerBombDataAmmo
    PowerBombTankAmmo: PowerBombTankAmmo
