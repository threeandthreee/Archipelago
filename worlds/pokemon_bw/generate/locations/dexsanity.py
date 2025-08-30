from typing import TYPE_CHECKING, Callable

from BaseClasses import LocationProgressType, CollectionState

from ...locations import PokemonBWLocation

if TYPE_CHECKING:
    from ... import PokemonBWWorld
    from BaseClasses import Region
    from ...data import SpeciesData


def lookup(domain: int) -> dict[str, int]:
    from ...data.locations.dexsanity import location_table

    return {name: data.dex_number + domain for name, data in location_table.items()}


def create(world: "PokemonBWWorld", regions: dict[str, "Region"], catchable_species_data: dict[str, "SpeciesData"]) -> None:
    from ...data.locations.dexsanity import location_table

    # These lambdas have to be created from functions, because else they would all use the same 'name' variable
    def get_standard_rule(x: str) -> Callable[[CollectionState], bool]:
        return lambda state: state.has(x.split(" - ")[-1], world.player)

    def get_special_rule(x: str) -> Callable[[CollectionState], bool]:
        return lambda state: location_table[x].special_rule(state, world)

    catchable_dex: set[str] = {data.dex_name for data in catchable_species_data.values()}
    count = min(world.options.dexsanity.value, len(catchable_dex))
    possible = [f"Pokédex - {species}" for species in catchable_dex]
    world.random.shuffle(possible)

    for _ in range(count):
        name = possible.pop()  # location name
        r: "Region" = regions["Pokédex"]
        l: PokemonBWLocation = PokemonBWLocation(world.player, name, world.location_name_to_id[name], r)
        l.progress_type = LocationProgressType.DEFAULT
        if location_table[name].special_rule is not None:
            l.access_rule = get_special_rule(name)
        else:
            l.access_rule = get_standard_rule(name)
        r.locations.append(l)
