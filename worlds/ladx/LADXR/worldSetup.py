from .patches import enemies, bingo
from .locations.items import *
from .entranceInfo import ENTRANCE_INFO
from . import logic


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
        self.goal = None
        self.bingo_goals = None
        self.multichest = RUPEES_20
        self.map = None  # Randomly generated map data
        self.inside_to_outside = True
        self.keep_two_way = True
        self.one_to_one = True

    def getEntrancePool(self, settings, connectorsOnly=False):
        entrances = []

        if connectorsOnly:
            if settings.entranceshuffle in {"split", "mixed", "wild", "chaos", "insane", "madness"}:
                entrances = [k for k, v in ENTRANCE_INFO.items() if v.type == "connector"]
            entrances += [f"{k}:inside" for k in entrances]
            return entrances

        if settings.dungeonshuffle and settings.entranceshuffle == "none":
            entrances = [k for k, v in ENTRANCE_INFO.items() if v.type == "dungeon"]
        if settings.entranceshuffle in {"simple", "split", "mixed", "wild", "chaos", "insane", "madness"}:
            types = {"single"}
            if settings.tradequest:
                types.add("trade")
            if settings.shufflejunk:
                types.update(["dummy", "trade"])
            if settings.shuffleannoying:
                types.add("insanity")
            if settings.shufflewater:
                types.add("water")
            if settings.randomstartlocation:
                types.add("start")
            if settings.dungeonshuffle:
                types.add("dungeon")
            if settings.entranceshuffle in {"mixed", "wild", "chaos", "insane", "madness"}:
                types.add("connector")
            entrances = [k for k, v in ENTRANCE_INFO.items() if v.type in types]

        entrances += [f"{k}:inside" for k in entrances]
        return entrances


    def _pair_equal_length_lists(self, outsides, insides, rnd):
        mapping = {}
        n = min(len(outsides), len(insides))
        for i in range(n):
            o = outsides[i]
            i_ = insides[i]
            mapping[o] = i_
            mapping[i_] = o
        return mapping

    def _two_way_shuffle(self, entrances, rnd):
        mapping = {}
        all_entrances = list(entrances)
        rnd.shuffle(all_entrances)
        n = len(all_entrances)
        i = 0
        while i + 1 < n:
            a, b = all_entrances[i], all_entrances[i + 1]
            mapping[a] = b
            mapping[b] = a
            i += 2
        if n % 2:
            last = all_entrances[-1]
            choice = rnd.choice(all_entrances[:-1])
            mapping[last] = choice
            mapping[choice] = last
        return mapping

    def _decoupled_shuffle(self, sources, targets, rnd):
        mapping = {}
        n = min(len(sources), len(targets))
        for i in range(n):
            mapping[sources[i]] = targets[i]
        return mapping

    def _randomizeEntrances(self, rnd, settings, entrancePool):
        entrances = list(entrancePool)
        outsides = [e for e in entrances if not e.endswith(":inside")]
        insides  = [e for e in entrances if e.endswith(":inside")]

        rnd.shuffle(outsides)
        rnd.shuffle(insides)

        mapping = {}

        mode = settings.entranceshuffle
        if mode == "simple":
            mapping.update(self._pair_equal_length_lists(outsides, insides, rnd))
        elif mode == "split":
            singles = [e for e in entrances if ENTRANCE_INFO[e.replace(":inside", "")].type == "single"]
            connectors = [e for e in entrances if ENTRANCE_INFO[e.replace(":inside", "")].type == "connector"]
            mapping.update(self._pair_equal_length_lists(
                [x for x in singles if not x.endswith(":inside")],
                [x for x in singles if x.endswith(":inside")],
                rnd
            ))
            mapping.update(self._pair_equal_length_lists(
                [x for x in connectors if not x.endswith(":inside")],
                [x for x in connectors if x.endswith(":inside")],
                rnd
            ))
        elif mode == "mixed":
            mapping.update(self._pair_equal_length_lists(outsides, insides, rnd))
        elif mode == "wild":
            mapping.update(self._two_way_shuffle(entrances, rnd))
        elif mode == "chaos":
            mapping.update(self._decoupled_shuffle(outsides, insides, rnd))
        elif mode == "insane":
            mapping.update(self._decoupled_shuffle(entrances, entrances, rnd))
        else:  # none / vanilla
            mapping = VANILLA_ENTRANCE_MAPPING.copy()

        self.entrance_mapping = mapping
        self._checkEntranceRules()

    def pickEntrances(self, settings, rnd):
        if settings.entranceshuffle == "none":
            if settings.randomstartlocation:
                start_location = start_locations[rnd.randrange(len(start_locations))]
                if start_location != "start_house":
                    # simple swap for starting house
                    self.entrance_mapping = dict(self.entrance_mapping)  # make mutable copy
                    self.entrance_mapping[start_location] = "start_house:inside"
                    self.entrance_mapping["start_house:inside"] = start_location
                    self.entrance_mapping["start_house"] = f"{start_location}:inside"
                    self.entrance_mapping[f"{start_location}:inside"] = "start_house"
            return

        entrancePool = self.getEntrancePool(settings)
        self._randomizeEntrances(rnd, settings, entrancePool)


    def _checkEntranceRules(self):
        mapping = self.entrance_mapping
        keys = list(mapping.keys())
        values = list(mapping.values())

        # inside-to-outside
        if self.inside_to_outside:
            for k, v in zip(keys, values):
                if k.endswith(":inside"):
                    assert not v.endswith(":inside"), f"inside-to-outside rule violated: {k}->{v}"
                else:
                    assert v.endswith(":inside"), f"inside-to-outside rule violated: {k}->{v}"

        # two-way check (bidirectional) without following cycles
        if self.keep_two_way:
            for k in keys:
                v = mapping[k]
                if v in mapping:
                    # only check if v is a key, don't touch mapping[v] if not
                    assert mapping.get(v) == k, f"keep-two-way rule violated: {k}->{v}"

        # one-to-one
        if self.one_to_one:
            found = set()
            for v in values:
                assert v not in found, f"one-on-one rule violated: {v}"
                found.add(v)


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

        if settings.goal == 'random':
            self.goal = rnd.randint(-1, 8)
        elif settings.goal == 'open':
            self.goal = -1
        elif settings.goal in {"seashells", "bingo", "bingo-full"}:
            self.goal = settings.goal
        elif "-" in settings.goal:
            a, b = settings.goal.split("-")
            if a == "open":
                a = -1
            self.goal = rnd.randint(int(a), int(b))
        else:
            self.goal = int(settings.goal)
        if self.goal in {"bingo", "bingo-full"}:
            self.bingo_goals = bingo.randomizeGoals(rnd, settings)

        self.multichest = rnd.choices(MULTI_CHEST_OPTIONS, MULTI_CHEST_WEIGHTS)[0]

        self.inside_to_outside = settings.entranceshuffle not in {"wild", "insane", "madness"}
        self.keep_two_way = settings.entranceshuffle not in {"chaos", "insane", "madness"}
        self.one_to_one = settings.entranceshuffle not in {"madness"}
        self.base_logic = logic.Logic(settings, world_setup=self)
        self.pickEntrances(settings, rnd)


    def loadFromRom(self, rom):
        import patches.overworld
        if patches.overworld.isNormalOverworld(rom):
            import patches.entrances
            self.entrance_mapping = patches.entrances.readEntrances(rom)
        else:
            self.entrance_mapping = {"d%d" % (n): "d%d" % (n) for n in range(9)}
        self.boss_mapping = patches.enemies.readBossMapping(rom)
        self.miniboss_mapping = patches.enemies.readMiniBossMapping(rom)
        self.goal = 8 # Better then nothing
