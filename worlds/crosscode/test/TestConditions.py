from BaseClasses import ItemClassification

from . import CrossCodeTestBase
from ..Items import single_items_dict
from ..Locations import locations_data, events_data
from ..Regions import modes, region_packs

class TestItemConditions(CrossCodeTestBase):
    auto_construct = False

    def test_item_conditions_on_locations_exist(self):
        for data in locations_data:
            for item, amount in data.cond.items:
                item_name = item if amount == 1 else f"{item} x{amount}"
                assert(item_name in single_items_dict)

    def test_item_conditions_on_locations_are_progression(self):
        for data in locations_data:
            for item, amount in data.cond.items:
                item_name = item if amount == 1 else f"{item} x{amount}"
                item_info = single_items_dict[item_name]
                assert(item_info.classification == ItemClassification.progression)

    def test_item_conditions_on_locations_are_in_pool(self):
        for data in locations_data:
            for item, amount in data.cond.items:
                item_name = item if amount == 1 else f"{item} x{amount}"
                item_info = single_items_dict[item_name]
                for mode in modes:
                    assert(item_info.quantity[mode] >= 1)

    def test_item_conditions_on_regions_exist(self):
        for mode in modes:
            for connection in region_packs[mode].region_connections:
                for item, _ in connection.cond.items:
                    assert(item in single_items_dict)

    def test_item_conditions_on_regions_are_progression(self):
        for mode in modes:
            for connection in region_packs[mode].region_connections:
                for item, _ in connection.cond.items:
                    item_info = single_items_dict[item]
                    assert(item_info.classification == ItemClassification.progression)

    def test_item_conditions_on_regions_are_in_pool(self):
        for mode in modes:
            for data in locations_data:
                for item, _ in data.cond.items:
                    item_info = single_items_dict[item]
                    assert(item_info.quantity[mode] >= 1)

class TestLocationConditions(CrossCodeTestBase):
    auto_construct = False
    locations_dict = {location.name: location for location in [*locations_data, *events_data]}

    def test_location_conditions_on_locations(self):
        for data in locations_data:
            for location in data.cond.locations:
                assert(location in self.locations_dict)

    def test_region_conditions_on_locations(self):
        for data in locations_data:
            for mode, regions in data.cond.regions.items():
                for region in regions:
                    assert(region in region_packs[mode].region_list)

    def test_location_conditions_on_regions(self):
        for mode in modes:
            for connection in region_packs[mode].region_connections:
                for location in connection.cond.locations:
                    assert(location in self.locations_dict)

    def test_region_conditions_on_regions(self):
        for mode in modes:
            for connection in region_packs[mode].region_connections:
                if mode not in connection.cond.regions:
                    continue
                for region in connection.cond.regions[mode]:
                    assert(region in region_packs[mode].region_list)
