import unittest

from script.rename_folder import RenameFolder as RF


class TestRenameFolder(unittest.TestCase):
    base = RF()

    def test_existence(self):
        self.assertFalse(RF()._check_existence(".m2"))
        self.assertTrue(RF()._check_existence("default"))
        self.assertFalse(RF()._check_existence("Carrefour"))

    def test_string_form(self):
        self.assertEqual(RF().conform_path("test"), "/home/jaime/.m2 test")

    def test_base(self):
        self.assertEqual(RF().base, "/home/jaime/.m2")
        
    def test_fail(self):
        self.assertTrue((1 + 1 == 3))
