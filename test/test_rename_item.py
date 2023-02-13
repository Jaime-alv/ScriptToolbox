import unittest

from script.rename_items import Constant, FileStart, RenameItems


class TestRenameItem(unittest.TestCase):
    basedir: str = "/home/jaime/proyectos/Scripts/Global/test/example"

    base: RenameItems = RenameItems(Constant(), FileStart, basedir)

    folder: str = "/home/jaime/proyectos/Scripts/Global/test/example"

    def test_tuple(self):
        self.assertTupleEqual(tuple([x.value for x in FileStart]), ("IMG-", "VID-"))
        self.assertTupleEqual(
            self.base.grab_starting_strings(FileStart), ("IMG-", "VID-")
        )

    def test_clean_name(self):
        self.assertEqual(self.base.strip_string("VID-44"), "44")
        self.assertEqual(self.base.strip_string("IMG-44"), "44")
        self.assertEqual(self.base.strip_string("VD-44"), "VD-44")
        self.assertEqual(self.base.strip_string("44"), "44")

    def test_constant(self):
        self.assertEqual(Constant().NEW_FILE, "_")
