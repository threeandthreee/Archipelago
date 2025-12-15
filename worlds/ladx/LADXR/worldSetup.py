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


class WorldSetup:
    def __init__(self):
        self.entrance_mapping = {k: f"{k}:inside" for k in ENTRANCE_INFO.keys()}
        self.entrance_mapping.update({f"{k}:inside": k for k in ENTRANCE_INFO.keys()})
        self.boss_mapping = list(range(9))
        self.miniboss_mapping = {
            # Main minibosses
            0: "ROLLING_BONES", 1: "HINOX", 2: "DODONGO", 3: "CUE_BALL", 4: "GHOMA", 5: "SMASHER", 6: "GRIM_CREEPER", 7: "BLAINO",
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


class EntranceShuffler:
    settings: Settings
    inside_to_outside: bool
    keep_two_way: bool
    one_on_one: bool

    entrance_mapping: dict[str, str]
    all_entrances: set[str]
    entrance_pools: dict[str, set[str]] = { "global": set() }
    zones: list[dict] = []
    dead_ends: set[str] = set()

    def __init__(self, settings):
        self.settings = settings
        self.inside_to_outside = settings.entrancerules in {"normal", "chaos"}
        self.keep_two_way = settings.entrancerules in {"normal", "wild"}
        self.one_on_one = settings.entrancerules != "madness"

        self.entrance_mapping = {k: f"{k}:inside" for k in ENTRANCE_INFO.keys()}
        self.entrance_mapping.update({f"{k}:inside": k for k in ENTRANCE_INFO.keys()})
        self.all_entrances = {k for k in self.entrance_mapping.keys()}

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
            elif scope == "global":
                self.entrance_pools["global"].update(entrance_type_groups[type_group])
        if self.settings.randomstartlocation == "global":
            self.entrance_pools["global"].add("start_house")
            self.entrance_pools["global"].add("start_house:inside")
        
        # unmap entrances to be shuffled
        for pool in self.entrance_pools.values():
            for entrance in pool:
                del self.entrance_mapping[entrance]

        # create a partial logic for our initial disconnected state
        logic = self._create_logic(partial=True)

        # map out how entrances connect
        for k, v in logic.world.entrances.items():
            locations = set()
            entrances = set()
            self._recursive_find_contiguous(v.location, locations, entrances, logic)
            zone = next((z for z in self.zones if z["locations"] & locations), None)
            if zone:
                zone["locations"].update(locations)
                zone["paths"][k] = entrances
            else:
                self.zones.append({
                    "locations": locations,
                    "paths": {k: entrances}
                })

        if self.keep_two_way:
            for zone in self.zones:
                for entrance, destinations in zone["paths"].items():
                    if not destinations - {entrance}:
                        self.dead_ends.add(entrance)
            self.dead_ends.discard("start_house:inside")

    def shuffle_entrances(self, rnd, world_setup: WorldSetup):
        if self.settings.randomstartlocation == "limited":
            start_location = rnd.choice(start_locations)
            self.entrance_mapping["start_house"] = f"{start_location}:inside"
            self.entrance_mapping["start_house:inside"] = start_location
            self.entrance_mapping[start_location] = "start_house:inside"
            self.entrance_mapping[f"{start_location}:inside"] = "start_house"

        CAREFUL_FILL_ITEM_THRESHOLD = 10
        # intentionally ordered roughly by impact
        CAREFUL_FILL_ITEM_POOL = [POWER_BRACELET, SWORD, FLIPPERS, FEATHER, BOMB, PEGASUS_BOOTS, HOOKSHOT,
                                  SHOVEL, OCARINA, ROOSTER, MAGIC_POWDER, TOADSTOOL,
                                  TAIL_KEY, SLIME_KEY, ANGLER_KEY, FACE_KEY, BIRD_KEY, RUPEES_500]
        careful_fill_inventory = []
        
        # 0: careful - look at item spots and connection requirements to avoid a choked start
        # 1: priority - only make connections that lead to new areas
        # 2: remaining - make connection to any unreached area
        # 3: finish - make any connection available
        fill_stage = 0

        entrances_reached = set()
        self._recursive_traverse_entrances("start_house:inside", entrances_reached)
        while(len(self.entrance_mapping) < len(self.all_entrances)):
            mapped_entrances = set(self.entrance_mapping.keys())
            mapped_exits = set(self.entrance_mapping.values())
            entrances = sorted(entrances_reached - mapped_entrances)
            assert entrances
            rnd.shuffle(entrances)
            ex: str|None = None
            for en in entrances: # pick an entrance and exit to connect
                # narrow the pool of exits
                exits = next(v for v in self.entrance_pools.values() if en in v).copy()
                exits.discard(en)
                if self.one_on_one:
                    exits = exits - mapped_exits
                if self.inside_to_outside:
                    exits = {e for e in exits if e.endswith(":inside") != en.endswith(":inside")}
                if fill_stage < 2: # discard exits that dont lead to new areas
                    for zone in self.zones:
                        for entrance, destinations in zone["paths"].items():
                            if not destinations - entrances_reached:
                                exits.discard(entrance)
                elif fill_stage == 2: # only take exits we haven't reached
                    exits = exits - entrances_reached
                if not exits:
                    continue
                if fill_stage == 0: # careful fill
                    logic = self._create_logic(world_setup, partial=True)
                    # don't do dungeons during careful fill
                    exits = {e for e in exits if not (len(e) == 9 and e.startswith("d") and e.endswith(":inside"))}
                    for e in exits:
                        inventory = careful_fill_inventory.copy()
                        location = logic.world.entrances[e].location
                        zone = next(z for z in self.zones if e in z["paths"])
                        explorer = self._create_explorer(logic, inventory, [logic.start, location])
                        while explorer.getRequiredItemsForNextLocations() & set(CAREFUL_FILL_ITEM_POOL):
                            item_count = len([item for loc in explorer.getAccessableLocations() for item in loc.items])
                            next_item = next(x for x in CAREFUL_FILL_ITEM_POOL
                                             if x in explorer.getRequiredItemsForNextLocations())
                            # not enough item locations reached to support simulated inventory
                            if item_count <= len(inventory):
                                break
                            # if this exit gives us a path through the zone, accept it
                            if not ex and any(x for x in zone["paths"][e] 
                                              if logic.world.entrances[x].location in explorer.getAccessableLocations()):
                                ex = e
                            if ex and item_count >= CAREFUL_FILL_ITEM_THRESHOLD:
                                fill_stage = 1 # end careful fill
                                break
                            inventory.append(next_item)
                            explorer = self._create_explorer(logic, inventory, [logic.start, location])
                        if ex:
                            careful_fill_inventory = inventory
                            break
                else:
                    ex = rnd.choice(sorted(exits))
                if ex:
                    self._connect(en, ex)
                    self._recursive_traverse_entrances(ex, entrances_reached)
                    break
            if not ex: # no valid exits for any entrances, move to next fill stage
                fill_stage = fill_stage + 1
        return self.entrance_mapping

    def _create_logic(self, base_world_setup: WorldSetup|None = None, partial: bool = False) -> "logic.Logic":
        world_setup = WorldSetup()
        world_setup.entrance_mapping = self.entrance_mapping
        world_setup.is_partial = partial
        if base_world_setup:
            world_setup.boss_mapping = base_world_setup.boss_mapping
            world_setup.miniboss_mapping = base_world_setup.miniboss_mapping
        return logic.Logic(self.settings, world_setup=world_setup)

    def _create_explorer(self, logic: "logic.Logic", inventory: list[str], locations: dict[Location]) -> Explorer:
        explorer = Explorer()
        for item in inventory:
            explorer.addItem(item)
        for location in locations:
            explorer.visit(location)
        return explorer

    def _connect(self, en: str, ex: str) -> None:
        self.entrance_mapping[en] = ex
        if self.keep_two_way:
            self.entrance_mapping[ex] = en
        assert not self.one_on_one or len(self.entrance_mapping) == len(set(self.entrance_mapping.values())), \
            f"one-on-one rule violated: {en}->{ex}"
        assert not self.inside_to_outside or en.endswith(":inside") != ex.endswith(":inside"), \
            f"inside-to-outside rule violated: {en}->{ex}"
        assert en != ex, f"entrance mapped to itself: {en}->{ex}"

    def _recursive_find_contiguous(self, location:Location, seen_locations:set[Location], seen_entrances:set[str],
                                   logic: "logic.Logic") -> None:
        if not location or location in seen_locations:
            return
        seen_locations.add(location)
        entrances = {k for k, v in logic.world.entrances.items() if v.location == location}
        if entrances:
            seen_entrances.update(entrances)
        for connection in location.connections:
            self._recursive_find_contiguous(connection[0], seen_locations, seen_entrances, logic)

    def _recursive_traverse_entrances(self, entrance: str, seen_entrances: set[str]) -> None:
        if entrance in seen_entrances:
            return
        seen_entrances.add(entrance)
        mapped_exit = self.entrance_mapping.get(entrance, None)
        if mapped_exit:
            self._recursive_traverse_entrances(mapped_exit, seen_entrances)
        zone = next(z for z in self.zones if entrance in z["paths"])
        for destination in zone["paths"][entrance]:
            self._recursive_traverse_entrances(destination, seen_entrances)
