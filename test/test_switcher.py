import unittest

from script.switcher import Switcher


class TestSwitcher(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(1 + 1, 2)

    def test_strip_line(self):
        self.assertTrue(Switcher.strip_line("  foo", "foo"))
        self.assertFalse(Switcher.strip_line("  foo", "grab"))
