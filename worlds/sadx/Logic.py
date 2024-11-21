from dataclasses import dataclass
from typing import Dict, Tuple, List, Union

from .Enums import Character, Area, SubLevel, LevelMission, pascal_to_space, SubLevelMission, EVERYONE, SONIC_TAILS
from .Names import ItemName, LocationName
from .Names.LocationName import Boss
from .Options import SonicAdventureDXOptions


@dataclass
class LevelLocation:
    locationId: int
    area: Area
    character: Character
    levelMission: LevelMission
    normalLogicItems: List[str]
    hardLogicItems: List[str]
    expertLogicItems: List[str]

    def get_level_name(self) -> str:
        return f"{pascal_to_space(self.area.name)} ({self.character.name} - Mission {self.levelMission.name})"

    def get_logic_items(self, options: SonicAdventureDXOptions) -> List[str]:
        if options.logic_level.value == 2:
            return self.expertLogicItems
        elif options.logic_level.value == 1:
            return self.hardLogicItems
        else:
            return self.normalLogicItems


@dataclass
class UpgradeLocation:
    locationId: int
    locationName: str
    area: Area
    character: Character
    normalLogicItems: List[str]
    hardLogicItems: List[str]
    expertLogicItems: List[str]

    def get_logic_items(self, options: SonicAdventureDXOptions) -> List[str]:
        if options.logic_level.value == 2:
            return self.expertLogicItems
        elif options.logic_level.value == 1:
            return self.hardLogicItems
        else:
            return self.normalLogicItems


@dataclass
class CharacterUpgrade:
    character: Character
    upgrade: str


@dataclass
class EmblemLocation:
    locationId: int
    area: Area
    normalLogicCharacters: List[Union[CharacterUpgrade, Character]]
    hardLogicCharacters: List[Union[CharacterUpgrade, Character]]
    expertLogicCharacters: List[Union[CharacterUpgrade, Character]]
    emblemName: str

    def get_logic_characters_upgrades(self, options: SonicAdventureDXOptions) -> (
            List)[Union[CharacterUpgrade, Character]]:
        if options.logic_level.value == 2:
            return self.expertLogicCharacters
        elif options.logic_level.value == 1:
            return self.hardLogicCharacters
        else:
            return self.normalLogicCharacters

    def get_logic_characters(self, options: SonicAdventureDXOptions) -> List[Character]:
        if options.logic_level.value == 2:
            return self._get_characters(self.expertLogicCharacters)
        elif options.logic_level.value == 1:
            return self._get_characters(self.hardLogicCharacters)
        else:
            return self._get_characters(self.normalLogicCharacters)

    @staticmethod
    def _get_characters(logic: List[Union[CharacterUpgrade, Character]]) -> List[Character]:
        return [item.character if isinstance(item, CharacterUpgrade) else item for item in logic]


@dataclass
class LifeCapsuleLocation:
    locationId: int
    area: Area
    character: Character
    lifeCapsuleNumber: int
    normalLogicItems: List[str]
    hardLogicItems: List[str]
    expertLogicItems: List[str]

    def get_logic_items(self, options: SonicAdventureDXOptions) -> List[str]:
        if options.logic_level.value == 2:
            return self.expertLogicItems
        elif options.logic_level.value == 1:
            return self.hardLogicItems
        else:
            return self.normalLogicItems


@dataclass
class MissionLocation:
    locationId: int
    cardArea: Area
    objectiveArea: Area
    character: Character
    missionNumber: int
    normalLogicItems: List[str]
    hardLogicItems: List[str]
    expertLogicItems: List[str]

    def get_mission_name(self) -> str:
        return f"Mission {self.missionNumber} ({self.character.name})"

    def get_logic_items(self, options: SonicAdventureDXOptions) -> List[str]:
        if options.logic_level.value == 2:
            return self.expertLogicItems
        elif options.logic_level.value == 1:
            return self.hardLogicItems
        else:
            return self.normalLogicItems


@dataclass
class SubLevelLocation:
    locationId: int
    area: Area
    characters: List[Character]
    subLevel: SubLevel
    subLevelMission: SubLevelMission


@dataclass
class BossFightLocation:
    locationId: int
    area: Area
    characters: List[Character]
    boss: Boss
    unified: bool


area_connections: Dict[Tuple[Character, Area, Area], Tuple[List[str], List[str], List[str]]] = {
    (Character.Sonic, Area.Hotel, Area.EmeraldCoast): ([], [], []),
    (Character.Sonic, Area.MysticRuinsMain, Area.WindyValley): (
        [ItemName.KeyItem.WindStone], [ItemName.KeyItem.WindStone], [ItemName.KeyItem.WindStone]),
    (Character.Sonic, Area.Casino, Area.Casinopolis): ([ItemName.Sonic.LightShoes], [ItemName.Sonic.LightShoes], []),
    (Character.Sonic, Area.AngelIsland, Area.IceCap): (
        [ItemName.KeyItem.IceStone, ItemName.KeyItem.CasinoKeys, ItemName.KeyItem.Train, ItemName.KeyItem.Dynamite],
        [ItemName.KeyItem.IceStone, ItemName.KeyItem.CasinoKeys, ItemName.KeyItem.Train, ItemName.KeyItem.Dynamite],
        [ItemName.KeyItem.IceStone, ItemName.KeyItem.CasinoKeys, ItemName.KeyItem.Train, ItemName.KeyItem.Dynamite]),
    (Character.Sonic, Area.TwinkleParkLobby, Area.TwinklePark): ([], [], []),
    (Character.Sonic, Area.StationSquareMain, Area.SpeedHighway): (
        [ItemName.KeyItem.EmployeeCard], [ItemName.KeyItem.EmployeeCard], []),
    (Character.Sonic, Area.AngelIsland, Area.RedMountain): (
        [ItemName.Sonic.LightShoes, ItemName.Sonic.AncientLight],
        [ItemName.Sonic.LightShoes, ItemName.Sonic.AncientLight],
        []),
    (Character.Sonic, Area.EggCarrierMain, Area.SkyDeck): ([], [], []),
    (Character.Sonic, Area.Jungle, Area.LostWorld): ([], [], []),
    (Character.Sonic, Area.Jungle, Area.FinalEgg): ([], [], []),
    (Character.Sonic, Area.EggCarrierMain, Area.HotShelter): ([], [], []),
    (Character.Tails, Area.Hotel, Area.EmeraldCoast): ([], [], []),
    (Character.Tails, Area.MysticRuinsMain, Area.WindyValley): (
        [ItemName.KeyItem.WindStone], [ItemName.KeyItem.WindStone], [ItemName.KeyItem.WindStone]),
    (Character.Tails, Area.Casino, Area.Casinopolis): ([], [], []),
    (Character.Tails, Area.AngelIsland, Area.IceCap): (
        [ItemName.KeyItem.IceStone, ItemName.KeyItem.CasinoKeys, ItemName.KeyItem.Train, ItemName.KeyItem.Dynamite],
        [ItemName.KeyItem.IceStone, ItemName.KeyItem.CasinoKeys, ItemName.KeyItem.Train, ItemName.KeyItem.Dynamite],
        [ItemName.KeyItem.IceStone, ItemName.KeyItem.CasinoKeys, ItemName.KeyItem.Train, ItemName.KeyItem.Dynamite]),
    (Character.Tails, Area.TwinkleParkLobby, Area.TwinklePark): ([], [], []),
    (Character.Tails, Area.StationSquareMain, Area.SpeedHighway): (
        [ItemName.KeyItem.EmployeeCard], [ItemName.KeyItem.EmployeeCard], [ItemName.KeyItem.EmployeeCard]),
    (Character.Tails, Area.AngelIsland, Area.RedMountain): ([], [], []),
    (Character.Tails, Area.EggCarrierMain, Area.SkyDeck): ([], [], []),
    (Character.Tails, Area.Jungle, Area.LostWorld): ([], [], []),
    (Character.Tails, Area.Jungle, Area.FinalEgg): ([], [], []),
    (Character.Tails, Area.EggCarrierMain, Area.HotShelter): ([], [], []),
    (Character.Knuckles, Area.Hotel, Area.EmeraldCoast): ([], [], []),
    (Character.Knuckles, Area.MysticRuinsMain, Area.WindyValley): (
        [ItemName.KeyItem.WindStone], [ItemName.KeyItem.WindStone], [ItemName.KeyItem.WindStone]),
    (Character.Knuckles, Area.Casino, Area.Casinopolis): ([], [], []),
    (Character.Knuckles, Area.AngelIsland, Area.IceCap): (
        [ItemName.KeyItem.IceStone, ItemName.KeyItem.Dynamite], [ItemName.KeyItem.IceStone, ItemName.KeyItem.Dynamite],
        [ItemName.KeyItem.IceStone, ItemName.KeyItem.Dynamite]),
    (Character.Knuckles, Area.TwinkleParkLobby, Area.TwinklePark): ([], [], []),
    (Character.Knuckles, Area.StationSquareMain, Area.SpeedHighway): ([], [], []),
    (Character.Knuckles, Area.AngelIsland, Area.RedMountain): (
        [ItemName.Knuckles.ShovelClaw, ItemName.KeyItem.Dynamite],
        [ItemName.Knuckles.ShovelClaw, ItemName.KeyItem.Dynamite],
        [ItemName.Knuckles.ShovelClaw, ItemName.KeyItem.Dynamite]),
    (Character.Knuckles, Area.EggCarrierMain, Area.SkyDeck): ([], [], []),
    (Character.Knuckles, Area.Jungle, Area.LostWorld): (
        [ItemName.Knuckles.ShovelClaw], [ItemName.Knuckles.ShovelClaw], []),
    (Character.Knuckles, Area.Jungle, Area.FinalEgg): ([], [], []),
    (Character.Knuckles, Area.EggCarrierMain, Area.HotShelter): ([], [], []),
    (Character.Amy, Area.Hotel, Area.EmeraldCoast): ([], [], []),
    (Character.Amy, Area.MysticRuinsMain, Area.WindyValley): (
        [ItemName.KeyItem.WindStone], [ItemName.KeyItem.WindStone], [ItemName.KeyItem.WindStone]),
    (Character.Amy, Area.Casino, Area.Casinopolis): ([], [], []),
    (Character.Amy, Area.AngelIsland, Area.IceCap): (
        [ItemName.KeyItem.IceStone, ItemName.KeyItem.Dynamite], [ItemName.KeyItem.IceStone, ItemName.KeyItem.Dynamite],
        [ItemName.KeyItem.IceStone, ItemName.KeyItem.Dynamite]),
    (Character.Amy, Area.TwinkleParkLobby, Area.TwinklePark): ([], [], []),
    (Character.Amy, Area.StationSquareMain, Area.SpeedHighway): (
        [ItemName.KeyItem.EmployeeCard], [ItemName.KeyItem.EmployeeCard], [ItemName.KeyItem.EmployeeCard]),
    (Character.Amy, Area.AngelIsland, Area.RedMountain): ([], [], []),
    (Character.Amy, Area.EggCarrierMain, Area.SkyDeck): ([], [], []),
    (Character.Amy, Area.Jungle, Area.LostWorld): ([], [], []),
    (Character.Amy, Area.Jungle, Area.FinalEgg): ([], [], []),
    (Character.Amy, Area.EggCarrierMain, Area.HotShelter): ([], [], []),
    (Character.Big, Area.Hotel, Area.EmeraldCoast): ([], [], []),
    (Character.Big, Area.MysticRuinsMain, Area.WindyValley): (
        [ItemName.KeyItem.WindStone], [ItemName.KeyItem.WindStone], [ItemName.KeyItem.WindStone]),
    (Character.Big, Area.Casino, Area.Casinopolis): ([], [], []),
    (Character.Big, Area.AngelIsland, Area.IceCap): (
        [ItemName.KeyItem.IceStone, ItemName.KeyItem.StationKeys, ItemName.KeyItem.Train, ItemName.KeyItem.Dynamite],
        [ItemName.KeyItem.IceStone, ItemName.KeyItem.StationKeys, ItemName.KeyItem.Train, ItemName.KeyItem.Dynamite],
        [ItemName.KeyItem.IceStone, ItemName.KeyItem.StationKeys, ItemName.KeyItem.Train, ItemName.KeyItem.Dynamite]),
    (Character.Big, Area.TwinkleParkLobby, Area.TwinklePark): ([], [], []),
    (Character.Big, Area.StationSquareMain, Area.SpeedHighway): (
        [ItemName.KeyItem.EmployeeCard], [ItemName.KeyItem.EmployeeCard], [ItemName.KeyItem.EmployeeCard]),
    (Character.Big, Area.AngelIsland, Area.RedMountain): ([], [], []),
    (Character.Big, Area.EggCarrierMain, Area.SkyDeck): ([], [], []),
    (Character.Big, Area.Jungle, Area.LostWorld): ([], [], []),
    (Character.Big, Area.Jungle, Area.FinalEgg): ([], [], []),
    (Character.Big, Area.EggCarrierMain, Area.HotShelter): ([], [], []),
    (Character.Gamma, Area.Hotel, Area.EmeraldCoast): ([], [], []),
    (Character.Gamma, Area.MysticRuinsMain, Area.WindyValley): (
        [ItemName.KeyItem.WindStone], [ItemName.KeyItem.WindStone], [ItemName.KeyItem.WindStone]),
    (Character.Gamma, Area.Casino, Area.Casinopolis): ([], [], []),
    (Character.Gamma, Area.AngelIsland, Area.IceCap): ([ItemName.KeyItem.IceStone,
                                                        ItemName.KeyItem.Dynamite], [ItemName.KeyItem.IceStone,
                                                                                     ItemName.KeyItem.Dynamite],
                                                       [ItemName.KeyItem.IceStone,
                                                        ItemName.KeyItem.Dynamite]),
    (Character.Gamma, Area.TwinkleParkLobby, Area.TwinklePark): ([], [], []),
    (Character.Gamma, Area.StationSquareMain, Area.SpeedHighway): (
        [ItemName.KeyItem.EmployeeCard], [ItemName.KeyItem.EmployeeCard], [ItemName.KeyItem.EmployeeCard]),
    (Character.Gamma, Area.AngelIsland, Area.RedMountain): ([], [], []),
    (Character.Gamma, Area.EggCarrierMain, Area.SkyDeck): ([], [], []),
    (Character.Gamma, Area.Jungle, Area.LostWorld): ([], [], []),
    (Character.Gamma, Area.Jungle, Area.FinalEgg): ([], [], []),
    (Character.Gamma, Area.EggCarrierMain, Area.HotShelter): ([], [], []),

    (Character.Sonic, Area.StationSquareMain, Area.Station): (
        [ItemName.KeyItem.StationKeys], [ItemName.KeyItem.StationKeys], []),
    (Character.Sonic, Area.Station, Area.StationSquareMain): (
        [ItemName.KeyItem.StationKeys], [ItemName.KeyItem.StationKeys], [ItemName.KeyItem.StationKeys]),
    (Character.Sonic, Area.StationSquareMain, Area.Hotel): (
        [ItemName.KeyItem.HotelKeys], [ItemName.KeyItem.HotelKeys], []),
    (Character.Sonic, Area.Hotel, Area.StationSquareMain): (
        [ItemName.KeyItem.HotelKeys], [ItemName.KeyItem.HotelKeys], [ItemName.KeyItem.HotelKeys]),
    (Character.Sonic, Area.Station, Area.Casino): ([ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys], []),
    (Character.Sonic, Area.Casino, Area.Station): (
        [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys]),
    (Character.Sonic, Area.Hotel, Area.Casino): (
        [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys]),
    (Character.Sonic, Area.Casino, Area.Hotel): (
        [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys]),
    (Character.Sonic, Area.StationSquareMain, Area.TwinkleParkLobby): (
        [ItemName.KeyItem.TwinkleParkTicket], [ItemName.KeyItem.TwinkleParkTicket],
        [ItemName.KeyItem.TwinkleParkTicket]),
    (Character.Sonic, Area.TwinkleParkLobby, Area.StationSquareMain): (
        [ItemName.KeyItem.TwinkleParkTicket], [ItemName.KeyItem.TwinkleParkTicket],
        [ItemName.KeyItem.TwinkleParkTicket]),
    (Character.Sonic, Area.MysticRuinsMain, Area.AngelIsland): (
        [ItemName.KeyItem.Dynamite], [ItemName.KeyItem.Dynamite], [ItemName.KeyItem.Dynamite]),
    (Character.Sonic, Area.AngelIsland, Area.MysticRuinsMain): (
        [ItemName.KeyItem.Dynamite], [ItemName.KeyItem.Dynamite], [ItemName.KeyItem.Dynamite]),
    (Character.Sonic, Area.MysticRuinsMain, Area.Jungle): (
        [ItemName.KeyItem.JungleCart], [ItemName.KeyItem.JungleCart], [ItemName.KeyItem.JungleCart]),
    (Character.Sonic, Area.Jungle, Area.MysticRuinsMain): (
        [ItemName.KeyItem.JungleCart], [ItemName.KeyItem.JungleCart], [ItemName.KeyItem.JungleCart]),
    (Character.Sonic, Area.Station, Area.MysticRuinsMain): (
        [ItemName.KeyItem.Train], [ItemName.KeyItem.Train], [ItemName.KeyItem.Train]),
    (Character.Sonic, Area.MysticRuinsMain, Area.Station): (
        [ItemName.KeyItem.Train], [ItemName.KeyItem.Train], [ItemName.KeyItem.Train]),
    (Character.Sonic, Area.StationSquareMain, Area.EggCarrierMain): (
        [ItemName.KeyItem.Boat], [ItemName.KeyItem.Boat], [ItemName.KeyItem.Boat]),
    (Character.Sonic, Area.EggCarrierMain, Area.StationSquareMain): (
        [ItemName.KeyItem.Boat], [ItemName.KeyItem.Boat], [ItemName.KeyItem.Boat]),
    (Character.Sonic, Area.MysticRuinsMain, Area.EggCarrierMain): (
        [ItemName.KeyItem.Raft], [ItemName.KeyItem.Raft], [ItemName.KeyItem.Raft]),
    (Character.Sonic, Area.EggCarrierMain, Area.MysticRuinsMain): (
        [ItemName.KeyItem.Raft], [ItemName.KeyItem.Raft], [ItemName.KeyItem.Raft]),
    (Character.Tails, Area.StationSquareMain, Area.Station): (
        [ItemName.KeyItem.StationKeys], [ItemName.KeyItem.StationKeys], [ItemName.KeyItem.StationKeys]),
    (Character.Tails, Area.Station, Area.StationSquareMain): (
        [ItemName.KeyItem.StationKeys], [ItemName.KeyItem.StationKeys], [ItemName.KeyItem.StationKeys]),
    (Character.Tails, Area.StationSquareMain, Area.Hotel): (
        [ItemName.KeyItem.HotelKeys], [ItemName.KeyItem.HotelKeys], []),
    (Character.Tails, Area.Hotel, Area.StationSquareMain): (
        [ItemName.KeyItem.HotelKeys], [ItemName.KeyItem.HotelKeys], [ItemName.KeyItem.HotelKeys]),
    (Character.Tails, Area.Station, Area.Casino): (
        [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys]),
    (Character.Tails, Area.Casino, Area.Station): ([ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys], []),
    (Character.Tails, Area.Hotel, Area.Casino): (
        [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys]),
    (Character.Tails, Area.Casino, Area.Hotel): (
        [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys]),
    (Character.Tails, Area.StationSquareMain, Area.TwinkleParkLobby): (
        [ItemName.KeyItem.TwinkleParkTicket], [ItemName.KeyItem.TwinkleParkTicket],
        [ItemName.KeyItem.TwinkleParkTicket]),
    (Character.Tails, Area.TwinkleParkLobby, Area.StationSquareMain): (
        [ItemName.KeyItem.TwinkleParkTicket], [ItemName.KeyItem.TwinkleParkTicket],
        [ItemName.KeyItem.TwinkleParkTicket]),
    (Character.Tails, Area.MysticRuinsMain, Area.AngelIsland): (
        [ItemName.KeyItem.Dynamite], [ItemName.KeyItem.Dynamite], [ItemName.KeyItem.Dynamite]),
    (Character.Tails, Area.AngelIsland, Area.MysticRuinsMain): (
        [ItemName.KeyItem.Dynamite], [ItemName.KeyItem.Dynamite], [ItemName.KeyItem.Dynamite]),
    (Character.Tails, Area.MysticRuinsMain, Area.Jungle): (
        [ItemName.KeyItem.JungleCart], [ItemName.KeyItem.JungleCart], [ItemName.KeyItem.JungleCart]),
    (Character.Tails, Area.Jungle, Area.MysticRuinsMain): (
        [ItemName.KeyItem.JungleCart], [ItemName.KeyItem.JungleCart], [ItemName.KeyItem.JungleCart]),
    (Character.Tails, Area.Station, Area.MysticRuinsMain): (
        [ItemName.KeyItem.Train], [ItemName.KeyItem.Train], [ItemName.KeyItem.Train]),
    (Character.Tails, Area.MysticRuinsMain, Area.Station): (
        [ItemName.KeyItem.Train], [ItemName.KeyItem.Train], [ItemName.KeyItem.Train]),
    (Character.Tails, Area.StationSquareMain, Area.EggCarrierMain): (
        [ItemName.KeyItem.Boat], [ItemName.KeyItem.Boat], [ItemName.KeyItem.Boat]),
    (Character.Tails, Area.EggCarrierMain, Area.StationSquareMain): (
        [ItemName.KeyItem.Boat], [ItemName.KeyItem.Boat], [ItemName.KeyItem.Boat]),
    (Character.Tails, Area.MysticRuinsMain, Area.EggCarrierMain): (
        [ItemName.KeyItem.Raft], [ItemName.KeyItem.Raft], [ItemName.KeyItem.Raft]),
    (Character.Tails, Area.EggCarrierMain, Area.MysticRuinsMain): (
        [ItemName.KeyItem.Raft], [ItemName.KeyItem.Raft], [ItemName.KeyItem.Raft]),
    (Character.Knuckles, Area.StationSquareMain, Area.Station): (
        [ItemName.KeyItem.StationKeys], [ItemName.KeyItem.StationKeys], [ItemName.KeyItem.StationKeys]),
    (Character.Knuckles, Area.Station, Area.StationSquareMain): (
        [ItemName.KeyItem.StationKeys], [ItemName.KeyItem.StationKeys], [ItemName.KeyItem.StationKeys]),
    (Character.Knuckles, Area.StationSquareMain, Area.Hotel): (
        [ItemName.KeyItem.HotelKeys], [ItemName.KeyItem.HotelKeys], [ItemName.KeyItem.HotelKeys]),
    (Character.Knuckles, Area.Hotel, Area.StationSquareMain): (
        [ItemName.KeyItem.HotelKeys], [ItemName.KeyItem.HotelKeys], [ItemName.KeyItem.HotelKeys]),
    (Character.Knuckles, Area.Station, Area.Casino): (
        [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys]),
    (Character.Knuckles, Area.Casino, Area.Station): (
        [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys]),
    (Character.Knuckles, Area.Hotel, Area.Casino): (
        [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys]),
    (Character.Knuckles, Area.Casino, Area.Hotel): (
        [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys]),
    (Character.Knuckles, Area.StationSquareMain, Area.TwinkleParkLobby): (
        [ItemName.KeyItem.TwinkleParkTicket], [ItemName.KeyItem.TwinkleParkTicket],
        [ItemName.KeyItem.TwinkleParkTicket]),
    (Character.Knuckles, Area.TwinkleParkLobby, Area.StationSquareMain): (
        [ItemName.KeyItem.TwinkleParkTicket], [ItemName.KeyItem.TwinkleParkTicket], []),
    (Character.Knuckles, Area.MysticRuinsMain, Area.AngelIsland): (
        [ItemName.KeyItem.Dynamite], [ItemName.KeyItem.Dynamite], [ItemName.KeyItem.Dynamite]),
    (Character.Knuckles, Area.AngelIsland, Area.MysticRuinsMain): (
        [ItemName.KeyItem.Dynamite], [ItemName.KeyItem.Dynamite], [ItemName.KeyItem.Dynamite]),
    (Character.Knuckles, Area.MysticRuinsMain, Area.Jungle): (
        [ItemName.KeyItem.JungleCart], [ItemName.KeyItem.JungleCart], [ItemName.KeyItem.JungleCart]),
    (Character.Knuckles, Area.Jungle, Area.MysticRuinsMain): (
        [ItemName.KeyItem.JungleCart], [ItemName.KeyItem.JungleCart], [ItemName.KeyItem.JungleCart]),
    (Character.Knuckles, Area.Station, Area.MysticRuinsMain): (
        [ItemName.KeyItem.Train], [ItemName.KeyItem.Train], [ItemName.KeyItem.Train]),
    (Character.Knuckles, Area.MysticRuinsMain, Area.Station): (
        [ItemName.KeyItem.Train], [ItemName.KeyItem.Train], [ItemName.KeyItem.Train]),
    (Character.Knuckles, Area.StationSquareMain, Area.EggCarrierMain): (
        [ItemName.KeyItem.Boat], [ItemName.KeyItem.Boat], [ItemName.KeyItem.Boat]),
    (Character.Knuckles, Area.EggCarrierMain, Area.StationSquareMain): (
        [ItemName.KeyItem.Boat], [ItemName.KeyItem.Boat], [ItemName.KeyItem.Boat]),
    (Character.Knuckles, Area.MysticRuinsMain, Area.EggCarrierMain): (
        [ItemName.KeyItem.Raft], [ItemName.KeyItem.Raft], [ItemName.KeyItem.Raft]),
    (Character.Knuckles, Area.EggCarrierMain, Area.MysticRuinsMain): (
        [ItemName.KeyItem.Raft], [ItemName.KeyItem.Raft], [ItemName.KeyItem.Raft]),
    (Character.Amy, Area.StationSquareMain, Area.Station): (
        [ItemName.KeyItem.StationKeys], [ItemName.KeyItem.StationKeys], [ItemName.KeyItem.StationKeys]),
    (Character.Amy, Area.Station, Area.StationSquareMain): (
        [ItemName.KeyItem.StationKeys], [ItemName.KeyItem.StationKeys], [ItemName.KeyItem.StationKeys]),
    (Character.Amy, Area.StationSquareMain, Area.Hotel): (
        [ItemName.KeyItem.HotelKeys], [ItemName.KeyItem.HotelKeys], [ItemName.KeyItem.HotelKeys]),
    (Character.Amy, Area.Hotel, Area.StationSquareMain): (
        [ItemName.KeyItem.HotelKeys], [ItemName.KeyItem.HotelKeys], [ItemName.KeyItem.HotelKeys]),
    (Character.Amy, Area.Station, Area.Casino): (
        [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys]),
    (Character.Amy, Area.Casino, Area.Station): (
        [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys]),
    (Character.Amy, Area.Hotel, Area.Casino): (
        [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys]),
    (Character.Amy, Area.Casino, Area.Hotel): (
        [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys]),
    (Character.Amy, Area.StationSquareMain, Area.TwinkleParkLobby): (
        [ItemName.KeyItem.TwinkleParkTicket], [ItemName.KeyItem.TwinkleParkTicket],
        [ItemName.KeyItem.TwinkleParkTicket]),
    (Character.Amy, Area.TwinkleParkLobby, Area.StationSquareMain): (
        [ItemName.KeyItem.TwinkleParkTicket], [ItemName.KeyItem.TwinkleParkTicket], []),
    (Character.Amy, Area.MysticRuinsMain, Area.AngelIsland): (
        [ItemName.KeyItem.Dynamite], [ItemName.KeyItem.Dynamite], [ItemName.KeyItem.Dynamite]),
    (Character.Amy, Area.AngelIsland, Area.MysticRuinsMain): (
        [ItemName.KeyItem.Dynamite], [ItemName.KeyItem.Dynamite], [ItemName.KeyItem.Dynamite]),
    (Character.Amy, Area.MysticRuinsMain, Area.Jungle): (
        [ItemName.KeyItem.JungleCart], [ItemName.KeyItem.JungleCart], [ItemName.KeyItem.JungleCart]),
    (Character.Amy, Area.Jungle, Area.MysticRuinsMain): (
        [ItemName.KeyItem.JungleCart], [ItemName.KeyItem.JungleCart], [ItemName.KeyItem.JungleCart]),
    (Character.Amy, Area.Station, Area.MysticRuinsMain): (
        [ItemName.KeyItem.Train], [ItemName.KeyItem.Train], [ItemName.KeyItem.Train]),
    (Character.Amy, Area.MysticRuinsMain, Area.Station): (
        [ItemName.KeyItem.Train], [ItemName.KeyItem.Train], [ItemName.KeyItem.Train]),
    (Character.Amy, Area.StationSquareMain, Area.EggCarrierMain): (
        [ItemName.KeyItem.Boat], [ItemName.KeyItem.Boat], [ItemName.KeyItem.Boat]),
    (Character.Amy, Area.EggCarrierMain, Area.StationSquareMain): (
        [ItemName.KeyItem.Boat], [ItemName.KeyItem.Boat], [ItemName.KeyItem.Boat]),
    (Character.Amy, Area.MysticRuinsMain, Area.EggCarrierMain): (
        [ItemName.KeyItem.Raft], [ItemName.KeyItem.Raft], [ItemName.KeyItem.Raft]),
    (Character.Amy, Area.EggCarrierMain, Area.MysticRuinsMain): (
        [ItemName.KeyItem.Raft], [ItemName.KeyItem.Raft], [ItemName.KeyItem.Raft]),
    (Character.Big, Area.StationSquareMain, Area.Station): (
        [ItemName.KeyItem.StationKeys], [ItemName.KeyItem.StationKeys], [ItemName.KeyItem.StationKeys]),
    (Character.Big, Area.Station, Area.StationSquareMain): (
        [ItemName.KeyItem.StationKeys], [ItemName.KeyItem.StationKeys], [ItemName.KeyItem.StationKeys]),
    (Character.Big, Area.StationSquareMain, Area.Hotel): (
        [ItemName.KeyItem.HotelKeys], [ItemName.KeyItem.HotelKeys], [ItemName.KeyItem.HotelKeys]),
    (Character.Big, Area.Hotel, Area.StationSquareMain): (
        [ItemName.KeyItem.HotelKeys], [ItemName.KeyItem.HotelKeys], [ItemName.KeyItem.HotelKeys]),
    (Character.Big, Area.Station, Area.Casino): (
        [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys]),
    (Character.Big, Area.Casino, Area.Station): (
        [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys]),
    (Character.Big, Area.Hotel, Area.Casino): (
        [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys]),
    (Character.Big, Area.Casino, Area.Hotel): (
        [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys]),
    (Character.Big, Area.StationSquareMain, Area.TwinkleParkLobby): ([], [], []),
    (Character.Big, Area.TwinkleParkLobby, Area.StationSquareMain): (
        [ItemName.KeyItem.TwinkleParkTicket], [ItemName.KeyItem.TwinkleParkTicket], []),
    (Character.Big, Area.MysticRuinsMain, Area.AngelIsland): (
        [ItemName.KeyItem.Dynamite], [ItemName.KeyItem.Dynamite], [ItemName.KeyItem.Dynamite]),
    (Character.Big, Area.AngelIsland, Area.MysticRuinsMain): (
        [ItemName.KeyItem.Dynamite], [ItemName.KeyItem.Dynamite], [ItemName.KeyItem.Dynamite]),
    (Character.Big, Area.MysticRuinsMain, Area.Jungle): (
        [ItemName.KeyItem.JungleCart], [ItemName.KeyItem.JungleCart], [ItemName.KeyItem.JungleCart]),
    (Character.Big, Area.Jungle, Area.MysticRuinsMain): (
        [ItemName.KeyItem.JungleCart], [ItemName.KeyItem.JungleCart], [ItemName.KeyItem.JungleCart]),
    (Character.Big, Area.Station, Area.MysticRuinsMain): (
        [ItemName.KeyItem.Train], [ItemName.KeyItem.Train], [ItemName.KeyItem.Train]),
    (Character.Big, Area.MysticRuinsMain, Area.Station): (
        [ItemName.KeyItem.Train], [ItemName.KeyItem.Train], [ItemName.KeyItem.Train]),
    (Character.Big, Area.StationSquareMain, Area.EggCarrierMain): (
        [ItemName.KeyItem.Boat], [ItemName.KeyItem.Boat], [ItemName.KeyItem.Boat]),
    (Character.Big, Area.EggCarrierMain, Area.StationSquareMain): (
        [ItemName.KeyItem.Boat], [ItemName.KeyItem.Boat], [ItemName.KeyItem.Boat]),
    (Character.Big, Area.MysticRuinsMain, Area.EggCarrierMain): (
        [ItemName.KeyItem.Raft], [ItemName.KeyItem.Raft], [ItemName.KeyItem.Raft]),
    (Character.Big, Area.EggCarrierMain, Area.MysticRuinsMain): (
        [ItemName.KeyItem.Raft], [ItemName.KeyItem.Raft], [ItemName.KeyItem.Raft]),
    (Character.Gamma, Area.StationSquareMain, Area.Station): (
        [ItemName.KeyItem.StationKeys], [ItemName.KeyItem.StationKeys], [ItemName.KeyItem.StationKeys]),
    (Character.Gamma, Area.Station, Area.StationSquareMain): (
        [ItemName.KeyItem.StationKeys], [ItemName.KeyItem.StationKeys], [ItemName.KeyItem.StationKeys]),
    (Character.Gamma, Area.StationSquareMain, Area.Hotel): (
        [ItemName.KeyItem.HotelKeys], [ItemName.KeyItem.HotelKeys], [ItemName.KeyItem.HotelKeys]),
    (Character.Gamma, Area.Hotel, Area.StationSquareMain): (
        [ItemName.KeyItem.HotelKeys], [ItemName.KeyItem.HotelKeys], [ItemName.KeyItem.HotelKeys]),
    (Character.Gamma, Area.Station, Area.Casino): (
        [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys]),
    (Character.Gamma, Area.Casino, Area.Station): (
        [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys]),
    (Character.Gamma, Area.Hotel, Area.Casino): (
        [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys]),
    (Character.Gamma, Area.Casino, Area.Hotel): (
        [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys], [ItemName.KeyItem.CasinoKeys]),
    (Character.Gamma, Area.StationSquareMain, Area.TwinkleParkLobby): (
        [ItemName.KeyItem.TwinkleParkTicket], [ItemName.KeyItem.TwinkleParkTicket],
        [ItemName.KeyItem.TwinkleParkTicket]),
    (Character.Gamma, Area.TwinkleParkLobby, Area.StationSquareMain): (
        [ItemName.KeyItem.TwinkleParkTicket], [ItemName.KeyItem.TwinkleParkTicket], []),
    (Character.Gamma, Area.MysticRuinsMain, Area.AngelIsland): (
        [ItemName.KeyItem.Dynamite], [ItemName.KeyItem.Dynamite], [ItemName.KeyItem.Dynamite]),
    (Character.Gamma, Area.AngelIsland, Area.MysticRuinsMain): (
        [ItemName.KeyItem.Dynamite], [ItemName.KeyItem.Dynamite], [ItemName.KeyItem.Dynamite]),
    (Character.Gamma, Area.MysticRuinsMain, Area.Jungle): (
        [ItemName.KeyItem.JungleCart], [ItemName.KeyItem.JungleCart], [ItemName.KeyItem.JungleCart]),
    (Character.Gamma, Area.Jungle, Area.MysticRuinsMain): (
        [ItemName.KeyItem.JungleCart], [ItemName.KeyItem.JungleCart], [ItemName.KeyItem.JungleCart]),
    (Character.Gamma, Area.Station, Area.MysticRuinsMain): (
        [ItemName.KeyItem.Train], [ItemName.KeyItem.Train], [ItemName.KeyItem.Train]),
    (Character.Gamma, Area.MysticRuinsMain, Area.Station): (
        [ItemName.KeyItem.Train], [ItemName.KeyItem.Train], [ItemName.KeyItem.Train]),
    (Character.Gamma, Area.StationSquareMain, Area.EggCarrierMain): (
        [ItemName.KeyItem.Boat], [ItemName.KeyItem.Boat], [ItemName.KeyItem.Boat]),
    (Character.Gamma, Area.EggCarrierMain, Area.StationSquareMain): (
        [ItemName.KeyItem.Boat], [ItemName.KeyItem.Boat], [ItemName.KeyItem.Boat]),
    (Character.Gamma, Area.MysticRuinsMain, Area.EggCarrierMain): (
        [ItemName.KeyItem.Raft], [ItemName.KeyItem.Raft], [ItemName.KeyItem.Raft]),
    (Character.Gamma, Area.EggCarrierMain, Area.MysticRuinsMain): (
        [ItemName.KeyItem.Raft], [ItemName.KeyItem.Raft], [ItemName.KeyItem.Raft]),
}

level_location_table: List[LevelLocation] = [
    LevelLocation(6002, Area.TwinklePark, Character.Big, LevelMission.C, [], [], []),
    LevelLocation(6001, Area.TwinklePark, Character.Big, LevelMission.B,
                  [ItemName.Big.Lure1, ItemName.Big.Lure2, ItemName.Big.Lure3, ItemName.Big.Lure4], [], []),
    LevelLocation(6000, Area.TwinklePark, Character.Big, LevelMission.A,
                  [ItemName.Big.Lure1, ItemName.Big.Lure2, ItemName.Big.Lure3, ItemName.Big.Lure4],
                  [ItemName.Big.Lure1, ItemName.Big.Lure2, ItemName.Big.Lure3, ItemName.Big.Lure4],
                  [ItemName.Big.Lure1, ItemName.Big.Lure2, ItemName.Big.Lure3, ItemName.Big.Lure4]),
    LevelLocation(3002, Area.SpeedHighway, Character.Knuckles, LevelMission.C, [], [], []),
    LevelLocation(3001, Area.SpeedHighway, Character.Knuckles, LevelMission.B, [], [], []),
    LevelLocation(3000, Area.SpeedHighway, Character.Knuckles, LevelMission.A, [], [], []),
    LevelLocation(1002, Area.EmeraldCoast, Character.Sonic, LevelMission.C, [], [], []),
    LevelLocation(1001, Area.EmeraldCoast, Character.Sonic, LevelMission.B, [], [], []),
    LevelLocation(1000, Area.EmeraldCoast, Character.Sonic, LevelMission.A, [], [], []),
    LevelLocation(6202, Area.EmeraldCoast, Character.Big, LevelMission.C, [], [], []),
    LevelLocation(6201, Area.EmeraldCoast, Character.Big, LevelMission.B,
                  [ItemName.Big.Lure1, ItemName.Big.Lure2, ItemName.Big.Lure3, ItemName.Big.Lure4], [], []),
    LevelLocation(6200, Area.EmeraldCoast, Character.Big, LevelMission.A,
                  [ItemName.Big.Lure1, ItemName.Big.Lure2, ItemName.Big.Lure3, ItemName.Big.Lure4],
                  [ItemName.Big.Lure1, ItemName.Big.Lure2, ItemName.Big.Lure3, ItemName.Big.Lure4],
                  [ItemName.Big.Lure1, ItemName.Big.Lure2, ItemName.Big.Lure3, ItemName.Big.Lure4]),
    LevelLocation(5102, Area.EmeraldCoast, Character.Gamma, LevelMission.C, [], [], []),
    LevelLocation(5101, Area.EmeraldCoast, Character.Gamma, LevelMission.B, [], [], []),
    LevelLocation(5100, Area.EmeraldCoast, Character.Gamma, LevelMission.A, [], [], []),
    LevelLocation(1202, Area.Casinopolis, Character.Sonic, LevelMission.C, [], [], []),
    LevelLocation(1201, Area.Casinopolis, Character.Sonic, LevelMission.B, [], [], []),
    LevelLocation(1200, Area.Casinopolis, Character.Sonic, LevelMission.A, [], [], []),
    LevelLocation(2102, Area.Casinopolis, Character.Tails, LevelMission.C, [], [], []),
    LevelLocation(2101, Area.Casinopolis, Character.Tails, LevelMission.B, [], [], []),
    LevelLocation(2100, Area.Casinopolis, Character.Tails, LevelMission.A, [ItemName.Tails.JetAnklet], [], []),
    LevelLocation(3102, Area.Casinopolis, Character.Knuckles, LevelMission.C, [], [], []),
    LevelLocation(3101, Area.Casinopolis, Character.Knuckles, LevelMission.B, [], [], []),
    LevelLocation(3100, Area.Casinopolis, Character.Knuckles, LevelMission.A, [], [], []),
    LevelLocation(1402, Area.TwinklePark, Character.Sonic, LevelMission.C, [], [], []),
    LevelLocation(1401, Area.TwinklePark, Character.Sonic, LevelMission.B, [], [], []),
    LevelLocation(1400, Area.TwinklePark, Character.Sonic, LevelMission.A, [], [], []),
    LevelLocation(4002, Area.TwinklePark, Character.Amy, LevelMission.C, [], [], []),
    LevelLocation(4001, Area.TwinklePark, Character.Amy, LevelMission.B, [], [], []),
    LevelLocation(4000, Area.TwinklePark, Character.Amy, LevelMission.A, [], [], []),
    LevelLocation(1502, Area.SpeedHighway, Character.Sonic, LevelMission.C, [], [], []),
    LevelLocation(1501, Area.SpeedHighway, Character.Sonic, LevelMission.B, [], [], []),
    LevelLocation(1500, Area.SpeedHighway, Character.Sonic, LevelMission.A, [], [], []),
    LevelLocation(2402, Area.SpeedHighway, Character.Tails, LevelMission.C, [], [], []),
    LevelLocation(2401, Area.SpeedHighway, Character.Tails, LevelMission.B, [], [], []),
    LevelLocation(2400, Area.SpeedHighway, Character.Tails, LevelMission.A, [ItemName.Tails.JetAnklet], [], []),
    LevelLocation(1102, Area.WindyValley, Character.Sonic, LevelMission.C, [], [], []),
    LevelLocation(1101, Area.WindyValley, Character.Sonic, LevelMission.B, [], [], []),
    LevelLocation(1100, Area.WindyValley, Character.Sonic, LevelMission.A, [], [], []),
    LevelLocation(2002, Area.WindyValley, Character.Tails, LevelMission.C, [], [], []),
    LevelLocation(2001, Area.WindyValley, Character.Tails, LevelMission.B, [], [], []),
    LevelLocation(2000, Area.WindyValley, Character.Tails, LevelMission.A, [ItemName.Tails.JetAnklet], [], []),
    LevelLocation(5202, Area.WindyValley, Character.Gamma, LevelMission.C, [ItemName.Gamma.JetBooster],
                  [ItemName.Gamma.JetBooster], []),
    LevelLocation(5201, Area.WindyValley, Character.Gamma, LevelMission.B, [ItemName.Gamma.JetBooster],
                  [ItemName.Gamma.JetBooster], []),
    LevelLocation(5200, Area.WindyValley, Character.Gamma, LevelMission.A, [ItemName.Gamma.JetBooster],
                  [ItemName.Gamma.JetBooster], []),
    LevelLocation(1302, Area.IceCap, Character.Sonic, LevelMission.C, [], [], []),
    LevelLocation(1301, Area.IceCap, Character.Sonic, LevelMission.B, [], [], []),
    LevelLocation(1300, Area.IceCap, Character.Sonic, LevelMission.A, [], [], []),
    LevelLocation(2202, Area.IceCap, Character.Tails, LevelMission.C, [], [], []),
    LevelLocation(2201, Area.IceCap, Character.Tails, LevelMission.B, [], [], []),
    LevelLocation(2200, Area.IceCap, Character.Tails, LevelMission.A, [], [], []),
    LevelLocation(6102, Area.IceCap, Character.Big, LevelMission.C, [], [], []),
    LevelLocation(6101, Area.IceCap, Character.Big, LevelMission.B,
                  [ItemName.Big.Lure1, ItemName.Big.Lure2, ItemName.Big.Lure3, ItemName.Big.Lure4], [], []),
    LevelLocation(6100, Area.IceCap, Character.Big, LevelMission.A,
                  [ItemName.Big.Lure1, ItemName.Big.Lure2, ItemName.Big.Lure3, ItemName.Big.Lure4],
                  [ItemName.Big.Lure1, ItemName.Big.Lure2, ItemName.Big.Lure3, ItemName.Big.Lure4],
                  [ItemName.Big.Lure1, ItemName.Big.Lure2, ItemName.Big.Lure3, ItemName.Big.Lure4]),
    LevelLocation(1602, Area.RedMountain, Character.Sonic, LevelMission.C, [], [], []),
    LevelLocation(1601, Area.RedMountain, Character.Sonic, LevelMission.B, [], [], []),
    LevelLocation(1600, Area.RedMountain, Character.Sonic, LevelMission.A, [], [], []),
    LevelLocation(3202, Area.RedMountain, Character.Knuckles, LevelMission.C, [ItemName.Knuckles.ShovelClaw], [], []),
    LevelLocation(3201, Area.RedMountain, Character.Knuckles, LevelMission.B, [ItemName.Knuckles.ShovelClaw], [], []),
    LevelLocation(3200, Area.RedMountain, Character.Knuckles, LevelMission.A, [ItemName.Knuckles.ShovelClaw], [], []),
    LevelLocation(5302, Area.RedMountain, Character.Gamma, LevelMission.C, [], [], []),
    LevelLocation(5301, Area.RedMountain, Character.Gamma, LevelMission.B, [], [], []),
    LevelLocation(5300, Area.RedMountain, Character.Gamma, LevelMission.A, [], [], []),
    LevelLocation(1802, Area.LostWorld, Character.Sonic, LevelMission.C, [ItemName.Sonic.LightShoes], [], []),
    LevelLocation(1801, Area.LostWorld, Character.Sonic, LevelMission.B, [ItemName.Sonic.LightShoes], [], []),
    LevelLocation(1800, Area.LostWorld, Character.Sonic, LevelMission.A, [ItemName.Sonic.LightShoes], [], []),
    LevelLocation(3302, Area.LostWorld, Character.Knuckles, LevelMission.C, [ItemName.Knuckles.ShovelClaw], [], []),
    LevelLocation(3301, Area.LostWorld, Character.Knuckles, LevelMission.B, [ItemName.Knuckles.ShovelClaw], [], []),
    LevelLocation(3300, Area.LostWorld, Character.Knuckles, LevelMission.A, [ItemName.Knuckles.ShovelClaw], [], []),
    LevelLocation(1902, Area.FinalEgg, Character.Sonic, LevelMission.C, [ItemName.Sonic.LightShoes], [], []),
    LevelLocation(1901, Area.FinalEgg, Character.Sonic, LevelMission.B, [ItemName.Sonic.LightShoes], [], []),
    LevelLocation(1900, Area.FinalEgg, Character.Sonic, LevelMission.A, [ItemName.Sonic.LightShoes], [], []),
    LevelLocation(4202, Area.FinalEgg, Character.Amy, LevelMission.C, [], [], []),
    LevelLocation(4201, Area.FinalEgg, Character.Amy, LevelMission.B, [], [], []),
    LevelLocation(4200, Area.FinalEgg, Character.Amy, LevelMission.A, [], [], []),
    LevelLocation(5002, Area.FinalEgg, Character.Gamma, LevelMission.C, [], [], []),
    LevelLocation(5001, Area.FinalEgg, Character.Gamma, LevelMission.B, [], [], []),
    LevelLocation(5000, Area.FinalEgg, Character.Gamma, LevelMission.A, [], [], []),
    LevelLocation(1702, Area.SkyDeck, Character.Sonic, LevelMission.C, [], [], []),
    LevelLocation(1701, Area.SkyDeck, Character.Sonic, LevelMission.B, [], [], []),
    LevelLocation(1700, Area.SkyDeck, Character.Sonic, LevelMission.A, [], [], []),
    LevelLocation(2302, Area.SkyDeck, Character.Tails, LevelMission.C, [], [], []),
    LevelLocation(2301, Area.SkyDeck, Character.Tails, LevelMission.B, [], [], []),
    LevelLocation(2300, Area.SkyDeck, Character.Tails, LevelMission.A, [ItemName.Tails.JetAnklet], [], []),
    LevelLocation(3402, Area.SkyDeck, Character.Knuckles, LevelMission.C, [ItemName.Knuckles.ShovelClaw], [], []),
    LevelLocation(3401, Area.SkyDeck, Character.Knuckles, LevelMission.B, [ItemName.Knuckles.ShovelClaw], [], []),
    LevelLocation(3400, Area.SkyDeck, Character.Knuckles, LevelMission.A, [ItemName.Knuckles.ShovelClaw], [], []),
    LevelLocation(4102, Area.HotShelter, Character.Amy, LevelMission.C, [], [], []),
    LevelLocation(4101, Area.HotShelter, Character.Amy, LevelMission.B, [], [], []),
    LevelLocation(4100, Area.HotShelter, Character.Amy, LevelMission.A, [], [], []),
    LevelLocation(6302, Area.HotShelter, Character.Big, LevelMission.C, [], [], []),
    LevelLocation(6301, Area.HotShelter, Character.Big, LevelMission.B,
                  [ItemName.Big.Lure1, ItemName.Big.Lure2, ItemName.Big.Lure3, ItemName.Big.Lure4], [], []),
    LevelLocation(6300, Area.HotShelter, Character.Big, LevelMission.A,
                  [ItemName.Big.Lure1, ItemName.Big.Lure2, ItemName.Big.Lure3, ItemName.Big.Lure4],
                  [ItemName.Big.Lure1, ItemName.Big.Lure2, ItemName.Big.Lure3, ItemName.Big.Lure4], []),
    LevelLocation(5402, Area.HotShelter, Character.Gamma, LevelMission.C, [ItemName.Gamma.JetBooster], [], []),
    LevelLocation(5401, Area.HotShelter, Character.Gamma, LevelMission.B, [ItemName.Gamma.JetBooster], [], []),
    LevelLocation(5400, Area.HotShelter, Character.Gamma, LevelMission.A, [ItemName.Gamma.JetBooster], [], []),
]

upgrade_location_table: List[UpgradeLocation] = [
    UpgradeLocation(100, LocationName.Sonic.LightShoes, Area.StationSquareMain, Character.Sonic, [], [], []),
    UpgradeLocation(200, LocationName.Tails.JetAnklet, Area.StationSquareMain, Character.Tails, [], [], []),
    UpgradeLocation(602, LocationName.Big.Lure1, Area.StationSquareMain, Character.Big, [], [], []),
    UpgradeLocation(101, LocationName.Sonic.CrystalRing, Area.Hotel, Character.Sonic, [ItemName.Sonic.LightShoes],
                    [ItemName.Sonic.LightShoes], []),
    UpgradeLocation(300, LocationName.Knuckles.ShovelClaw, Area.MysticRuinsMain, Character.Knuckles, [], [], []),
    UpgradeLocation(604, LocationName.Big.Lure3, Area.IceCap, Character.Big, [], [], []),
    UpgradeLocation(600, LocationName.Big.LifeBelt, Area.AngelIsland, Character.Big,
                    [ItemName.KeyItem.IceStone, ItemName.KeyItem.StationKeys, ItemName.KeyItem.Train],
                    [ItemName.KeyItem.IceStone, ItemName.KeyItem.StationKeys, ItemName.KeyItem.Train],
                    [ItemName.KeyItem.IceStone, ItemName.KeyItem.StationKeys, ItemName.KeyItem.Train]),
    UpgradeLocation(102, LocationName.Sonic.AncientLight, Area.AngelIsland, Character.Sonic, [], [], []),
    UpgradeLocation(301, LocationName.Knuckles.FightingGloves, Area.Jungle, Character.Knuckles, [], [], []),
    UpgradeLocation(603, LocationName.Big.Lure2, Area.Jungle, Character.Big, [], [], []),
    UpgradeLocation(601, LocationName.Big.PowerRod, Area.Jungle, Character.Big, [], [], []),
    UpgradeLocation(400, LocationName.Amy.WarriorFeather, Area.EggCarrierMain, Character.Amy, [], [], []),
    UpgradeLocation(401, LocationName.Amy.LongHammer, Area.EggCarrierMain, Character.Amy, [], [], []),
    UpgradeLocation(500, LocationName.Gamma.JetBooster, Area.EggCarrierMain, Character.Gamma, [], [], []),
    UpgradeLocation(501, LocationName.Gamma.LaserBlaster, Area.EggCarrierMain, Character.Gamma, [], [], []),
    UpgradeLocation(605, LocationName.Big.Lure4, Area.EggCarrierMain, Character.Big, [], [], []),
    UpgradeLocation(201, LocationName.Tails.RhythmBadge, Area.AngelIsland, Character.Tails, [], [], []),
]

field_emblem_location_table: List[EmblemLocation] = [
    EmblemLocation(10, Area.Station,
                   [Character.Sonic, Character.Knuckles, Character.Tails, Character.Amy, Character.Big],
                   [Character.Sonic, Character.Knuckles, Character.Tails, Character.Amy, Character.Big],
                   [Character.Sonic, Character.Knuckles, Character.Tails, Character.Amy, Character.Big],
                   "Station Emblem"),
    EmblemLocation(11, Area.StationSquareMain,
                   [Character.Sonic, Character.Tails, Character.Knuckles, Character.Amy, Character.Big,
                    Character.Gamma],
                   [Character.Sonic, Character.Tails, Character.Knuckles, Character.Amy, Character.Big,
                    Character.Gamma],
                   [Character.Sonic, Character.Tails, Character.Knuckles, Character.Amy, Character.Big,
                    Character.Gamma], "Burger Shop Emblem"),
    EmblemLocation(12, Area.StationSquareMain,
                   [Character.Tails, CharacterUpgrade(Character.Knuckles, ItemName.Knuckles.ShovelClaw)],
                   [Character.Tails, CharacterUpgrade(Character.Knuckles, ItemName.Knuckles.ShovelClaw)],
                   [Character.Amy, Character.Tails, CharacterUpgrade(Character.Knuckles, ItemName.Knuckles.ShovelClaw)],
                   "City Hall Emblem"),
    EmblemLocation(13, Area.Casino, [Character.Tails], [Character.Tails], [Character.Tails], "Casino Emblem"),
    EmblemLocation(20, Area.MysticRuinsMain,
                   [Character.Tails, Character.Knuckles, CharacterUpgrade(Character.Gamma, ItemName.Gamma.JetBooster)],
                   [Character.Sonic, Character.Tails, Character.Knuckles,
                    CharacterUpgrade(Character.Gamma, ItemName.Gamma.JetBooster)],
                   [Character.Sonic, Character.Tails, Character.Knuckles,
                    CharacterUpgrade(Character.Gamma, ItemName.Gamma.JetBooster)], "Tails' Workshop Emblem"),
    EmblemLocation(21, Area.AngelIsland, [Character.Knuckles], [Character.Tails, Character.Knuckles,
                                                                CharacterUpgrade(Character.Gamma,
                                                                                 ItemName.Gamma.JetBooster)],
                   [Character.Sonic, Character.Tails, Character.Knuckles,
                    CharacterUpgrade(Character.Gamma,
                                     ItemName.Gamma.JetBooster)], "Shrine Emblem"),
    EmblemLocation(22, Area.Jungle, [Character.Sonic, Character.Tails, Character.Knuckles, Character.Amy, Character.Big,
                                     Character.Gamma],
                   [Character.Sonic, Character.Tails, Character.Knuckles, Character.Amy, Character.Big,
                    Character.Gamma],
                   [Character.Sonic, Character.Tails, Character.Knuckles, Character.Amy, Character.Big,
                    Character.Gamma], "Jungle Path Emblem"),
    EmblemLocation(23, Area.Jungle, [Character.Tails, Character.Knuckles],
                   [Character.Sonic, Character.Tails, Character.Knuckles],
                   [Character.Sonic, Character.Tails, Character.Knuckles], "Tree Stump Emblem"),
    EmblemLocation(30, Area.EggCarrierMain, [Character.Tails, Character.Knuckles],
                   [Character.Sonic, Character.Tails, Character.Knuckles, Character.Amy],
                   [Character.Sonic, Character.Tails, Character.Knuckles, Character.Amy], "Pool Emblem"),
    EmblemLocation(31, Area.EggCarrierMain, [Character.Tails], [Character.Tails, Character.Sonic],
                   [Character.Tails, Character.Sonic], "Spinning Platform Emblem"),
    EmblemLocation(32, Area.EggCarrierMain, [Character.Tails, Character.Sonic],
                   [Character.Tails, Character.Sonic, Character.Big], [Character.Tails, Character.Sonic, Character.Big],
                   "Hidden Bed Emblem"),
    EmblemLocation(33, Area.EggCarrierMain, [Character.Sonic], [Character.Sonic, Character.Big],
                   [Character.Sonic, Character.Big], "Main Platform Emblem"),
]

life_capsule_location_table: List[LifeCapsuleLocation] = [
    LifeCapsuleLocation(1010, Area.EmeraldCoast, Character.Sonic, 1, [], [], []),
    LifeCapsuleLocation(1011, Area.EmeraldCoast, Character.Sonic, 2, [], [], []),
    LifeCapsuleLocation(1012, Area.EmeraldCoast, Character.Sonic, 3, [], [], []),
    LifeCapsuleLocation(1013, Area.EmeraldCoast, Character.Sonic, 4, [], [], []),
    LifeCapsuleLocation(1110, Area.WindyValley, Character.Sonic, 1, [ItemName.Sonic.LightShoes], [], []),
    LifeCapsuleLocation(1111, Area.WindyValley, Character.Sonic, 2, [], [], []),
    LifeCapsuleLocation(1112, Area.WindyValley, Character.Sonic, 3, [], [], []),
    LifeCapsuleLocation(1113, Area.WindyValley, Character.Sonic, 4, [ItemName.Sonic.LightShoes], [], []),
    LifeCapsuleLocation(1114, Area.WindyValley, Character.Sonic, 5, [], [], []),
    LifeCapsuleLocation(1210, Area.Casinopolis, Character.Sonic, 1, [], [], []),
    LifeCapsuleLocation(1211, Area.Casinopolis, Character.Sonic, 2, [], [], []),
    LifeCapsuleLocation(1212, Area.Casinopolis, Character.Sonic, 3, [], [], []),
    LifeCapsuleLocation(1310, Area.IceCap, Character.Sonic, 1, [], [], []),
    LifeCapsuleLocation(1410, Area.TwinklePark, Character.Sonic, 1, [], [], []),
    LifeCapsuleLocation(1411, Area.TwinklePark, Character.Sonic, 2, [], [], []),
    LifeCapsuleLocation(1412, Area.TwinklePark, Character.Sonic, 3, [], [], []),
    LifeCapsuleLocation(1413, Area.TwinklePark, Character.Sonic, 4, [], [], []),
    LifeCapsuleLocation(1510, Area.SpeedHighway, Character.Sonic, 1, [], [], []),
    LifeCapsuleLocation(1511, Area.SpeedHighway, Character.Sonic, 2, [], [], []),
    LifeCapsuleLocation(1512, Area.SpeedHighway, Character.Sonic, 3, [], [], []),
    LifeCapsuleLocation(1513, Area.SpeedHighway, Character.Sonic, 4, [], [], []),
    LifeCapsuleLocation(1514, Area.SpeedHighway, Character.Sonic, 5, [], [], []),
    LifeCapsuleLocation(1515, Area.SpeedHighway, Character.Sonic, 6, [], [], []),
    LifeCapsuleLocation(1516, Area.SpeedHighway, Character.Sonic, 7, [], [], []),
    LifeCapsuleLocation(1517, Area.SpeedHighway, Character.Sonic, 8, [], [], []),
    LifeCapsuleLocation(1518, Area.SpeedHighway, Character.Sonic, 9, [], [], []),
    LifeCapsuleLocation(1610, Area.RedMountain, Character.Sonic, 1, [], [], []),
    LifeCapsuleLocation(1611, Area.RedMountain, Character.Sonic, 2, [], [], []),
    LifeCapsuleLocation(1612, Area.RedMountain, Character.Sonic, 3, [], [], []),
    LifeCapsuleLocation(1613, Area.RedMountain, Character.Sonic, 4, [], [], []),
    LifeCapsuleLocation(1614, Area.RedMountain, Character.Sonic, 5, [ItemName.Sonic.LightShoes],
                        [ItemName.Sonic.LightShoes], []),
    LifeCapsuleLocation(1615, Area.RedMountain, Character.Sonic, 6, [ItemName.Sonic.LightShoes],
                        [ItemName.Sonic.LightShoes], []),
    LifeCapsuleLocation(1616, Area.RedMountain, Character.Sonic, 7, [], [], []),
    LifeCapsuleLocation(1617, Area.RedMountain, Character.Sonic, 8, [], [], []),
    LifeCapsuleLocation(1710, Area.SkyDeck, Character.Sonic, 1, [], [], []),
    LifeCapsuleLocation(1711, Area.SkyDeck, Character.Sonic, 2, [], [], []),
    LifeCapsuleLocation(1712, Area.SkyDeck, Character.Sonic, 3, [], [], []),
    LifeCapsuleLocation(1713, Area.SkyDeck, Character.Sonic, 4, [], [], []),
    LifeCapsuleLocation(1714, Area.SkyDeck, Character.Sonic, 5, [], [], []),
    LifeCapsuleLocation(1715, Area.SkyDeck, Character.Sonic, 6, [], [], []),
    LifeCapsuleLocation(1716, Area.SkyDeck, Character.Sonic, 7, [], [], []),
    LifeCapsuleLocation(1717, Area.SkyDeck, Character.Sonic, 8, [], [], []),
    LifeCapsuleLocation(1718, Area.SkyDeck, Character.Sonic, 9, [], [], []),
    LifeCapsuleLocation(1719, Area.SkyDeck, Character.Sonic, 10, [], [], []),
    LifeCapsuleLocation(1720, Area.SkyDeck, Character.Sonic, 11, [], [], []),
    LifeCapsuleLocation(1721, Area.SkyDeck, Character.Sonic, 12, [], [], []),
    LifeCapsuleLocation(1810, Area.LostWorld, Character.Sonic, 1, [], [], []),
    LifeCapsuleLocation(1811, Area.LostWorld, Character.Sonic, 2, [ItemName.Sonic.LightShoes], [], []),
    LifeCapsuleLocation(1910, Area.FinalEgg, Character.Sonic, 1, [], [], []),
    LifeCapsuleLocation(1911, Area.FinalEgg, Character.Sonic, 2, [], [], []),
    LifeCapsuleLocation(1912, Area.FinalEgg, Character.Sonic, 3, [], [], []),
    LifeCapsuleLocation(1913, Area.FinalEgg, Character.Sonic, 4, [], [], []),
    LifeCapsuleLocation(1914, Area.FinalEgg, Character.Sonic, 5, [], [], []),
    LifeCapsuleLocation(1915, Area.FinalEgg, Character.Sonic, 6, [], [], []),
    LifeCapsuleLocation(1916, Area.FinalEgg, Character.Sonic, 7, [], [], []),
    LifeCapsuleLocation(1917, Area.FinalEgg, Character.Sonic, 8, [], [], []),
    LifeCapsuleLocation(1918, Area.FinalEgg, Character.Sonic, 9, [], [], []),
    LifeCapsuleLocation(1919, Area.FinalEgg, Character.Sonic, 10, [], [], []),
    LifeCapsuleLocation(1920, Area.FinalEgg, Character.Sonic, 11, [], [], []),
    LifeCapsuleLocation(1921, Area.FinalEgg, Character.Sonic, 12, [], [], []),
    LifeCapsuleLocation(1922, Area.FinalEgg, Character.Sonic, 13, [], [], []),
    LifeCapsuleLocation(1923, Area.FinalEgg, Character.Sonic, 14, [], [], []),
    LifeCapsuleLocation(1924, Area.FinalEgg, Character.Sonic, 15, [], [], []),
    LifeCapsuleLocation(1925, Area.FinalEgg, Character.Sonic, 16, [], [], []),
    LifeCapsuleLocation(2010, Area.WindyValley, Character.Tails, 1, [], [], []),
    LifeCapsuleLocation(2110, Area.Casinopolis, Character.Tails, 1, [], [], []),
    LifeCapsuleLocation(2111, Area.Casinopolis, Character.Tails, 2, [], [], []),
    LifeCapsuleLocation(2310, Area.SkyDeck, Character.Tails, 1, [], [], []),
    LifeCapsuleLocation(2311, Area.SkyDeck, Character.Tails, 2, [], [], []),
    LifeCapsuleLocation(2312, Area.SkyDeck, Character.Tails, 3, [], [], []),
    LifeCapsuleLocation(2313, Area.SkyDeck, Character.Tails, 4, [], [], []),
    LifeCapsuleLocation(2410, Area.SpeedHighway, Character.Tails, 1, [], [], []),
    LifeCapsuleLocation(2411, Area.SpeedHighway, Character.Tails, 2, [], [], []),
    LifeCapsuleLocation(2412, Area.SpeedHighway, Character.Tails, 3, [], [], []),
    LifeCapsuleLocation(2413, Area.SpeedHighway, Character.Tails, 4, [], [], []),
    LifeCapsuleLocation(3010, Area.SpeedHighway, Character.Knuckles, 1, [], [], []),
    LifeCapsuleLocation(3011, Area.SpeedHighway, Character.Knuckles, 2, [], [], []),
    LifeCapsuleLocation(3012, Area.SpeedHighway, Character.Knuckles, 3, [], [], []),
    LifeCapsuleLocation(3110, Area.Casinopolis, Character.Knuckles, 1, [], [], []),
    LifeCapsuleLocation(3111, Area.Casinopolis, Character.Knuckles, 2, [], [], []),
    LifeCapsuleLocation(3210, Area.RedMountain, Character.Knuckles, 1, [], [], []),
    LifeCapsuleLocation(3211, Area.RedMountain, Character.Knuckles, 2, [], [], []),
    LifeCapsuleLocation(3212, Area.RedMountain, Character.Knuckles, 3, [], [], []),
    LifeCapsuleLocation(3213, Area.RedMountain, Character.Knuckles, 4, [], [], []),
    LifeCapsuleLocation(3410, Area.SkyDeck, Character.Knuckles, 1, [], [], []),
    LifeCapsuleLocation(4010, Area.TwinklePark, Character.Amy, 1, [], [], []),
    LifeCapsuleLocation(4110, Area.HotShelter, Character.Amy, 1, [], [], []),
    LifeCapsuleLocation(4111, Area.HotShelter, Character.Amy, 2, [], [], []),
    LifeCapsuleLocation(4112, Area.HotShelter, Character.Amy, 3, [], [], []),
    LifeCapsuleLocation(4113, Area.HotShelter, Character.Amy, 4, [], [], []),
    LifeCapsuleLocation(4210, Area.FinalEgg, Character.Amy, 1, [], [], []),
    LifeCapsuleLocation(4211, Area.FinalEgg, Character.Amy, 2, [], [], []),
    LifeCapsuleLocation(5110, Area.EmeraldCoast, Character.Gamma, 1, [], [], []),
    LifeCapsuleLocation(5210, Area.WindyValley, Character.Gamma, 1, [ItemName.Gamma.JetBooster],
                        [ItemName.Gamma.JetBooster], [ItemName.Gamma.JetBooster]),
    LifeCapsuleLocation(5211, Area.WindyValley, Character.Gamma, 2, [ItemName.Gamma.JetBooster],
                        [ItemName.Gamma.JetBooster], [ItemName.Gamma.JetBooster]),
    LifeCapsuleLocation(5310, Area.RedMountain, Character.Gamma, 1, [], [], []),
    LifeCapsuleLocation(5410, Area.HotShelter, Character.Gamma, 1, [ItemName.Gamma.JetBooster], [], []),
    LifeCapsuleLocation(5411, Area.HotShelter, Character.Gamma, 2, [ItemName.Gamma.JetBooster], [], []),
    LifeCapsuleLocation(5412, Area.HotShelter, Character.Gamma, 3, [ItemName.Gamma.JetBooster], [], []),
    LifeCapsuleLocation(5413, Area.HotShelter, Character.Gamma, 4, [ItemName.Gamma.JetBooster], [], []),
    LifeCapsuleLocation(6110, Area.IceCap, Character.Big, 1, [], [], []),
    LifeCapsuleLocation(6210, Area.EmeraldCoast, Character.Big, 1, [], [], []),
    LifeCapsuleLocation(6310, Area.HotShelter, Character.Big, 1, [], [], []),
]

mission_location_table: List[MissionLocation] = [
    MissionLocation(801, Area.StationSquareMain, Area.StationSquareMain, Character.Sonic, 1, [], [], []),
    MissionLocation(802, Area.MysticRuinsMain, Area.MysticRuinsMain, Character.Sonic, 2, [], [], []),
    MissionLocation(803, Area.Hotel, Area.Hotel, Character.Sonic, 3, [ItemName.Sonic.LightShoes], [], []),
    MissionLocation(804, Area.MysticRuinsMain, Area.MysticRuinsMain, Character.Tails, 4, [], [], []),
    MissionLocation(805, Area.Casino, Area.Casino, Character.Knuckles, 5, [], [], []),
    MissionLocation(806, Area.MysticRuinsMain, Area.MysticRuinsMain, Character.Amy, 6, [], [], []),
    MissionLocation(807, Area.MysticRuinsMain, Area.Jungle, Character.Gamma, 7, [], [], []),
    MissionLocation(808, Area.StationSquareMain, Area.StationSquareMain, Character.Big, 8, [], [], []),
    MissionLocation(809, Area.StationSquareMain, Area.EmeraldCoast, Character.Sonic, 9, [], [], []),
    MissionLocation(810, Area.Hotel, Area.Hotel, Character.Tails, 10, [], [], []),
    MissionLocation(811, Area.MysticRuinsMain, Area.WindyValley, Character.Sonic, 11, [], [], []),
    MissionLocation(812, Area.MysticRuinsMain, Area.MysticRuinsMain, Character.Knuckles, 12,
                    [ItemName.Knuckles.ShovelClaw], [ItemName.Knuckles.ShovelClaw], [ItemName.Knuckles.ShovelClaw]),
    MissionLocation(813, Area.Casino, Area.Casinopolis, Character.Sonic, 13, [], [], []),
    MissionLocation(814, Area.StationSquareMain, Area.Hotel, Character.Big, 14, [], [], []),
    MissionLocation(815, Area.MysticRuinsMain, Area.WindyValley, Character.Sonic, 15, [], [], []),
    MissionLocation(816, Area.MysticRuinsMain, Area.WindyValley, Character.Tails, 16, [], [], []),
    MissionLocation(817, Area.StationSquareMain, Area.Casinopolis, Character.Sonic, 17, [], [], []),
    MissionLocation(818, Area.Station, Area.TwinklePark, Character.Amy, 18, [], [], []),
    MissionLocation(819, Area.StationSquareMain, Area.TwinklePark, Character.Amy, 19, [], [], []),
    MissionLocation(820, Area.AngelIsland, Area.IceCap, Character.Sonic, 20,
                    [ItemName.KeyItem.IceStone, ItemName.KeyItem.CasinoKeys, ItemName.KeyItem.Train],
                    [ItemName.KeyItem.IceStone, ItemName.KeyItem.CasinoKeys, ItemName.KeyItem.Train],
                    [ItemName.KeyItem.IceStone, ItemName.KeyItem.CasinoKeys, ItemName.KeyItem.Train]),
    MissionLocation(821, Area.Jungle, Area.FinalEgg, Character.Gamma, 21, [], [], []),
    MissionLocation(822, Area.Hotel, Area.EmeraldCoast, Character.Big, 22, [], [], []),
    MissionLocation(823, Area.TwinkleParkLobby, Area.TwinklePark, Character.Sonic, 23, [], [], []),
    MissionLocation(824, Area.Casino, Area.Casinopolis, Character.Tails, 24, [], [], []),
    MissionLocation(825, Area.StationSquareMain, Area.Casinopolis, Character.Knuckles, 25, [], [], []),
    MissionLocation(826, Area.StationSquareMain, Area.Casinopolis, Character.Knuckles, 26, [], [], []),
    MissionLocation(827, Area.StationSquareMain, Area.SpeedHighway, Character.Sonic, 27, [], [], []),
    MissionLocation(828, Area.StationSquareMain, Area.SpeedHighway, Character.Sonic, 28, [], [], []),
    MissionLocation(829, Area.StationSquareMain, Area.StationSquareMain, Character.Big, 29, [ItemName.Big.LifeBelt], [],
                    []),
    MissionLocation(830, Area.Jungle, Area.RedMountain, Character.Sonic, 30, [], [], []),
    MissionLocation(831, Area.Station, Area.Casinopolis, Character.Tails, 31, [], [], []),
    MissionLocation(832, Area.AngelIsland, Area.AngelIsland, Character.Knuckles, 32, [], [], []),
    MissionLocation(833, Area.EggCarrierMain, Area.EggCarrierMain, Character.Sonic, 33, [], [], []),
    MissionLocation(834, Area.EggCarrierMain, Area.EggCarrierMain, Character.Sonic, 34, [ItemName.Sonic.LightShoes],
                    [ItemName.Sonic.LightShoes], []),
    MissionLocation(835, Area.MysticRuinsMain, Area.AngelIsland, Character.Big, 35,
                    [ItemName.KeyItem.IceStone, ItemName.KeyItem.StationKeys, ItemName.KeyItem.Train],
                    [ItemName.KeyItem.IceStone, ItemName.KeyItem.StationKeys, ItemName.KeyItem.Train],
                    [ItemName.KeyItem.IceStone, ItemName.KeyItem.StationKeys, ItemName.KeyItem.Train]),
    MissionLocation(836, Area.EggCarrierMain, Area.SkyDeck, Character.Sonic, 36, [], [], []),
    MissionLocation(837, Area.Jungle, Area.Jungle, Character.Tails, 37, [ItemName.Tails.JetAnklet], [], []),
    MissionLocation(838, Area.Jungle, Area.LostWorld, Character.Knuckles, 38, [ItemName.Knuckles.ShovelClaw],
                    [ItemName.Knuckles.ShovelClaw], [ItemName.Knuckles.ShovelClaw]),
    MissionLocation(839, Area.Hotel, Area.EmeraldCoast, Character.Gamma, 39, [ItemName.Gamma.JetBooster],
                    [ItemName.Gamma.JetBooster], [ItemName.Gamma.JetBooster]),
    MissionLocation(840, Area.MysticRuinsMain, Area.LostWorld, Character.Sonic, 40, [ItemName.Sonic.LightShoes],
                    [ItemName.Sonic.LightShoes], [ItemName.Sonic.LightShoes]),
    MissionLocation(841, Area.Jungle, Area.LostWorld, Character.Sonic, 41, [ItemName.Sonic.LightShoes], [], []),
    MissionLocation(842, Area.EggCarrierMain, Area.HotShelter, Character.Gamma, 42, [], [], []),
    MissionLocation(843, Area.EggCarrierMain, Area.HotShelter, Character.Amy, 43, [], [], []),
    MissionLocation(844, Area.EggCarrierMain, Area.EggCarrierMain, Character.Big, 44, [], [], []),
    MissionLocation(845, Area.Jungle, Area.FinalEgg, Character.Sonic, 45, [], [], []),
    MissionLocation(846, Area.Jungle, Area.FinalEgg, Character.Sonic, 46, [], [], []),
    MissionLocation(847, Area.MysticRuinsMain, Area.MysticRuinsMain, Character.Tails, 47, [], [], []),
    MissionLocation(848, Area.StationSquareMain, Area.Casinopolis, Character.Knuckles, 48, [], [], []),
    MissionLocation(849, Area.StationSquareMain, Area.TwinklePark, Character.Sonic, 49, [], [], []),
    MissionLocation(850, Area.Jungle, Area.FinalEgg, Character.Amy, 50, [], [], []),
    MissionLocation(851, Area.Jungle, Area.WindyValley, Character.Gamma, 51, [ItemName.Gamma.JetBooster],
                    [ItemName.Gamma.JetBooster], [ItemName.Gamma.JetBooster]),
    MissionLocation(852, Area.Jungle, Area.Jungle, Character.Big, 52, [], [], []),
    MissionLocation(853, Area.AngelIsland, Area.IceCap, Character.Sonic, 53, [], [], []),
    MissionLocation(854, Area.AngelIsland, Area.IceCap, Character.Tails, 54, [], [], []),
    MissionLocation(855, Area.TwinkleParkLobby, Area.SpeedHighway, Character.Sonic, 55, [], [], []),
    MissionLocation(856, Area.MysticRuinsMain, Area.RedMountain, Character.Knuckles, 56, [ItemName.Knuckles.ShovelClaw],
                    [ItemName.Knuckles.ShovelClaw], [ItemName.Knuckles.ShovelClaw]),
    MissionLocation(857, Area.AngelIsland, Area.RedMountain, Character.Sonic, 57, [], [], []),
    MissionLocation(858, Area.Jungle, Area.LostWorld, Character.Sonic, 58, [], [], []),
    MissionLocation(859, Area.EggCarrierMain, Area.SkyDeck, Character.Knuckles, 59, [], [], []),
    MissionLocation(860, Area.MysticRuinsMain, Area.IceCap, Character.Big, 60, [], [], []),
]

sub_level_location_table: List[SubLevelLocation] = [
    SubLevelLocation(15, Area.TwinkleParkLobby, EVERYONE, SubLevel.TwinkleCircuit, SubLevelMission.B),
    SubLevelLocation(16, Area.TwinkleParkLobby, EVERYONE, SubLevel.TwinkleCircuit, SubLevelMission.A),
    SubLevelLocation(25, Area.Jungle, SONIC_TAILS, SubLevel.SandHill, SubLevelMission.B),
    SubLevelLocation(26, Area.Jungle, SONIC_TAILS, SubLevel.SandHill, SubLevelMission.A),
    SubLevelLocation(27, Area.MysticRuinsMain, SONIC_TAILS, SubLevel.SkyChaseAct1, SubLevelMission.B),
    SubLevelLocation(28, Area.MysticRuinsMain, SONIC_TAILS, SubLevel.SkyChaseAct1, SubLevelMission.A),
    SubLevelLocation(35, Area.EggCarrierMain, SONIC_TAILS, SubLevel.SkyChaseAct2, SubLevelMission.B),
    SubLevelLocation(36, Area.EggCarrierMain, SONIC_TAILS, SubLevel.SkyChaseAct2, SubLevelMission.A),
]

boss_location_table: List[BossFightLocation] = [
    BossFightLocation(700, Area.StationSquareMain, [Character.Sonic], LocationName.Boss.Chaos0, False),
    BossFightLocation(710, Area.Hotel, [Character.Knuckles], LocationName.Boss.Chaos2, False),
    BossFightLocation(720, Area.Casino, [Character.Tails], LocationName.Boss.EggWalker, False),
    BossFightLocation(730, Area.MysticRuinsMain, [Character.Sonic], LocationName.Boss.EggHornet, False),
    BossFightLocation(731, Area.MysticRuinsMain, [Character.Tails], LocationName.Boss.EggHornet, False),
    BossFightLocation(739, Area.MysticRuinsMain, [Character.Sonic, Character.Tails], LocationName.Boss.EggHornet, True),
    BossFightLocation(740, Area.MysticRuinsMain, [Character.Sonic], LocationName.Boss.Chaos4, False),
    BossFightLocation(741, Area.MysticRuinsMain, [Character.Tails], LocationName.Boss.Chaos4, False),
    BossFightLocation(742, Area.MysticRuinsMain, [Character.Knuckles], LocationName.Boss.Chaos4, False),
    BossFightLocation(749, Area.MysticRuinsMain, [Character.Sonic, Character.Tails, Character.Knuckles],
                      LocationName.Boss.Chaos4, True),
    BossFightLocation(750, Area.Jungle, [Character.Sonic], LocationName.Boss.EggViper, False),
    BossFightLocation(760, Area.Jungle, [Character.Gamma], LocationName.Boss.E101Beta, False),
    BossFightLocation(770, Area.EggCarrierMain, [Character.Sonic], LocationName.Boss.Chaos6, False),
    BossFightLocation(771, Area.EggCarrierMain, [Character.Knuckles], LocationName.Boss.Chaos6, False),
    BossFightLocation(772, Area.EggCarrierMain, [Character.Big], LocationName.Boss.Chaos6, False),
    BossFightLocation(779, Area.EggCarrierMain, [Character.Sonic, Character.Knuckles, Character.Big],
                      LocationName.Boss.Chaos6, True),
    BossFightLocation(780, Area.EggCarrierMain, [Character.Gamma], LocationName.Boss.E101mkII, False),
    BossFightLocation(790, Area.EggCarrierMain, [Character.Amy], LocationName.Boss.Zero, False),
]
