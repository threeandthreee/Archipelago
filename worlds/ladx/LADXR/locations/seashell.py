from .itemInfo import ItemInfo
from .droppedKey import DroppedKey
from .constants import *
from .items import *


class Seashell(DroppedKey):
    # Thanks to patches, a seashell is just a dropped key as far as the randomizer is concerned.

    def configure(self, options):
        if not options.seashells:
            self.OPTIONS = [SEASHELL]



class SeashellMansionBonus(ItemInfo):
    OPTIONS = [POWER_BRACELET, SHIELD, BOW, HOOKSHOT, MAGIC_ROD, PEGASUS_BOOTS, OCARINA,
        FEATHER, SHOVEL, MAGIC_POWDER, BOMB, SWORD, FLIPPERS, MEDICINE,
        TAIL_KEY, ANGLER_KEY, FACE_KEY, BIRD_KEY, GOLD_LEAF, SLIME_KEY, ROOSTER,
        RUPEES_50, RUPEES_20, RUPEES_100, RUPEES_200, RUPEES_500,
        SEASHELL, MESSAGE, BOOMERANG, HEART_PIECE, BOWWOW, ARROWS_10, SINGLE_ARROW,
        MAX_POWDER_UPGRADE, MAX_BOMBS_UPGRADE, MAX_ARROWS_UPGRADE, RED_TUNIC, BLUE_TUNIC,
        HEART_CONTAINER, BAD_HEART_CONTAINER, TOADSTOOL, SONG1, SONG2, SONG3,
        INSTRUMENT1, INSTRUMENT2, INSTRUMENT3, INSTRUMENT4, INSTRUMENT5, INSTRUMENT6, INSTRUMENT7, INSTRUMENT8,
        TRADING_ITEM_YOSHI_DOLL, TRADING_ITEM_RIBBON, TRADING_ITEM_DOG_FOOD, TRADING_ITEM_BANANAS, TRADING_ITEM_STICK,
        TRADING_ITEM_HONEYCOMB, TRADING_ITEM_PINEAPPLE, TRADING_ITEM_HIBISCUS, TRADING_ITEM_LETTER, TRADING_ITEM_BROOM,
        TRADING_ITEM_FISHING_HOOK, TRADING_ITEM_NECKLACE, TRADING_ITEM_SCALE, TRADING_ITEM_MAGNIFYING_GLASS
    ]

    def __init__(self, index):
        self.index = index
        super().__init__(0x2E9)

    def patch(self, rom, option, *, multiworld=None):
        rom.banks[0x3E][0x3E30 + self.index] = CHEST_ITEMS[option]

    def read(self, rom):
        value = rom.banks[0x3E][0x3E30 + self.index]
        for k, v in CHEST_ITEMS.items():
            if v == value:
                return k
        raise ValueError("Could not find bonus seashell contents in ROM (0x%02x)" % (value))

    def configure(self, options):
        if not options.seashells:
            self.OPTIONS = [SEASHELL]

    @property
    def nameId(self):
        return "0x%03X-%s" % (self.room, self.index)


class SeashellMansion(DroppedKey):
    pass
