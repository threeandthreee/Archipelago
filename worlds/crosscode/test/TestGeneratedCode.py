from functools import reduce
from test.TestBase import WorldTestBase
from . import CrossCodeTestBase
from ..Items import single_items_data, single_items_dict
from ..Locations import locations_data, events_data, needed_items
from ..Regions import modes, region_packs

class TestLocationAttributes(CrossCodeTestBase):
    auto_construct = False

    def test_regions_exist(self):
        for mode in modes:
            all_regions = set()
            all_regions |= set(region_packs[mode].region_list)
            all_regions |= set(region_packs[mode].excluded_regions)
            for data in locations_data:
                assert(data.region[mode] in all_regions)


class TestItemQuantities(CrossCodeTestBase):
    auto_construct = False

    def test_item_quantities_equal_to_locations(self):
        for mode in modes:
            number_of_locations = 0
            for data in locations_data:
                if mode in data.region and data.region[mode] not in region_packs[mode].excluded_regions:
                    number_of_locations += 1

            items_from_locations = 0
            for item in single_items_data:
                if mode in item.quantity:
                    items_from_locations += item.quantity[mode]

            items_to_generate = needed_items[mode]

            total_items = items_from_locations + items_to_generate
            assert(total_items == number_of_locations)
