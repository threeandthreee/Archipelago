from dataclasses import dataclass
from Options import Choice, Toggle, PerGameCommonOptions, DefaultOnToggle, StartInventoryPool


class TutorialSkip(Toggle):
    """Remove the need to complete the tutorial and unlock tutorial related tech. Grant a free launch for every selected planet."""
    display_name = "Tutorial skip"

class CampaignChoice(Choice):
    """Select Serpulo, Erekir or both for the randomized campaign."""
    display_name = "Campaign choice"
    option_serpulo_only = 0
    option_erekir_only = 1
    option_all_planets = 2
    default = 0

class DisableInvasions(Toggle):
    """Disable invasions and prevent losing progress."""
    display_name = "Disable invasions"

class FasterProduction(Toggle):
    """Enable faster production and harvesting of resources."""
    display_name = "Faster production"

class DeathLink(Toggle):
    """Enable death link."""
    display_name = "Death link"

class MilitaryLevelTracking(DefaultOnToggle):
    """Ensure the player has enough military power to clear sectors. If turned off, the logic will consider that the player can clear every sector once they have the minimal requirement to land on that sector."""
    display_name = "Military level tracking"

class RandomizeCoreUnitsWeapon(Toggle):
    """Will randomize core units weapon. Erekir core unit will be made vulnerable and be given an ability instead."""
    display_name = "Randomize core units weapon"

class LogisticDistribution(Choice):
    """Change how logistics research are distributed."""
    display_name = "Logistic distribution"
    option_randomized_logistics = 0
    option_early_logistics = 1
    option_local_early_logistics = 2
    option_starter_logistics = 3
    default = 1


@dataclass
class MindustryOptions(PerGameCommonOptions):
    """
    Options for Mindustry randomizer.
    """
    start_inventory_from_pool: StartInventoryPool
    tutorial_skip: TutorialSkip
    campaign_choice: CampaignChoice
    disable_invasions: DisableInvasions
    faster_production: FasterProduction
    death_link: DeathLink
    military_level_tracking: MilitaryLevelTracking
    randomize_core_units_weapon: RandomizeCoreUnitsWeapon
    logistic_distribution: LogisticDistribution
