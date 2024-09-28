"""
Pulls data from JSON files in worlds/pokemon_frlg/data/ into classes.
This also includes marrying automatically extracted data with manually
defined data (like location names or usable Pokémon species), some cleanup
and sorting, and Warp methods.
"""
import orjson
import pkgutil
from pkg_resources import resource_listdir, resource_isdir
from dataclasses import dataclass
from enum import IntEnum
from typing import Dict, List, NamedTuple, Optional, Set, FrozenSet, Any, Union, Tuple
from BaseClasses import ItemClassification

BASE_OFFSET = 6420000
FAMESANITY_OFFSET = 10000
NUM_REAL_SPECIES = 386


class Warp:
    """
    Represents warp events in the game like doorways or warp pads
    """
    is_one_way: bool
    source_map: str
    source_ids: List[str]
    dest_map: str
    dest_ids: List[str]
    name: Optional[str]
    parent_region_id: Optional[str]

    def __init__(self, encoded_string: Optional[str] = None,
                 name: Optional[str] = None,
                 parent_region_id: Optional[str] = None) -> None:
        if encoded_string is not None:
            decoded_warp = Warp.decode(encoded_string)
            self.is_one_way = decoded_warp.is_one_way
            self.source_map = decoded_warp.source_map
            self.source_ids = decoded_warp.source_ids
            self.dest_map = decoded_warp.dest_map
            self.dest_ids = decoded_warp.dest_ids
        self.name = name
        self.parent_region_id = parent_region_id

    def connects_to(self, other: "Warp") -> bool:
        """
        Returns true if this warp sends the player to `other`
        """
        return self.dest_map == other.source_map and set(self.dest_ids) <= set(other.source_ids)

    @staticmethod
    def decode(encoded_string: str) -> "Warp":
        """
        Create a Warp object from an encoded string
        """
        warp = Warp()
        warp.is_one_way = encoded_string.endswith("!")
        if warp.is_one_way:
            encoded_string = encoded_string[:-1]

        warp_source, warp_dest = encoded_string.split("/")
        warp_source_map, warp_source_indices = warp_source.split(":")
        warp_dest_map, warp_dest_indices = warp_dest.split(":")

        warp.source_map = warp_source_map
        warp.dest_map = warp_dest_map

        warp.source_ids = [int(index) for index in warp_source_indices.split(",")]
        warp.dest_ids = [int(index) for index in warp_dest_indices.split(",")]

        return warp


class ItemData(NamedTuple):
    name: str
    item_id: int
    classification: ItemClassification
    tags: FrozenSet[str]


class LocationData(NamedTuple):
    id: str
    name: str
    parent_region_id: str
    default_item: int
    address: Dict[str, Union[int, List[int]]]
    flag: int
    tags: FrozenSet[str]


@dataclass
class EncounterSpeciesData:
    species_id: int
    min_level: int
    max_level: int


class EncounterTableData(NamedTuple):
    slots: Dict[str, List[EncounterSpeciesData]]
    address: Dict[str, int]


@dataclass
class MapData:
    name: str
    header_address: Dict[str, int]
    land_encounters: Optional[EncounterTableData]
    water_encounters: Optional[EncounterTableData]
    fishing_encounters: Optional[EncounterTableData]
    kanto: bool


class EventData(NamedTuple):
    id: str
    name: Union[str, List[str]]
    item: Union[str, List[str]]
    parent_region_id: str
    tags: FrozenSet[str]


class RegionData:
    id: str
    name: str
    parent_map: Optional[MapData]
    encounter_region: str
    has_land: bool
    has_water: bool
    has_fishing: bool
    kanto: bool
    exits: Dict[str, str]
    warps: List[str]
    locations: List[str]
    events: List[str]

    def __init__(self, region_id: str, name: str, parent_map: Optional[MapData], encounter_region: str,
                 has_land: bool, has_water: bool, has_fishing: bool, kanto: bool):
        self.id = region_id
        self.name = name
        self.parent_map = parent_map
        self.encounter_region = encounter_region
        self.has_land = has_land
        self.has_water = has_water
        self.has_fishing = has_fishing
        self.kanto = kanto
        self.exits = []
        self.warps = []
        self.locations = []
        self.events = []


class BaseStats(NamedTuple):
    hp: int
    attack: int
    defense: int
    speed: int
    special_attack: int
    special_defense: int


class LearnsetMove(NamedTuple):
    level: int
    move_id: int


class EvolutionMethodEnum(IntEnum):
    LEVEL = 0
    LEVEL_ATK_LT_DEF = 1
    LEVEL_ATK_EQ_DEF = 2
    LEVEL_ATK_GT_DEF = 3
    LEVEL_SILCOON = 4
    LEVEL_CASCOON = 5
    LEVEL_NINJASK = 6
    LEVEL_SHEDINJA = 7
    ITEM = 8
    FRIENDSHIP = 9
    FRIENDSHIP_DAY = 10
    FRIENDSHIP_NIGHT = 11
    TRADE = 12
    TRADE_ITEM = 13
    BEAUTY = 14


EVOLUTION_METHOD_TYPE: Dict[str, EvolutionMethodEnum] = {
    "LEVEL": EvolutionMethodEnum.LEVEL,
    "LEVEL_ATK_LT_DEF": EvolutionMethodEnum.LEVEL_ATK_LT_DEF,
    "LEVEL_ATK_EQ_DEF": EvolutionMethodEnum.LEVEL_ATK_EQ_DEF,
    "LEVEL_ATK_GT_DEF": EvolutionMethodEnum.LEVEL_ATK_GT_DEF,
    "LEVEL_SILCOON": EvolutionMethodEnum.LEVEL_SILCOON,
    "LEVEL_CASCOON": EvolutionMethodEnum.LEVEL_CASCOON,
    "LEVEL_NINJASK": EvolutionMethodEnum.LEVEL_NINJASK,
    "LEVEL_SHEDINJA": EvolutionMethodEnum.LEVEL_SHEDINJA,
    "ITEM": EvolutionMethodEnum.ITEM,
    "FRIENDSHIP": EvolutionMethodEnum.FRIENDSHIP,
    "FRIENDSHIP_DAY": EvolutionMethodEnum.FRIENDSHIP_DAY,
    "FRIENDSHIP_NIGHT": EvolutionMethodEnum.FRIENDSHIP_NIGHT,
    "TRADE": EvolutionMethodEnum.TRADE,
    "TRADE_ITEM": EvolutionMethodEnum.TRADE_ITEM,
    "BEAUTY": EvolutionMethodEnum.BEAUTY
}


class EvolutionData(NamedTuple):
    param: int
    species_id: int
    method: EvolutionMethodEnum


@dataclass
class SpeciesData:
    species_id_name: str
    name: str
    species_id: int
    national_dex_number: int
    base_stats: BaseStats
    types: Tuple[int, int]
    abilities: Tuple[int, int]
    evolutions: List[EvolutionData]
    pre_evolution: Optional[int]
    catch_rate: int
    friendship: int
    learnset: List[LearnsetMove]
    tm_hm_compatibility: int
    learnset_address: Dict[str, int]
    address: Dict[str, int]


@dataclass
class StarterData:
    species_id: int
    player_address: Dict[str, int]
    rival_address: Dict[str, int]


@dataclass
class MiscPokemonData:
    species_id: Dict[str, int]
    level: [str, int]
    address: Dict[str, int]
    level_address: Dict[str, int]


class TrainerPokemonDataTypeEnum(IntEnum):
    NO_ITEM_DEFAULT_MOVES = 0
    NO_ITEM_CUSTOM_MOVES = 1
    ITEM_DEFAULT_MOVES = 2
    ITEM_CUSTOM_MOVES = 3


POKEMON_DATA_TYPE: Dict[str, TrainerPokemonDataTypeEnum] = {
    "NO_ITEM_DEFAULT_MOVES": TrainerPokemonDataTypeEnum.NO_ITEM_DEFAULT_MOVES,
    "NO_ITEM_CUSTOM_MOVES": TrainerPokemonDataTypeEnum.NO_ITEM_CUSTOM_MOVES,
    "ITEM_DEFAULT_MOVES": TrainerPokemonDataTypeEnum.ITEM_DEFAULT_MOVES,
    "ITEM_CUSTOM_MOVES": TrainerPokemonDataTypeEnum.ITEM_CUSTOM_MOVES
}


@dataclass
class TrainerPokemonData:
    species_id: int
    level: int
    moves: Optional[Tuple[int, int, int, int]]
    locked: bool


@dataclass
class TrainerPartyData:
    pokemon: List[TrainerPokemonData]
    pokemon_data_type: TrainerPokemonDataTypeEnum
    address: Dict[str, int]


@dataclass
class TrainerData:
    party: TrainerPartyData
    address: Dict[str, int]


class PokemonFRLGData:
    constants: Dict[str, int]
    ram_addresses: Dict[str, Dict[str, int]]
    rom_addresses: Dict[str, Dict[str, int]]
    regions: Dict[str, RegionData]
    locations: Dict[str, LocationData]
    events: Dict[str, EventData]
    items: Dict[int, ItemData]
    maps: Dict[str, MapData]
    warps: Dict[str, Warp]
    warp_map: Dict[str, Optional[str]]
    species: Dict[int, SpeciesData]
    starters: Dict[str, StarterData]
    legendary_pokemon: Dict[str, MiscPokemonData]
    misc_pokemon: Dict[str, MiscPokemonData]
    trainers: Dict[str, TrainerData]
    tmhm_moves: List[int]
    abilities: Dict[str, int]
    moves: Dict[str, int]

    def __init__(self) -> None:
        self.constants = {}
        self.ram_addresses = {}
        self.rom_addresses = {}
        self.regions = {}
        self.locations = {}
        self.events = {}
        self.items = {}
        self.maps = {}
        self.warps = {}
        self.warp_map = {}
        self.species = {}
        self.starters = {}
        self.legendary_pokemon = {}
        self.misc_pokemon = {}
        self.trainers = {}
        self.tmhm_moves = []
        self.abilities = {}
        self.moves = {}


# Excludes extras like copies of Unown and special species values like SPECIES_EGG
ALL_SPECIES: List[Tuple[str, str, int]] = [
    ("SPECIES_BULBASAUR", "Bulbasaur", 1),
    ("SPECIES_IVYSAUR", "Ivysaur", 2),
    ("SPECIES_VENUSAUR", "Venusaur", 3),
    ("SPECIES_CHARMANDER", "Charmander", 4),
    ("SPECIES_CHARMELEON", "Charmeleon", 5),
    ("SPECIES_CHARIZARD", "Charizard", 6),
    ("SPECIES_SQUIRTLE", "Squirtle", 7),
    ("SPECIES_WARTORTLE", "Wartortle", 8),
    ("SPECIES_BLASTOISE", "Blastoise", 9),
    ("SPECIES_CATERPIE", "Caterpie", 10),
    ("SPECIES_METAPOD", "Metapod", 11),
    ("SPECIES_BUTTERFREE", "Butterfree", 12),
    ("SPECIES_WEEDLE", "Weedle", 13),
    ("SPECIES_KAKUNA", "Kakuna", 14),
    ("SPECIES_BEEDRILL", "Beedrill", 15),
    ("SPECIES_PIDGEY", "Pidgey", 16),
    ("SPECIES_PIDGEOTTO", "Pidgeotto", 17),
    ("SPECIES_PIDGEOT", "Pidgeot", 18),
    ("SPECIES_RATTATA", "Rattata", 19),
    ("SPECIES_RATICATE", "Raticate", 20),
    ("SPECIES_SPEAROW", "Spearow", 21),
    ("SPECIES_FEAROW", "Fearow", 22),
    ("SPECIES_EKANS", "Ekans", 23),
    ("SPECIES_ARBOK", "Arbok", 24),
    ("SPECIES_PIKACHU", "Pikachu", 25),
    ("SPECIES_RAICHU", "Raichu", 26),
    ("SPECIES_SANDSHREW", "Sandshrew", 27),
    ("SPECIES_SANDSLASH", "Sandslash", 28),
    ("SPECIES_NIDORAN_F", "Nidoran F", 29),
    ("SPECIES_NIDORINA", "Nidorina", 30),
    ("SPECIES_NIDOQUEEN", "Nidoqueen", 31),
    ("SPECIES_NIDORAN_M", "Nidoran M", 32),
    ("SPECIES_NIDORINO", "Nidorino", 33),
    ("SPECIES_NIDOKING", "Nidoking", 34),
    ("SPECIES_CLEFAIRY", "Clefairy", 35),
    ("SPECIES_CLEFABLE", "Clefable", 36),
    ("SPECIES_VULPIX", "Vulpix", 37),
    ("SPECIES_NINETALES", "Ninetales", 38),
    ("SPECIES_JIGGLYPUFF", "Jigglypuff", 39),
    ("SPECIES_WIGGLYTUFF", "Wigglytuff", 40),
    ("SPECIES_ZUBAT", "Zubat", 41),
    ("SPECIES_GOLBAT", "Golbat", 42),
    ("SPECIES_ODDISH", "Oddish", 43),
    ("SPECIES_GLOOM", "Gloom", 44),
    ("SPECIES_VILEPLUME", "Vileplume", 45),
    ("SPECIES_PARAS", "Paras", 46),
    ("SPECIES_PARASECT", "Parasect", 47),
    ("SPECIES_VENONAT", "Venonat", 48),
    ("SPECIES_VENOMOTH", "Venomoth", 49),
    ("SPECIES_DIGLETT", "Diglett", 50),
    ("SPECIES_DUGTRIO", "Dugtrio", 51),
    ("SPECIES_MEOWTH", "Meowth", 52),
    ("SPECIES_PERSIAN", "Persian", 53),
    ("SPECIES_PSYDUCK", "Psyduck", 54),
    ("SPECIES_GOLDUCK", "Golduck", 55),
    ("SPECIES_MANKEY", "Mankey", 56),
    ("SPECIES_PRIMEAPE", "Primeape", 57),
    ("SPECIES_GROWLITHE", "Growlithe", 58),
    ("SPECIES_ARCANINE", "Arcanine", 59),
    ("SPECIES_POLIWAG", "Poliwag", 60),
    ("SPECIES_POLIWHIRL", "Poliwhirl", 61),
    ("SPECIES_POLIWRATH", "Poliwrath", 62),
    ("SPECIES_ABRA", "Abra", 63),
    ("SPECIES_KADABRA", "Kadabra", 64),
    ("SPECIES_ALAKAZAM", "Alakazam", 65),
    ("SPECIES_MACHOP", "Machop", 66),
    ("SPECIES_MACHOKE", "Machoke", 67),
    ("SPECIES_MACHAMP", "Machamp", 68),
    ("SPECIES_BELLSPROUT", "Bellsprout", 69),
    ("SPECIES_WEEPINBELL", "Weepinbell", 70),
    ("SPECIES_VICTREEBEL", "Victreebel", 71),
    ("SPECIES_TENTACOOL", "Tentacool", 72),
    ("SPECIES_TENTACRUEL", "Tentacruel", 73),
    ("SPECIES_GEODUDE", "Geodude", 74),
    ("SPECIES_GRAVELER", "Graveler", 75),
    ("SPECIES_GOLEM", "Golem", 76),
    ("SPECIES_PONYTA", "Ponyta", 77),
    ("SPECIES_RAPIDASH", "Rapidash", 78),
    ("SPECIES_SLOWPOKE", "Slowpoke", 79),
    ("SPECIES_SLOWBRO", "Slowbro", 80),
    ("SPECIES_MAGNEMITE", "Magnemite", 81),
    ("SPECIES_MAGNETON", "Magneton", 82),
    ("SPECIES_FARFETCHD", "Farfetch'd", 83),
    ("SPECIES_DODUO", "Doduo", 84),
    ("SPECIES_DODRIO", "Dodrio", 85),
    ("SPECIES_SEEL", "Seel", 86),
    ("SPECIES_DEWGONG", "Dewgong", 87),
    ("SPECIES_GRIMER", "Grimer", 88),
    ("SPECIES_MUK", "Muk", 89),
    ("SPECIES_SHELLDER", "Shellder", 90),
    ("SPECIES_CLOYSTER", "Cloyster", 91),
    ("SPECIES_GASTLY", "Gastly", 92),
    ("SPECIES_HAUNTER", "Haunter", 93),
    ("SPECIES_GENGAR", "Gengar", 94),
    ("SPECIES_ONIX", "Onix", 95),
    ("SPECIES_DROWZEE", "Drowzee", 96),
    ("SPECIES_HYPNO", "Hypno", 97),
    ("SPECIES_KRABBY", "Krabby", 98),
    ("SPECIES_KINGLER", "Kingler", 99),
    ("SPECIES_VOLTORB", "Voltorb", 100),
    ("SPECIES_ELECTRODE", "Electrode", 101),
    ("SPECIES_EXEGGCUTE", "Exeggcute", 102),
    ("SPECIES_EXEGGUTOR", "Exeggutor", 103),
    ("SPECIES_CUBONE", "Cubone", 104),
    ("SPECIES_MAROWAK", "Marowak", 105),
    ("SPECIES_HITMONLEE", "Hitmonlee", 106),
    ("SPECIES_HITMONCHAN", "Hitmonchan", 107),
    ("SPECIES_LICKITUNG", "Lickitung", 108),
    ("SPECIES_KOFFING", "Koffing", 109),
    ("SPECIES_WEEZING", "Weezing", 110),
    ("SPECIES_RHYHORN", "Rhyhorn", 111),
    ("SPECIES_RHYDON", "Rhydon", 112),
    ("SPECIES_CHANSEY", "Chansey", 113),
    ("SPECIES_TANGELA", "Tangela", 114),
    ("SPECIES_KANGASKHAN", "Kangaskhan", 115),
    ("SPECIES_HORSEA", "Horsea", 116),
    ("SPECIES_SEADRA", "Seadra", 117),
    ("SPECIES_GOLDEEN", "Goldeen", 118),
    ("SPECIES_SEAKING", "Seaking", 119),
    ("SPECIES_STARYU", "Staryu", 120),
    ("SPECIES_STARMIE", "Starmie", 121),
    ("SPECIES_MR_MIME", "Mr. Mime", 122),
    ("SPECIES_SCYTHER", "Scyther", 123),
    ("SPECIES_JYNX", "Jynx", 124),
    ("SPECIES_ELECTABUZZ", "Electabuzz", 125),
    ("SPECIES_MAGMAR", "Magmar", 126),
    ("SPECIES_PINSIR", "Pinsir", 127),
    ("SPECIES_TAUROS", "Tauros", 128),
    ("SPECIES_MAGIKARP", "Magikarp", 129),
    ("SPECIES_GYARADOS", "Gyarados", 130),
    ("SPECIES_LAPRAS", "Lapras", 131),
    ("SPECIES_DITTO", "Ditto", 132),
    ("SPECIES_EEVEE", "Eevee", 133),
    ("SPECIES_VAPOREON", "Vaporeon", 134),
    ("SPECIES_JOLTEON", "Jolteon", 135),
    ("SPECIES_FLAREON", "Flareon", 136),
    ("SPECIES_PORYGON", "Porygon", 137),
    ("SPECIES_OMANYTE", "Omanyte", 138),
    ("SPECIES_OMASTAR", "Omastar", 139),
    ("SPECIES_KABUTO", "Kabuto", 140),
    ("SPECIES_KABUTOPS", "Kabutops", 141),
    ("SPECIES_AERODACTYL", "Aerodactyl", 142),
    ("SPECIES_SNORLAX", "Snorlax", 143),
    ("SPECIES_ARTICUNO", "Articuno", 144),
    ("SPECIES_ZAPDOS", "Zapdos", 145),
    ("SPECIES_MOLTRES", "Moltres", 146),
    ("SPECIES_DRATINI", "Dratini", 147),
    ("SPECIES_DRAGONAIR", "Dragonair", 148),
    ("SPECIES_DRAGONITE", "Dragonite", 149),
    ("SPECIES_MEWTWO", "Mewtwo", 150),
    ("SPECIES_MEW", "Mew", 151),
    ("SPECIES_CHIKORITA", "Chikorita", 152),
    ("SPECIES_BAYLEEF", "Bayleef", 153),
    ("SPECIES_MEGANIUM", "Meganium", 154),
    ("SPECIES_CYNDAQUIL", "Cyndaquil", 155),
    ("SPECIES_QUILAVA", "Quilava", 156),
    ("SPECIES_TYPHLOSION", "Typhlosion", 157),
    ("SPECIES_TOTODILE", "Totodile", 158),
    ("SPECIES_CROCONAW", "Croconaw", 159),
    ("SPECIES_FERALIGATR", "Feraligatr", 160),
    ("SPECIES_SENTRET", "Sentret", 161),
    ("SPECIES_FURRET", "Furret", 162),
    ("SPECIES_HOOTHOOT", "Hoothoot", 163),
    ("SPECIES_NOCTOWL", "Noctowl", 164),
    ("SPECIES_LEDYBA", "Ledyba", 165),
    ("SPECIES_LEDIAN", "Ledian", 166),
    ("SPECIES_SPINARAK", "Spinarak", 167),
    ("SPECIES_ARIADOS", "Ariados", 168),
    ("SPECIES_CROBAT", "Crobat", 169),
    ("SPECIES_CHINCHOU", "Chinchou", 170),
    ("SPECIES_LANTURN", "Lanturn", 171),
    ("SPECIES_PICHU", "Pichu", 172),
    ("SPECIES_CLEFFA", "Cleffa", 173),
    ("SPECIES_IGGLYBUFF", "Igglybuff", 174),
    ("SPECIES_TOGEPI", "Togepi", 175),
    ("SPECIES_TOGETIC", "Togetic", 176),
    ("SPECIES_NATU", "Natu", 177),
    ("SPECIES_XATU", "Xatu", 178),
    ("SPECIES_MAREEP", "Mareep", 179),
    ("SPECIES_FLAAFFY", "Flaaffy", 180),
    ("SPECIES_AMPHAROS", "Ampharos", 181),
    ("SPECIES_BELLOSSOM", "Bellossom", 182),
    ("SPECIES_MARILL", "Marill", 183),
    ("SPECIES_AZUMARILL", "Azumarill", 184),
    ("SPECIES_SUDOWOODO", "Sudowoodo", 185),
    ("SPECIES_POLITOED", "Politoed", 186),
    ("SPECIES_HOPPIP", "Hoppip", 187),
    ("SPECIES_SKIPLOOM", "Skiploom", 188),
    ("SPECIES_JUMPLUFF", "Jumpluff", 189),
    ("SPECIES_AIPOM", "Aipom", 190),
    ("SPECIES_SUNKERN", "Sunkern", 191),
    ("SPECIES_SUNFLORA", "Sunflora", 192),
    ("SPECIES_YANMA", "Yanma", 193),
    ("SPECIES_WOOPER", "Wooper", 194),
    ("SPECIES_QUAGSIRE", "Quagsire", 195),
    ("SPECIES_ESPEON", "Espeon", 196),
    ("SPECIES_UMBREON", "Umbreon", 197),
    ("SPECIES_MURKROW", "Murkrow", 198),
    ("SPECIES_SLOWKING", "Slowking", 199),
    ("SPECIES_MISDREAVUS", "Misdreavus", 200),
    ("SPECIES_UNOWN", "Unown", 201),
    ("SPECIES_WOBBUFFET", "Wobbuffet", 202),
    ("SPECIES_GIRAFARIG", "Girafarig", 203),
    ("SPECIES_PINECO", "Pineco", 204),
    ("SPECIES_FORRETRESS", "Forretress", 205),
    ("SPECIES_DUNSPARCE", "Dunsparce", 206),
    ("SPECIES_GLIGAR", "Gligar", 207),
    ("SPECIES_STEELIX", "Steelix", 208),
    ("SPECIES_SNUBBULL", "Snubbull", 209),
    ("SPECIES_GRANBULL", "Granbull", 210),
    ("SPECIES_QWILFISH", "Qwilfish", 211),
    ("SPECIES_SCIZOR", "Scizor", 212),
    ("SPECIES_SHUCKLE", "Shuckle", 213),
    ("SPECIES_HERACROSS", "Heracross", 214),
    ("SPECIES_SNEASEL", "Sneasel", 215),
    ("SPECIES_TEDDIURSA", "Teddiursa", 216),
    ("SPECIES_URSARING", "Ursaring", 217),
    ("SPECIES_SLUGMA", "Slugma", 218),
    ("SPECIES_MAGCARGO", "Magcargo", 219),
    ("SPECIES_SWINUB", "Swinub", 220),
    ("SPECIES_PILOSWINE", "Piloswine", 221),
    ("SPECIES_CORSOLA", "Corsola", 222),
    ("SPECIES_REMORAID", "Remoraid", 223),
    ("SPECIES_OCTILLERY", "Octillery", 224),
    ("SPECIES_DELIBIRD", "Delibird", 225),
    ("SPECIES_MANTINE", "Mantine", 226),
    ("SPECIES_SKARMORY", "Skarmory", 227),
    ("SPECIES_HOUNDOUR", "Houndour", 228),
    ("SPECIES_HOUNDOOM", "Houndoom", 229),
    ("SPECIES_KINGDRA", "Kingdra", 230),
    ("SPECIES_PHANPY", "Phanpy", 231),
    ("SPECIES_DONPHAN", "Donphan", 232),
    ("SPECIES_PORYGON2", "Porygon2", 233),
    ("SPECIES_STANTLER", "Stantler", 234),
    ("SPECIES_SMEARGLE", "Smeargle", 235),
    ("SPECIES_TYROGUE", "Tyrogue", 236),
    ("SPECIES_HITMONTOP", "Hitmontop", 237),
    ("SPECIES_SMOOCHUM", "Smoochum", 238),
    ("SPECIES_ELEKID", "Elekid", 239),
    ("SPECIES_MAGBY", "Magby", 240),
    ("SPECIES_MILTANK", "Miltank", 241),
    ("SPECIES_BLISSEY", "Blissey", 242),
    ("SPECIES_RAIKOU", "Raikou", 243),
    ("SPECIES_ENTEI", "Entei", 244),
    ("SPECIES_SUICUNE", "Suicune", 245),
    ("SPECIES_LARVITAR", "Larvitar", 246),
    ("SPECIES_PUPITAR", "Pupitar", 247),
    ("SPECIES_TYRANITAR", "Tyranitar", 248),
    ("SPECIES_LUGIA", "Lugia", 249),
    ("SPECIES_HO_OH", "Ho-Oh", 250),
    ("SPECIES_CELEBI", "Celebi", 251),
    ("SPECIES_TREECKO", "Treecko", 252),
    ("SPECIES_GROVYLE", "Grovyle", 253),
    ("SPECIES_SCEPTILE", "Sceptile", 254),
    ("SPECIES_TORCHIC", "Torchic", 255),
    ("SPECIES_COMBUSKEN", "Combusken", 256),
    ("SPECIES_BLAZIKEN", "Blaziken", 257),
    ("SPECIES_MUDKIP", "Mudkip", 258),
    ("SPECIES_MARSHTOMP", "Marshtomp", 259),
    ("SPECIES_SWAMPERT", "Swampert", 260),
    ("SPECIES_POOCHYENA", "Poochyena", 261),
    ("SPECIES_MIGHTYENA", "Mightyena", 262),
    ("SPECIES_ZIGZAGOON", "Zigzagoon", 263),
    ("SPECIES_LINOONE", "Linoone", 264),
    ("SPECIES_WURMPLE", "Wurmple", 265),
    ("SPECIES_SILCOON", "Silcoon", 266),
    ("SPECIES_BEAUTIFLY", "Beautifly", 267),
    ("SPECIES_CASCOON", "Cascoon", 268),
    ("SPECIES_DUSTOX", "Dustox", 269),
    ("SPECIES_LOTAD", "Lotad", 270),
    ("SPECIES_LOMBRE", "Lombre", 271),
    ("SPECIES_LUDICOLO", "Ludicolo", 272),
    ("SPECIES_SEEDOT", "Seedot", 273),
    ("SPECIES_NUZLEAF", "Nuzleaf", 274),
    ("SPECIES_SHIFTRY", "Shiftry", 275),
    ("SPECIES_NINCADA", "Nincada", 290),
    ("SPECIES_NINJASK", "Ninjask", 291),
    ("SPECIES_SHEDINJA", "Shedinja", 292),
    ("SPECIES_TAILLOW", "Taillow", 276),
    ("SPECIES_SWELLOW", "Swellow", 277),
    ("SPECIES_SHROOMISH", "Shroomish", 285),
    ("SPECIES_BRELOOM", "Breloom", 286),
    ("SPECIES_SPINDA", "Spinda", 327),
    ("SPECIES_WINGULL", "Wingull", 278),
    ("SPECIES_PELIPPER", "Pelipper", 279),
    ("SPECIES_SURSKIT", "Surskit", 283),
    ("SPECIES_MASQUERAIN", "Masquerain", 284),
    ("SPECIES_WAILMER", "Wailmer", 320),
    ("SPECIES_WAILORD", "Wailord", 321),
    ("SPECIES_SKITTY", "Skitty", 300),
    ("SPECIES_DELCATTY", "Delcatty", 301),
    ("SPECIES_KECLEON", "Kecleon", 352),
    ("SPECIES_BALTOY", "Baltoy", 343),
    ("SPECIES_CLAYDOL", "Claydol", 344),
    ("SPECIES_NOSEPASS", "Nosepass", 299),
    ("SPECIES_TORKOAL", "Torkoal", 324),
    ("SPECIES_SABLEYE", "Sableye", 302),
    ("SPECIES_BARBOACH", "Barboach", 339),
    ("SPECIES_WHISCASH", "Whiscash", 340),
    ("SPECIES_LUVDISC", "Luvdisc", 370),
    ("SPECIES_CORPHISH", "Corphish", 341),
    ("SPECIES_CRAWDAUNT", "Crawdaunt", 342),
    ("SPECIES_FEEBAS", "Feebas", 349),
    ("SPECIES_MILOTIC", "Milotic", 350),
    ("SPECIES_CARVANHA", "Carvanha", 318),
    ("SPECIES_SHARPEDO", "Sharpedo", 319),
    ("SPECIES_TRAPINCH", "Trapinch", 328),
    ("SPECIES_VIBRAVA", "Vibrava", 329),
    ("SPECIES_FLYGON", "Flygon", 330),
    ("SPECIES_MAKUHITA", "Makuhita", 296),
    ("SPECIES_HARIYAMA", "Hariyama", 297),
    ("SPECIES_ELECTRIKE", "Electrike", 309),
    ("SPECIES_MANECTRIC", "Manectric", 310),
    ("SPECIES_NUMEL", "Numel", 322),
    ("SPECIES_CAMERUPT", "Camerupt", 323),
    ("SPECIES_SPHEAL", "Spheal", 363),
    ("SPECIES_SEALEO", "Sealeo", 364),
    ("SPECIES_WALREIN", "Walrein", 365),
    ("SPECIES_CACNEA", "Cacnea", 331),
    ("SPECIES_CACTURNE", "Cacturne", 332),
    ("SPECIES_SNORUNT", "Snorunt", 361),
    ("SPECIES_GLALIE", "Glalie", 362),
    ("SPECIES_LUNATONE", "Lunatone", 337),
    ("SPECIES_SOLROCK", "Solrock", 338),
    ("SPECIES_AZURILL", "Azurill", 298),
    ("SPECIES_SPOINK", "Spoink", 325),
    ("SPECIES_GRUMPIG", "Grumpig", 326),
    ("SPECIES_PLUSLE", "Plusle", 311),
    ("SPECIES_MINUN", "Minun", 312),
    ("SPECIES_MAWILE", "Mawile", 303),
    ("SPECIES_MEDITITE", "Meditite", 307),
    ("SPECIES_MEDICHAM", "Medicham", 308),
    ("SPECIES_SWABLU", "Swablu", 333),
    ("SPECIES_ALTARIA", "Altaria", 334),
    ("SPECIES_WYNAUT", "Wynaut", 360),
    ("SPECIES_DUSKULL", "Duskull", 355),
    ("SPECIES_DUSCLOPS", "Dusclops", 356),
    ("SPECIES_ROSELIA", "Roselia", 315),
    ("SPECIES_SLAKOTH", "Slakoth", 287),
    ("SPECIES_VIGOROTH", "Vigoroth", 288),
    ("SPECIES_SLAKING", "Slaking", 289),
    ("SPECIES_GULPIN", "Gulpin", 316),
    ("SPECIES_SWALOT", "Swalot", 317),
    ("SPECIES_TROPIUS", "Tropius", 357),
    ("SPECIES_WHISMUR", "Whismur", 293),
    ("SPECIES_LOUDRED", "Loudred", 294),
    ("SPECIES_EXPLOUD", "Exploud", 295),
    ("SPECIES_CLAMPERL", "Clamperl", 366),
    ("SPECIES_HUNTAIL", "Huntail", 367),
    ("SPECIES_GOREBYSS", "Gorebyss", 368),
    ("SPECIES_ABSOL", "Absol", 359),
    ("SPECIES_SHUPPET", "Shuppet", 353),
    ("SPECIES_BANETTE", "Banette", 354),
    ("SPECIES_SEVIPER", "Seviper", 336),
    ("SPECIES_ZANGOOSE", "Zangoose", 335),
    ("SPECIES_RELICANTH", "Relicanth", 369),
    ("SPECIES_ARON", "Aron", 304),
    ("SPECIES_LAIRON", "Lairon", 305),
    ("SPECIES_AGGRON", "Aggron", 306),
    ("SPECIES_CASTFORM", "Castform", 351),
    ("SPECIES_VOLBEAT", "Volbeat", 313),
    ("SPECIES_ILLUMISE", "Illumise", 314),
    ("SPECIES_LILEEP", "Lileep", 345),
    ("SPECIES_CRADILY", "Cradily", 346),
    ("SPECIES_ANORITH", "Anorith", 347),
    ("SPECIES_ARMALDO", "Armaldo", 348),
    ("SPECIES_RALTS", "Ralts", 280),
    ("SPECIES_KIRLIA", "Kirlia", 281),
    ("SPECIES_GARDEVOIR", "Gardevoir", 282),
    ("SPECIES_BAGON", "Bagon", 371),
    ("SPECIES_SHELGON", "Shelgon", 372),
    ("SPECIES_SALAMENCE", "Salamence", 373),
    ("SPECIES_BELDUM", "Beldum", 374),
    ("SPECIES_METANG", "Metang", 375),
    ("SPECIES_METAGROSS", "Metagross", 376),
    ("SPECIES_REGIROCK", "Regirock", 377),
    ("SPECIES_REGICE", "Regice", 378),
    ("SPECIES_REGISTEEL", "Registeel", 379),
    ("SPECIES_KYOGRE", "Kyogre", 382),
    ("SPECIES_GROUDON", "Groudon", 383),
    ("SPECIES_RAYQUAZA", "Rayquaza", 384),
    ("SPECIES_LATIAS", "Latias", 380),
    ("SPECIES_LATIOS", "Latios", 381),
    ("SPECIES_JIRACHI", "Jirachi", 385),
    ("SPECIES_DEOXYS", "Deoxys", 386),
    ("SPECIES_CHIMECHO", "Chimecho", 358),
]


def load_json_data(data_name: str) -> Union[List[Any], Dict[str, Any]]:
    return orjson.loads(pkgutil.get_data(__name__, "data/" + data_name).decode("utf-8-sig"))


def _init() -> None:
    extracted_data: Dict[str, Any] = load_json_data("extracted_data.json")
    data.constants = extracted_data["constants"]
    data.ram_addresses = extracted_data["misc_ram_addresses"]
    data.rom_addresses = extracted_data["misc_rom_addresses"]

    location_data = load_json_data("locations.json")
    event_data = load_json_data("events.json")
    item_data = load_json_data("items.json")

    # Create map data
    for map_name, map_json in extracted_data["maps"].items():
        land_encounters = None
        water_encounters = None
        fishing_encounters = None

        if "land_encounters" in map_json:
            land_slots: Dict[str, List[EncounterSpeciesData]] = {}
            for version, slots in map_json["land_encounters"]["slots"].items():
                version_slots: List[EncounterSpeciesData] = []
                for slot_data in slots:
                    version_slots.append(EncounterSpeciesData(
                        slot_data["default_species"],
                        slot_data["min_level"],
                        slot_data["max_level"]
                    ))
                land_slots[version] = version_slots
            land_encounters = EncounterTableData(
                land_slots,
                map_json["land_encounters"]["address"]
            )
        if "water_encounters" in map_json:
            water_slots: Dict[str, List[EncounterSpeciesData]] = {}
            for version, slots in map_json["water_encounters"]["slots"].items():
                version_slots: List[EncounterSpeciesData] = []
                for slot_data in slots:
                    version_slots.append(EncounterSpeciesData(
                        slot_data["default_species"],
                        slot_data["min_level"],
                        slot_data["max_level"]
                    ))
                water_slots[version] = version_slots
            water_encounters = EncounterTableData(
                water_slots,
                map_json["water_encounters"]["address"]
            )
        if "fishing_encounters" in map_json:
            fishing_slots: Dict[str, List[EncounterSpeciesData]] = {}
            for version, slots in map_json["fishing_encounters"]["slots"].items():
                version_slots: List[EncounterSpeciesData] = []
                for slot_data in slots:
                    version_slots.append(EncounterSpeciesData(
                        slot_data["default_species"],
                        slot_data["min_level"],
                        slot_data["max_level"]
                    ))
                fishing_slots[version] = version_slots
            fishing_encounters = EncounterTableData(
                fishing_slots,
                map_json["fishing_encounters"]["address"]
            )

        data.maps[map_name] = MapData(
            map_name,
            map_json["header_address"],
            land_encounters,
            water_encounters,
            fishing_encounters,
            True
        )

    # Load/merge region json files
    region_json_list = []
    for file in resource_listdir(__name__, "data/regions"):
        if not resource_isdir(__name__, "data/regions/" + file):
            region_json_list.append(load_json_data("regions/" + file))

    regions_json = {}
    for region_subset in region_json_list:
        for region_name, region_json in region_subset.items():
            if region_name in regions_json:
                raise AssertionError("Pokemon FRLG: Region [{region_name}] was defined multiple times")
            regions_json[region_name] = region_json

    # Create region data
    claimed_locations: Set[str] = set()
    claimed_warps: Set[str] = set()

    data.regions = {}
    for region_id, region_json in regions_json.items():
        parent_map = data.maps[region_json["parent_map"]] if region_json["parent_map"] is not None else None

        if parent_map is not None:
            parent_map.kanto = region_json["kanto"]

        new_region = RegionData(
            region_id,
            region_json["name"],
            parent_map,
            region_json["encounter_region"],
            region_json["has_land"],
            region_json["has_water"],
            region_json["has_fishing"],
            region_json["kanto"]
        )

        # Locations
        for location_id in region_json["locations"]:
            if location_id in claimed_locations:
                raise AssertionError(f"Pokemon FRLG: Location [{location_id}] was claimed by multiple regions")

            location_json = extracted_data["locations"][location_id]

            if "BULBASAUR_REWARD" in location_id:
                import re
                trainer = re.match("TRAINER_([A-Z0-9_]+)_BULBASAUR_REWARD", location_id).group(1)
                alternate_rival_jsons = [extracted_data["locations"][alternate] for alternate in [
                    f"TRAINER_{trainer}_CHARMANDER_REWARD",
                    f"TRAINER_{trainer}_SQUIRTLE_REWARD"
                ]]

                location_address: Dict[str, List[int]] = {}

                for game_version_revision in location_json["address"].keys():
                    location_address[game_version_revision] = [location_json["address"][game_version_revision]]

                for game_version_revision in location_address.keys():
                    for alternate_rival_json in alternate_rival_jsons:
                        location_address[game_version_revision].append(
                            alternate_rival_json["address"][game_version_revision])

                new_location = LocationData(
                    location_id,
                    location_data[location_id]["name"],
                    region_id,
                    location_json["default_item"],
                    location_address,
                    location_json["flag"],
                    frozenset(location_data[location_id]["tags"])
                )
            else:
                new_location = LocationData(
                    location_id,
                    location_data[location_id]["name"],
                    region_id,
                    location_json["default_item"],
                    location_json["address"],
                    location_json["flag"],
                    frozenset(location_data[location_id]["tags"])
                )

            new_region.locations.append(location_id)
            data.locations[location_id] = new_location
            claimed_locations.add(location_id)

        # Events
        for event_id in region_json["events"]:
            new_event = EventData(
                event_id,
                event_data[event_id]["name"],
                event_data[event_id]["item"],
                region_id,
                frozenset(event_data[event_id]["tags"])
            )
            new_region.events.append(event_id)
            data.events[event_id] = new_event

        # Exits
        new_region.exits = region_json["exits"]

        # Warps
        for encoded_warp, name in region_json["warps"].items():
            if encoded_warp in claimed_warps:
                raise AssertionError(f"Pokemon FRLG: Warp [{encoded_warp}] was claimed by multiple regions")
            new_region.warps.append(encoded_warp)
            data.warps[encoded_warp] = Warp(encoded_warp, name, region_id)
            claimed_warps.add(encoded_warp)

        new_region.warps.sort()

        data.regions[region_id] = new_region

    # Create item data
    data.items = {}
    for item_id_name, attributes in item_data.items():
        if attributes["classification"] == "PROGRESSION":
            item_classification = ItemClassification.progression
        elif attributes["classification"] == "USEFUL":
            item_classification = ItemClassification.useful
        elif attributes["classification"] == "FILLER":
            item_classification = ItemClassification.filler
        elif attributes["classification"] == "TRAP":
            item_classification = ItemClassification.trap
        else:
            raise ValueError(f"Unknown classification {attributes['classification']} for item {item_id_name}")

        data.items[data.constants[item_id_name]] = ItemData(
            attributes["name"],
            data.constants[item_id_name],
            item_classification,
            frozenset(attributes["tags"])
        )

    # Create warp map
    for warp, destination in extracted_data["warps"].items():
        data.warp_map[warp] = None if destination == "" else destination

    # Create species data
    max_species_id = 0
    for species_id_name, species_name, species_dex_number in ALL_SPECIES:
        species_id = data.constants[species_id_name]
        max_species_id = max(species_id, max_species_id)
        species_data = extracted_data["species"][species_id]

        learnset = [LearnsetMove(item["level"], item["move_id"]) for item in species_data["learnset"]["moves"]]

        data.species[species_id] = SpeciesData(
            species_id_name,
            species_name,
            species_id,
            species_dex_number,
            BaseStats(
                species_data["base_stats"][0],
                species_data["base_stats"][1],
                species_data["base_stats"][2],
                species_data["base_stats"][3],
                species_data["base_stats"][4],
                species_data["base_stats"][5]
            ),
            (species_data["types"][0], species_data["types"][1]),
            (species_data["abilities"][0], species_data["abilities"][1]),
            [EvolutionData(
                evolution_data["param"],
                evolution_data["species"],
                EVOLUTION_METHOD_TYPE[evolution_data["method"]]
            ) for evolution_data in species_data["evolutions"]],
            None,
            species_data["catch_rate"],
            species_data["friendship"],
            learnset,
            int(species_data["tmhm_learnset"], 16),
            species_data["learnset"]["address"],
            species_data["address"]
        )

    for species in data.species.values():
        for evolution in species.evolutions:
            data.species[evolution.species_id].pre_evolution = species.species_id

    # Create starter data
    for name, starter_data in extracted_data["starter_pokemon"].items():
        data.starters[name] = StarterData(
            starter_data["species"],
            starter_data["player_address"],
            starter_data["rival_address"]
        )

    # Create legendary pokemon data
    for name, legendary_data in extracted_data["legendary_pokemon"].items():
        data.legendary_pokemon[name] = MiscPokemonData(
            legendary_data["species"],
            legendary_data["level"],
            legendary_data["address"],
            legendary_data["level_address"]
        )

    # Create misc pokemon data
    for name, misc_data in extracted_data["misc_pokemon"].items():
        data.misc_pokemon[name] = MiscPokemonData(
            misc_data["species"],
            misc_data["level"],
            misc_data["address"],
            misc_data["level_address"]
        )

    # Create trainer data
    for name, trainer_data in extracted_data["trainers"].items():
        party_data = trainer_data["party"]
        data.trainers[name] = TrainerData(
            TrainerPartyData([
                    TrainerPokemonData(
                        pokemon["species"],
                        pokemon["level"],
                        (pokemon["moves"][0],
                         pokemon["moves"][1],
                         pokemon["moves"][2],
                         pokemon["moves"][3]) if "moves" in pokemon else None,
                        False
                    ) for pokemon in party_data],
                POKEMON_DATA_TYPE[trainer_data["data_type"]],
                trainer_data["party_address"]
            ),
            trainer_data["address"]
        )

    # TM/HM Moves
    data.tmhm_moves = extracted_data["tmhm_moves"]

    # Abilities
    data.abilities = {j: data.constants[i] for i, j in [
        ("ABILITY_STENCH", "Stench"),
        ("ABILITY_DRIZZLE", "Drizzle"),
        ("ABILITY_SPEED_BOOST", "Speed Boost"),
        ("ABILITY_BATTLE_ARMOR", "Battle Armor"),
        ("ABILITY_STURDY", "Sturdy"),
        ("ABILITY_DAMP", "Damp"),
        ("ABILITY_LIMBER", "Limber"),
        ("ABILITY_SAND_VEIL", "Sand Veil"),
        ("ABILITY_STATIC", "Static"),
        ("ABILITY_VOLT_ABSORB", "Volt Absorb"),
        ("ABILITY_WATER_ABSORB", "Water Absorb"),
        ("ABILITY_OBLIVIOUS", "Oblivious"),
        ("ABILITY_CLOUD_NINE", "Cloud Nine"),
        ("ABILITY_COMPOUND_EYES", "Compoundeyes"),
        ("ABILITY_INSOMNIA", "Insomnia"),
        ("ABILITY_COLOR_CHANGE", "Color Change"),
        ("ABILITY_IMMUNITY", "Immunity"),
        ("ABILITY_FLASH_FIRE", "Flash Fire"),
        ("ABILITY_SHIELD_DUST", "Shield Dust"),
        ("ABILITY_OWN_TEMPO", "Own Tempo"),
        ("ABILITY_SUCTION_CUPS", "Suction Cups"),
        ("ABILITY_INTIMIDATE", "Intimidate"),
        ("ABILITY_SHADOW_TAG", "Shadow Tag"),
        ("ABILITY_ROUGH_SKIN", "Rough Skin"),
        ("ABILITY_WONDER_GUARD", "Wonder Guard"),
        ("ABILITY_LEVITATE", "Levitate"),
        ("ABILITY_EFFECT_SPORE", "Effect Spore"),
        ("ABILITY_SYNCHRONIZE", "Synchronize"),
        ("ABILITY_CLEAR_BODY", "Clear Body"),
        ("ABILITY_NATURAL_CURE", "Natural Cure"),
        ("ABILITY_LIGHTNING_ROD", "Lightningrod"),
        ("ABILITY_SERENE_GRACE", "Serene Grace"),
        ("ABILITY_SWIFT_SWIM", "Swift Swim"),
        ("ABILITY_CHLOROPHYLL", "Chlorophyll"),
        ("ABILITY_ILLUMINATE", "Illuminate"),
        ("ABILITY_TRACE", "Trace"),
        ("ABILITY_HUGE_POWER", "Huge Power"),
        ("ABILITY_POISON_POINT", "Poison Point"),
        ("ABILITY_INNER_FOCUS", "Inner Focus"),
        ("ABILITY_MAGMA_ARMOR", "Magma Armor"),
        ("ABILITY_WATER_VEIL", "Water Veil"),
        ("ABILITY_MAGNET_PULL", "Magnet Pull"),
        ("ABILITY_SOUNDPROOF", "Soundproof"),
        ("ABILITY_RAIN_DISH", "Rain Dish"),
        ("ABILITY_SAND_STREAM", "Sand Stream"),
        ("ABILITY_PRESSURE", "Pressure"),
        ("ABILITY_THICK_FAT", "Thick Fat"),
        ("ABILITY_EARLY_BIRD", "Early Bird"),
        ("ABILITY_FLAME_BODY", "Flame Body"),
        ("ABILITY_RUN_AWAY", "Run Away"),
        ("ABILITY_KEEN_EYE", "Keen Eye"),
        ("ABILITY_HYPER_CUTTER", "Hyper Cutter"),
        ("ABILITY_PICKUP", "Pickup"),
        ("ABILITY_TRUANT", "Truant"),
        ("ABILITY_HUSTLE", "Hustle"),
        ("ABILITY_CUTE_CHARM", "Cute Charm"),
        ("ABILITY_PLUS", "Plus"),
        ("ABILITY_MINUS", "Minus"),
        ("ABILITY_FORECAST", "Forecast"),
        ("ABILITY_STICKY_HOLD", "Sticky Hold"),
        ("ABILITY_SHED_SKIN", "Shed Skin"),
        ("ABILITY_GUTS", "Guts"),
        ("ABILITY_MARVEL_SCALE", "Marvel Scale"),
        ("ABILITY_LIQUID_OOZE", "Liquid Ooze"),
        ("ABILITY_OVERGROW", "Overgrow"),
        ("ABILITY_BLAZE", "Blaze"),
        ("ABILITY_TORRENT", "Torrent"),
        ("ABILITY_SWARM", "Swarm"),
        ("ABILITY_ROCK_HEAD", "Rock Head"),
        ("ABILITY_DROUGHT", "Drought"),
        ("ABILITY_ARENA_TRAP", "Arena Trap"),
        ("ABILITY_VITAL_SPIRIT", "Vital Spirit"),
        ("ABILITY_WHITE_SMOKE", "White Smoke"),
        ("ABILITY_PURE_POWER", "Pure Power"),
        ("ABILITY_SHELL_ARMOR", "Shell Armor"),
        ("ABILITY_CACOPHONY", "Cacophony"),
        ("ABILITY_AIR_LOCK", "Air Lock")
    ]}

    # Moves
    data.moves = {j: data.constants[i] for i, j in [
        ("MOVE_POUND", "Pound"),
        ("MOVE_KARATE_CHOP", "Karate Chop"),
        ("MOVE_DOUBLE_SLAP", "Doubleslap"),
        ("MOVE_COMET_PUNCH", "Comet Punch"),
        ("MOVE_MEGA_PUNCH", "Mega Punch"),
        ("MOVE_PAY_DAY", "Pay Day"),
        ("MOVE_FIRE_PUNCH", "Fire Punch"),
        ("MOVE_ICE_PUNCH", "Ice Punch"),
        ("MOVE_THUNDER_PUNCH", "Thunderpunch"),
        ("MOVE_SCRATCH", "Scratch"),
        ("MOVE_VICE_GRIP", "Vicegrip"),
        ("MOVE_GUILLOTINE", "Guillotine"),
        ("MOVE_RAZOR_WIND", "Razor Wind"),
        ("MOVE_SWORDS_DANCE", "Swords Dance"),
        ("MOVE_CUT", "Cut"),
        ("MOVE_GUST", "Gust"),
        ("MOVE_WING_ATTACK", "Wing Attack"),
        ("MOVE_WHIRLWIND", "Whirlwind"),
        ("MOVE_FLY", "Fly"),
        ("MOVE_BIND", "Bind"),
        ("MOVE_SLAM", "Slam"),
        ("MOVE_VINE_WHIP", "Vine Whip"),
        ("MOVE_STOMP", "Stomp"),
        ("MOVE_DOUBLE_KICK", "Double Kick"),
        ("MOVE_MEGA_KICK", "Mega Kick"),
        ("MOVE_JUMP_KICK", "Jump Kick"),
        ("MOVE_ROLLING_KICK", "Rolling Kick"),
        ("MOVE_SAND_ATTACK", "Sand-Attack"),
        ("MOVE_HEADBUTT", "Headbutt"),
        ("MOVE_HORN_ATTACK", "Horn Attack"),
        ("MOVE_FURY_ATTACK", "Fury Attack"),
        ("MOVE_HORN_DRILL", "Horn Drill"),
        ("MOVE_TACKLE", "Tackle"),
        ("MOVE_BODY_SLAM", "Body Slam"),
        ("MOVE_WRAP", "Wrap"),
        ("MOVE_TAKE_DOWN", "Take Down"),
        ("MOVE_THRASH", "Thrash"),
        ("MOVE_DOUBLE_EDGE", "Double-Edge"),
        ("MOVE_TAIL_WHIP", "Tail Whip"),
        ("MOVE_POISON_STING", "Poison Sting"),
        ("MOVE_TWINEEDLE", "Twineedle"),
        ("MOVE_PIN_MISSILE", "Pin Missile"),
        ("MOVE_LEER", "Leer"),
        ("MOVE_BITE", "Bite"),
        ("MOVE_GROWL", "Growl"),
        ("MOVE_ROAR", "Roar"),
        ("MOVE_SING", "Sing"),
        ("MOVE_SUPERSONIC", "Supersonic"),
        ("MOVE_SONIC_BOOM", "Sonicboom"),
        ("MOVE_DISABLE", "Disable"),
        ("MOVE_ACID", "Acid"),
        ("MOVE_EMBER", "Ember"),
        ("MOVE_FLAMETHROWER", "Flamethrower"),
        ("MOVE_MIST", "Mist"),
        ("MOVE_WATER_GUN", "Water Gun"),
        ("MOVE_HYDRO_PUMP", "Hydro Pump"),
        ("MOVE_SURF", "Surf"),
        ("MOVE_ICE_BEAM", "Ice Beam"),
        ("MOVE_BLIZZARD", "Blizzard"),
        ("MOVE_PSYBEAM", "Psybeam"),
        ("MOVE_BUBBLE_BEAM", "Bubblebeam"),
        ("MOVE_AURORA_BEAM", "Aurora Beam"),
        ("MOVE_HYPER_BEAM", "Hyper Beam"),
        ("MOVE_PECK", "Peck"),
        ("MOVE_DRILL_PECK", "Drill Peck"),
        ("MOVE_SUBMISSION", "Submission"),
        ("MOVE_LOW_KICK", "Low Kick"),
        ("MOVE_COUNTER", "Counter"),
        ("MOVE_SEISMIC_TOSS", "Seismic Toss"),
        ("MOVE_STRENGTH", "Strength"),
        ("MOVE_ABSORB", "Absorb"),
        ("MOVE_MEGA_DRAIN", "Mega Drain"),
        ("MOVE_LEECH_SEED", "Leech Seed"),
        ("MOVE_GROWTH", "Growth"),
        ("MOVE_RAZOR_LEAF", "Razor Leaf"),
        ("MOVE_SOLAR_BEAM", "Solarbeam"),
        ("MOVE_POISON_POWDER", "Poisonpowder"),
        ("MOVE_STUN_SPORE", "Stun Spore"),
        ("MOVE_SLEEP_POWDER", "Sleep Powder"),
        ("MOVE_PETAL_DANCE", "Petal Dance"),
        ("MOVE_STRING_SHOT", "String Shot"),
        ("MOVE_DRAGON_RAGE", "Dragon Rage"),
        ("MOVE_FIRE_SPIN", "Fire Spin"),
        ("MOVE_THUNDER_SHOCK", "Thundershock"),
        ("MOVE_THUNDERBOLT", "Thunderbolt"),
        ("MOVE_THUNDER_WAVE", "Thunder Wave"),
        ("MOVE_THUNDER", "Thunder"),
        ("MOVE_ROCK_THROW", "Rock Throw"),
        ("MOVE_EARTHQUAKE", "Earthquake"),
        ("MOVE_FISSURE", "Fissure"),
        ("MOVE_DIG", "Dig"),
        ("MOVE_TOXIC", "Toxic"),
        ("MOVE_CONFUSION", "Confusion"),
        ("MOVE_PSYCHIC", "Psychic"),
        ("MOVE_HYPNOSIS", "Hypnosis"),
        ("MOVE_MEDITATE", "Meditate"),
        ("MOVE_AGILITY", "Agility"),
        ("MOVE_QUICK_ATTACK", "Quick Attack"),
        ("MOVE_RAGE", "Rage"),
        ("MOVE_TELEPORT", "Teleport"),
        ("MOVE_NIGHT_SHADE", "Night Shade"),
        ("MOVE_MIMIC", "Mimic"),
        ("MOVE_SCREECH", "Screech"),
        ("MOVE_DOUBLE_TEAM", "Double Team"),
        ("MOVE_RECOVER", "Recover"),
        ("MOVE_HARDEN", "Harden"),
        ("MOVE_MINIMIZE", "Minimize"),
        ("MOVE_SMOKESCREEN", "Smokescreen"),
        ("MOVE_CONFUSE_RAY", "Confuse Ray"),
        ("MOVE_WITHDRAW", "Withdraw"),
        ("MOVE_DEFENSE_CURL", "Defense Curl"),
        ("MOVE_BARRIER", "Barrier"),
        ("MOVE_LIGHT_SCREEN", "Light Screen"),
        ("MOVE_HAZE", "Haze"),
        ("MOVE_REFLECT", "Reflect"),
        ("MOVE_FOCUS_ENERGY", "Focus Energy"),
        ("MOVE_BIDE", "Bide"),
        ("MOVE_METRONOME", "Metronome"),
        ("MOVE_MIRROR_MOVE", "Mirror Move"),
        ("MOVE_SELF_DESTRUCT", "Selfdestruct"),
        ("MOVE_EGG_BOMB", "Egg Bomb"),
        ("MOVE_LICK", "Lick"),
        ("MOVE_SMOG", "Smog"),
        ("MOVE_SLUDGE", "Sludge"),
        ("MOVE_BONE_CLUB", "Bone Club"),
        ("MOVE_FIRE_BLAST", "Fire Blast"),
        ("MOVE_WATERFALL", "Waterfall"),
        ("MOVE_CLAMP", "Clamp"),
        ("MOVE_SWIFT", "Swift"),
        ("MOVE_SKULL_BASH", "Skull Bash"),
        ("MOVE_SPIKE_CANNON", "Spike Cannon"),
        ("MOVE_CONSTRICT", "Constrict"),
        ("MOVE_AMNESIA", "Amnesia"),
        ("MOVE_KINESIS", "Kinesis"),
        ("MOVE_SOFT_BOILED", "Softboiled"),
        ("MOVE_HI_JUMP_KICK", "Hi Jump Kick"),
        ("MOVE_GLARE", "Glare"),
        ("MOVE_DREAM_EATER", "Dream Eater"),
        ("MOVE_POISON_GAS", "Poison Gas"),
        ("MOVE_BARRAGE", "Barrage"),
        ("MOVE_LEECH_LIFE", "Leech Life"),
        ("MOVE_LOVELY_KISS", "Lovely Kiss"),
        ("MOVE_SKY_ATTACK", "Sky Attack"),
        ("MOVE_TRANSFORM", "Transform"),
        ("MOVE_BUBBLE", "Bubble"),
        ("MOVE_DIZZY_PUNCH", "Dizzy Punch"),
        ("MOVE_SPORE", "Spore"),
        ("MOVE_FLASH", "Flash"),
        ("MOVE_PSYWAVE", "Psywave"),
        ("MOVE_SPLASH", "Splash"),
        ("MOVE_ACID_ARMOR", "Acid Armor"),
        ("MOVE_CRABHAMMER", "Crabhammer"),
        ("MOVE_EXPLOSION", "Explosion"),
        ("MOVE_FURY_SWIPES", "Fury Swipes"),
        ("MOVE_BONEMERANG", "Bonemerang"),
        ("MOVE_REST", "Rest"),
        ("MOVE_ROCK_SLIDE", "Rock Slide"),
        ("MOVE_HYPER_FANG", "Hyper Fang"),
        ("MOVE_SHARPEN", "Sharpen"),
        ("MOVE_CONVERSION", "Conversion"),
        ("MOVE_TRI_ATTACK", "Tri Attack"),
        ("MOVE_SUPER_FANG", "Super Fang"),
        ("MOVE_SLASH", "Slash"),
        ("MOVE_SUBSTITUTE", "Substitute"),
        ("MOVE_SKETCH", "Sketch"),
        ("MOVE_TRIPLE_KICK", "Triple Kick"),
        ("MOVE_THIEF", "Thief"),
        ("MOVE_SPIDER_WEB", "Spider Web"),
        ("MOVE_MIND_READER", "Mind Reader"),
        ("MOVE_NIGHTMARE", "Nightmare"),
        ("MOVE_FLAME_WHEEL", "Flame Wheel"),
        ("MOVE_SNORE", "Snore"),
        ("MOVE_CURSE", "Curse"),
        ("MOVE_FLAIL", "Flail"),
        ("MOVE_CONVERSION_2", "Conversion 2"),
        ("MOVE_AEROBLAST", "Aeroblast"),
        ("MOVE_COTTON_SPORE", "Cotton Spore"),
        ("MOVE_REVERSAL", "Reversal"),
        ("MOVE_SPITE", "Spite"),
        ("MOVE_POWDER_SNOW", "Powder Snow"),
        ("MOVE_PROTECT", "Protect"),
        ("MOVE_MACH_PUNCH", "Mach Punch"),
        ("MOVE_SCARY_FACE", "Scary Face"),
        ("MOVE_FAINT_ATTACK", "Faint Attack"),
        ("MOVE_SWEET_KISS", "Sweet Kiss"),
        ("MOVE_BELLY_DRUM", "Belly Drum"),
        ("MOVE_SLUDGE_BOMB", "Sludge Bomb"),
        ("MOVE_MUD_SLAP", "Mud-Slap"),
        ("MOVE_OCTAZOOKA", "Octazooka"),
        ("MOVE_SPIKES", "Spikes"),
        ("MOVE_ZAP_CANNON", "Zap Cannon"),
        ("MOVE_FORESIGHT", "Foresight"),
        ("MOVE_DESTINY_BOND", "Destiny Bond"),
        ("MOVE_PERISH_SONG", "Perish Song"),
        ("MOVE_ICY_WIND", "Icy Wind"),
        ("MOVE_DETECT", "Detect"),
        ("MOVE_BONE_RUSH", "Bone Rush"),
        ("MOVE_LOCK_ON", "Lock-On"),
        ("MOVE_OUTRAGE", "Outrage"),
        ("MOVE_SANDSTORM", "Sandstorm"),
        ("MOVE_GIGA_DRAIN", "Giga Drain"),
        ("MOVE_ENDURE", "Endure"),
        ("MOVE_CHARM", "Charm"),
        ("MOVE_ROLLOUT", "Rollout"),
        ("MOVE_FALSE_SWIPE", "False Swipe"),
        ("MOVE_SWAGGER", "Swagger"),
        ("MOVE_MILK_DRINK", "Milk Drink"),
        ("MOVE_SPARK", "Spark"),
        ("MOVE_FURY_CUTTER", "Fury Cutter"),
        ("MOVE_STEEL_WING", "Steel Wing"),
        ("MOVE_MEAN_LOOK", "Mean Look"),
        ("MOVE_ATTRACT", "Attract"),
        ("MOVE_SLEEP_TALK", "Sleep Talk"),
        ("MOVE_HEAL_BELL", "Heal Bell"),
        ("MOVE_RETURN", "Return"),
        ("MOVE_PRESENT", "Present"),
        ("MOVE_FRUSTRATION", "Frustration"),
        ("MOVE_SAFEGUARD", "Safeguard"),
        ("MOVE_PAIN_SPLIT", "Pain Split"),
        ("MOVE_SACRED_FIRE", "Sacred Fire"),
        ("MOVE_MAGNITUDE", "Magnitude"),
        ("MOVE_DYNAMIC_PUNCH", "Dynamicpunch"),
        ("MOVE_MEGAHORN", "Megahorn"),
        ("MOVE_DRAGON_BREATH", "Dragonbreath"),
        ("MOVE_BATON_PASS", "Baton Pass"),
        ("MOVE_ENCORE", "Encore"),
        ("MOVE_PURSUIT", "Pursuit"),
        ("MOVE_RAPID_SPIN", "Rapid Spin"),
        ("MOVE_SWEET_SCENT", "Sweet Scent"),
        ("MOVE_IRON_TAIL", "Iron Tail"),
        ("MOVE_METAL_CLAW", "Metal Claw"),
        ("MOVE_VITAL_THROW", "Vital Throw"),
        ("MOVE_MORNING_SUN", "Morning Sun"),
        ("MOVE_SYNTHESIS", "Synthesis"),
        ("MOVE_MOONLIGHT", "Moonlight"),
        ("MOVE_HIDDEN_POWER", "Hidden Power"),
        ("MOVE_CROSS_CHOP", "Cross Chop"),
        ("MOVE_TWISTER", "Twister"),
        ("MOVE_RAIN_DANCE", "Rain Dance"),
        ("MOVE_SUNNY_DAY", "Sunny Day"),
        ("MOVE_CRUNCH", "Crunch"),
        ("MOVE_MIRROR_COAT", "Mirror Coat"),
        ("MOVE_PSYCH_UP", "Psych Up"),
        ("MOVE_EXTREME_SPEED", "Extremespeed"),
        ("MOVE_ANCIENT_POWER", "Ancientpower"),
        ("MOVE_SHADOW_BALL", "Shadow Ball"),
        ("MOVE_FUTURE_SIGHT", "Future Sight"),
        ("MOVE_ROCK_SMASH", "Rock Smash"),
        ("MOVE_WHIRLPOOL", "Whirlpool"),
        ("MOVE_BEAT_UP", "Beat Up"),
        ("MOVE_FAKE_OUT", "Fake Out"),
        ("MOVE_UPROAR", "Uproar"),
        ("MOVE_STOCKPILE", "Stockpile"),
        ("MOVE_SPIT_UP", "Spit Up"),
        ("MOVE_SWALLOW", "Swallow"),
        ("MOVE_HEAT_WAVE", "Heat Wave"),
        ("MOVE_HAIL", "Hail"),
        ("MOVE_TORMENT", "Torment"),
        ("MOVE_FLATTER", "Flatter"),
        ("MOVE_WILL_O_WISP", "Will-O-Wisp"),
        ("MOVE_MEMENTO", "Memento"),
        ("MOVE_FACADE", "Facade"),
        ("MOVE_FOCUS_PUNCH", "Focus Punch"),
        ("MOVE_SMELLING_SALT", "Smellingsalt"),
        ("MOVE_FOLLOW_ME", "Follow Me"),
        ("MOVE_NATURE_POWER", "Nature Power"),
        ("MOVE_CHARGE", "Charge"),
        ("MOVE_TAUNT", "Taunt"),
        ("MOVE_HELPING_HAND", "Helping Hand"),
        ("MOVE_TRICK", "Trick"),
        ("MOVE_ROLE_PLAY", "Role Play"),
        ("MOVE_WISH", "Wish"),
        ("MOVE_ASSIST", "Assist"),
        ("MOVE_INGRAIN", "Ingrain"),
        ("MOVE_SUPERPOWER", "Superpower"),
        ("MOVE_MAGIC_COAT", "Magic Coat"),
        ("MOVE_RECYCLE", "Recycle"),
        ("MOVE_REVENGE", "Revenge"),
        ("MOVE_BRICK_BREAK", "Brick Break"),
        ("MOVE_YAWN", "Yawn"),
        ("MOVE_KNOCK_OFF", "Knock Off"),
        ("MOVE_ENDEAVOR", "Endeavor"),
        ("MOVE_ERUPTION", "Eruption"),
        ("MOVE_SKILL_SWAP", "Skill Swap"),
        ("MOVE_IMPRISON", "Imprison"),
        ("MOVE_REFRESH", "Refresh"),
        ("MOVE_GRUDGE", "Grudge"),
        ("MOVE_SNATCH", "Snatch"),
        ("MOVE_SECRET_POWER", "Secret Power"),
        ("MOVE_DIVE", "Dive"),
        ("MOVE_ARM_THRUST", "Arm Thrust"),
        ("MOVE_CAMOUFLAGE", "Camouflage"),
        ("MOVE_TAIL_GLOW", "Tail Glow"),
        ("MOVE_LUSTER_PURGE", "Luster Purge"),
        ("MOVE_MIST_BALL", "Mist Ball"),
        ("MOVE_FEATHER_DANCE", "Featherdance"),
        ("MOVE_TEETER_DANCE", "Teeter Dance"),
        ("MOVE_BLAZE_KICK", "Blaze Kick"),
        ("MOVE_MUD_SPORT", "Mud Sport"),
        ("MOVE_ICE_BALL", "Ice Ball"),
        ("MOVE_NEEDLE_ARM", "Needle Arm"),
        ("MOVE_SLACK_OFF", "Slack Off"),
        ("MOVE_HYPER_VOICE", "Hyper Voice"),
        ("MOVE_POISON_FANG", "Poison Fang"),
        ("MOVE_CRUSH_CLAW", "Crush Claw"),
        ("MOVE_BLAST_BURN", "Blast Burn"),
        ("MOVE_HYDRO_CANNON", "Hydro Cannon"),
        ("MOVE_METEOR_MASH", "Meteor Mash"),
        ("MOVE_ASTONISH", "Astonish"),
        ("MOVE_WEATHER_BALL", "Weather Ball"),
        ("MOVE_AROMATHERAPY", "Aromatherapy"),
        ("MOVE_FAKE_TEARS", "Fake Tears"),
        ("MOVE_AIR_CUTTER", "Air Cutter"),
        ("MOVE_OVERHEAT", "Overheat"),
        ("MOVE_ODOR_SLEUTH", "Odor Sleuth"),
        ("MOVE_ROCK_TOMB", "Rock Tomb"),
        ("MOVE_SILVER_WIND", "Silver Wind"),
        ("MOVE_METAL_SOUND", "Metal Sound"),
        ("MOVE_GRASS_WHISTLE", "Grasswhistle"),
        ("MOVE_TICKLE", "Tickle"),
        ("MOVE_COSMIC_POWER", "Cosmic Power"),
        ("MOVE_WATER_SPOUT", "Water Spout"),
        ("MOVE_SIGNAL_BEAM", "Signal Beam"),
        ("MOVE_SHADOW_PUNCH", "Shadow Punch"),
        ("MOVE_EXTRASENSORY", "Extrasensory"),
        ("MOVE_SKY_UPPERCUT", "Sky Uppercut"),
        ("MOVE_SAND_TOMB", "Sand Tomb"),
        ("MOVE_SHEER_COLD", "Sheer Cold"),
        ("MOVE_MUDDY_WATER", "Muddy Water"),
        ("MOVE_BULLET_SEED", "Bullet Seed"),
        ("MOVE_AERIAL_ACE", "Aerial Ace"),
        ("MOVE_ICICLE_SPEAR", "Icicle Spear"),
        ("MOVE_IRON_DEFENSE", "Iron Defense"),
        ("MOVE_BLOCK", "Block"),
        ("MOVE_HOWL", "Howl"),
        ("MOVE_DRAGON_CLAW", "Dragon Claw"),
        ("MOVE_FRENZY_PLANT", "Frenzy Plant"),
        ("MOVE_BULK_UP", "Bulk Up"),
        ("MOVE_BOUNCE", "Bounce"),
        ("MOVE_MUD_SHOT", "Mud Shot"),
        ("MOVE_POISON_TAIL", "Poison Tail"),
        ("MOVE_COVET", "Covet"),
        ("MOVE_VOLT_TACKLE", "Volt Tackle"),
        ("MOVE_MAGICAL_LEAF", "Magical Leaf"),
        ("MOVE_WATER_SPORT", "Water Sport"),
        ("MOVE_CALM_MIND", "Calm Mind"),
        ("MOVE_LEAF_BLADE", "Leaf Blade"),
        ("MOVE_DRAGON_DANCE", "Dragon Dance"),
        ("MOVE_ROCK_BLAST", "Rock Blast"),
        ("MOVE_SHOCK_WAVE", "Shock Wave"),
        ("MOVE_WATER_PULSE", "Water Pulse"),
        ("MOVE_DOOM_DESIRE", "Doom Desire"),
        ("MOVE_PSYCHO_BOOST", "Psycho Boost")
    ]}


data = PokemonFRLGData()
_init()

LEGENDARY_POKEMON = frozenset([data.constants[species] for species in [
    "SPECIES_ARTICUNO",
    "SPECIES_ZAPDOS",
    "SPECIES_MOLTRES",
    "SPECIES_MEWTWO",
    "SPECIES_MEW",
    "SPECIES_RAIKOU",
    "SPECIES_ENTEI",
    "SPECIES_SUICUNE",
    "SPECIES_LUGIA",
    "SPECIES_HO_OH",
    "SPECIES_CELEBI",
    "SPECIES_REGIROCK",
    "SPECIES_REGICE",
    "SPECIES_REGISTEEL",
    "SPECIES_LATIAS",
    "SPECIES_LATIOS",
    "SPECIES_KYOGRE",
    "SPECIES_GROUDON",
    "SPECIES_RAYQUAZA",
    "SPECIES_JIRACHI",
    "SPECIES_DEOXYS",
]])
