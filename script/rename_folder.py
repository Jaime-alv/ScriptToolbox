# Copyright (C) 2023 Jaime Alvarez
# MIT License
"""Rename two folders automatically back and forth."""
import os
from pathlib import Path
from typing import NamedTuple


class Constants(NamedTuple):
    """Class system with constants."""

    # original folder name
    FOLDER: str = ".m2"
    # surname used for original folder
    DEFAULT: str = "default"
    # alternative name
    ALT: str = "Carrefour"
    # where to look for FOLDER
    HOME: str = "HOME"
    # join character script uses for rename
    JOIN: str = "_"


class RenameFolder:
    """Main script."""

    def __init__(self, constant: Constants) -> None:
        """Load paths as string."""
        self.constant = constant
        self.home: str = self.__get_home_directory(self.constant.HOME)
        self.base: str = self.conform_home(self.constant.FOLDER)
        self.default: str = self.conform_path(self.constant.DEFAULT)
        self.alt: str = self.conform_path(self.constant.ALT)

    def _check_existence(self, surname: str) -> bool:
        """Check if a folder, with a certain extension, exists.

        /home/user/something {surname}
        Args:
            surname (str): folder extension

        Returns:
            bool: boolean value
        """
        return Path(self.conform_path(surname)).exists()

    @staticmethod
    def __get_home_directory(home: str) -> str:
        """Get base directory to work from.

        Args:
            home (str): UNIX directory

        Returns:
            str: absolute path
        """
        return str(os.getenv(home))

    def conform_path(self, surname: str) -> str:
        """Form a string with the absolute path to a folder.

        Args:
            surname (str): folder extension

        Returns:
            str: absolute path
        """
        return f"{self.base}{self.constant.JOIN}{surname}"

    def conform_home(self, folder: str) -> str:
        """Return absolute path to base folder.

        Args:
            folder (str): folder name

        Returns:
            str: path as string
        """
        return f"{self.home}/{folder}"

    def __rename_folder(self, target: str, rename_from: str, surname: str) -> str:
        """Rename two folders back and forth.

        First, rename base folder and append the surname.
        Second, rename the old folder so it can be active again.

        Args:
            target (str): current active folder
            rename_from (str): active folder when the script ends
            surname (str): new active folder

        Returns:
            str: which folder is active
        """
        os.rename(self.base, target)
        os.rename(rename_from, self.base)
        return self.achievement(surname, self.constant.FOLDER)

    @staticmethod
    def achievement(target: str, folder: str) -> str:
        """Format string with new active folder.

        Args:
            target (str): Surname of active folder

        Returns:
            str: result of operation
        """
        return f"{target.capitalize()} {folder} active!"

    def check_active(self) -> str:
        """Rename folder based on active folder.

        Returns:
            str: result of operation
        """
        if self._check_existence(self.constant.DEFAULT):
            return self.__rename_folder(self.alt, self.default, self.constant.DEFAULT)
        return self.__rename_folder(self.default, self.alt, self.constant.ALT)

    def __repr__(self) -> str:
        """Give user feedback."""
        return self.__call__()

    def __call__(self) -> str:
        """Start process and call to action."""
        return self.check_active()


if __name__ == "__main__":
    print(RenameFolder(constant=Constants()))
