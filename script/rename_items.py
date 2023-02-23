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

    def __init__(
        self, constant: Constant, enum_strings: FileStart, filepath: str = ""
    ) -> None:
        """Initialize process and check everything is OK."""
        self.constant = constant
        self.start: tuple = self.grab_starting_strings(enum_strings)
        self.filepath: str = filepath
        self.all_files: int = self.count_items(self.filepath)
        self.dir_content: Iterable[Path] = self.grab_files(
            Path(self.filepath), self.start
        )

        if not self.__check_folder_integrity():
            Utils.launch_exit("Error.")
        Utils.broadcast_message((self.count_files(self.all_files, self.filepath)))

    def __check_folder_integrity(self) -> bool:
        """Call functions for checking several integrity checks."""
        folder: Path = Path(self.filepath)
        return all(
            (
                self._folder_not_blank(),
                self._check_folder_existence(folder),
                self._folder_not_empty(),
            )
        )

    @staticmethod
    def grab_starting_strings(enum_strings: FileStart) -> tuple:
        """Return a tuple with all elements to check as starting string."""
        return tuple(x.value for x in enum_strings)  # type: ignore

    @staticmethod
    def count_items(filepath: str) -> int:
        """Count number of files inside a folder.

        Exclude folders inside parent folder.
        Args:
            filepath (str): absolute path

        Returns:
            int: total number of files
        """
        return len(list(filter(lambda file: file.is_file(), Path(filepath).iterdir())))

    def _folder_not_empty(self) -> bool:
        """Check folder include at least one file inside."""
        return self.all_files > 0

    def _folder_not_blank(self) -> bool:
        """Check filepath is not an empty string."""
        return self.filepath != ""

    @staticmethod
    def _check_folder_existence(folder: Path) -> bool:
        """Check if folder exists and it's a working directory."""
        return folder.exists() and folder.is_dir()

    @staticmethod
    def grab_files(filepath: Path, start: tuple[str]) -> Iterable[Path]:
        """Filter files inside a directory."""
        return filter(
            lambda file: file.is_file() and file.name.startswith(start),
            filepath.iterdir(),
        )

    def iterate_filtered_files(self, filter_items: Iterable[Path]) -> str:
        """Iterate through an iterable with all files you want to rename.

        Args:
            filter_items (Iterable[Path]): Iterable

        Returns:
            str: final result from operation
        """
        files: list[str] = [x.name for x in filter_items]
        total_items: int = len(files)
        for file in files:
            self._rename_file(file)
            self.add_one_item(total_items)
        return self.renamed_elements()

    def _rename_file(self, file: str) -> None:
        """Rename file and add one to global counter.

        Args:
            file (str): file name without path
        """
        old_file = f"{self.filepath}/{file}"
        new_file: str = self.conform_filepath(file)
        os.rename(old_file, new_file)

    def add_one_item(self, total: int) -> None:
        """Add one item to counter and broadcast current item.

        Args:
            total (int): Total number of items
        """
        self.counter += 1
        message: str = self.log_info(self.counter, total)
        Utils.broadcast_message(message)

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

    def __repr__(self) -> str:
        """Show result of operation."""
        return self.call_process(self.dir_content)

    def call_process(self, folder: Iterable[Path]) -> str:
        """Run the process if all checks are OK."""
        return self.iterate_filtered_files(folder)

    @staticmethod
    def count_files(items: int, directory: str) -> str:
        """Show how many files are inside a directory."""
        return f"{items} files inside {directory}"

    @staticmethod
    def log_info(item: int, total: int) -> str:
        """Show which file is being renamed."""
        return f"Renaming item: {item}/{total}"


class Utils:
    """Helper functions."""

    @staticmethod
    def launch_exit(message: str = "") -> NoReturn:
        """Launch exit sequence."""
        cont: str = "Press Enter key to continue..."
        if message != "":
            final_message: str = f"{message}\n{cont}"
        else:
            final_message: str = cont
        Utils.broadcast_message(final_message)
        input()
        sys.exit()

    @staticmethod
    def broadcast_message(message: str) -> None:
        """Print a message or log it."""
        print(message)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        temp: str = sys.argv[1]
    else:
        temp: str = input("Input folder: ")
    print(RenameItems(constant=Constant(), enum_strings=FileStart, filepath=temp))  # type: ignore
    Utils.launch_exit()
