from .items import SongData
from typing import Dict, List, Set, Optional
from collections import ChainMap

class RotNCollections:
    DIAMOND_NAME: str = "Diamond"
    DIAMOND_CODE: int = 1

    # Thanks to DeamonHunter for genning this info
    SONG_DATA: Dict[str, SongData] = {
        "Disco Disaster": SongData(50, "TrackName_DiscoDisaster", "Base", 1, 4, 7, 22),
        "Elusional": SongData(51, "TrackName_Elusional", "Base", 2, 6, 11, 21),
        "Visualize Yourself": SongData(52, "TrackName_VisualizeYourself", "Base", 3, 7, 14, 24),
        "Spookhouse Pop": SongData(53, "TrackName_SpookhousePop", "Base", 4, 6, 16, 23),
        "Om and On": SongData(54, "TrackName_OmAndOn", "Base", 4, 6, 18, 26),
        "Morning Dove": SongData(55, "TrackName_MorningDove", "Base", 6, 8, 16, 22),
        "Heph's Mess": SongData(56, "TrackName_HephsMess", "Base", 2, 5, 13, 19),
        "Amalgamaniac": SongData(57, "TrackName_Amalgamaniac", "Base", 4, 7, 14, 24),
        "Hang Ten Heph": SongData(58, "TrackName_HangTenHeph", "Base", 4, 8, 17, 25),
        "Count Funkula": SongData(59, "TrackName_CountFunkula", "Base", 3, 7, 19, 29),
        "Overthinker": SongData(60, "TrackName_Overthinker", "Base", 4, 9, 13, 28),
        "Cryp2que": SongData(61, "TrackName_Cryp2que", "Base", 3, 8, 13, 27),
        "Nocturning": SongData(62, "TrackName_Nocturning", "Base", 3, 6, 12, 23),
        "Glass Cages (feat. Sarah Hubbard)": SongData(63, "TrackName_GlassCages", "Base", 4, 8, 17, 25),
        "Hallow Queen": SongData(64, "TrackName_HallowQueen", "Base", 4, 8, 16, 18),
        "Progenitor": SongData(65, "TrackName_Progenitor", "Base", 3, 13, 19, 25),
        "Matriarch": SongData(66, "TrackName_Matriarch", "Base", 7, 11, 18, 23),
        "Under the Thunder": SongData(67, "TrackName_Thunder", "Base", 4, 12, 17, 27),
        "Eldritch House": SongData(68, "TrackName_EldritchHouse", "Base", 4, 9, 16, 25),
        "RAVEVENGE (feat. Aram Zero)": SongData(69, "TrackName_RAVEvenge", "Base", 5, 9, 14, 27),
        "Rift Within": SongData(70, "TrackName_RiftWithin", "Base", 4, 10, 17, 26),
        "Suzu's Quest": SongData(71, "TrackName_SuzusQuest", "Base", 6, 12, 19, 24),
        "Necropolis": SongData(72, "TrackName_Necropolis", "Base", 4, 10, 16, 18),
        "Baboosh": SongData(73, "TrackName_Baboosh", "Base", 6, 12, 19, 30),
        "Necro Sonatica": SongData(74, "TrackName_NecroSonatica", "Base", 8, 16, 21, 30),
        "She Banned": SongData(75, "TrackName_SheBanned", "Base", 5, 11, 17, 22),
        "King's Ruse": SongData(76, "TrackName_KingsRuse", "Base", 3, 11, 15, 28),
        "What's in the Box": SongData(77, "TrackName_WhatsInTheBox", "Base", 4, 9, 14, 26),
        "Brave the Harvester": SongData(78, "TrackName_BravetheHarvester", "Base", 6, 14, 20, 27),
        "Final Fugue": SongData(79, "TrackName_FinalFugue", "Base", 6, 13, 20, 30),
        "Twombtorial": SongData(80, "TrackName_Twombtorial", "Base", 5, 13, 19, 23),
        "Portamello": SongData(81, "TrackName_Portamello", "Base", 5, 10, 15, 20),
        "Slugger's Refrain": SongData(82, "TrackName_DLC_Apricot01", "Apricot", 6, 14, 21, 30),
        "Got Danged": SongData(83, "TrackName_DLC_Apricot02", "Apricot", 5, 12, 20, 30),
        "Bootus Bleez": SongData(84, "TrackName_DLC_Apricot03", "Apricot", 6, 10, 19, 29),
    }

    FREE_PACKS: List[str] = [
        "Base",
        "Apricot"
    ]

    song_locations: Dict[str, int] = {}
    song_items: Dict[str, SongData] = {}

    filler_items: Dict[str, int] = {
        "Apple": 2,
        "Cheese": 3,
        "Chicken": 4,
        "Ham": 5,
        "Vibe Charge": 6,
    }

    filler_weights: Dict[str, int] = {
        "Apple": 10,
        "Cheese": 7,
        "Chicken": 4,
        "Ham": 1,
        "Vibe Charge": 5,
    }

    item_names_to_id: ChainMap = ChainMap({}, filler_items)
    location_names_to_id: ChainMap = ChainMap(song_locations)

    def __init__(self) -> None:
        self.item_names_to_id[self.DIAMOND_NAME] = self.DIAMOND_CODE

        for key, data in self.SONG_DATA.items():
            self.song_items[key] = data

        self.item_names_to_id.update({name: data.code for name, data in self.song_items.items()})

        location_id_index = 1
        for name in self.SONG_DATA.keys():
            self.song_locations[f"{name}-0"] = location_id_index 
            self.song_locations[f"{name}-1"] = location_id_index + 1
            location_id_index += 2

    def getSongsWithSettings(self, diff_lower: int, diff_higher:int) -> List[str]:
        filtered_list = []

        for key, data in self.song_items.items():
            if data.diff_easy != -1 and diff_lower <= data.diff_easy <= diff_higher:
                filtered_list.append(key)
                continue

            if data.diff_medium != -1 and diff_lower <= data.diff_medium <= diff_higher:
                filtered_list.append(key)
                continue

            if data.diff_hard != -1 and diff_lower <= data.diff_hard <= diff_higher:
                filtered_list.append(key)
                continue

            if data.diff_impossible != -1 and diff_lower <= data.diff_impossible <= diff_higher:
                filtered_list.append(key)
                continue

        return filtered_list
