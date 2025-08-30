from typing import TYPE_CHECKING

from ...locations import PokemonBWLocation

if TYPE_CHECKING:
    from ... import PokemonBWWorld
    from BaseClasses import Region
    from ...data import RulesDict


def lookup(domain: int) -> dict[str, int]:
    from ...data.locations.ingame_items.special import tm_hm_ncps, gym_tms

    return {
        name: data.flag_id * 100 + domain + (
            int(name[:-2].split("#")[-1]) if "#" in name else 0
        )
        for name, data in tm_hm_ncps.items()
    } | {
        name: data.flag_id * 100 + domain + (
            int(name[:-2].split("#")[-1]) if "#" in name else 0
        )
        for name, data in gym_tms.items()
    }


def create(world: "PokemonBWWorld", regions: dict[str, "Region"], rules: "RulesDict") -> None:
    from ...data.locations.ingame_items.special import tm_hm_ncps, gym_tms

    for name, data in tm_hm_ncps.items():
        if data.inclusion_rule is None or data.inclusion_rule(world):
            r: "Region" = regions[data.region]
            l: PokemonBWLocation = PokemonBWLocation(world.player, name, world.location_name_to_id[name], r)
            l.progress_type = data.progress_type(world)
            if data.rule is not None:
                l.access_rule = rules[data.rule]
            r.locations.append(l)
    for name, data in gym_tms.items():
        if data.inclusion_rule is None or data.inclusion_rule(world):
            r: "Region" = regions[data.region]
            l: PokemonBWLocation = PokemonBWLocation(world.player, name, world.location_name_to_id[name], r)
            l.progress_type = data.progress_type(world)
            if data.rule is not None:
                l.access_rule = rules[data.rule]
            r.locations.append(l)
