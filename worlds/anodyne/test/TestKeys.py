from . import AnodyneTestBase


class TestVanillaSmallKeys(AnodyneTestBase):
    options = {
        "small_key_shuffle": "vanilla",
    }


class TestBedroomKeysWithoutEarlyAccess(AnodyneTestBase):
    options = {
        "split_windmill": "true",
        "small_key_shuffle": "any_world",
    }

    def test_requirement(self):
        self.collect_by_name(["Broom", "Small Key (Street)", "Temple of the Seeing One Statue"])
        self.assertTrue(self.can_reach_location("Temple of the Seeing One - Entrance Chest"))
        self.assertFalse(self.can_reach_location("Temple of the Seeing One - Boss Chest"))
        self.assertFalse(self.can_reach_location("Temple of the Seeing One - After Statue Left Chest"))
        self.assertFalse(self.can_reach_region("Overworld post windmill"))

        keys = self.get_items_by_name("Small Key (Temple of the Seeing One)")

        self.collect(keys[0])
        self.assertFalse(self.can_reach_location("Temple of the Seeing One - Boss Chest"))
        self.assertFalse(self.can_reach_location("Temple of the Seeing One - After Statue Left Chest"))
        self.assertFalse(self.can_reach_region("Overworld post windmill"))

        self.collect(keys[1])
        self.assertTrue(self.can_reach_location("Temple of the Seeing One - Boss Chest"))
        self.assertTrue(self.can_reach_location("Temple of the Seeing One - After Statue Left Chest"))
        self.assertFalse(self.can_reach_region("Overworld post windmill"))

        self.collect(keys[2])
        self.assertTrue(self.can_reach_location("Temple of the Seeing One - Boss Chest"))
        self.assertTrue(self.can_reach_location("Temple of the Seeing One - After Statue Left Chest"))
        self.assertTrue(self.can_reach_region("Overworld post windmill"))


class TestBedroomKeysWithShuffledNexusGates(AnodyneTestBase):
    options = {
        "split_windmill": "true",
        "nexus_gate_shuffle": "all_except_endgame",
        "small_key_shuffle": "any_world",
    }

    def test_requirement(self):
        self.collect_by_name(["Broom", "Small Key (Street)", "Temple of the Seeing One Statue"])
        self.assertTrue(self.can_reach_location("Temple of the Seeing One - Entrance Chest"))
        self.assertFalse(self.can_reach_location("Temple of the Seeing One - Boss Chest"))
        self.assertFalse(self.can_reach_location("Temple of the Seeing One - After Statue Left Chest"))
        self.assertFalse(self.can_reach_region("Overworld post windmill"))

        keys = self.get_items_by_name("Small Key (Temple of the Seeing One)")

        self.collect(keys[0])
        self.assertFalse(self.can_reach_location("Temple of the Seeing One - Boss Chest"))
        self.assertFalse(self.can_reach_location("Temple of the Seeing One - After Statue Left Chest"))
        self.assertFalse(self.can_reach_region("Overworld post windmill"))

        self.collect(keys[1])
        self.assertFalse(self.can_reach_location("Temple of the Seeing One - Boss Chest"))
        self.assertFalse(self.can_reach_location("Temple of the Seeing One - After Statue Left Chest"))
        self.assertFalse(self.can_reach_region("Overworld post windmill"))

        self.collect_by_name("Nexus Gate (Young Town)")
        self.assertFalse(self.can_reach_location("Temple of the Seeing One - Boss Chest"))
        self.assertFalse(self.can_reach_location("Temple of the Seeing One - After Statue Left Chest"))
        self.assertTrue(self.can_reach_region("Overworld post windmill"))

        self.collect(keys[2])
        self.assertTrue(self.can_reach_location("Temple of the Seeing One - Boss Chest"))
        self.assertTrue(self.can_reach_location("Temple of the Seeing One - After Statue Left Chest"))
        self.assertTrue(self.can_reach_region("Overworld post windmill"))


class TestBedroomKeysWithSuburbGateOpen(AnodyneTestBase):
    options = {
        "split_windmill": "true",
        "custom_nexus_gates_open": ["Suburb"],
        "small_key_shuffle": "any_world",
    }

    def test_requirement(self):
        self.collect_by_name(["Broom", "Small Key (Street)", "Temple of the Seeing One Statue"])
        self.assertTrue(self.can_reach_location("Temple of the Seeing One - Entrance Chest"))
        self.assertFalse(self.can_reach_location("Temple of the Seeing One - Boss Chest"))
        self.assertFalse(self.can_reach_location("Temple of the Seeing One - After Statue Left Chest"))
        self.assertTrue(self.can_reach_region("Overworld post windmill"))

        keys = self.get_items_by_name("Small Key (Temple of the Seeing One)")

        self.collect(keys[0])
        self.assertFalse(self.can_reach_location("Temple of the Seeing One - Boss Chest"))
        self.assertFalse(self.can_reach_location("Temple of the Seeing One - After Statue Left Chest"))
        self.assertTrue(self.can_reach_region("Overworld post windmill"))

        self.collect(keys[1])
        self.assertFalse(self.can_reach_location("Temple of the Seeing One - Boss Chest"))
        self.assertFalse(self.can_reach_location("Temple of the Seeing One - After Statue Left Chest"))
        self.assertTrue(self.can_reach_region("Overworld post windmill"))

        self.collect(keys[2])
        self.assertTrue(self.can_reach_location("Temple of the Seeing One - Boss Chest"))
        self.assertTrue(self.can_reach_location("Temple of the Seeing One - After Statue Left Chest"))
        self.assertTrue(self.can_reach_region("Overworld post windmill"))


class TestBedroomKeysWithInternalGateOpen(AnodyneTestBase):
    options = {
        "split_windmill": "true",
        "custom_nexus_gates_open": ["Bedroom exit"],
        "small_key_shuffle": "any_world",
    }

    def test_requirement(self):
        self.collect_by_name("Broom")
        self.assertTrue(self.can_reach_location("Temple of the Seeing One - Entrance Chest"))
        self.assertTrue(self.can_reach_location("Temple of the Seeing One - Boss Chest"))
        self.assertFalse(self.can_reach_location("Temple of the Seeing One - After Statue Left Chest"))
        self.assertFalse(self.can_reach_region("Overworld post windmill"))

        self.collect_by_name(["Temple of the Seeing One Statue"])
        self.assertTrue(self.can_reach_location("Temple of the Seeing One - Boss Chest"))
        self.assertTrue(self.can_reach_location("Temple of the Seeing One - After Statue Left Chest"))
        self.assertFalse(self.can_reach_region("Overworld post windmill"))

        keys = self.get_items_by_name("Small Key (Temple of the Seeing One)")

        self.collect(keys[0])
        self.assertTrue(self.can_reach_location("Temple of the Seeing One - Boss Chest"))
        self.assertTrue(self.can_reach_location("Temple of the Seeing One - After Statue Left Chest"))
        self.assertFalse(self.can_reach_region("Overworld post windmill"))

        self.collect(keys[1])
        self.assertTrue(self.can_reach_location("Temple of the Seeing One - Boss Chest"))
        self.assertTrue(self.can_reach_location("Temple of the Seeing One - After Statue Left Chest"))
        self.assertFalse(self.can_reach_region("Overworld post windmill"))

        self.collect(keys[2])
        self.assertTrue(self.can_reach_location("Temple of the Seeing One - Boss Chest"))
        self.assertTrue(self.can_reach_location("Temple of the Seeing One - After Statue Left Chest"))
        self.assertTrue(self.can_reach_region("Overworld post windmill"))
