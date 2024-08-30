from dataclasses import dataclass
from Options import DefaultOnToggle, Choice, Toggle, PerGameCommonOptions


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

class deathLink(Toggle):
    """Enable death link."""
    display_name = "Death link"


@dataclass
class MindustryOptions(PerGameCommonOptions):
    """
    Options for Mindustry randomizer.
    """
    tutorial_skip: TutorialSkip
    campaign_choice: CampaignChoice
    disable_invasions: DisableInvasions
    faster_production: FasterProduction
    death_link: deathLink
