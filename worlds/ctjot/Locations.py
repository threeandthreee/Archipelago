from BaseClasses import MultiWorld, Region, Location, ItemClassification

from . import CTJoTDefaults

import json
from typing import NamedTuple


class LocationData(NamedTuple):
    """
    Store the data associated with a Chrono Trigger treasure location
    """
    name: str
    code: int


class CTJoTLocationManager:
    """
    Manage location data.
    """
    _location_data = {}
    _LOCATION_ID_START = 5100000
    _name_to_id_mapping = {}

    # Location lists broken down by time period
    _locations_prehistory = [174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189]
    _locations_darkages = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    _locations_600ad_1000ad = [15, 54, 55, 56, 57, 58, 59, 60, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72,
                               73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93,
                               94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111,
                               112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128,
                               129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145,
                               146, 147, 148, 149, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171,
                               172, 173, 190, 191]
    _locations_future = [16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38,
                         39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 150, 151, 152, 153, 154, 155,
                         156, 157, 158, 242]

    # Prison tower is in 1000 AD, but only accessible after clearing the prison break sequence.
    # Physically in 1000 AD, Logically it's part of the future checks.
    # Separating it because it's not part of Lost Worlds.
    _locations_prison_tower_1000ad = [28]

    def __init__(self):
        """
        Read the location_data file and populate the location DB
        """
        import pkgutil
        locations = json.loads(pkgutil.get_data(__name__, "data/location_data.json").decode())
        for key, value in locations.items():
            self._location_data[key] = LocationData(key, value + self._LOCATION_ID_START)

        # Create a reverse lookup for mapping names to location IDs.
        self._name_to_id_mapping = {name: location.code for name, location in self._location_data.items()}
        self._id_to_name_mapping = {location.code: name for name, location in self._location_data.items()}
        self._filler_location_ids: list[int] = []

    def get_location_name_to_id_mapping(self) -> dict[str, int]:
        """
        Get a dictionary mapping location names to IDs.

        :return: Dictionary mapping location names to IDs
        """
        return self._name_to_id_mapping

    def add_filler_locations(self, multiworld: MultiWorld, player: int, region: Region):
        """
        Create locations to be used for filler/useful items.  These locations will not
        allow progression items to be placed and will change based on game mode/flags.

        In normal game mode there are a set number of progression locations.  Those will be set to
        allow any item.  The non-progression locations will be set to allow only items that do not
        lead to progression.  This way we don't force normal mode players to learn/check every treasure
        chest or risk locking someone else out of an important key item.

        :param multiworld: Multiworld instance for this session
        :param player: Player ID of the player we're generating a world for
        :param region: Region to add the filler locations to
        :return: List of filler location IDs
        """
        filler_location_ids = self.get_filler_location_ids(multiworld, player)

        # Create locations for all filler locations that are limited to non-progression items.
        for loc_id in filler_location_ids:
            location_data = self._location_data[self._id_to_name_mapping[loc_id + self._LOCATION_ID_START]]
            location = Location(player,
                                location_data.name,
                                location_data.code,
                                region)
            location.access_rule = lambda state: True
            location.item_rule = \
                lambda item: item.classification in [ItemClassification.filler,
                                                     ItemClassification.useful,
                                                     ItemClassification.trap]
            region.locations.append(location)

    def get_location(self, player: int, location_entry, region: Region) -> Location:
        """
        Get a Location object for the given location entry from the player's yaml file.

        :param player: Player ID to assign to this location
        :param location_entry: Location data from the player's settings
        :param region: Region this location is to be added to
        :return: Configured location object
        """
        location_name = location_entry["name"]
        location_id = self._name_to_id_mapping[location_name]
        return Location(player, location_name, location_id, region)

    def get_filler_location_ids(self, multiworld: MultiWorld, player: int) -> list[int]:
        """
        Determine which location IDs are used for filler based on game mode
        and which locations were selected for key items.

        :param multiworld: Multiworld instance for this game
        :param player: Player ID to whom these locations belong
        :return: List of filler location IDs
        """
        filler_location_ids = []
        game_mode = getattr(multiworld, "game_mode")[player].value

        if game_mode == "Lost worlds":
            # Add locations for prehistory, dark ages, and future
            filler_location_ids.extend(self._locations_prehistory)
            filler_location_ids.extend(self._locations_darkages)
            filler_location_ids.extend(self._locations_future)
        elif game_mode == "Legacy of cyrus":
            # Add locations for prehistory, dark ages, 600AD, 1000AD
            filler_location_ids.extend(self._locations_prehistory)
            filler_location_ids.extend(self._locations_darkages)
            filler_location_ids.extend(self._locations_600ad_1000ad)
        else:
            # Add all chronosanity locations
            filler_location_ids.extend(self._locations_prehistory)
            filler_location_ids.extend(self._locations_darkages)
            filler_location_ids.extend(self._locations_600ad_1000ad)
            filler_location_ids.extend(self._locations_prison_tower_1000ad)
            filler_location_ids.extend(self._locations_future)

        if game_mode == "Vanilla rando":
            # Add the vanilla rando exclusive Bekkler's tent and Cyrus' Grave locations
            filler_location_ids.extend([312, 313])

        # Filter out locations chosen for key items
        locations_from_config = getattr(multiworld, "locations")[player].value
        if len(locations_from_config) == 0:
            locations_from_config = CTJoTDefaults.DEFAULT_LOCATIONS
        for location_entry in locations_from_config:
            if location_entry["classification"] != "event":
                filler_location_ids.remove(
                    self._name_to_id_mapping[location_entry["name"]] - self._LOCATION_ID_START)

        return filler_location_ids
