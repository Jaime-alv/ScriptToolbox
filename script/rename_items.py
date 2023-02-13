# Copyright (C) 2023 Jaime Alvarez
# MIT License
"""Script for renaming files from some starting string."""
import os
import re
import sys
from enum import Enum
from pathlib import Path
from typing import Iterable, NamedTuple, NoReturn


class FileStart(Enum):
    """All start strings reside here."""

    CASE_ONE = "IMG-"
    CASE_TWO = "VID-"


class Constant(NamedTuple):
    """General constants."""

    NEW_FILE: str = "_"
    SUBSTITUTE_WITH: str = ""


class RenameItems:
    """Main process."""

    counter: int = 0
    all_files: int = 0

    def __init__(
        self, constant: Constant, enum_strings: FileStart, filepath: str = ""
    ) -> None:
        """Initialize process and check everything is OK."""
        self.constant = constant
        self.start: tuple = self.grab_starting_strings(enum_strings)
        self.filepath: str = filepath

        if self.__check_folder_integrity():
            self.dir_content: Iterable[Path] = self._grab_files(Path(self.filepath))
            Utils.count_files(self.all_files, self.filepath)
        else:
            Utils.launch_exit("Error.\nPress Enter key to continue...")

    def __check_folder_integrity(self) -> bool:
        """Call functions for checking several integrity checks."""
        folder: Path = Path(self.filepath)
        return all(
            (
                self._folder_not_blank(),
                self._check_folder_existence(folder),
                self._folder_not_empty(folder),
            )
        )

    @staticmethod
    def grab_starting_strings(enum_strings: FileStart) -> tuple:
        """Return a tuple with all elements to check as starting string."""
        return tuple(x.value for x in enum_strings)  # type: ignore

    def _folder_not_empty(self, folder: Path) -> bool:
        """Check folder include at least one file inside."""
        self.all_files = len(list(self._grab_files(folder)))
        return self.all_files > 0

    def _folder_not_blank(self) -> bool:
        """Check filepath is not an empty string."""
        return self.filepath != ""

    @staticmethod
    def _check_folder_existence(folder: Path) -> bool:
        """Check if folder exists and it's a working directory."""
        return folder.exists() and folder.is_dir()

    @staticmethod
    def _grab_files(filepath: Path) -> Iterable[Path]:
        """Filter files inside a directory."""
        return filter(lambda x: x.is_file(), filepath.glob("*"))

    def filter_folder_by_name(self) -> Iterable[Path]:
        """Filter folder files with a helper function."""
        return filter(self._filter_helper_function, self.dir_content)

    def _filter_helper_function(self, file: Path) -> bool:
        """Return boolean value if file starts with elements from FileStart class.

        Args:
            file (Path): filepaths of files

        Returns:
            bool: boolean value
        """
        return file.name.startswith(self.start)

    def iterate_filtered_files(self, filter_items: Iterable[Path]) -> str:
        """Iterate through an iterable with all files you want to rename.

        Args:
            filter_items (Iterable[Path]): Iterable

        Returns:
            str: final result from operation
        """
        files: list[str] = [x.name for x in filter_items]
        for file in files:
            self._rename_file(file)
        return self.renamed_elements()

    def _rename_file(self, file: str) -> None:
        """Rename file and add one to global counter.

        Args:
            file (str): file name without path
        """
        old_file = f"{self.filepath}/{file}"
        new_file: str = self.conform_filepath(file)
        os.rename(old_file, new_file)
        self.counter += 1

    def renamed_elements(self) -> str:
        """Return result of operation."""
        return f"{self.counter} elements renamed."

    def strip_string(self, file: str) -> str:
        """Replace FileStart elements with nothing ""."""
        join_tuple = "|".join(self.start)
        return re.sub(join_tuple, self.constant.SUBSTITUTE_WITH, file)

    def conform_filepath(self, file: str) -> str:
        """Rename file and conform absolute path for file.

        If a file with the same name exists, give a different name with a new
        character from Constants.

        Args:
            file (str): file name without path

        Returns:
            str: absolute path
        """
        file_name: str = self.strip_string(file)
        new_filepath: str = f"{self.filepath}/{file_name}"
        if Path(new_filepath).exists():
            file_name: str = self.substitute_end_dot(file)
            return f"{self.filepath}/{file_name}"
        return new_filepath

    def substitute_end_dot(self, string: str) -> str:
        """Substitute end dot with underscore dot so there are no identical files."""
        return re.sub("(.)([a-z]+)$", f"{self.constant.NEW_FILE}.\\2", string)

    def __call__(self) -> str:
        """Run the process if all checks are OK."""
        files = self.filter_folder_by_name()
        return self.iterate_filtered_files(files)

    def __repr__(self) -> str:
        """Show result of operation."""
        return self.__call__()


class Utils:
    """Helper functions."""

    @staticmethod
    def launch_exit(message: str = "Press Enter key to continue...") -> NoReturn:
        """Launch exit sequence."""
        print(message)
        input()
        sys.exit()

    @staticmethod
    def count_files(items: int, directory: str) -> None:
        """Show how many files are inside a directory."""
        print(f"{items} files inside {directory}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        temp: str = sys.argv[1]
    else:
        temp: str = input("Input folder: ")
    print(RenameItems(constant=Constant(), enum_strings=FileStart, filepath=temp))  # type: ignore
    Utils.launch_exit()
