import os
import unittest
from pathlib import Path

from script.rename_folder import Constants as Cte
from script.rename_folder import RenameFolder as Rf

if not Path("./test/rename_folder/example_folder").exists():
    Path("./test/rename_folder/example_folder").mkdir(parents=True, exist_ok=True)


class TestRenameFolder(unittest.TestCase):
    def test_named_tuple(self):
        cte: Cte = Cte(".git")
        self.assertEqual(cte.FOLDER, ".git")

    def test_cwd(self):
        self.assertEqual(os.getcwd(), "/home/jaime/projects/Scripts/Global")

    def test_new_values_for_constant(self):
        cte: Cte = Cte(FOLDER=".m2", WORKING_DIRECTORY="none")
        self.assertEqual(cte.WORKING_DIRECTORY, "none")
        cte_default: Cte = Cte("git")
        self.assertEqual(
            cte_default.WORKING_DIRECTORY, ""
        )

    def test_existence_folder(self):
        cte = Cte(
            FOLDER="example_folder",
            WORKING_DIRECTORY="/home/jaime/projects/Scripts/Global/test/rename_folder",
        )
        folder: Rf = Rf(cte)
        self.assertEqual(
            folder.default,
            f"{cte.WORKING_DIRECTORY}/example_folder{cte.JOIN}{cte.DEFAULT}",
        )
        self.assertEqual(
            folder.alt,
            f"{cte.WORKING_DIRECTORY}/example_folder{cte.JOIN}{cte.ALT}",
        )

    def test_script_full_flow(self):
        cte = Cte(
            FOLDER="example_folder",
            WORKING_DIRECTORY="/home/jaime/projects/Scripts/Global/test/rename_folder",
        )
        original: str = f"{cte.WORKING_DIRECTORY}/example_folder{cte.JOIN}{cte.DEFAULT}"
        alternative: str = f"{cte.WORKING_DIRECTORY}/example_folder{cte.JOIN}{cte.ALT}"
        if Path(original).exists():
            Path(original).rmdir()
        if Path(alternative).exists():
            Path(alternative).rmdir()
        folder: Rf = Rf(cte)
        folder.rename_folder()
        self.assertTrue(
            Path(
                f"{cte.WORKING_DIRECTORY}/example_folder{cte.JOIN}{cte.DEFAULT}"
            ).exists()
        )

    def test_script(self):
        cte = Cte(
            FOLDER="example_folder",
            WORKING_DIRECTORY="/home/jaime/projects/Scripts/Global/test/rename_folder",
        )
        original: str = f"{cte.WORKING_DIRECTORY}/example_folder{cte.JOIN}{cte.DEFAULT}"
        alternative: str = f"{cte.WORKING_DIRECTORY}/example_folder{cte.JOIN}{cte.ALT}"
        folder: Rf = Rf(cte)
        if Path(original).exists():
            result: str = str(folder.rename_folder())
            self.assertEqual(result, f"{cte.DEFAULT.capitalize()} {cte.FOLDER} active!")
            self.assertTrue(Path(alternative).exists())
            self.assertFalse(Path(original).exists())
        if Path(alternative).exists():
            result: str = str(folder.rename_folder())
            self.assertEqual(result, f"{cte.ALT.capitalize()} {cte.FOLDER} active!")
            self.assertTrue(Path(original).exists())
            self.assertFalse(Path(alternative).exists())

    def test_absolute_path(self):
        demo_cte = Cte(WORKING_DIRECTORY="/home/jaime")
        self.assertTrue(Path(demo_cte.WORKING_DIRECTORY).exists())
        relative_cte = Cte(WORKING_DIRECTORY="./../")
        self.assertTrue(Path(relative_cte.WORKING_DIRECTORY).exists())
