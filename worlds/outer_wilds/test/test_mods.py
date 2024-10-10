from . import OuterWildsTestBase


class TestHN1(OuterWildsTestBase):
    options = {
        "enable_hn1_mod": 1
    }

    def test_hn1(self):
        self.assertEqual(self.getLocationCount(), 109)  # 87(+2V) base game + 20 HN1 locations


class TestHN1Logsanity(OuterWildsTestBase):
    options = {
        "enable_hn1_mod": 1,
        "logsanity": 1
    }

    def test_hn1_logsanity(self):
        # 87(+2V) base game default locations + 176 base game logsanity locations +
        # 20 HN1 default locations + 41 HN1 logsanity locations
        self.assertEqual(self.getLocationCount(), 326)

