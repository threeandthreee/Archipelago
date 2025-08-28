from typing import TYPE_CHECKING

from BaseClasses import Item, Location, ItemClassification

if TYPE_CHECKING:
    from .. import PokemonBWWorld


def place_badges_pre_fill(world: "PokemonBWWorld") -> None:
    from ..data.locations.ingame_items import special

    match world.options.shuffle_badges.current_key:
        case "vanilla":
            badge_items: dict[str, Item] = world.to_be_locked_items["badges"]
            badge_locations: dict[str, Location] = {
                loc.name: loc
                for loc in world.get_locations()
                if loc.name in special.gym_badges
            }
            badge_locations["Striaton Gym - Badge reward"].place_locked_item(badge_items["Trio Badge"])
            badge_locations["Nacrene Gym - Badge reward"].place_locked_item(badge_items["Basic Badge"])
            badge_locations["Castelia Gym - Badge reward"].place_locked_item(badge_items["Insect Badge"])
            badge_locations["Nimbasa Gym - Badge reward"].place_locked_item(badge_items["Bolt Badge"])
            badge_locations["Driftveil Gym - Badge reward"].place_locked_item(badge_items["Quake Badge"])
            badge_locations["Mistralton Gym - Badge reward"].place_locked_item(badge_items["Jet Badge"])
            badge_locations["Icirrus Gym - Badge reward"].place_locked_item(badge_items["Freeze Badge"])
            badge_locations["Opelucid Gym - Badge reward"].place_locked_item(badge_items["Legend Badge"])
        case "shuffle":
            badge_items: dict[str, Item] = world.to_be_locked_items["badges"]
            badge_locations: list[Location] = [
                loc
                for loc in world.get_locations()
                if loc.name in special.gym_badges
            ]
            world.random.shuffle(badge_locations)
            for item in badge_items.values():
                location = badge_locations.pop()
                location.place_locked_item(item)
        case "any_badge":
            pass
        case "anything":
            pass
        case _:
            raise Exception(f"Bad shuffle_badges option value for player {world.player_name}")


def place_badges_fill(world: "PokemonBWWorld", progitempool: list[Item], fill_locations: list[Location]) -> None:
    from ..data.locations.ingame_items import special

    match world.options.shuffle_badges.current_key:
        case "vanilla":
            pass
        case "shuffle":
            pass
        case "any_badge":
            badge_items: list[Item] = [
                item
                for item in progitempool
                if "badge" in item.name.lower()
            ]
            badge_locations: list[Location] = [
                loc
                for loc in world.get_locations()
                if loc.name in special.gym_badges
            ]
            for _ in range(min(8, len(badge_items))):
                item = badge_items.pop()
                location = badge_locations.pop()
                location.place_locked_item(item)
                progitempool.remove(item)
                fill_locations.remove(location)
        case "anything":
            pass
        case _:
            raise Exception(f"Bad shuffle_badges option value for player {world.player_name}")


def place_tm_hm_pre_fill(world: "PokemonBWWorld") -> None:
    from ..data.locations.ingame_items.special import tm_hm_ncps, gym_tms
    from ..data.locations import all_tm_locations
    from ..data.items import tm_hm

    match world.options.shuffle_tm_hm.current_key:
        case "shuffle":
            tm_hm_items: list[Item] = world.to_be_locked_items["tm_hm"]
            # Sort HMs to front to prevent problems with HM rules
            to_place = 0
            for to_check in range(1, len(tm_hm_items)):
                if tm_hm_items[to_check].name in tm_hm.hm:
                    tm_hm_items[to_check], tm_hm_items[to_place] = tm_hm_items[to_place], tm_hm_items[to_check]
                    to_place += 1
            tm_hm_locations: list[Location] = [
                loc
                for loc in world.get_locations()
                if loc.name in all_tm_locations
            ]
            for item in tm_hm_items:
                for location in tm_hm_locations:
                    hm_rule = all_tm_locations[location.name].hm_rule
                    if hm_rule is None or hm_rule(item.name):
                        tm_hm_locations.remove(location)
                        location.place_locked_item(item)
                        break
        case "hm_with_badge":
            tms: list[Item] = world.to_be_locked_items["tms"]
            hms: list[Item] = world.to_be_locked_items["hms"]
            other_tm_locations: list[Location] = [
                loc
                for loc in world.get_locations()
                if loc.name in tm_hm_ncps
            ]
            gym_tm_locations: list[Location] = [
                loc
                for loc in world.get_locations()
                if loc.name in gym_tms
            ]
            # No hm rules needed because gym tm locations never have hm rules and other tm locations only get tms
            for item in hms:
                location = gym_tm_locations.pop()
                location.place_locked_item(item)
            for item in tms:
                location = other_tm_locations.pop()
                location.place_locked_item(item)
        case "any_tm_hm":
            pass
        case "anything":
            pass
        case _:
            raise Exception(f"Bad shuffle_tm_hm option value for player {world.player_name}")


def place_tm_hm_fill(world: "PokemonBWWorld",
                     progitempool: list[Item],
                     usefulitempool: list[Item],
                     filleritempool: list[Item],
                     fill_locations: list[Location]) -> None:
    from ..data.locations.ingame_items.special import tm_hm_ncps, gym_tms
    from ..data.locations import all_tm_locations

    match world.options.shuffle_tm_hm.current_key:
        case "shuffle":
            pass
        case "hm_with_badge":
            pass
        case "any_tm_hm":
            tm_hm_items: dict[Item, list[Item]] = {
                item: pool
                for pool in (progitempool, usefulitempool, filleritempool)
                for item in pool
                if (item.name.lower().startswith("tm") or item.name.lower().startswith("hm")) and item.name[2].isdigit()
            }
            tm_hm_locations: list[Location] = [
                loc
                for loc in fill_locations
                if loc.name in all_tm_locations and loc.player == world.player
            ]
            for location in tm_hm_locations:
                hm_rule = all_tm_locations[location.name].hm_rule
                for item in tm_hm_items:
                    if hm_rule is None or hm_rule(item.name):
                        tm_hm_items.pop(item).remove(item)  # This won't be changed. Don't try to argue with me.
                        location.place_locked_item(item)
                        fill_locations.remove(location)
                        break
        case "anything":
            pass
        case _:
            raise Exception(f"Bad shuffle_tm_hm option value for player {world.player_name}")
