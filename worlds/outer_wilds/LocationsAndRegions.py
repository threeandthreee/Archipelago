import pkgutil
import typing
from typing import Callable, Dict, List, NamedTuple, Optional, Set

from BaseClasses import Location, MultiWorld, Region
from worlds.generic.Rules import set_rule
from . import jsonc
from .Options import OuterWildsGameOptions
from .RuleEval import eval_rule

if typing.TYPE_CHECKING:
    from . import OuterWildsWorld


class OuterWildsLocation(Location):
    game = "Outer Wilds"


class OuterWildsLocationData(NamedTuple):
    region: str
    address: Optional[int] = None
    can_create: Callable[[MultiWorld, int], bool] = lambda multiworld, player: True
    creation_settings: Optional[List[str]] = None


class OuterWildsRegionData(NamedTuple):
    connecting_regions: List[str] = []


jsonc_locations_data = pkgutil.get_data(__name__, 'shared_static_logic/locations.jsonc')
locations_data = jsonc.loads(jsonc_locations_data.decode('utf-8'))

jsonc_connections_data = pkgutil.get_data(__name__, 'shared_static_logic/connections.jsonc')
connections_data = jsonc.loads(jsonc_connections_data.decode('utf-8'))


location_data_table: Dict[str, OuterWildsLocationData] = {}
for location_datum in locations_data:
    location_data_table[location_datum["name"]] = OuterWildsLocationData(
        address=location_datum["address"],
        region=(location_datum["region"] if "region" in location_datum else None),
        creation_settings=(location_datum["creation_settings"] if "creation_settings" in location_datum else None)
    )

all_non_event_locations_table = {name: data.address for name, data
                                 in location_data_table.items() if data.address is not None}

location_names: Set[str] = set(entry["name"] for entry in locations_data)
location_name_groups = {
    # For now, all of our location groups are auto-generated
    # We don't need an "Everywhere" group because AP makes that for us

    "Frequencies": {
        "Scan Any Distress Beacon",
        "Scan Any Quantum Fluctuation",
        "TH: Receive Hide & Seek Frequency",
    },
    "Signals": set(n for n in location_names if n.endswith(" Signal")),

    "Ember Twin": set(n for n in location_names if n.startswith("ET: ") or n.startswith("ET Ship Log: ")),
    "Ash Twin": set(n for n in location_names if n.startswith("AT: ") or n.startswith("AT Ship Log: ")),
    "Hourglass Twins": set(n for n in location_names if
                           n.startswith("ET: ") or n.startswith("ET Ship Log: ") or
                           n.startswith("AT: ") or n.startswith("AT Ship Log: ")),
    "Timber Hearth": set(n for n in location_names if n.startswith("TH: ") or n.startswith("TH Ship Log: ")),
    "Attlerock": set(n for n in location_names if n.startswith("AR: ") or n.startswith("AR Ship Log: ")),
    "Brittle Hollow": set(n for n in location_names if n.startswith("BH: ") or n.startswith("BH Ship Log: ")),
    "Giant's Deep": set(n for n in location_names if n.startswith("GD: ") or n.startswith("GD Ship Log: ")),
    "Dark Bramble": set(n for n in location_names if n.startswith("DB: ") or n.startswith("DB Ship Log: ")),
    "Quantum Moon": set(n for n in location_names if n.startswith("QM: ") or n.startswith("QM Ship Log: ")),

    "Ship Logs": set(n for n in location_names if "Ship Log: " in n),
}


def get_locations_to_create(options: OuterWildsGameOptions) -> Dict[str, OuterWildsLocationData]:
    # filter locations by settings (currently logsanity is the only setting relevant here)
    relevant_settings = set()
    if options.logsanity.value == 1:
        relevant_settings.add("logsanity")

    return {k: v for k, v in location_data_table.items()
            if v.creation_settings is None or relevant_settings.issuperset(v.creation_settings)}


region_data_table: Dict[str, OuterWildsRegionData] = {}


def create_regions(world: "OuterWildsWorld") -> None:
    mw = world.multiworld
    p = world.player
    options = world.options

    # start by ensuring every region is a key in region_data_table
    for ld in locations_data:
        region_name = ld["region"]
        if region_name not in region_data_table:
            region_data_table[region_name] = OuterWildsRegionData()

    for cd in connections_data:
        if cd["from"] not in region_data_table:
            region_data_table[cd["from"]] = OuterWildsRegionData()
        if cd["to"] not in region_data_table:
            region_data_table[cd["to"]] = OuterWildsRegionData()

    # actually create the Regions, initially all empty
    for region_name in region_data_table.keys():
        mw.regions.append(Region(region_name, p, mw))

    locations_to_create = get_locations_to_create(options)

    # add locations and connections to each region
    for region_name, region_data in region_data_table.items():
        region = mw.get_region(region_name, p)
        region.add_locations({
            location_name: location_data.address for location_name, location_data in locations_to_create.items()
            if location_data.region == region_name
        }, OuterWildsLocation)

        exit_connections = [cd for cd in connections_data if cd["from"] == region_name]
        exit_names = []
        rules = {}
        for exit_connection in exit_connections:
            exit_name = exit_connection["to"]
            assert exit_name not in exit_names
            exit_names.append(exit_name)
            rule = exit_connection["requires"]
            rules[exit_name] = None if len(rule) == 0 else lambda state, r=rule: eval_rule(state, p, r)
        region.add_exits(exit_names, rules)

    # add access rules to the created locations
    for ld in locations_data:
        if ld["name"] in locations_to_create and len(ld["requires"]) > 0:
            set_rule(mw.get_location(ld["name"], p),
                     lambda state, r=ld["requires"]: eval_rule(state, p, r))
