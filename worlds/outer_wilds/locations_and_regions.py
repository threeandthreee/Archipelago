from io import BytesIO
import pickle
import pkgutil
import typing
from typing import Callable, Dict, List, NamedTuple, Optional, Set

from BaseClasses import CollectionState, Location, MultiWorld, Region
from worlds.generic.Rules import set_rule
from .options import OuterWildsGameOptions, Spawn
from .rule_eval import eval_rule
from .warp_platforms import warp_platform_to_logical_region, warp_platform_required_items

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


pickled_data = pkgutil.get_data(__name__, "shared_static_logic/static_logic.pickle")
locations_data = pickle.load(BytesIO(pickled_data))["LOCATIONS"]

pickled_data = pkgutil.get_data(__name__, "shared_static_logic/static_logic.pickle")
connections_data = pickle.load(BytesIO(pickled_data))["CONNECTIONS"]


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

    # add dynamic logic, i.e. connections based on player options
    menu = mw.get_region("Menu", p)
    if world.spawn == Spawn.option_vanilla:
        menu.add_exits(["Timber Hearth Village"])
    elif world.spawn == Spawn.option_hourglass_twins:
        menu.add_exits(["Hourglass Twins"])
    elif world.spawn == Spawn.option_timber_hearth:
        menu.add_exits(["Timber Hearth"])
    elif world.spawn == Spawn.option_brittle_hollow:
        menu.add_exits(["Brittle Hollow"])
    elif world.spawn == Spawn.option_giants_deep:
        menu.add_exits(["Giant's Deep"])

    if world.warps == 'vanilla':
        def has_codes(state): return state.has("Nomai Warp Codes", p)

        hgt = mw.get_region("Hourglass Twins", p)
        hgt.add_exits([
            "Sun Station",
            "Ash Twin Interior",
            "Timber Hearth",
            "Hanging City Ceiling",
            "Giant's Deep",
        ], {
            "Sun Station": lambda state: state.has_all(["Nomai Warp Codes", "Spacesuit"], p),
            "Ash Twin Interior": has_codes,
            "Timber Hearth": has_codes,
            "Hanging City Ceiling": has_codes,
            "Giant's Deep": has_codes,
        })

        mw.get_region("Sun Station", p).connect(
            hgt, "SS vanilla warp",
            lambda state: state.has_all(["Nomai Warp Codes", "Spacesuit"], p))
        mw.get_region("Ash Twin Interior", p).connect(hgt, "ATP vanilla warp", has_codes)
        mw.get_region("Timber Hearth", p).connect(hgt, "TH vanilla warp", has_codes)
        mw.get_region("Hanging City Ceiling", p).connect(hgt, "BHF vanilla warp", has_codes)
        mw.get_region("Giant's Deep", p).connect(hgt, "GD vanilla warp", has_codes)

        mw.get_region("White Hole Station", p).add_exits(["Brittle Hollow"], {"Brittle Hollow": has_codes})
    else:
        for (platform_1, platform_2) in world.warps:
            region_name_1 = warp_platform_to_logical_region[platform_1]
            region_name_2 = warp_platform_to_logical_region[platform_2]
            if region_name_1 == region_name_2:
                continue
            required_items = ["Nomai Warp Codes"]
            required_items.extend(warp_platform_required_items.get(platform_1, []))
            required_items.extend(warp_platform_required_items.get(platform_2, []))

            def rule(state: CollectionState) -> bool:
                nonlocal required_items
                return state.has_all(required_items, p)
            r1 = mw.get_region(region_name_1, p)
            r2 = mw.get_region(region_name_2, p)
            r1.connect(r2, "%s->%s warp" % (region_name_1, region_name_2), rule)
            r2.connect(r1, "%s->%s warp" % (region_name_2, region_name_1), rule)
