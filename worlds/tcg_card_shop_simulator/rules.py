from BaseClasses import LocationProgressType
from .items import *
from .locations import *


def has_card_pack(world, state, rarity):
    return state.has(f"{rarity} Pack (32)", world.player) or state.has(f"{rarity} Pack (64)", world.player) or state.has(f"{rarity} Box (4)", world.player) or state.has(f"{rarity} Box (8)", world.player)


def get_rules(world):
    rules = {
        "sell_locations": {
            "Sell Basic Card Pack":
                lambda state:
                has_card_pack(world, state, "Basic Card"),
            "Sell Basic Card Box":
                lambda state:
                state.has("Basic Card Box (4)", world.player) or state.has("Basic Card Box (8)", world.player),
            "Sell Rare Card Pack":
                lambda state:
                has_card_pack(world, state, "Rare Card"),
            "Sell Rare Card Box":
                lambda state:
                state.has("Rare Card Box (4)", world.player) or state.has("Rare Card Box (8)", world.player),
            "Sell Epic Card Pack":
                lambda state:
                has_card_pack(world, state, "Epic Card"),
            "Sell Epic Card Box":
                lambda state:
                state.has("Epic Card Box (4)", world.player) or state.has("Epic Card Box (8)", world.player),
            "Sell Legendary Card Pack":
                lambda state:
                has_card_pack(world, state, "Legendary Card"),
            "Sell Legendary Card Box":
                lambda state:
                state.has("Legendary Card Box (4)", world.player) or state.has("Legendary Card Box (8)", world.player),
            "Sell Fire Battle Deck":
                lambda state:
                state.has("Fire Battle Deck (18)", world.player),
            "Sell Earth Battle Deck":
                lambda state:
                state.has("Earth Battle Deck (18)", world.player),
            "Sell Water Battle Deck":
                lambda state:
                state.has("Water Battle Deck (18)", world.player),
            "Sell Wind Battle Deck":
                lambda state:
                state.has("Wind Battle Deck (18)", world.player),
            "Sell Basic Destiny Pack":
                lambda state:
                has_card_pack(world, state, "Basic Destiny"),
            "Sell Basic Destiny Box":
                lambda state:
                state.has("Basic Destiny Box (4)", world.player) or state.has("Basic Destiny Box (8)", world.player),
            "Sell Rare Destiny Pack":
                lambda state:
                has_card_pack(world, state, "Rare Destiny"),
            "Sell Rare Destiny Box":
                lambda state:
                state.has("Rare Destiny Box (4)", world.player) or state.has("Rare Destiny Box (8)", world.player),
            "Sell Epic Destiny Pack":
                lambda state:
                has_card_pack(world, state, "Epic Destiny"),
            "Sell Epic Destiny Box":
                lambda state:
                state.has("Epic Destiny Box (4)", world.player) or state.has("Epic Destiny Box (8)", world.player),
            "Sell Legendary Destiny Pack":
                lambda state:
                has_card_pack(world, state, "Legendary Destiny"),
            "Sell Legendary Destiny Box":
                lambda state:
                state.has("Legendary Destiny Box (4)", world.player) or state.has("Legendary Destiny Box (8)", world.player),
            "Sell Fire Destiny Deck":
                lambda state:
                state.has("Fire Destiny Deck (18)", world.player),
            "Sell Earth Destiny Deck":
                lambda state:
                state.has("Earth Destiny Deck (18)", world.player),
            "Sell Water Destiny Deck":
                lambda state:
                state.has("Water Destiny Deck (18)", world.player),
            "Sell Wind Destiny Deck":
                lambda state:
                state.has("Wind Destiny Deck (18)", world.player),
            "Sell Cleanser":
                lambda state:
                state.has("Cleanser (8)", world.player) or state.has("Cleanser (16)", world.player),
            "Sell Card Sleeves (Clear)":
                lambda state:
                state.has("Card Sleeves (Clear)", world.player),
            "Sell Card Sleeves (Tetramon)":
                lambda state:
                state.has("Card Sleeves (Tetramon)", world.player),
            "Sell D20 Dice Red":
                lambda state:
                state.has("D20 Dice Red (16)", world.player),
            "Sell D20 Dice Blue":
                lambda state:
                state.has("D20 Dice Blue (16)", world.player),
            "Sell D20 Dice Black":
                lambda state:
                state.has("D20 Dice Black (16)", world.player),
            "Sell D20 Dice White":
                lambda state:
                state.has("D20 Dice White (16)", world.player),
            "Sell Card Sleeves (Fire)":
                lambda state:
                state.has("Card Sleeves (Fire)", world.player),
            "Sell Card Sleeves (Earth)":
                lambda state:
                state.has("Card Sleeves (Earth)", world.player),
            "Sell Card Sleeves (Water)":
                lambda state:
                state.has("Card Sleeves (Water)", world.player),
            "Sell Card Sleeves (Wind)":
                lambda state:
                state.has("Card Sleeves (Wind)", world.player),
            "Sell Deck Box Red":
                lambda state:
                state.has("Deck Box Red (8)", world.player) or state.has("Deck Box Red (16)", world.player),
            "Sell Deck Box Green":
                lambda state:
                state.has("Deck Box Green (8)", world.player) or state.has("Deck Box Green (16)", world.player),
            "Sell Deck Box Blue":
                lambda state:
                state.has("Deck Box Blue (8)", world.player) or state.has("Deck Box Blue (16)", world.player),
            "Sell Deck Box Yellow":
                lambda state:
                state.has("Deck Box Yellow (8)", world.player) or state.has("Deck Box Yellow (16)", world.player),
            "Sell Collection Book":
                lambda state:
                state.has("Collection Book (4)", world.player),
            "Sell Premium Collection Book":
                lambda state:
                state.has("Premium Collection Book (4)", world.player),
            "Sell Playmat (Drilceros)":
                lambda state:
                state.has("Playmat (Drilceros)", world.player),
            "Sell Playmat (Clamigo)":
                lambda state:
                state.has("Playmat (Clamigo)", world.player),
            "Sell Playmat (Wispo)":
                lambda state:
                state.has("Playmat (Wispo)", world.player),
            "Sell Playmat (Lunight)":
                lambda state:
                state.has("Playmat (Lunight)", world.player),
            "Sell Playmat (Kyrone)":
                lambda state:
                state.has("Playmat (Kyrone)", world.player),
            "Sell Playmat (Duel)":
                lambda state:
                state.has("Playmat (Duel)", world.player),
            "Sell Playmat (Dracunix1)":
                lambda state:
                state.has("Playmat (Dracunix1)", world.player),
            "Sell Playmat (Dracunix2)":
                lambda state:
                state.has("Playmat (Dracunix2)", world.player),
            "Sell Playmat (The Four Dragons)":
                lambda state:
                state.has("Playmat (The Four Dragons)", world.player),
            "Sell Playmat (Drakon)":
                lambda state:
                state.has("Playmat (Drakon)", world.player),
            "Sell Playmat (GigatronX Evo)":
                lambda state:
                state.has("Playmat (GigatronX Evo)", world.player),
            "Sell Playmat (Fire)":
                lambda state:
                state.has("Playmat (Fire)", world.player),
            "Sell Playmat (Earth)":
                lambda state:
                state.has("Playmat (Earth)", world.player),
            "Sell Playmat (Water)":
                lambda state:
                state.has("Playmat (Water)", world.player),
            "Sell Playmat (Wind)":
                lambda state:
                state.has("Playmat (Wind)", world.player),
            "Sell Playmat (Tetramon)":
                lambda state:
                state.has("Playmat (Tetramon)", world.player),
            "Sell Manga 1":
                lambda state:
                state.has("Manga 1", world.player),
            "Sell Manga 2":
                lambda state:
                state.has("Manga 2", world.player),
            "Sell Manga 3":
                lambda state:
                state.has("Manga 3", world.player),
            "Sell Manga 4":
                lambda state:
                state.has("Manga 4", world.player),
            "Sell Manga 5":
                lambda state:
                state.has("Manga 5", world.player),
            "Sell Manga 6":
                lambda state:
                state.has("Manga 6", world.player),
            "Sell Manga 7":
                lambda state:
                state.has("Manga 7", world.player),
            "Sell Manga 8":
                lambda state:
                state.has("Manga 8", world.player),
            "Sell Manga 9":
                lambda state:
                state.has("Manga 9", world.player),
            "Sell Manga 10":
                lambda state:
                state.has("Manga 10", world.player),
            "Sell Manga 11":
                lambda state:
                state.has("Manga 11", world.player),
            "Sell Manga 12":
                lambda state:
                state.has("Manga 12", world.player),
            "Sell Pigni Plushie":
                lambda state:
                state.has("Pigni Plushie (12)", world.player),
            "Sell Nanomite Plushie":
                lambda state:
                state.has("Nanomite Plushie (16)", world.player),
            "Sell Minstar Plushie":
                lambda state:
                state.has("Minstar Plushie (24)", world.player),
            "Sell Nocti Plushie":
                lambda state:
                state.has("Nocti Plushie (6)", world.player),
            "Sell Burpig Figurine":
                lambda state:
                state.has("Burpig Figurine (12)", world.player),
            "Sell Decimite Figurine":
                lambda state:
                state.has("Decimite Figurine (8)", world.player),
            "Sell Trickstar Figurine":
                lambda state:
                state.has("Trickstar Figurine (12)", world.player),
            "Sell Lunight Figurine":
                lambda state:
                state.has("Lunight Figurine (8)", world.player),
            "Sell Inferhog Figurine":
                lambda state:
                state.has("Inferhog Figurine (2)", world.player),
            "Sell Meganite Figurine":
                lambda state:
                state.has("Meganite Figurine (2)", world.player),
            "Sell Princestar Figurine":
                lambda state:
                state.has("Princestar Figurine (2)", world.player),
            "Sell Vampicant Figurine":
                lambda state:
                state.has("Vampicant Figurine (2)", world.player),
            "Sell Blazoar Plushie":
                lambda state:
                state.has("Blazoar Plushie (2)", world.player),
            "Sell Giganite Statue":
                lambda state:
                state.has("Giganite Statue (2)", world.player),
            "Sell Kingstar Plushie":
                lambda state:
                state.has("Kingstar Plushie (2)", world.player),
            "Sell Dracunix Figurine":
                lambda state:
                state.has("Dracunix Figurine (1)", world.player),
            "Sell Bonfiox Plushie":
                lambda state:
                state.has("Bonfiox Plushie (8)", world.player),
            "Sell Drilceros Action Figure":
                lambda state:
                state.has("Drilceros Action Figure (4)", world.player),
            "Sell ToonZ Plushie":
                lambda state:
                state.has("ToonZ Plushie (6)", world.player),
            "Sell System Gate #1":
                lambda state:
                state.has("System Gate #1", world.player),
            "Sell System Gate #2":
                lambda state:
                state.has("System Gate #2", world.player),
            "Sell Mafia Works":
                lambda state:
                state.has("Mafia Works", world.player),
            "Sell Necromonsters":
                lambda state:
                state.has("Necromonsters", world.player),
            "Sell Claim!":
                lambda state:
                state.has("Claim!", world.player),
            "Sell Penny Sleeves":
                lambda state:
                state.has("Penny Sleeves", world.player),
            "Sell Tower Deckbox":
                lambda state:
                state.has("Tower Deckbox", world.player),
            "Sell Magnetic Holder":
                lambda state:
                state.has("Magnetic Holder", world.player),
            "Sell Toploader":
                lambda state:
                state.has("Toploader", world.player),
            "Sell Card Preserver":
                lambda state:
                state.has("Card Preserver", world.player),
            "Sell Playmat Gray":
                lambda state:
                state.has("Playmat Gray", world.player),
            "Sell Playmat Green":
                lambda state:
                state.has("Playmat Green", world.player),
            "Sell Playmat Purple":
                lambda state:
                state.has("Playmat Purple", world.player),
            "Sell Playmat Yellow":
                lambda state:
                state.has("Playmat Yellow", world.player),
            "Sell Pocket Pages":
                lambda state:
                state.has("Pocket Pages", world.player),
            "Sell Card Holder":
                lambda state:
                state.has("Card Holder", world.player),
            "Sell Collectors Album":
                lambda state:
                state.has("Collectors Album", world.player),
            "Sell Playmat (Dracunix2)":
                lambda state:
                state.has("Playmat (Dracunix2)", world.player),
            "Sell Playmat (GigatronX)":
                lambda state:
                state.has("Playmat (GigatronX)", world.player),
            "Sell Playmat (Katengu Black)":
                lambda state:
                state.has("Playmat (Katengu Black)", world.player),
            "Sell Playmat (Katengu White)":
                lambda state:
                state.has("Playmat (Katengu White)", world.player),
        },
        "locations": {
            "Shop B Expansion 1": lambda state:
                state.has("Progressive Shop Expansion B", world.player, 1) and state.has("Warehouse Key", world.player),

            "Shop B Expansion 2": lambda state:

                state.has("Progressive Shop Expansion B", world.player, 2) and state.has("Warehouse Key", world.player),

            "Shop B Expansion 3": lambda state:

                state.has("Progressive Shop Expansion B", world.player, 3) and state.has("Warehouse Key", world.player),

            "Shop B Expansion 4": lambda state:

                state.has("Progressive Shop Expansion B", world.player, 4) and state.has("Warehouse Key", world.player),

            "Shop B Expansion 5": lambda state:

                state.has("Progressive Shop Expansion B", world.player, 5) and state.has("Warehouse Key", world.player),

            "Shop B Expansion 6": lambda state:

                state.has("Progressive Shop Expansion B", world.player, 6) and state.has("Warehouse Key", world.player),

            "Shop B Expansion 7": lambda state:

                state.has("Progressive Shop Expansion B", world.player, 7) and state.has("Warehouse Key", world.player),

            "Shop B Expansion 8": lambda state:

                state.has("Progressive Shop Expansion B", world.player, 8) and state.has("Warehouse Key", world.player),

            "Shop B Expansion 9": lambda state:

                state.has("Progressive Shop Expansion B", world.player, 9) and state.has("Warehouse Key", world.player),

            "Shop B Expansion 10": lambda state:

                state.has("Progressive Shop Expansion B", world.player, 10) and state.has("Warehouse Key", world.player),

            "Shop B Expansion 11": lambda state:

                state.has("Progressive Shop Expansion B", world.player, 11) and state.has("Warehouse Key", world.player),

            "Shop B Expansion 12": lambda state:

                state.has("Progressive Shop Expansion B", world.player, 12) and state.has("Warehouse Key", world.player),

            "Shop B Expansion 13": lambda state:

                state.has("Progressive Shop Expansion B", world.player, 13) and state.has("Warehouse Key", world.player),

            "Shop B Expansion 14": lambda state:

                state.has("Progressive Shop Expansion B", world.player, 14) and state.has("Warehouse Key", world.player),
        },
        "entrances": {
            "Level 5":
                lambda state:
                 state.has("Single Sided Shelf", world.player) and state.has("Progressive Card Table", world.player),
            "Level 10":
                lambda state:
                 state.has("Worker - Zachery", world.player) and state.has("Progressive Warehouse Shelf", world.player) and state.has("Progressive Shop Expansion A", world.player, 2),
            "Level 15":
                lambda state:
                  (state.has("Cleanser (8)", world.player) or state.has("Cleanser (16)", world.player)),
            "Level 20":
                lambda state:
                 has_card_pack(world, state, "Basic Card") and state.has("Play Table", world.player) and state.has("Progressive Shop Expansion A", world.player, 4),
            "Level 25":
                lambda state:
                state.has("Small Cabinet", world.player) and state.has("Progressive Shop Expansion A", world.player, 6),
            "Level 30":
                lambda state:
                state.has("Checkout Counter", world.player) and state.has("Progressive Shop Expansion A", world.player, 10),
            "Level 35":
                lambda state:
                state.has("Progressive Shop Expansion A", world.player, 12),
            "Level 40":
                lambda state:
                has_card_pack(world, state, "Rare Card") and state.has("Progressive Shop Expansion A", world.player, 13),
            "Level 45":
                lambda state:
                has_card_pack(world, state, "Epic Card") and state.has("Progressive Shop Expansion A", world.player, 14),
            "Level 50":
                lambda state:
                has_card_pack(world, state, "Legendary Card") and state.has("Progressive Shop Expansion A", world.player, 15),
            "Level 55":
                lambda state:
                has_card_pack(world, state, "Basic Destiny") and state.has("Progressive Shop Expansion A", world.player, 16),
            "Level 60":
                lambda state:
                has_card_pack(world, state, "Rare Destiny") and state.has("Progressive Shop Expansion A", world.player, 17),
            "Level 65":
                lambda state:
                has_card_pack(world, state, "Epic Destiny") and state.has("Progressive Shop Expansion A", world.player, 18),
            "Level 70":
                lambda state:
                has_card_pack(world, state, "Legendary Destiny") and state.has("Progressive Shop Expansion A", world.player, 19),
            "Level 75":
                lambda state:
                state.has("Progressive Shop Expansion A", world.player, 20),
            "Level 80":
                lambda state:
                state.has("Progressive Shop Expansion B", world.player, 1),
            "Level 85":
                lambda state:
                state.has("Progressive Shop Expansion B", world.player, 2),
            "Level 90":
                lambda state:
                state.has("Progressive Shop Expansion B", world.player, 3),
            "Level 95":
                lambda state:
                state.has("Progressive Shop Expansion B", world.player, 4),
            "Level 100":
                lambda state:
                state.has("Progressive Shop Expansion B", world.player, 5),
            "Level 105":
                lambda state:
                state.has("Progressive Shop Expansion B", world.player, 6),
            "Level 110":
                lambda state:
                state.has("Progressive Shop Expansion B", world.player, 7),
            "Common Card Pack":
                lambda state:
                has_card_pack(world, state, "Basic Card"),
            "Rare Card Pack":
                lambda state:
                has_card_pack(world, state, "Rare Card"),
            "Epic Card Pack":
                lambda state:
                has_card_pack(world, state, "Epic Card"),
            "Legendary Card Pack":
                lambda state:
                has_card_pack(world, state, "Legendary Card"),
            "Destiny Common Card Pack":
                lambda state:
                has_card_pack(world, state, "Basic Destiny"),
            "Destiny Rare Card Pack":
                lambda state:
                has_card_pack(world, state, "Rare Destiny"),
            "Destiny Epic Card Pack":
                lambda state:
                has_card_pack(world, state, "Epic Destiny"),
            "Destiny Legendary Card Pack":
                lambda state:
                has_card_pack(world, state, "Legendary Destiny"),
            "Play Table":
                lambda state:
                state.has("Play Table", world.player, 1),

        }
    }
    return rules


def set_rules(world, excluded_locs, starting_locs, final_region, ghost_counts):



    # if world.options.goal.value == 2:
    #     print(f"Im a ghost Card Goal")
    #     finish_level = 35 + world.options.ghost_goal_amount.value # 72
    #     for i in range(finish_level, 116):
    #         print(f"Level {i}")
    #         world.get_location(f"Level {i}")

    rules_lookup = get_rules(world)

    for entrance_name, rule in rules_lookup["entrances"].items():
        try:
            match = re.search(r'Level (\d+)', entrance_name)
            if match and final_region < int(match.group(1)):
                continue
            world.get_entrance(entrance_name).access_rule = rule
        except KeyError as e:
            print(f"Key error, {e}")
            pass

    for location_name, rule in rules_lookup["locations"].items():
        try:
            if location_name in excluded_locs:
                continue
            world.get_location(location_name).access_rule = rule
        except KeyError as e:
            print(f"Key error, {e}")
            pass

    for location_name, rule in rules_lookup["sell_locations"].items():
        try:
            for n in range(1, world.options.sell_check_amount.value + 1):
                if f"{location_name} {n}" in excluded_locs or f"{location_name} {n}" in starting_locs:
                    continue

                world.get_location(f"{location_name} {n}").access_rule = rule
        except KeyError as e:
            print(f"Key error, {e}")
            pass

    for expansion in Expansion:
        for rarity in Rarity:
            for i in range(world.options.sell_card_check_count.value):
                name = f"Sell {expansion.name} {rarity.name} cards #{i + 1}"
                try:
                    loc = world.get_location(name)
                except KeyError:
                    continue
                world.get_location(name).access_rule = lambda state: state.has(
                    "Progressive Card Table", world.player, 1)

    for pA in range(2, 31):
        try:
            if f"Shop A Expansion {pA}" in excluded_locs:
                continue
            world.get_location(f"Shop A Expansion {pA}").access_rule = lambda state, _pA=pA: state.has("Progressive Shop Expansion A", world.player, _pA)
        except KeyError as e:
            print(f"Key error, {e}")
            pass

    # victory conditions
    if world.options.goal.value == 0:
        world.multiworld.completion_condition[world.player] = lambda state: state.has("Progressive Shop Expansion A", world.player, world.options.shop_expansion_goal.value)

    if world.options.goal.value == 1:
        world.multiworld.get_location(f"Level {world.options.level_goal.value}", world.player).place_locked_item(TCGSimulatorItem("Victory", ItemClassification.progression, None, world.player))
        world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory", world.player)

    if world.options.goal.value == 2:
        lambdas = {}
        for bagsize, amount in ghost_counts.items():
            plural = "s" if bagsize > 1 else ""
            item_name = f"{bagsize} Ghost Card{plural}"
            lambdas[bagsize] = (lambda state, item=item_name, count=amount: state.has(item, world.player, count))
        world.multiworld.completion_condition[world.player] = lambda state: all(check(state) for check in lambdas.values())