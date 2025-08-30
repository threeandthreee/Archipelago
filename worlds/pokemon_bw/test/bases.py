from test.bases import WorldTestBase
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .. import PokemonBWWorld


class PokemonBWTestBase(WorldTestBase):
    game = "Pokemon Black and White"
    world: "PokemonBWWorld"
    options = {"goal": "ghetsis"}


# Options irrelevant for testing:
# version (always random)
# reusable_tms (too complex to test)

# Options that are already included in default options:
# goal: ghetsis
# shuffle_badges: shuffle
# shuffle_tm_hm: shuffle
# dexsanity: 0
# season_control: vanilla
# modify_item_pool: []
# modify_logic: ["Require Dowsing Machine", "Prioritize key item locations"]

# Options that have high failure rate in single worlds:
# shuffle_badges: any_badge


###################################################
# Goal                                            #
###################################################

class TestGoalChampion(PokemonBWTestBase):
    options = {"goal": "champion"}


class TestGoalCynthia(PokemonBWTestBase):
    options = {"goal": "cynthia"}


class TestGoalCobalion(PokemonBWTestBase):
    options = {"goal": "cobalion"}


class TestGoalTMHMHunt(PokemonBWTestBase):
    options = {"goal": "tmhm_hunt"}


class TestGoalSevenSagesHunt(PokemonBWTestBase):
    options = {"goal": "seven_sages_hunt"}


class TestGoalLegendaryHunt(PokemonBWTestBase):
    options = {"goal": "legendary_hunt"}


class TestGoalPokemonMaster(PokemonBWTestBase):
    options = {"goal": "pokemon_master"}


###################################################
# Shuffle Badges                                  #
###################################################

class TestShuffleBadgesVanilla(PokemonBWTestBase):
    options = {"shuffle_badges": "vanilla"}


class TestShuffleBadgesAnybadge(PokemonBWTestBase):
    options = {"shuffle_badges": "any_badge"}


class TestShuffleBadgesAnything(PokemonBWTestBase):
    options = {"shuffle_badges": "anything"}


###################################################
# Shuffle TM/HM                                   #
###################################################

class TestShuffleTMHMHMWithBadge(PokemonBWTestBase):
    options = {"shuffle_tm_hm": "hm_with_badge"}


class TestShuffleTMHMAnyTMHM(PokemonBWTestBase):
    options = {"shuffle_tm_hm": "any_tm_hm"}


class TestShuffleTMHMAnything(PokemonBWTestBase):
    options = {"shuffle_tm_hm": "anything"}


###################################################
# Dexsanity                                       #
###################################################

class TestDexsanityPartial(PokemonBWTestBase):
    options = {"dexsanity": 100}


class TestDexsanityFull(PokemonBWTestBase):
    options = {"dexsanity": 649}


###################################################
# Season Control                                  #
###################################################

class TestSeasonControlChangeable(PokemonBWTestBase):
    options = {"season_control": "changeable"}


class TestSeasonControlRandomized(PokemonBWTestBase):
    options = {"season_control": "randomized"}


###################################################
# Modify Item Pool                                #
###################################################

class TestModifyItemPoolAll(PokemonBWTestBase):
    options = {"modify_item_pool": ["Useless key items", "Useful filler", "Ban bad filler"]}


###################################################
# Modify Logic                                    #
###################################################

class TestModifyLogicInverse(PokemonBWTestBase):
    options = {"modify_logic": []}
