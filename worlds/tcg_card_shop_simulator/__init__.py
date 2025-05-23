from typing import ClassVar

from Options import OptionError
from Utils import visualize_regions
from worlds.AutoWorld import WebWorld, World
from BaseClasses import Tutorial
from .options import *
from .regions import *
from .locations import *
from .items import *
from .rules import *


class TCGSimulatorWeb(WebWorld):
    theme = "partyTime"

    setup_en = Tutorial(
        tutorial_name="Multiworld Setup Guide",
        description="A guide to setting up the TCG Card Shop Simulator randomizer connected to an Archipelago Multiworld.",
        language="English",
        file_name="setup_en.md",
        link="setup/en",
        authors=["FyreDay"]
    )

    tutorials = [setup_en]


class TCGSimulatorWorld(World):

    game = "TCG Card Shop Simulator"
    web = TCGSimulatorWeb()
    options_dataclass = TCGSimulatorOptions
    options: TCGSimulatorOptions

    option_groups = tcg_cardshop_simulator_option_groups

    item_name_to_id: ClassVar[Dict[str, int]] = {item_name: item_data.code for item_name, item_data in full_item_dict.items()}
    location_name_to_id: ClassVar[Dict[str, int]] = full_location_dict

    location_dict = {}
    card_dict = {}

    local_items = {}
    local_locations = {}

    starting_names = []
    excluded_items = []
    excluded_locs = []
    startingLocs = []

    pg1_ids = []
    pg2_ids = []
    pg3_ids = []
    tt_ids = []
    lastRegion = -1

    ghost_item_counts = {}

    def swap_within_n(self, lst, target, n, invalid_indexes):
        if target not in lst:
            return invalid_indexes  # Return unchanged invalid list if target not found

        index = lst.index(target)  # Find the index of the target

        # Generate a valid swap index (between 0 and n, but not in invalid_indexes)
        valid_indexes = [i for i in range(min(n + 1, len(lst))) if i not in invalid_indexes]

        if not valid_indexes:
            return invalid_indexes  # No valid swaps available

        swap_index = self.random.choice(valid_indexes)  # Pick a valid index

        # Swap the target element with the chosen index
        lst[index], lst[swap_index] = lst[swap_index], lst[index]

        # Add the new index to the invalid list
        invalid_indexes.append(swap_index)

        return invalid_indexes

    def randomize_shops(self):
        self.pg1_ids = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 67, 68, 69, 70, 24, 25, 26, 27, 28, 29, 30, 31,
                   32,
                   33, 34, 35, 36, 37, 38, 39, 71, 72, 73, 74]
        self.pg2_ids = [40, 41, 75, 76, 43, 44, 45, 46, 77, 78, 79, 80, 16, 17, 18, 19, 20, 21, 22, 23, 42, 66, 83, 81, 87,
                   95, 90, 82, 86, 85, 84, 88, 91, 92, 94, 93, 89, 115, 116, 117, 118, 101, 102, 103, 104, 105, 106,
                   107, 108, 109, 110, 111, 112]

        self.pg3_ids = [47, 48, 49, 50, 52, 55, 58, 61, 53, 56, 59, 62, 54, 57, 60, 63, 65, 64, 51]

        self.tt_ids = [124, 130, 119, 123, 120, 125, 126, 127, 128, 121, 122, 129, 99, 100, 97, 96, 98]

        self.random.shuffle(self.pg1_ids)
        self.random.shuffle(self.pg2_ids)
        self.random.shuffle(self.pg3_ids)
        self.random.shuffle(self.tt_ids)

        invalid_swaps: list[int] = []

        random_basic = random.randint(0, 3)
        invalid_swaps = self.swap_within_n(self.pg1_ids, self.pg1_ids.index(random_basic), 12, invalid_swaps)

        random_rare = random.randint(4, 7)
        invalid_swaps = self.swap_within_n(self.pg1_ids, self.pg1_ids.index(random_rare), 16, invalid_swaps)

        random_epic = random.randint(8, 11)
        invalid_swaps = self.swap_within_n(self.pg1_ids, self.pg1_ids.index(random_epic), 16, invalid_swaps)

        random_legendary = random.randint(12, 15)
        invalid_swaps = self.swap_within_n(self.pg1_ids, self.pg1_ids.index(random_legendary), 16, invalid_swaps)

        random_d_basic = random.randint(24, 27)
        invalid_swaps = self.swap_within_n(self.pg1_ids, self.pg1_ids.index(random_d_basic), 20, invalid_swaps)

        random_d_rare = random.randint(28, 31)
        invalid_swaps = self.swap_within_n(self.pg1_ids, self.pg1_ids.index(random_d_rare), 20, invalid_swaps)

        random_d_epic = random.randint(32, 35)
        invalid_swaps = self.swap_within_n(self.pg1_ids, self.pg1_ids.index(random_d_epic), 20, invalid_swaps)

        random_d_legendary = random.randint(36, 39)
        invalid_swaps = self.swap_within_n(self.pg1_ids, self.pg1_ids.index(random_d_legendary), 20, invalid_swaps)

        random_cleanser = random.randint(40, 41)
        self.swap_within_n(self.pg2_ids, self.pg2_ids.index(random_cleanser), 8, invalid_swaps)

    def __init__(self, multiworld, player):
        self.itempool = []
        self.starting_names = []
        self.pg1_ids = []
        self.pg2_ids = []
        self.pg3_ids = []
        self.tt_ids = []
        self.excluded_items = []
        self.excluded_locs = []
        super().__init__(multiworld, player)

    def generate_early(self) -> None:
        if self.options.money_bags.value == 0 and self.options.xp_boosts.value == 0 and self.options.random_card.value == 0 and self.options.random_new_card.value == 0:
            raise OptionError("All Junk Weights are Zero")
        if self.options.trap_fill.value != 0 and self.options.stink_trap.value == 0 and self.options.poltergeist_trap.value == 0 and self.options.decrease_card_luck_trap == 0 and self.options.market_change_trap == 0 and self.options.currency_trap == 0:
            raise OptionError("All Trap Weights are Zero")

        self.randomize_shops()
        loc_dict, card_locs, starting_str, starting_l, final_level, excludedItems = generate_locations(self, self.pg1_ids,self.pg2_ids,self.pg3_ids,self.tt_ids)
        self.location_dict = loc_dict.copy()
        self.card_dict = card_locs.copy()
        self.starting_names = starting_str[:]
        self.startingLocs = starting_l[:]
        self.lastRegion = final_level
        self.excluded_items = excludedItems[:]

    def create_regions(self):
        excludedLocs = create_regions(self, self.location_dict , self.card_dict, self.lastRegion)
        self.excluded_locs = excludedLocs[:]
        loc_dict = connect_entrances(self,self.location_dict, self.lastRegion)
        self.location_dict = loc_dict

    def create_item(self, item: str) -> TCGSimulatorItem:
        if item in junk_weights.keys():
            return TCGSimulatorItem(item, ItemClassification.filler, self.item_name_to_id[item], self.player)
        return TCGSimulatorItem(item, ItemClassification.progression, self.item_name_to_id[item], self.player)

    def create_items(self):
        starting_items, ghost_counts = create_items(self, self.starting_names, self.excluded_items, self.excluded_locs)

        self.push_precollected(starting_items[0])
        self.push_precollected(starting_items[1])
        self.push_precollected(starting_items[2])

        self.ghost_item_counts = ghost_counts

    def set_rules(self):
        set_rules(self, self.excluded_locs, self.startingLocs, self.lastRegion, self.ghost_item_counts)

    # def generate_output(self, output_directory: str):
        # visualize_regions(self.multiworld.get_region("Menu", self.player), f"Player{self.player}.puml",
        #                   show_entrance_names=False,
        #                   regions_to_highlight=self.multiworld.get_all_state(self.player).reachable_regions[
        #                       self.player])

    def fill_slot_data(self) -> id:
        return {
            "ModVersion": "0.3.2",
            "ShopPg1Mapping": self.pg1_ids,
            "ShopPg2Mapping": self.pg2_ids,
            "ShopPg3Mapping": self.pg3_ids,
            "ShopTTMapping": self.tt_ids,
            "Goal": self.options.goal.value,
            "ShopExpansionGoal": self.options.shop_expansion_goal.value,
            "LevelGoal": self.options.level_goal.value,
            "Deathlink": self.options.deathlink.value,
            "SellCheckAmount": self.options.sell_check_amount.value,
            "ChecksPerPack": self.options.checks_per_pack.value,
            "CardCollectPercentage": self.options.card_collect_percent.value,
            "NumberOfGameChecks": self.options.game_check_count.value,
            "GamesPerCheck": self.options.games_per_check.value,
            "NumberOfSellCardChecks": self.options.sell_card_check_count.value,
            "SellCardsPerCheck": self.options.sell_cards_per_check.value,
            "CardSanity": self.options.card_sanity.value,
            "FoilInSanity": self.options.foil_sanity.value,
            "BorderInSanity": self.options.border_sanity.value,
            "GhostGoalAmount": self.options.ghost_goal_amount.value,
            "BetterTrades": self.options.better_trades.value,
            "TrapFill": self.options.trap_fill.value,
            "FinalLevelRequirement": self.lastRegion
        }
