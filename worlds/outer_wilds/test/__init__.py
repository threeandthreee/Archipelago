import os
import sys
from typing import List

from test.bases import WorldTestBase, CollectionState
from ..options import Goal

path = os.path.dirname(__file__)
path = os.path.join(path, 'shared_static_logic')
if path not in sys.path:
    sys.path.append(path)


class OuterWildsTestBase(WorldTestBase):
    game = "Outer Wilds"
    player: int = 1

    def makeStateWith(self, item_names: List[str]) -> CollectionState:
        state = CollectionState(self.multiworld)
        for i in self.get_items_by_name(item_names):
            state.collect(i)
        return state

    def getLocationCount(self) -> int:
        return sum(1 for _ in self.multiworld.get_locations(1))

    def isReachableWith(self, location_name: str, item_names: List[str]) -> bool:
        state = self.makeStateWith(item_names)
        return state.can_reach_location(location_name, 1)

    def assertReachableWith(self, location_name: str, item_names: List[str]) -> None:
        self.assertTrue(self.isReachableWith(location_name, item_names))

    def assertNotReachableWith(self, location_name: str, item_names: List[str]) -> None:
        self.assertFalse(self.isReachableWith(location_name, item_names))

    # we can't realistically prove there is no other combination of items that works,
    # so what this actually tests is having all item_names is enough to reach the location,
    # and missing any one of those item_names is not enough to reach it.
    def requiresAllOf(self, location_name: str, item_names: List[str]) -> bool:
        items = self.get_items_by_name(item_names)
        state = CollectionState(self.multiworld)

        # check that it can be reached with all the items
        for i in items:
            state.collect(i)
        if not state.can_reach_location(location_name, 1):
            return False

        # check that removing any one item makes it unreachable again
        for i in items:
            state.remove(i)
            if state.can_reach_location(location_name, 1):
                return False
            state.collect(i)

        return True

    # Note that pre-collected items like Launch Codes are ignored by AP reachability logic,
    # so it doesn't matter
    def assertRequiresAllOf(self, location_name: str, item_names: List[str]) -> None:
        self.assertTrue(self.requiresAllOf(location_name, item_names))

    # Checks that the listed locations requiresAllOf(item_names), and that
    # every other location in the multiworld does not requiresAllOf(item_names).
    # This may have unintuitive results for locations which can be reached multiple ways.
    def assertEverywhereRequiringAllOf(self, location_names: List[str], item_names: List[str]) -> None:
        for location in self.multiworld.get_locations():
            if location.name in location_names:
                self.assertTrue(
                    self.requiresAllOf(location.name, item_names),
                    f"location '{location}' should require exactly {item_names} to reach, but it doesn't"
                )
            else:
                self.assertFalse(
                    self.requiresAllOf(location.name, item_names),
                    f"location '{location}' was not one of the locations being asserted on, "
                    f"but it requires exactly {item_names} to reach, so it should be"
                )

    def test_all_worlds(self) -> None:
        self.assertAccessDependency(
            ["Victory - Song of Five", "Victory - Song of Six"],
            [["Coordinates"]]
        )

        # for now, we create the Victory events unconditionally, and the Goal
        # setting only changes which one is used in the completion_condition,
        # so these "go mode" tests pass regardless of the Goal setting
        self.assertRequiresAllOf("Victory - Song of Five", [
            "Spacesuit",
            "Launch Codes",
            "Nomai Warp Codes",
            "Warp Core Installation Manual",
            "Silent Running Mode",
            "Signalscope",
            "Distress Beacon Frequency",
            "Escape Pod 3 Signal",
            "Scout",
            "Coordinates"
        ])

        self.assertNotReachableWith("Victory - Song of Six", [
            "Spacesuit",
            "Launch Codes",
            "Nomai Warp Codes",
            "Warp Core Installation Manual",
            "Silent Running Mode",
            "Signalscope",
            "Distress Beacon Frequency",
            "Escape Pod 3 Signal",
            "Scout",
            "Coordinates"
        ])

        self.assertRequiresAllOf("Victory - Song of Six", [
            "Spacesuit",
            "Launch Codes",
            "Nomai Warp Codes",
            "Warp Core Installation Manual",
            "Silent Running Mode",
            "Signalscope",
            "Distress Beacon Frequency",
            "Escape Pod 3 Signal",
            "Scout",
            "Coordinates",
            # added by Song of Six
            "Imaging Rule",
            "Shrine Door Codes",
            "Entanglement Rule"
        ])


class TestDefaultWorld(OuterWildsTestBase):
    options = {}

    def test_default_world(self):
        self.assertEqual(self.getLocationCount(), 87)  # default locations, including Victory events

        # with default locations, Insulation only blocks 2 checks
        self.assertAccessDependency(
            ["GD: Enter the Core", "GD: See the Coordinates"],
            [["Electrical Insulation"]]
        )

        self.assertEverywhereRequiringAllOf(
            ["Ruptured Core (Text Wheel)"],
            ["Launch Codes", "Scout", "Ghost Matter Wavelength", "Translator"]
        )

        # logsanity locations don't exist, so trying to access one raises
        self.assertRaises(KeyError, lambda: self.multiworld.get_location("Ship Log: Village 1 - Identify", 1))

        # Feldspar's Camp is one of the few places with two different "logical paths", so check that both are in-logic
        self.assertNotReachableWith("DB: Feldspar's Camp Fuel Tank", ["Silent Running Mode"])
        self.assertNotReachableWith("DB: Feldspar's Camp Fuel Tank", ["Silent Running Mode", "Signalscope"])
        self.assertReachableWith("DB: Feldspar's Camp Fuel Tank", [
            "Silent Running Mode", "Signalscope", "Feldspar's Signal"
        ])
        self.assertReachableWith("DB: Feldspar's Camp Fuel Tank", [
            "Silent Running Mode", "Scout"
        ])


class TestSongOfSixWorld(OuterWildsTestBase):
    options = {
        "goal": Goal.option_song_of_six
    }

    def test_six_world(self):
        self.assertEqual(self.getLocationCount(), 87)  # same as song of five

        # same as song of five
        self.assertAccessDependency(
            ["GD: Enter the Core", "GD: See the Coordinates"],
            [["Electrical Insulation"]]
        )


class TestLogsanityWorld(OuterWildsTestBase):
    options = {
        "logsanity": "true"
    }

    def test_logsanity_world(self):
        self.assertEqual(self.getLocationCount(), 263)  # 87 default + 176 logsanity locations

        # make sure the logsanity locations exist; this one requires nothing to reach
        self.assertReachableWith("TH Ship Log: Village 1 - Identify", [])

        # and some of those new locations are Insulation-gated
        self.assertAccessDependency(
            [
                "GD: Enter the Core", "GD: See the Coordinates",
                "GD Ship Log: Ocean Depths 2 - Coral Forest",
                "GD Ship Log: Probe Tracking Module 1 - Millions",
                "GD Ship Log: Probe Tracking Module 2 - Anomaly Located",
                "GD Ship Log: Probe Tracking Module 3 - Statue",
                "GD Ship Log: Probe Tracking Module 4 - Coordinates"
            ],
            [["Electrical Insulation"]]
        )

        self.assertNotReachableWith("GD: Enter the Core", [])
        self.assertNotReachableWith("GD: Enter the Core", ["Tornado Aerodynamic Adjustments"])
        self.assertNotReachableWith("GD: Enter the Core", ["Electrical Insulation"])
        self.assertReachableWith("GD: Enter the Core", [
            "Tornado Aerodynamic Adjustments", "Electrical Insulation"
        ])

        self.assertNotReachableWith("GD Ship Log: Bramble Island", [])
        self.assertReachableWith("GD Ship Log: Bramble Island", ["Ghost Matter Wavelength"])

        self.assertNotReachableWith("GD: Bramble Island Recorder", [])
        self.assertReachableWith("GD: Bramble Island Recorder", ["Ghost Matter Wavelength"])

        self.assertNotReachableWith("GD: Bramble Island Fuel Tank", [])
        self.assertReachableWith("GD: Bramble Island Fuel Tank", ["Ghost Matter Wavelength"])


class TestSuitlessWorld(OuterWildsTestBase):
    options = {
        "shuffle_spacesuit": "true"
    }


class TestSuitlessSongOfSixWorld(OuterWildsTestBase):
    options = {
        "shuffle_spacesuit": "true",
        "goal": Goal.option_song_of_six
    }


class TestSuitlessLogsanityWorld(OuterWildsTestBase):
    options = {
        "shuffle_spacesuit": "true",
        "logsanity": "true"
    }


class TestSuitlessLogsanitySongOfSixWorld(OuterWildsTestBase):
    options = {
        "shuffle_spacesuit": "true",
        "logsanity": "true",
        "goal": Goal.option_song_of_six
    }

    def test_suitless_logic(self):
        # Spacesuit is required for PTM locations (via region logic rather than location logic)
        self.assertNotReachableWith("GD Ship Log: Probe Tracking Module 1 - Millions", [
            "Tornado Aerodynamic Adjustments", "Electrical Insulation", "Translator"
        ])
        self.assertReachableWith("GD Ship Log: Probe Tracking Module 1 - Millions", [
            "Tornado Aerodynamic Adjustments", "Electrical Insulation", "Spacesuit", "Translator"
        ])


class TestRandomOrbitsOff(OuterWildsTestBase):
    options = {
        "randomize_orbits": "false",
    }

