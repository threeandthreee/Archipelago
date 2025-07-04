from . import AnodyneTestBase


class TestCustomNexusGates1(AnodyneTestBase):
    options = {
        "custom_nexus_gates_open": ["Red Cave exit"],
        "big_key_shuffle": "any_world",
    }

    def test_requirement(self):
        self.assertFalse(self.can_reach_region("Apartment floor 1"))
        self.assertTrue(self.can_reach_region("Beach"))
        self.assertFalse(self.can_reach_region("Bedroom entrance"))
        self.assertFalse(self.can_reach_region("Blue"))
        self.assertFalse(self.can_reach_region("Cell"))
        self.assertFalse(self.can_reach_region("Circus"))
        self.assertTrue(self.can_reach_region("Fields"))
        self.assertTrue(self.can_reach_region("Red Cave exit"))
        self.assertTrue(self.can_reach_region("Red Cave top"))
        self.assertFalse(self.can_reach_region("Red Cave left"))
        self.assertFalse(self.can_reach_region("Red Cave right"))
        self.assertTrue(self.can_reach_region("Red Cave center"))
        self.assertTrue(self.can_reach_region("Red Sea"))
        self.assertTrue(self.can_reach_region("Street"))


class TestCustomNexusGates2(AnodyneTestBase):
    options = {
        "custom_nexus_gates_open": ["Windmill entrance"],
        "big_key_shuffle": "any_world",
        "start_broom": "normal",
    }

    def test_requirement(self):
        self.assertFalse(self.can_reach_region("Apartment floor 1"))
        self.assertFalse(self.can_reach_region("Beach"))
        self.assertFalse(self.can_reach_region("Bedroom entrance"))
        self.assertFalse(self.can_reach_region("Blue"))
        self.assertFalse(self.can_reach_region("Cell"))
        self.assertFalse(self.can_reach_region("Circus"))
        self.assertFalse(self.can_reach_region("Fields"))
        self.assertFalse(self.can_reach_region("Red Cave top"))
        self.assertFalse(self.can_reach_region("Red Cave left"))
        self.assertFalse(self.can_reach_region("Red Cave right"))
        self.assertFalse(self.can_reach_region("Red Cave center"))
        self.assertFalse(self.can_reach_region("Red Sea"))
        self.assertTrue(self.can_reach_region("Windmill entrance"))
        self.assertTrue(self.can_reach_region("Street"))


class TestCustomNexusGates3(AnodyneTestBase):
    options = {
        "custom_nexus_gates_open": ["Cell", "Space", "Suburb"],
        "big_key_shuffle": "any_world",
    }

    def test_requirement(self):
        self.assertFalse(self.can_reach_region("Apartment floor 1"))
        self.assertTrue(self.can_reach_region("Beach"))
        self.assertTrue(self.can_reach_region("Bedroom entrance"))  # through the front, because of Street
        self.assertFalse(self.can_reach_region("Blue"))
        self.assertTrue(self.can_reach_region("Cell"))
        self.assertTrue(self.can_reach_region("Circus"))
        self.assertTrue(self.can_reach_region("Fields"))
        self.assertTrue(self.can_reach_region("Red Cave top"))
        self.assertFalse(self.can_reach_region("Red Cave left"))
        self.assertFalse(self.can_reach_region("Red Cave right"))
        self.assertTrue(self.can_reach_region("Red Cave center"))
        self.assertTrue(self.can_reach_region("Red Sea"))
        self.assertTrue(self.can_reach_region("Overworld"))
        self.assertTrue(self.can_reach_region("Overworld post windmill"))
        self.assertTrue(self.can_reach_region("Space"))
        self.assertTrue(self.can_reach_region("Cliff"))
        self.assertTrue(self.can_reach_region("Cliff post windmill"))
        self.assertFalse(self.can_reach_region("Crowd floor 1"))
        self.assertTrue(self.can_reach_region("Hotel roof"))
        self.assertFalse(self.can_reach_region("Hotel floor 1"))
        self.assertTrue(self.can_reach_region("Street"))
