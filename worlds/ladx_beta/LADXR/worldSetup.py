from .patches import enemies
from .locations.items import *
from .entranceInfo import ENTRANCE_INFO
from . import logic
from .utils import Error
from .explorer import Explorer
from .settings import Settings
from .logic.location import Location


MULTI_CHEST_OPTIONS = [MAGIC_POWDER, BOMB, MEDICINE, RUPEES_50, RUPEES_20, RUPEES_100, RUPEES_200, RUPEES_500, SEASHELL, GEL, ARROWS_10, SINGLE_ARROW]
MULTI_CHEST_WEIGHTS = [20,           20,   20,       50,        50,        20,         10,         5,          5,        20,  10,        10]

# List of all the possible locations where we can place our starting house
start_locations = [
    "phone_d8",
    "rooster_house",
    "writes_phone",
    "castle_phone",
    "photo_house",
    "start_house",
    "prairie_right_phone",
    "banana_seller",
    "prairie_low_phone",
    "animal_phone",
]

start_blacklist = [
    "mamu"
]


class WorldSetup:
    def __init__(self):
        self.entrance_mapping = {k: f"{k}:inside" for k in ENTRANCE_INFO.keys()}
        self.entrance_mapping.update({f"{k}:inside": k for k in ENTRANCE_INFO.keys()})
        self.boss_mapping = list(range(9))
        self.miniboss_mapping = {
            # Main minibosses
            '0': "ROLLING_BONES", '1': "HINOX", '2': "DODONGO", '3': "CUE_BALL", '4': "GHOMA", '5': "SMASHER", '6': "GRIM_CREEPER", '7': "BLAINO",
            # Color dungeon needs to be special, as always.
            "c1": "AVALAUNCH", "c2": "GIANT_BUZZ_BLOB",
            # Overworld
            "moblin_cave": "MOBLIN_KING",
            "armos_temple": "ARMOS_KNIGHT",
        }
        self.goal = "8"
        self.bingo_goals = None
        self.multichest = RUPEES_20
        self.map = None  # Randomly generated map data
        self.is_partial = False


    def pickEntrances(self, settings, rnd, world_setup):
        if settings.overworld in {"random", "dungeonchain", "alttp"}:
            return
        if settings.overworld == "dungeondive":
            self.entrance_mapping = {"d%d" % (n): "d%d:inside" % (n) for n in range(9)}
            self.entrance_mapping.update({"d%d:inside" % (n): "d%d" % (n) for n in range(9)})

        entrance_shuffler = EntranceShuffler(settings)
        self.entrance_mapping = entrance_shuffler.shuffle_entrances(rnd, world_setup)

    def randomize(self, settings, rnd):
        if settings.boss != "default":
            values = list(range(9))
            if settings.heartcontainers:
                # Color dungeon boss does not drop a heart container so we cannot shuffle him when we
                # have heart container shuffling
                values.remove(8)
            self.boss_mapping = []
            for n in range(8 if settings.heartcontainers else 9):
                value = rnd.choice(values)
                self.boss_mapping.append(value)
                if value in (3, 6) or settings.boss == "shuffle":
                    values.remove(value)
            if settings.heartcontainers:
                self.boss_mapping += [8]
        if settings.miniboss != "default":
            values = [name for name in self.miniboss_mapping.values()]
            for key in self.miniboss_mapping.keys():
                self.miniboss_mapping[key] = rnd.choice(values)
                if settings.miniboss == 'shuffle':
                    values.remove(self.miniboss_mapping[key])

        if settings.goal == 'open':
            self.goal = -1
        elif settings.goal == "seashells":
            self.goal = settings.goal
        elif settings.goal == "specific":
            instrument_count = max(1, int(settings.goalcount))
            instruments = [c for c in "12345678"]
            rnd.shuffle(instruments)
            self.goal = "=" + "".join(instruments[:instrument_count])
        else:
            self.goal = int(settings.goal)

        self.multichest = rnd.choices(MULTI_CHEST_OPTIONS, MULTI_CHEST_WEIGHTS)[0]
        self.pickEntrances(settings, rnd, self)

    def loadFromRom(self, rom):
        import patches.overworld
        if patches.overworld.isNormalOverworld(rom):
            import patches.entrances
            self.entrance_mapping = patches.entrances.readEntrances(rom)
        else:
            self.entrance_mapping = {"d%d" % (n): "d%d:inside" % (n) for n in range(9)}
            self.entrance_mapping.update({"d%d:inside" % (n): "d%d" % (n) for n in range(9)})
        self.boss_mapping = patches.enemies.readBossMapping(rom)
        self.miniboss_mapping = patches.enemies.readMiniBossMapping(rom)
        self.goal = 8 # Better then nothing


class Zone:
    """
    Represents a contiguous region of locations.
    """
    logic: "logic.Logic"
    locations: set[Location]
    paths: dict[str, str]

    def __init__(self, logic: "logic.Logic", all_shuffled_entrances: set[str], initial_entrance: str):
        self.logic = logic
        self.locations = set()
        entrances = set()
        self._recursive_find_contiguous(logic.world.entrances[initial_entrance].location, self.locations, entrances)
        self.paths = { initial_entrance: entrances & all_shuffled_entrances - {initial_entrance} }

    def merge(self, other) -> None:
        assert self.locations == other.locations and self.logic == other.logic
        self.paths.update(other.paths)

    def subtract(self, other) -> None:
        assert self.locations > other.locations and self.logic == other.logic
        self.locations -= other.locations

    def _recursive_find_contiguous(self, location:Location, seen_locations:set[Location], seen_entrances:set[str]) -> None:
        """
        updates seen_locations and seen_entrances based on everything reachable from the provided location
        """
        if not location or location in seen_locations:
            return
        seen_locations.add(location)
        entrances = {k for k, v in self.logic.world.entrances.items() if v.location == location}
        seen_entrances.update(entrances)
        for location, condition in location.connections:
            self._recursive_find_contiguous(location, seen_locations, seen_entrances)


class EntranceShuffler:
    settings: Settings
    inside_to_outside: bool
    keep_two_way: bool
    one_on_one: bool

    initial_entrance_mapping: dict[str, str]
    entrance_mapping: dict[str, str]
    all_entrances: set[str]
    all_shuffled_entrances: set[str]
    entrance_pools: dict[str, set[str]]

    verification_logic: "logic.Logic"
    logic: "logic.Logic"

    zones: set[Zone]
    dead_ends: set[str]

    def __init__(self, settings):
        self.settings = settings
        self.inside_to_outside = settings.entrancerules in {"normal", "chaos"}
        self.keep_two_way = settings.entrancerules in {"normal", "wild"}
        self.one_on_one = settings.entrancerules != "madness"

        self.initial_entrance_mapping = {k: f"{k}:inside" for k in ENTRANCE_INFO.keys()}
        self.initial_entrance_mapping.update({f"{k}:inside": k for k in ENTRANCE_INFO.keys()})
        self.all_entrances = {k for k in self.initial_entrance_mapping.keys()}
        self.all_shuffled_entrances = set()
        self.entrance_pools = { "global": set() }
        self.zones = set()
        self.dead_ends = set()
        self.entrance_pairs = set()

        # categorize entrances into types
        entrance_type_groups: dict[str, set[str]] = {}
        for k, v in ENTRANCE_INFO.items():
            entrance_type_groups.setdefault(v.type, set())    
            entrance_type_groups[v.type].add(k)
            entrance_type_groups[v.type].add(f"{k}:inside")
        if self.settings.tradequest:
            entrance_type_groups["single"].update(entrance_type_groups["trade"])
        else:
            entrance_type_groups["dummy"].update(entrance_type_groups["trade"])
        del entrance_type_groups["trade"]

        # break entrances into pools based on settings
        shuffles: dict[str, str] = {
            "dungeon": self.settings.dungeonshuffle,
            "connector": self.settings.shuffleconnectors,
            "single": self.settings.shufflebasic,
            "dummy": self.settings.shufflejunk,
            "insanity": self.settings.shuffleannoying,
            "water": self.settings.shufflewater,
        }
        for type_group, scope in shuffles.items():
            if scope == "limited":
                self.entrance_pools[type_group] = entrance_type_groups[type_group]
                self.all_shuffled_entrances.update(self.entrance_pools[type_group])
            elif scope == "global":
                self.entrance_pools["global"].update(entrance_type_groups[type_group])
        if self.settings.randomstartlocation == "global":
            self.entrance_pools["global"].add("start_house")
            self.entrance_pools["global"].add("start_house:inside")
        self.all_shuffled_entrances.update(self.entrance_pools["global"])

        # create a logic before messing with entrances for verification later
        world_setup = WorldSetup()
        self.verification_logic = logic.Logic(self.settings, world_setup=world_setup)

        # unmap entrances to be shuffled
        to_unmap = { en for pool in self.entrance_pools.values() for en in pool }
        self.initial_entrance_mapping = { k:v for k, v in self.initial_entrance_mapping.items() if k not in to_unmap }

        # create a partial logic for our disconnected state
        world_setup.entrance_mapping = self.initial_entrance_mapping
        world_setup.is_partial = True
        self.logic = logic.Logic(self.settings, world_setup=world_setup)

        # set up zones while categorizing some entrances
        possible_dead_ends = set()
        not_dead_ends = set()
        possible_entrance_pairs = {}
        for en in self.logic.world.entrances.keys():
            zone = Zone(self.logic, self.all_shuffled_entrances, en)
            self.zones.add(zone)
            if en in self.all_shuffled_entrances:
                if not zone.paths[en]:
                    possible_dead_ends.add(en)
                else:
                    not_dead_ends.update(zone.paths[en])
                    if len(zone.paths[en]) == 1:
                        possible_entrance_pairs[en] = next(iter(zone.paths[en]))
        self.dead_ends = possible_dead_ends - not_dead_ends
        if self.keep_two_way: # bird_cave:inside is a choke point, works best as a dead end
            self.dead_ends.add('bird_cave:inside')
        self.entrance_pairs = {a: b for a, b in possible_entrance_pairs.items() if possible_entrance_pairs.get(b) == a}

        # merge zones with the same location set
        zones_by_location = {}
        zones_to_remove = set()
        for zone in self.zones:
            key = frozenset(zone.locations)
            if key not in zones_by_location:
                zones_by_location[key] = zone
            else:
                zones_by_location[key].merge(zone)
                zones_to_remove.add(zone)
        self.zones -= zones_to_remove

        # subtract any subset zones from larger ones
        ordered_zones = sorted(self.zones, key=lambda zone: len(zone.locations), reverse=True)
        for i, a in enumerate(ordered_zones):
            for b in ordered_zones[i + 1:]:
                if a.locations > b.locations:
                    a.subtract(b)
        
    def shuffle_entrances(self, rnd, world_setup: WorldSetup):
        self.entrance_mapping = self.initial_entrance_mapping.copy()

        if self.settings.randomstartlocation == "limited":
            start_location = rnd.choice(start_locations)
            self.entrance_mapping["start_house"] = f"{start_location}:inside"
            self.entrance_mapping["start_house:inside"] = start_location
            self.entrance_mapping[start_location] = "start_house:inside"
            self.entrance_mapping[f"{start_location}:inside"] = "start_house"

        fill_stage = 0
        # 0: expand
        # 1: dont contract
        # 2: dead ends
        # 3: connect entrance pairs
        # 4: insert entrance pairs

        entrances_reached = set()
        self._recursive_traverse_entrances("start_house:inside", entrances_reached)
        seen_zones = {zone for zone in self.zones if entrances_reached & set(zone.paths)}
        while(len(self.entrance_mapping) < len(self.all_entrances)):
            mapped_entrances = set(self.entrance_mapping.keys())
            mapped_exits = set(self.entrance_mapping.values())
            entrances = sorted(entrances_reached - mapped_entrances)
            rnd.shuffle(entrances)
            ex: str|None = None
            # pick an entrance and exit to connect
            for en in entrances:
                exits = self._find_targets_for_entrance(en, self.one_on_one, self.inside_to_outside)

                # save entrance pairs for the end
                if fill_stage < 3:
                    exits -= set(self.entrance_pairs) 

                # if half of the unmapped exits in the pool are dead ends, force a dead end
                # or else we end up trying to map a dead end to a dead end later
                if len((exits - mapped_exits) & self.dead_ends) * 2 >= len(exits):
                    exits &= self.dead_ends  

                # fill stage 0, strictly expand map
                # fill stage 1, anything that doesnt reduce exits is fine
                if fill_stage <= 1:
                    for zone in self.zones:
                        for entrance, destinations in zone.paths.items():
                            if len(destinations - entrances_reached) < (2 - fill_stage):
                                exits.discard(entrance)
                    # avoid problem starts while we're here
                    if en == 'start_house:inside':
                        exits.difference_update(start_blacklist)

                # drop exits to seen zones if it doesnt empty the pool
                exits_to_seen_zones = {en for zone in seen_zones for en in set(zone.paths)}
                if exits - exits_to_seen_zones:
                    exits -= exits_to_seen_zones
                
                if not exits:
                    continue

                ex = rnd.choice(sorted(exits))
                if ex:
                    seen_zones.update({zone for zone in self.zones if entrances_reached & set(zone.paths)})
                    self._connect(en, ex)
                    self._recursive_traverse_entrances(ex, entrances_reached)
                    break
            if not ex: # no valid exits for any entrances, move to next fill stage
                fill_stage += 1
                print(f'----moving to fill_stage {fill_stage}----')
                if fill_stage == 4:
                    break

        # insert remaining entrance pairs
        entrances = sorted(self.entrance_pairs.keys())
        rnd.shuffle(entrances)
        for en in entrances:
            if en in self.entrance_mapping:
                continue
            targets = self._find_targets_for_entrance(en, False, self.inside_to_outside)
            targets &= set(self.entrance_mapping)
            if targets:
                target = rnd.choice(sorted(targets))
                self._insert(en, self.entrance_pairs[en], target)

        # if decoupled, leftover unmapped entrances can be inserted paired with itself
        if not self.keep_two_way:
            entrances = sorted(self.all_entrances - set(self.entrance_mapping) - set(self.entrance_mapping.values()))
            rnd.shuffle(entrances)
            for en in entrances:
                targets = self._find_targets_for_entrance(en, False, self.inside_to_outside)
                targets &= set(self.entrance_mapping)
                if targets:
                    target = rnd.choice(sorted(targets))
                    self._insert(en, en, target)

        print(f'unmapped entrances {self.all_entrances-set(self.entrance_mapping)}')
        print(f'unmapped exits {self.all_entrances-set(self.entrance_mapping.values())}')
        
        # verify valid mapping
        world_setup = WorldSetup()
        world_setup.entrance_mapping = self.entrance_mapping
        final_logic = logic.Logic(self.settings, world_setup=world_setup)
        assert len(final_logic.location_list) == len(self.verification_logic.location_list)
        assert len(final_logic.iteminfo_list) == len(self.verification_logic.iteminfo_list)

        return self.entrance_mapping

    def _connect(self, en: str, ex: str) -> None:
        print(f'{en} -> {ex}')
        self.entrance_mapping[en] = ex
        if self.keep_two_way:
            self.entrance_mapping[ex] = en

    def _insert(self, en: str, ex: str, target: str) -> None:
        target_ex = self.entrance_mapping[target]
        self._connect(target, ex)
        self._connect(en, target_ex)

    def _find_targets_for_entrance(self, en: str, one_on_one: bool, inside_to_outside: bool) -> set[str]:
        # exit must come from same pool as entrance
        targets = next(v for v in self.entrance_pools.values() if en in v).copy()
        targets.discard(en)             

        # enforce entrance rules
        if one_on_one:
            targets -= set(self.entrance_mapping.values())
        if inside_to_outside:
            targets = {t for t in targets if t.endswith(":inside") != en.endswith(":inside")}
        
        return targets

    def _recursive_traverse_entrances(self, entrance: str, seen_entrances: set[str]) -> None:
        if entrance in seen_entrances:
            return
        seen_entrances.add(entrance)
        mapped_exit = self.entrance_mapping.get(entrance, None)
        if mapped_exit:
            self._recursive_traverse_entrances(mapped_exit, seen_entrances)
        zone = next(z for z in self.zones if entrance in z.paths)
        for destination in zone.paths[entrance]:
            self._recursive_traverse_entrances(destination, seen_entrances)
