from . import CrossCodeTestBase

overworld_area_unlocks = [
    "Green Leaf Shade",
    "Blue Ice Shade",
    "Red Flame Shade",
    "Green Seed Shade",
    "Star Shade",
    "Meteor Shade",
]

dungeon_unlocks = [
    "Mine Pass",
    "Yellow Sand Shade",
    "Purple Bolt Shade",
    "Azure Drop Shade",
]

class TestProgressiveAreasOverworld(CrossCodeTestBase):
    options = { "progressive_area_unlocks": "overworld" }

    def test_overworld_items_are_progressive(self):
        local_overworld_area_unlocks = self.get_items_by_name("Progressive Overworld Area Unlock")
        self.assertEqual(len(overworld_area_unlocks), len(local_overworld_area_unlocks))

    def test_dungeon_items_are_not_progressive(self):
        local_dungeon_unlocks = self.get_items_by_name(dungeon_unlocks)
        self.assertEqual(len(dungeon_unlocks), len(local_dungeon_unlocks))
