from typing import TYPE_CHECKING, Callable

from ...locations import PokemonBWLocation
from BaseClasses import ItemClassification, CollectionState
from ...items import PokemonBWItem

if TYPE_CHECKING:
    from ... import PokemonBWWorld
    from BaseClasses import Region
    from ...data import SpeciesData, RulesDict


def create(world: "PokemonBWWorld", regions: dict[str, "Region"], rules: "RulesDict") -> dict[str, "SpeciesData"]:
    from ...data.locations.encounters.static import static, legendary, gift, trade, fossils
    from ...data.pokemon.species import by_id as species_by_id, by_name as species_by_name
    from ...data import TradeEncounterData, StaticEncounterData

    catchable_species_data: dict[str, "SpeciesData"] = {}

    def get_trade_rule(x: str) -> Callable[[CollectionState], bool]:
        return lambda state: state.has(x, world.player)

    def f(table: dict[str, StaticEncounterData | TradeEncounterData]):
        for name, data in table.items():
            if type(data) is TradeEncounterData or ((data.inclusion_rule is None) or data.inclusion_rule(world)):
                r: "Region" = regions[data.encounter_region]
                l: PokemonBWLocation = PokemonBWLocation(world.player, name, None, r)
                species_id: tuple[int, int] = data.species_black \
                    if world.options.version == "black" else data.species_white
                species_name: str = species_by_id[species_id]
                item: PokemonBWItem = PokemonBWItem(species_name, ItemClassification.progression, None, world.player)
                l.place_locked_item(item)
                if type(data) is StaticEncounterData:
                    if data.access_rule is not None:
                        l.access_rule = rules[data.access_rule]
                elif world.options.version == "black":
                    l.access_rule = get_trade_rule(species_by_id[(data.wanted_black, 0)])
                else:
                    l.access_rule = get_trade_rule(species_by_id[(data.wanted_white, 0)])
                r.locations.append(l)

                species_data: "SpeciesData" = species_by_name[species_name]
                catchable_species_data[species_name] = species_data

    f(static)
    f(legendary)
    f(gift)
    f(trade)
    f(fossils)

    return catchable_species_data
