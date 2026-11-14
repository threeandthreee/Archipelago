from .locations.items import *
FILLER = 'FILLER'

DEFAULT_ITEM_POOL = {
    SWORD: 2,
    FEATHER: 1,
    HOOKSHOT: 1,
    BOW: 1,
    BOMB: 1,
    MAGIC_POWDER: 1,
    MAGIC_ROD: 1,
    OCARINA: 1,
    PEGASUS_BOOTS: 1,
    POWER_BRACELET: 2,
    SHIELD: 2,
    SHOVEL: 1,
    ROOSTER: 1,
    TOADSTOOL: 1,
    BOOMERANG: 1,

    TAIL_KEY: 1, SLIME_KEY: 1, ANGLER_KEY: 1, FACE_KEY: 1, BIRD_KEY: 1,
    GOLD_LEAF: 5,

    FLIPPERS: 1,
    BOWWOW: 1,
    SONG1: 1, SONG2: 1, SONG3: 1,

    BLUE_TUNIC: 1, RED_TUNIC: 1,
    MAX_ARROWS_UPGRADE: 1, MAX_BOMBS_UPGRADE: 1, MAX_POWDER_UPGRADE: 1,

    HEART_CONTAINER: 8,
    HEART_PIECE: 12,

    RUPEES_100: 3,
    RUPEES_20: 6,
    RUPEES_200: 3,
    RUPEES_50: 19,

    SEASHELL: 26,
    MEDICINE: 3,
    GEL: 4,
    MESSAGE: 1,

    COMPASS1: 1, COMPASS2: 1, COMPASS3: 1, COMPASS4: 1,
    COMPASS5: 1, COMPASS6: 1, COMPASS7: 1, COMPASS8: 1, COMPASS9: 1,
    KEY1: 3, KEY2: 5, KEY3: 9, KEY4: 5, KEY5: 3, KEY6: 3, KEY7: 3, KEY8: 7, KEY9: 3,
    MAP1: 1, MAP2: 1, MAP3: 1, MAP4: 1, MAP5: 1, MAP6: 1, MAP7: 1, MAP8: 1, MAP9: 1,
    NIGHTMARE_KEY1: 1, NIGHTMARE_KEY2: 1, NIGHTMARE_KEY3: 1, NIGHTMARE_KEY4: 1,
    NIGHTMARE_KEY5: 1, NIGHTMARE_KEY6: 1, NIGHTMARE_KEY7: 1, NIGHTMARE_KEY8: 1, NIGHTMARE_KEY9: 1,
    STONE_BEAK1: 1, STONE_BEAK2: 1, STONE_BEAK3: 1, STONE_BEAK4: 1,
    STONE_BEAK5: 1, STONE_BEAK6: 1, STONE_BEAK7: 1, STONE_BEAK8: 1, STONE_BEAK9: 1,
    
    INSTRUMENT1: 1, INSTRUMENT2: 1, INSTRUMENT3: 1, INSTRUMENT4: 1,
    INSTRUMENT5: 1, INSTRUMENT6: 1, INSTRUMENT7: 1, INSTRUMENT8: 1,

    TRADING_ITEM_YOSHI_DOLL: 1,
    TRADING_ITEM_RIBBON: 1,
    TRADING_ITEM_DOG_FOOD: 1,
    TRADING_ITEM_BANANAS: 1,
    TRADING_ITEM_STICK: 1,
    TRADING_ITEM_HONEYCOMB: 1,
    TRADING_ITEM_PINEAPPLE: 1,
    TRADING_ITEM_HIBISCUS: 1,
    TRADING_ITEM_LETTER: 1,
    TRADING_ITEM_BROOM: 1,
    TRADING_ITEM_FISHING_HOOK: 1,
    TRADING_ITEM_NECKLACE: 1,
    TRADING_ITEM_SCALE: 1,
    TRADING_ITEM_MAGNIFYING_GLASS: 1,

    "MEDICINE2": 1, "RAFT": 1, "ANGLER_KEYHOLE": 1, "CASTLE_BUTTON": 1
}


class ItemPool:    
    def __init__(self, world_setup, world):
        self.min_rupees = 1970
        self.__pool = {}
        self.__setup(world_setup, world)

    def add(self, item, count=1):
        self.__pool[item] = self.__pool.get(item, 0) + count

    def remove(self, item, count=1):
        if count < 0 or count > self.get(item):
            count = self.get(item)
        self.__pool[item] = self.__pool.get(item, 0) - count
        if self.__pool[item] == 0:
            del self.__pool[item]

    def replace(self, item, replacement, count=1):
        if count < 0 or count > self.get(item):
            count = self.get(item)
        self.add(replacement, count)
        self.remove(item, count)

    def get(self, item):
        return self.__pool.get(item, 0)

    def count(self):
        total = 0
        for count in self.__pool.values():
            total += count
        return total

    def removeRupees(self, count):
        for n in range(count):
            self.removeRupee()

    def removeRupee(self):
        for item in (RUPEES_20, RUPEES_50, RUPEES_100, RUPEES_200, RUPEES_500):
            if self.get(item) > 0:
                self.remove(item)
                break

    def balanceRupees(self):
        while self.countRupees() < self.min_rupees and self.get(RUPEES_20):
            self.replace(RUPEES_20, RUPEES_50)
        while self.countRupees() < self.min_rupees and self.get(RUPEES_50):
            self.replace(RUPEES_50, RUPEES_100)
        while self.countRupees() < self.min_rupees and self.get(RUPEES_100):
            self.replace(RUPEES_100, RUPEES_200)
        while self.countRupees() < self.min_rupees and self.get(RUPEES_200):
            self.replace(RUPEES_200, RUPEES_500)
        
        while self.countRupees() >= self.min_rupees + 300 and self.get(RUPEES_500):
            self.replace(RUPEES_500, RUPEES_200)
        while self.countRupees() >= self.min_rupees + 100 and self.get(RUPEES_200):
            self.replace(RUPEES_200, RUPEES_100)
        while self.countRupees() >= self.min_rupees + 50 and self.get(RUPEES_100):
            self.replace(RUPEES_100, RUPEES_50)
        while self.countRupees() >= self.min_rupees + 30 and self.get(RUPEES_50):
            self.replace(RUPEES_50, RUPEES_20)

        assert self.countRupees() >= self.min_rupees


    def countRupees(self):
        count = 0
        for value in [20, 50, 100, 200, 500]:
            count += self.get(f'RUPEES_{value}') * value
        return count

    def numberRupees(self):
        number = 0
        for value in [20, 50, 100, 200, 500]:
            number += self.get(f'RUPEES_{value}')
        return number

    def __setup(self, world_setup, world):
        settings = world.ladxr_settings
        default_item_pool = DEFAULT_ITEM_POOL

        for item, count in default_item_pool.items():
            self.add(item, count)

        # overworld settings change overall item count
        if settings.overworld == "dungeondive":
            self.min_rupees -= 400
            self.remove(MAX_ARROWS_UPGRADE)
            self.remove(MAX_BOMBS_UPGRADE)
            self.remove(MAX_POWDER_UPGRADE)
            self.remove(SEASHELL, 26)
            self.remove(TAIL_KEY)
            self.remove(SLIME_KEY)
            self.remove(ANGLER_KEY)
            self.remove(FACE_KEY)
            self.remove(BIRD_KEY)
            self.remove(GOLD_LEAF, 5)
            self.remove(SONG2)
            self.remove(SONG3)
            self.remove(HEART_PIECE, 12)
            self.add(HEART_CONTAINER, 3)
            self.removeRupees(16)
            self.remove(MESSAGE)
            self.remove(BOWWOW)
            self.remove(ROOSTER)
            self.remove("MEDICINE2")
            self.remove("RAFT")
            self.remove("ANGLER_KEYHOLE")
            self.remove("CASTLE_BUTTON")
            self.remove(TRADING_ITEM_YOSHI_DOLL)
            self.remove(TRADING_ITEM_RIBBON)
            self.remove(TRADING_ITEM_DOG_FOOD)
            self.remove(TRADING_ITEM_BANANAS)
            self.remove(TRADING_ITEM_STICK)
            self.remove(TRADING_ITEM_HONEYCOMB)
            self.remove(TRADING_ITEM_PINEAPPLE)
            self.remove(TRADING_ITEM_HIBISCUS)
            self.remove(TRADING_ITEM_LETTER)
            self.remove(TRADING_ITEM_BROOM)
            self.remove(TRADING_ITEM_FISHING_HOOK)
            self.remove(TRADING_ITEM_NECKLACE)
            self.remove(TRADING_ITEM_SCALE)
            self.remove(TRADING_ITEM_MAGNIFYING_GLASS)
        elif settings.overworld == "nodungeons":
            for n in range(9):
                self.remove("MAP%d" % (n + 1))
                self.remove("COMPASS%d" % (n + 1))
                self.remove("STONE_BEAK%d" % (n + 1))
                self.remove("KEY%d" % (n + 1), -1)
                self.remove("NIGHTMARE_KEY%d" % (n + 1))
            self.remove(BLUE_TUNIC)
            self.remove(RED_TUNIC)
            self.remove(MAX_ARROWS_UPGRADE)
            self.remove(MAX_BOMBS_UPGRADE)
            self.remove(MAX_POWDER_UPGRADE)
            self.remove(SEASHELL, 2)
            self.removeRupees(16)
            self.remove(HEART_PIECE, 12)
            self.add(HEART_CONTAINER, 4)
            self.remove(GEL, 4)
            self.remove(MESSAGE, 1)

        if not settings.tradequest:
            self.remove(TRADING_ITEM_YOSHI_DOLL)
            self.remove(TRADING_ITEM_RIBBON)
            self.remove(TRADING_ITEM_DOG_FOOD)
            self.remove(TRADING_ITEM_BANANAS)
            self.remove(TRADING_ITEM_STICK)
            self.remove(TRADING_ITEM_HONEYCOMB)
            self.remove(TRADING_ITEM_PINEAPPLE)
            self.remove(TRADING_ITEM_HIBISCUS)
            self.remove(TRADING_ITEM_LETTER)
            self.remove(TRADING_ITEM_BROOM)
            self.remove(TRADING_ITEM_FISHING_HOOK)
            self.remove(TRADING_ITEM_NECKLACE)
            self.remove(TRADING_ITEM_SCALE)
            self.remove(TRADING_ITEM_MAGNIFYING_GLASS)

        # goal adjustments
        goal = world_setup.goal
        if isinstance(goal, str) and goal.startswith('='):
            instruments_to_remove = [i for i in range(1, 9) if str(i) not in goal]
            for i in instruments_to_remove:
                self.remove(f"INSTRUMENT{i}")
        elif settings.goal == "seashells":
            self.remove(SEASHELL, 2)
            for n in range(8):
                self.remove("INSTRUMENT%d" % (n + 1))
            if "Strict Seashells" not in world.options.item_pool:
                self.add(SEASHELL, 8)

        # total number of items shouldnt change after this point
        target_item_count = self.count()

        # removals
        if not settings.rooster:
            self.remove(ROOSTER)
        num_rupees = self.numberRupees()
        if num_rupees > 15 and 'Greatly Reduce Rupees' in world.options.item_pool:
            self.removeRupees(num_rupees - 15)
        elif num_rupees > 25 and 'Reduce Rupees' in world.options.item_pool:
            self.removeRupees(num_rupees - 25)
        if 'Remove Heart Containers' in world.options.item_pool:
            self.remove(HEART_PIECE, -1)
            self.remove(HEART_CONTAINER, -1)
        elif 'Consolidate Hearts' in world.options.item_pool:
            self.add(HEART_CONTAINER, self.get(HEART_PIECE) // 4)
            self.remove(HEART_PIECE, -1)
        if 'Remove Tunics' in world.options.item_pool:
            self.remove(BLUE_TUNIC)
            self.remove(RED_TUNIC)
        if 'Remove Capacity Upgrades' in world.options.item_pool:
            self.remove(MAX_ARROWS_UPGRADE)
            self.remove(MAX_BOMBS_UPGRADE)
            self.remove(MAX_POWDER_UPGRADE)
        if 'Remove Extras' in world.options.item_pool:
            self.remove(MEDICINE, -1)
            self.remove(GEL, -1)
            self.remove(MESSAGE)
        if 'Remove Boomerang' in world.options.item_pool:
            self.remove(BOOMERANG)

        self.add(FILLER, target_item_count - self.count())
        self.balanceRupees()

        # additions
        items_to_add = []
        if "Extra Keys" in world.options.item_pool:
            for n in range(9):
                items_to_add.append("KEY%d" % (n + 1))
        if "Extra Nightmare Keys" in world.options.item_pool:
            for n in range(9):
                items_to_add.append("NIGHTMARE_KEY%d" % (n + 1))
        if "Extra Equipment" in world.options.item_pool:
            items_to_add.extend([
                BOMB,
                BOW,
                FEATHER,
                FLIPPERS,
                HOOKSHOT,
                MAGIC_ROD,
                OCARINA,
                PEGASUS_BOOTS,
                POWER_BRACELET,
            ])
        if "Add Bad Heart Containers" in world.options.item_pool:
            heart_containers = self.get('HEART_CONTAINER')
            heart_pieces = self.get('HEART_PIECE')
            to_add = 2 + heart_containers + heart_pieces // 4
            items_to_add.extend(['BAD_HEART_CONTAINER'] * to_add)

        # we could try to swap these in for filler now but its easier to just let AP do it
        world.priority_filler = items_to_add

    def toDict(self):
        return self.__pool.copy()
