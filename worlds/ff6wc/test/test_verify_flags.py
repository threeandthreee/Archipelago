import unittest
from worlds.ff6wc.Options import verify_flagstring


class TestVerifyFlags(unittest.TestCase):
    def test_ok_flags(self) -> None:
        verify_flagstring(["-i", "x"])
        verify_flagstring([])

    def test_new_flags(self) -> None:
        """ These flags are from a newer version of Worlds Collide that isn't supported yet. """
        self.assertRaises(ValueError, verify_flagstring, ["-i", "x", "-chrm", "0", "0"])

    def test_bad_flags(self) -> None:
        self.assertRaises(ValueError, verify_flagstring, ["-i", "x", "-bkbkb00"])
