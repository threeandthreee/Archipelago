import re
from collections import Counter
from dataclasses import dataclass
from typing import Optional, Dict, List

from BaseClasses import Item, ItemClassification
from Options import OptionError


class TCGSimulatorItem(Item):
    game: str = "TCG Card Shop Simulator"


@dataclass
class ItemData:
    code: int
    classification: ItemClassification
    amount: Optional[int] = 1

def create_item(world, name: str, classification: ItemClassification, amount: Optional[int] = 1):
    for i in range(amount):
        world.itempool.append(Item(name, classification, world.item_name_to_id[name], world.player))


def generate_ghost_card_items(world, ghost_goal_amount, locs_available):
    if locs_available * 5 < ghost_goal_amount:
        raise OptionError("Not enough locations for ghost goal")

    result = []
    remaining = ghost_goal_amount
    remaining_slots = locs_available

    while remaining > 0 and remaining_slots > 0:
        max_size = min(5 if remaining_slots < 50 else 2, remaining)
        min_size = max(1, remaining - (remaining_slots - 1) * 5)
        size = world.random.randint(min_size, max_size)

        result.append(size)
        remaining -= size
        remaining_slots -= 1

    return result


def create_items(world, starting_names, ignored_items, ignored_locs):

    total_location_count = len(world.multiworld.get_unfilled_locations(world.player))
    # print(f"total locs at start {total_location_count}")
    # print(f"total Itempool at start {len(world.itempool)}")
    # print(f"info {world.player} : {world.options.goal.value}")
    #
    # print(f"total items at before forloop {len(world.itempool)}")
    starting_items: List[Item] = []
    num  = 0
    for item_name, item_data in item_dict.items():
        #starting item should not be shuffled
        if item_name in starting_names:
            # print(f"starting is {item_name}")
            starting_items.append(Item(item_name, item_data.classification, world.item_name_to_id[item_name], world.player))
            continue
        if re.sub(r' \(\d+\)$', '', item_name) in ignored_items:
            print(item_name)
            continue
        num = num +1
        create_item(world, item_name, item_data.classification, item_data.amount)
    # print(f"total items at before progressive {len(world.itempool)}")



    for item_name, item_data in progressive_dict.items():
        override = 0

        if item_name == "Progressive Shop Expansion A":
            if world.options.goal.value == 0:
                override = world.options.shop_expansion_goal.value + world.options.shop_expansion_goal.value % 2
            else:
                override = item_data.amount - sum(1 for item in ignored_locs if re.search(r'^Shop A Expansion', item))
            # print(f"{override} Progressive A")

        if item_name == "Progressive Shop Expansion B":
            override = item_data.amount + 1 - sum(1 for item in ignored_locs if re.search(r'^Shop B Expansion', item))
            # print(sum(1 for item in ignored_item_names if re.search(r'^Shop B Expansion', item)))
            # print(f"{override} Progressive B")

        # if item_name == "Progressive Ghost Card" and world.options.goal.value == 2:
        #     override = 80 if world.options.ghost_goal_amount.value > 75 else world.options.ghost_goal_amount.value + 5
        #     # print(f"in ghost goal? {world.options.goal.value == 2} count: {override}")

        # print(f"item : {item_name} with {item_data.amount} override: {override}")
        create_item(world, item_name, item_data.classification, item_data.amount if override == 0 else override)

    print(f"total locs at remaining {total_location_count}")
    print(f"total items at remaining {len(world.itempool)}")
    remaining_locations: int = total_location_count - len(world.itempool)
    ghost_counts = 0
    if world.options.goal.value == 2:
        ghost_items = generate_ghost_card_items(world, world.options.ghost_goal_amount.value, remaining_locations)

        ghost_counts = Counter(ghost_items)
        print(f"ghost counts: {ghost_counts} from {ghost_items}")
        for bagsize, amount in ghost_counts.items():
            plural = "s" if bagsize > 1 else ""
            item_name = f"{bagsize} Ghost Card{plural}"
            create_item(world, item_name, ItemClassification.progression, amount)

        remaining_locations = remaining_locations - len(ghost_items)

    print(f"Remaining locations here: {remaining_locations}")

    trap_count = round(remaining_locations * world.options.trap_fill.value / 100)

    # -1 on LevelGoal because I place a victory item at the goal level
    junk_count = remaining_locations - trap_count - (1 if world.options.goal == 1 else 0)

    print(f"junk count {junk_count + trap_count}")

    trap_weights = {
        "Stink Trap": world.options.stink_trap,
        "Poltergeist Trap": world.options.poltergeist_trap,
        "Credit Card Failure Trap": world.options.credit_card_failure_trap,
        "Market Change Trap":world.options.market_change_trap,
        "Decrease Card Luck":world.options.decrease_card_luck_trap,
        "Currency Trap":world.options.currency_trap
    }

    junk_weights["Small Xp"] =  world.options.xp_boosts * 0.5 if world.options.goal.value != 1 else 0
    junk_weights["Medium Xp"] = world.options.xp_boosts * 0.3 if world.options.goal.value != 1 else 0
    junk_weights["Large Xp"] = world.options.xp_boosts * 0.2 if world.options.goal.value != 1 else 0
    junk_weights["Small Money"] = world.options.money_bags * 0.5
    junk_weights["Medium Money"] = world.options.money_bags * 0.3
    junk_weights["Large Money"] = world.options.money_bags * 0.2
    junk_weights["Random Card"] = world.options.random_card
    junk_weights["Random New Card"] = world.options.random_new_card
    junk_weights["Progressive Customer Money"] = world.options.customer_wealth
    junk_weights["Increase Card Luck"] = world.options.card_luck

    junk = get_junk_item_names(world.multiworld.random, junk_count)

    for name in junk:
        create_item(world, name, ItemClassification.filler)

    trap = get_trap_item_names(world.multiworld.random, trap_count, trap_weights)
    for name in trap:
        create_item(world, name, ItemClassification.trap)
    world.multiworld.itempool += world.itempool
    return starting_items, ghost_counts

def get_junk_item_names(rand, k: int) -> str:
    junk = rand.choices(
        list(junk_weights.keys()),
        weights=list(junk_weights.values()),
        k=k)
    return junk


def get_trap_item_names(rand, k: int, trap_weights) -> str:
    trap = rand.choices(
        list(trap_weights.keys()),
        weights=list(trap_weights.values()),
        k=k)
    return trap


item_dict: Dict[str, ItemData] = {
    "Fire Battle Deck (18)": ItemData(0x1F280005, ItemClassification.progression),
    "Earth Battle Deck (18)": ItemData(0x1F280006, ItemClassification.progression),
    "Water Battle Deck (18)": ItemData(0x1F280007, ItemClassification.progression),
    "Wind Battle Deck (18)": ItemData(0x1F280008, ItemClassification.progression),
    "Fire Destiny Deck (18)": ItemData(0x1F28000D, ItemClassification.progression),
    "Earth Destiny Deck (18)": ItemData(0x1F28000E, ItemClassification.progression),
    "Water Destiny Deck (18)": ItemData(0x1F28000F, ItemClassification.progression),
    "Wind Destiny Deck (18)": ItemData(0x1F280010, ItemClassification.progression),
    "Card Sleeves (Clear)": ItemData(0x1F280012, ItemClassification.progression),
    "Card Sleeves (Tetramon)": ItemData(0x1F280013, ItemClassification.progression),
    "D20 Dice Red (16)": ItemData(0x1F280014, ItemClassification.progression),
    "D20 Dice Blue (16)": ItemData(0x1F280015, ItemClassification.progression),
    "D20 Dice Black (16)": ItemData(0x1F280016, ItemClassification.progression),
    "D20 Dice White (16)": ItemData(0x1F280017, ItemClassification.progression),
    "Card Sleeves (Fire)": ItemData(0x1F280018, ItemClassification.progression),
    "Card Sleeves (Earth)": ItemData(0x1F280019, ItemClassification.progression),
    "Card Sleeves (Water)": ItemData(0x1F28001A, ItemClassification.progression),
    "Card Sleeves (Wind)": ItemData(0x1F28001B, ItemClassification.progression),
    "Collection Book (4)": ItemData(0x1F280020, ItemClassification.progression),
    "Premium Collection Book (4)": ItemData(0x1F280021, ItemClassification.progression),
    "Playmat (Drilceros)": ItemData(0x1F280022, ItemClassification.progression),
    "Playmat (Clamigo)": ItemData(0x1F280023, ItemClassification.progression),
    "Playmat (Wispo)": ItemData(0x1F280024, ItemClassification.progression),
    "Playmat (Lunight)": ItemData(0x1F280025, ItemClassification.progression),
    "Playmat (Kyrone)": ItemData(0x1F280026, ItemClassification.progression),
    "Playmat (Duel)": ItemData(0x1F280027, ItemClassification.progression),
    "Playmat (Dracunix1)": ItemData(0x1F280028, ItemClassification.progression),
    "Playmat (The Four Dragons)": ItemData(0x1F280029, ItemClassification.progression),
    "Playmat (Drakon)": ItemData(0x1F28002A, ItemClassification.progression),
    "Playmat (GigatronX Evo)": ItemData(0x1F28002B, ItemClassification.progression),
    "Playmat (Fire)": ItemData(0x1F28002C, ItemClassification.progression),
    "Playmat (Earth)": ItemData(0x1F28002D, ItemClassification.progression),
    "Playmat (Water)": ItemData(0x1F28002E, ItemClassification.progression),
    "Playmat (Wind)": ItemData(0x1F28002F, ItemClassification.progression),
    "Playmat (Tetramon)": ItemData(0x1F280030, ItemClassification.progression),
    "Pigni Plushie (12)": ItemData(0x1F280031, ItemClassification.progression),
    "Nanomite Plushie (16)": ItemData(0x1F280032, ItemClassification.progression),
    "Minstar Plushie (24)": ItemData(0x1F280033, ItemClassification.progression),
    "Nocti Plushie (6)": ItemData(0x1F280034, ItemClassification.progression),
    "Burpig Figurine (12)": ItemData(0x1F280035, ItemClassification.progression),
    "Decimite Figurine (8)": ItemData(0x1F280036, ItemClassification.progression),
    "Trickstar Figurine (12)": ItemData(0x1F280037, ItemClassification.progression),
    "Lunight Figurine (8)": ItemData(0x1F280038, ItemClassification.progression),
    "Inferhog Figurine (2)": ItemData(0x1F280039, ItemClassification.progression),
    "Meganite Figurine (2)": ItemData(0x1F28003A, ItemClassification.progression),
    "Princestar Figurine (2)": ItemData(0x1F28003B, ItemClassification.progression),
    "Vampicant Figurine (2)": ItemData(0x1F28003C, ItemClassification.progression),
    "Blazoar Plushie (2)": ItemData(0x1F28003D, ItemClassification.progression),
    "Giganite Statue (2)": ItemData(0x1F28003E, ItemClassification.progression),
    "Kingstar Plushie (2)": ItemData(0x1F28003F, ItemClassification.progression),
    "Dracunix Figurine (1)": ItemData(0x1F280040, ItemClassification.progression),
    "Bonfiox Plushie (8)": ItemData(0x1F280041, ItemClassification.progression),
    "Drilceros Action Figure (4)": ItemData(0x1F280042, ItemClassification.progression),
    "ToonZ Plushie (6)": ItemData(0x1F280043, ItemClassification.progression),
    "Small Cabinet": ItemData(0x1F280044, ItemClassification.progression),
    "Small Metal Rack": ItemData(0x1F280045, ItemClassification.useful),
    "Single Sided Shelf": ItemData(0x1F280046, ItemClassification.progression),
    "Double Sided Shelf": ItemData(0x1F280047, ItemClassification.useful),
    "Wide Shelf": ItemData(0x1F280048, ItemClassification.useful),
    "Play Table": ItemData(0x1F28004E, ItemClassification.progression),
    "Workbench": ItemData(0x1F28004F, ItemClassification.useful),
    "Trash Bin": ItemData(0x1F280050, ItemClassification.progression),
    "Checkout Counter": ItemData(0x1F280051, ItemClassification.progression),
    "System Gate #1": ItemData(0x1F280052, ItemClassification.progression),
    "System Gate #2": ItemData(0x1F280053, ItemClassification.progression),
    "Mafia Works": ItemData(0x1F280054, ItemClassification.progression),
    "Necromonsters": ItemData(0x1F280055, ItemClassification.progression),
    "Claim!": ItemData(0x1F280056, ItemClassification.progression),
    "Penny Sleeves": ItemData(0x1F280057, ItemClassification.progression),
    "Tower Deckbox": ItemData(0x1F280058, ItemClassification.progression),
    "Magnetic Holder": ItemData(0x1F280059, ItemClassification.progression),
    "Toploader": ItemData(0x1F28005A, ItemClassification.progression),
    "Card Preserver": ItemData(0x1F28005B, ItemClassification.progression),
    "Playmat Gray": ItemData(0x1F28005C, ItemClassification.progression),
    "Playmat Green": ItemData(0x1F28005D, ItemClassification.progression),
    "Playmat Purple": ItemData(0x1F28005E, ItemClassification.progression),
    "Playmat Yellow": ItemData(0x1F28005F, ItemClassification.progression),
    "Pocket Pages": ItemData(0x1F280060, ItemClassification.progression),
    "Card Holder": ItemData(0x1F280061, ItemClassification.progression),
    "Collectors Album": ItemData(0x1F2800B5, ItemClassification.progression),
    "Worker - Zachery": ItemData(0x1F2800B6, ItemClassification.progression),
    "Worker - Terence": ItemData(0x1F2800B7, ItemClassification.progression),
    "Worker - Dennis": ItemData(0x1F2800B8, ItemClassification.progression),
    "Worker - Clark": ItemData(0x1F2800B9, ItemClassification.progression),
    "Worker - Angus": ItemData(0x1F2800BA, ItemClassification.progression),
    "Worker - Benji": ItemData(0x1F2800BB, ItemClassification.progression),
    "Worker - Lauren": ItemData(0x1F2800BC, ItemClassification.progression),
    "Worker - Axel": ItemData(0x1F2800BD, ItemClassification.progression),
    "Playmat (Dracunix2)": ItemData(0x1F2800BE, ItemClassification.progression),
    "Playmat (GigatronX)": ItemData(0x1F2800BF, ItemClassification.progression),
    "Playmat (Katengu Black)": ItemData(0x1F2800C2, ItemClassification.progression),
    "Playmat (Katengu White)": ItemData(0x1F2800C3, ItemClassification.progression),
    "Manga 1": ItemData(0x1F2800C4, ItemClassification.progression),
    "Manga 2": ItemData(0x1F2800C5, ItemClassification.progression),
    "Manga 3": ItemData(0x1F2800C6, ItemClassification.progression),
    "Manga 4": ItemData(0x1F2800C7, ItemClassification.progression),
    "Manga 5": ItemData(0x1F2800C8, ItemClassification.progression),
    "Manga 6": ItemData(0x1F2800C9, ItemClassification.progression),
    "Manga 7": ItemData(0x1F2800CA, ItemClassification.progression),
    "Manga 8": ItemData(0x1F2800CB, ItemClassification.progression),
    "Manga 9": ItemData(0x1F2800CC, ItemClassification.progression),
    "Manga 10": ItemData(0x1F2800CD, ItemClassification.progression),
    "Manga 11": ItemData(0x1F2800CE, ItemClassification.progression),
    "Manga 12": ItemData(0x1F2800CF, ItemClassification.progression),
    "Warehouse Key": ItemData(0x1F2800F5, ItemClassification.progression),
    "Basic Card Pack (32)": ItemData(0x1F280001, ItemClassification.progression),
    "Basic Card Pack (64)": ItemData(0x1F2800D8, ItemClassification.progression),
    "Basic Card Box (4)": ItemData(0x1F2800D9, ItemClassification.progression),
    "Basic Card Box (8)": ItemData(0x1F2800DA, ItemClassification.progression),
    "Rare Card Pack (32)": ItemData(0x1F280002, ItemClassification.progression),
    "Rare Card Pack (64)": ItemData(0x1F2800DB, ItemClassification.progression),
    "Rare Card Box (4)": ItemData(0x1F2800DC, ItemClassification.progression),
    "Rare Card Box (8)": ItemData(0x1F2800DD, ItemClassification.progression),
    "Epic Card Pack (32)": ItemData(0x1F280003, ItemClassification.progression),
    "Epic Card Pack (64)": ItemData(0x1F2800DE, ItemClassification.progression),
    "Epic Card Box (4)": ItemData(0x1F2800DF, ItemClassification.progression),
    "Epic Card Box (8)": ItemData(0x1F2800E0, ItemClassification.progression),
    "Legendary Card Pack (32)": ItemData(0x1F280004, ItemClassification.progression),
    "Legendary Card Pack (64)": ItemData(0x1F2800E1, ItemClassification.progression),
    "Legendary Card Box (4)": ItemData(0x1F2800E2, ItemClassification.progression),
    "Legendary Card Box (8)": ItemData(0x1F2800E3, ItemClassification.progression),
    "Basic Destiny Pack (32)": ItemData(0x1F280009, ItemClassification.progression),
    "Basic Destiny Pack (64)": ItemData(0x1F2800E4, ItemClassification.progression),
    "Basic Destiny Box (4)": ItemData(0x1F2800E5, ItemClassification.progression),
    "Basic Destiny Box (8)": ItemData(0x1F2800E6, ItemClassification.progression),
    "Rare Destiny Pack (32)": ItemData(0x1F28000A, ItemClassification.progression),
    "Rare Destiny Pack (64)": ItemData(0x1F2800E7, ItemClassification.progression),
    "Rare Destiny Box (4)": ItemData(0x1F2800E8, ItemClassification.progression),
    "Rare Destiny Box (8)": ItemData(0x1F2800E9, ItemClassification.progression),
    "Epic Destiny Pack (32)": ItemData(0x1F28000B, ItemClassification.progression),
    "Epic Destiny Pack (64)": ItemData(0x1F2800EA, ItemClassification.progression),
    "Epic Destiny Box (4)": ItemData(0x1F2800EB, ItemClassification.progression),
    "Epic Destiny Box (8)": ItemData(0x1F2800EC, ItemClassification.progression),
    "Legendary Destiny Pack (32)": ItemData(0x1F28000C, ItemClassification.progression),
    "Legendary Destiny Pack (64)": ItemData(0x1F2800ED, ItemClassification.progression),
    "Legendary Destiny Box (4)": ItemData(0x1F2800EE, ItemClassification.progression),
    "Legendary Destiny Box (8)": ItemData(0x1F2800EF, ItemClassification.progression),
    "Cleanser (8)": ItemData(0x1F280011, ItemClassification.progression),
    "Cleanser (16)": ItemData(0x1F2800F0, ItemClassification.progression),
    "Deck Box Red (8)": ItemData(0x1F28001C, ItemClassification.progression),
    "Deck Box Red (16)": ItemData(0x1F2800F1, ItemClassification.progression),
    "Deck Box Green (8)": ItemData(0x1F28001D, ItemClassification.progression),
    "Deck Box Green (16)": ItemData(0x1F2800F2, ItemClassification.progression),
    "Deck Box Blue (8)": ItemData(0x1F28001E, ItemClassification.progression),
    "Deck Box Blue (16)": ItemData(0x1F2800F3, ItemClassification.progression),
    "Deck Box Yellow (8)": ItemData(0x1F28001F, ItemClassification.progression),
    "Deck Box Yellow (16)": ItemData(0x1F2800F4, ItemClassification.progression),
    "FormatStandard": ItemData(0x1F2800FC, ItemClassification.useful),
    "FormatPauper": ItemData(0x1F2800FD, ItemClassification.useful),
    "FormatFireCup": ItemData(0x1F2800FE, ItemClassification.useful),
    "FormatEarthCup": ItemData(0x1F2800FF, ItemClassification.useful),
    "FormatWaterCup": ItemData(0x1F280100, ItemClassification.useful),
    "FormatWindCup": ItemData(0x1F280101, ItemClassification.useful),
    "FormatFirstEditionVintage": ItemData(0x1F280102, ItemClassification.useful),
    "FormatSilverBorder": ItemData(0x1F280103, ItemClassification.useful),
    "FormatGoldBorder": ItemData(0x1F280104, ItemClassification.useful),
    "FormatExBorder": ItemData(0x1F280105, ItemClassification.useful),
    "FormatFullArtBorder": ItemData(0x1F280106, ItemClassification.useful),
    "FormatFoil": ItemData(0x1F280107, ItemClassification.useful)
}

progressive_dict: Dict[str, ItemData] = {
    "Progressive Card Table": ItemData(0x1F280049, ItemClassification.progression, 2),
    "Progressive Card Display": ItemData(0x1F28004A, ItemClassification.useful, 3),
    "Progressive Personal Shelf": ItemData(0x1F28004B, ItemClassification.useful, 3),
    "Progressive Auto Scent": ItemData(0x1F28004C, ItemClassification.useful, 3),
    "Progressive Warehouse Shelf": ItemData(0x1F28004D, ItemClassification.progression, 2),
    "Progressive Shop Expansion A": ItemData(0x1F2800C0, ItemClassification.progression, 30),
    "Progressive Shop Expansion B": ItemData(0x1F2800C1, ItemClassification.progression, 14),
}
# unused 0x1F2800D7
random_ghost_dict: Dict[str, ItemData] = {
    "1 Ghost Card": ItemData(0x1F280108, ItemClassification.progression, 0),
    "2 Ghost Cards": ItemData(0x1F280109, ItemClassification.progression, 0),
    "3 Ghost Cards": ItemData(0x1F28010A, ItemClassification.progression, 0),
    "4 Ghost Cards": ItemData(0x1F28010B, ItemClassification.progression, 0),
    "5 Ghost Cards": ItemData(0x1F28010C, ItemClassification.progression, 0),
}
ghost_dict: Dict[str, ItemData] = {
    "Ghost Blazoar (white)": ItemData(0x1F280062, ItemClassification.progression_skip_balancing),
    "Ghost Blazoar (Black)": ItemData(0x1F280063, ItemClassification.progression_skip_balancing),
    "Foil Ghost Blazoar (white)": ItemData(0x1F280064, ItemClassification.progression_skip_balancing),
    "Foil Ghost Blazoar (Black)": ItemData(0x1F280065, ItemClassification.progression_skip_balancing),
    "Ghost Kyuenbi (white)": ItemData(0x1F280066, ItemClassification.progression_skip_balancing),
    "Ghost Kyuenbi (Black)": ItemData(0x1F280067, ItemClassification.progression_skip_balancing),
    "Foil Ghost Kyuenbi (white)": ItemData(0x1F280068, ItemClassification.progression_skip_balancing),
    "Foil Ghost Kyuenbi (Black)": ItemData(0x1F280069, ItemClassification.progression_skip_balancing),
    "Ghost Giganite (white)": ItemData(0x1F28006A, ItemClassification.progression_skip_balancing),
    "Ghost Giganite (Black)": ItemData(0x1F28006B, ItemClassification.progression_skip_balancing),
    "Foil Ghost Giganite (white)": ItemData(0x1F28006C, ItemClassification.progression_skip_balancing),
    "Foil Ghost Giganite (Black)": ItemData(0x1F28006D, ItemClassification.progression_skip_balancing),
    "Ghost Mammotree (white)": ItemData(0x1F28006E, ItemClassification.progression_skip_balancing),
    "Ghost Mammotree (Black)": ItemData(0x1F28006F, ItemClassification.progression_skip_balancing),
    "Foil Ghost Mammotree (white)": ItemData(0x1F280070, ItemClassification.progression_skip_balancing),
    "Foil Ghost Mammotree (Black)": ItemData(0x1F280071, ItemClassification.progression_skip_balancing),
    "Ghost Kingstar (white)": ItemData(0x1F280072, ItemClassification.progression_skip_balancing),
    "Ghost Kingstar (Black)": ItemData(0x1F280073, ItemClassification.progression_skip_balancing),
    "Foil Ghost Kingstar (white)": ItemData(0x1F280074, ItemClassification.progression_skip_balancing),
    "Foil Ghost Kingstar (Black)": ItemData(0x1F280075, ItemClassification.progression_skip_balancing),
    "Ghost Fistronk (white)": ItemData(0x1F280076, ItemClassification.progression_skip_balancing),
    "Ghost Fistronk (Black)": ItemData(0x1F280077, ItemClassification.progression_skip_balancing),
    "Foil Ghost Fistronk (white)": ItemData(0x1F280078, ItemClassification.progression_skip_balancing),
    "Foil Ghost Fistronk (Black)": ItemData(0x1F280079, ItemClassification.progression_skip_balancing),
    "Ghost Royalama (white)": ItemData(0x1F28007A, ItemClassification.progression_skip_balancing),
    "Ghost Royalama (Black)": ItemData(0x1F28007B, ItemClassification.progression_skip_balancing),
    "Foil Ghost Royalama (white)": ItemData(0x1F28007C, ItemClassification.progression_skip_balancing),
    "Foil Ghost Royalama (Black)": ItemData(0x1F28007D, ItemClassification.progression_skip_balancing),
    "Ghost Dracunix (white)": ItemData(0x1F28007E, ItemClassification.progression_skip_balancing),
    "Ghost Dracunix (Black)": ItemData(0x1F28007F, ItemClassification.progression_skip_balancing),
    "Foil Ghost Dracunix (white)": ItemData(0x1F280080, ItemClassification.progression_skip_balancing),
    "Foil Ghost Dracunix (Black)": ItemData(0x1F280081, ItemClassification.progression_skip_balancing),
    "Ghost Magnoria (white)": ItemData(0x1F280082, ItemClassification.progression_skip_balancing),
    "Ghost Magnoria (Black)": ItemData(0x1F280083, ItemClassification.progression_skip_balancing),
    "Foil Ghost Magnoria (white)": ItemData(0x1F280084, ItemClassification.progression_skip_balancing),
    "Foil Ghost Magnoria (Black)": ItemData(0x1F280085, ItemClassification.progression_skip_balancing),
    "Ghost Hydroid (white)": ItemData(0x1F280086, ItemClassification.progression_skip_balancing),
    "Ghost Hydroid (Black)": ItemData(0x1F280087, ItemClassification.progression_skip_balancing),
    "Foil Ghost Hydroid (white)": ItemData(0x1F280088, ItemClassification.progression_skip_balancing),
    "Foil Ghost Hydroid (Black)": ItemData(0x1F280089, ItemClassification.progression_skip_balancing),
    "Ghost Drakon (white)": ItemData(0x1F28008A, ItemClassification.progression_skip_balancing),
    "Ghost Drakon (Black)": ItemData(0x1F28008B, ItemClassification.progression_skip_balancing),
    "Foil Ghost Drakon (white)": ItemData(0x1F28008C, ItemClassification.progression_skip_balancing),
    "Foil Ghost Drakon (Black)": ItemData(0x1F28008D, ItemClassification.progression_skip_balancing),
    "Ghost Bogon (white)": ItemData(0x1F28008E, ItemClassification.progression_skip_balancing),
    "Ghost Bogon (Black)": ItemData(0x1F28008F, ItemClassification.progression_skip_balancing),
    "Foil Ghost Bogon (white)": ItemData(0x1F280090, ItemClassification.progression_skip_balancing),
    "Foil Ghost Bogon (Black)": ItemData(0x1F280091, ItemClassification.progression_skip_balancing),
    "Ghost Hydron (white)": ItemData(0x1F280092, ItemClassification.progression_skip_balancing),
    "Ghost Hydron (Black)": ItemData(0x1F280093, ItemClassification.progression_skip_balancing),
    "Foil Ghost Hydron (white)": ItemData(0x1F280094, ItemClassification.progression_skip_balancing),
    "Foil Ghost Hydron (Black)": ItemData(0x1F280095, ItemClassification.progression_skip_balancing),
    "Ghost Raizon (white)": ItemData(0x1F280096, ItemClassification.progression_skip_balancing),
    "Ghost Raizon (Black)": ItemData(0x1F280097, ItemClassification.progression_skip_balancing),
    "Foil Ghost Raizon (white)": ItemData(0x1F280098, ItemClassification.progression_skip_balancing),
    "Foil Ghost Raizon (Black)": ItemData(0x1F280099, ItemClassification.progression_skip_balancing),
    "Ghost Lucadence (white)": ItemData(0x1F28009A, ItemClassification.progression_skip_balancing),
    "Ghost Lucadence (Black)": ItemData(0x1F28009B, ItemClassification.progression_skip_balancing),
    "Foil Ghost Lucadence (white)": ItemData(0x1F28009C, ItemClassification.progression_skip_balancing),
    "Foil Ghost Lucadence (Black)": ItemData(0x1F28009D, ItemClassification.progression_skip_balancing),
    "Ghost Jigajawr (white)": ItemData(0x1F28009E, ItemClassification.progression_skip_balancing),
    "Ghost Jigajawr (Black)": ItemData(0x1F28009F, ItemClassification.progression_skip_balancing),
    "Foil Ghost Jigajawr (white)": ItemData(0x1F2800A0, ItemClassification.progression_skip_balancing),
    "Foil Ghost Jigajawr (Black)": ItemData(0x1F2800A1, ItemClassification.progression_skip_balancing),
    "Ghost Jacktern (white)": ItemData(0x1F2800A2, ItemClassification.progression_skip_balancing),
    "Ghost Jacktern (Black)": ItemData(0x1F2800A3, ItemClassification.progression_skip_balancing),
    "Foil Ghost Jacktern (white)": ItemData(0x1F2800A4, ItemClassification.progression_skip_balancing),
    "Foil Ghost Jacktern (Black)": ItemData(0x1F2800A5, ItemClassification.progression_skip_balancing),
    "Ghost GigatronX (white)": ItemData(0x1F2800A6, ItemClassification.progression_skip_balancing),
    "Ghost GigatronX (Black)": ItemData(0x1F2800A7, ItemClassification.progression_skip_balancing),
    "Foil Ghost GigatronX (white)": ItemData(0x1F2800A8, ItemClassification.progression_skip_balancing),
    "Foil Ghost GigatronX (Black)": ItemData(0x1F2800A9, ItemClassification.progression_skip_balancing),
    "Ghost Clawcifear (white)": ItemData(0x1F2800AA, ItemClassification.progression_skip_balancing),
    "Ghost Clawcifear (Black)": ItemData(0x1F2800AB, ItemClassification.progression_skip_balancing),
    "Foil Ghost Clawcifear (white)": ItemData(0x1F2800AC, ItemClassification.progression_skip_balancing),
    "Foil Ghost Clawcifear (Black)": ItemData(0x1F2800AD, ItemClassification.progression_skip_balancing),
    "Ghost Katengu (white)": ItemData(0x1F2800AE, ItemClassification.progression_skip_balancing),
    "Ghost Katengu (Black)": ItemData(0x1F2800AF, ItemClassification.progression_skip_balancing),
    "Foil Ghost Katengu (white)": ItemData(0x1F2800B0, ItemClassification.progression_skip_balancing),
    "Foil Ghost Katengu (Black)": ItemData(0x1F2800B1, ItemClassification.progression_skip_balancing),
}

junk_dict: Dict[str, ItemData] = {
    "Small Xp": ItemData(0x1F2800B2, ItemClassification.filler),
    "Small Money": ItemData(0x1F2800B3, ItemClassification.filler),
    "Medium Xp": ItemData(0x1F2800D0, ItemClassification.filler),
    "Medium Money": ItemData(0x1F2800D1, ItemClassification.filler),
    "Large Xp": ItemData(0x1F2800D2, ItemClassification.filler),
    "Large Money": ItemData(0x1F2800D3, ItemClassification.filler),
    "Random Card": ItemData(0x1F2800D4, ItemClassification.filler),
    "Random New Card": ItemData(0x1F2800D5, ItemClassification.filler),
    "Progressive Customer Money": ItemData(0x1F2800F6, ItemClassification.filler),
    "Increase Card Luck": ItemData(0x1F2800F7, ItemClassification.filler),
}

trap_dict: Dict[str, ItemData] = {
    "Stink Trap": ItemData(0x1F2800B4, ItemClassification.trap),
    "Poltergeist Trap": ItemData(0x1F2800D6, ItemClassification.trap),
    "Credit Card Failure Trap": ItemData(0x1F2800F8, ItemClassification.trap),
    "Decrease Card Luck": ItemData(0x1F2800FB, ItemClassification.trap),
    "Market Change Trap": ItemData(0x1F2800F9, ItemClassification.trap),
    "Currency Trap": ItemData(0x1F2800FA, ItemClassification.trap),
}

junk_weights = {
    "Small Xp": 25,
    "Small Money": 25,
    "Medium Money": 15,
    "Medium Xp": 15,
    "Large Money": 10,
    "Large Xp": 10,
    "Random Card": 50,
    "Random New Card": 50,
    "Progressive Customer Money": 50,
    "Increase Card Luck": 0
}

full_item_dict: Dict[str, ItemData] = {**item_dict, **progressive_dict, **junk_dict, **trap_dict, **ghost_dict, **random_ghost_dict}
