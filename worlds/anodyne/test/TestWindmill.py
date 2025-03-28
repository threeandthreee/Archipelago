from . import AnodyneTestBase


class TestVanillaWindmill(AnodyneTestBase):
    options = {
        "split_windmill": "false",
        "big_key_shuffle": "any_world",
        "custom_nexus_gates_open": ["Windmill entrance", "Red Cave exit", "Crowd exit", "Bedroom exit"],
    }

    def test_requirement(self):
        self.collect_by_name("Broom")  # collect just to re-evaluate reachable regions

        self.assertFalse(self.can_reach_region("Windmill"))
        self.assertFalse(self.can_reach_region("Cell"))
        self.assertFalse(self.can_reach_region("Space"))
        self.assertFalse(self.can_reach_region("Suburb"))

        self.collect_by_name("Red Key")
        self.collect_by_name("Blue Key")

        self.assertTrue(self.can_reach_region("Windmill"))
        self.assertTrue(self.can_reach_region("Cell"))
        self.assertTrue(self.can_reach_region("Space"))
        self.assertTrue(self.can_reach_region("Suburb"))


class TestSplitWindmill(AnodyneTestBase):
    options = {
        "split_windmill": "true",
        "big_key_shuffle": "any_world",
        "custom_nexus_gates_open": ["Windmill entrance", "Red Cave exit", "Crowd exit", "Bedroom exit"],
    }

    def test_requirement(self):
        self.collect_by_name("Broom")  # collect just to re-evaluate reachable regions

        self.assertFalse(self.can_reach_region("Windmill"))
        self.assertFalse(self.can_reach_region("Cell"))
        self.assertFalse(self.can_reach_region("Space"))
        self.assertFalse(self.can_reach_region("Suburb"))

        self.collect_by_name("Red Key")
        self.collect_by_name("Blue Key")

        self.assertTrue(self.can_reach_region("Windmill"))
        self.assertFalse(self.can_reach_region("Cell"))
        self.assertFalse(self.can_reach_region("Space"))
        self.assertFalse(self.can_reach_region("Suburb"))

        self.collect_by_name("Temple of the Seeing One Statue")
        self.assertTrue(self.can_reach_region("Suburb"))

        self.collect_by_name("Red Cave Statue")
        self.assertTrue(self.can_reach_region("Cell"))

        self.collect_by_name("Mountain Cavern Statue")
        self.assertTrue(self.can_reach_region("Space"))
