import unittest
from ..Data import Locations,Regions

class TestData(unittest.TestCase):
    def test_consistent_region_names(self):
        for loc_region in Locations.locations_by_region:
            self.assertIn(loc_region,Regions.all_regions,"Location region not a real region")