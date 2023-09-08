# Copyright (C) 2023 Jaime Alvarez
# MIT License
"""Rename two folders automatically back and forth."""
import argparse
import logging
import os
from pathlib import Path
from typing import NamedTuple


class Constants(NamedTuple):
    """Class system with constants."""

    # original folder name
    FOLDER: str = ""
    # surname used for original folder
    DEFAULT: str = "original"
    # alternative name
    ALT: str = "alt"
    # where to look for FOLDER
    WORKING_DIRECTORY: str = ""
    # join character script uses for rename
    JOIN: str = "_"

    def new(self, arg_parser: argparse.ArgumentParser, cwd: str) -> "Constants":
        """Create a new Constant tuple with the arguments from the command line.

        Args:
            arg_parser (argparse.ArgumentParser): Command line arguments
            cwd (str): Current working directory

        Returns:
            Constants: Inmutable class with settings
        """
        parser = arg_parser.parse_args()
        folder: str = parser.folder
        if parser.path:
            folder_path: str = parser.path
        else:
            folder_path: str = cwd
        if parser.join:
            folder_join: str = parser.join
        else:
            folder_join: str = self.JOIN
        if parser.default:
            folder_default_name = parser.default
        else:
            folder_default_name = self.DEFAULT
        if parser.alternative:
            folder_alternative_name = parser.alternative
        else:
            folder_alternative_name = self.ALT
        cte = Constants(
            FOLDER=folder,
            DEFAULT=folder_default_name,
            ALT=folder_alternative_name,
            WORKING_DIRECTORY=folder_path,
            JOIN=folder_join,
        )
        return cte


class RenameFolder:
    """Main script."""

    def __init__(self, constant: Constants) -> None:
        """Load constants variables."""
        self.constant = constant
        self.home: str = self.constant.WORKING_DIRECTORY
        self.base: str = self.conform_home(self.constant.FOLDER)
        self.default: str = self.conform_path(self.constant.DEFAULT)
        self.alt: str = self.conform_path(self.constant.ALT)

    def rename_folder(self) -> str:
        """If folder with DEFAULT exists => script launched at least once.
        Can make the change back and forth.

        If folder with ALT exists => make the change to original folder.

        Else => rename folder and create another one.

        Raises:
            FileNotFoundError: If there is no folder with name FOLDER, raise
            an exception message

        Returns:
            str | Exception: Good result or exception.
        """
        if Path(self.default).exists():
            return self.__rename_folder(self.alt, self.default, self.constant.DEFAULT)
        if Path(self.alt).exists():
            return self.__rename_folder(self.default, self.alt, self.constant.ALT)
        if Path(self.base).exists():
            Path(self.alt).mkdir(exist_ok=True)
            self.__rename_folder(self.default, self.alt, self.constant.ALT)
            return f"Create new /{self.constant.FOLDER} at {self.constant.WORKING_DIRECTORY}"
        raise FileNotFoundError

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


def error_message(constants: Constants) -> str:
    """Format a human readable message.
    Outputs a message with folder and path names so user can
    take necessary actions.

    Args:
        constants (Constants): Variables passed when running
        the script.

    Returns:
        str: formatted message
    """
    # fmt:off
    message: str = (
        f"\n {{\n    folder: {constants.FOLDER},\n    path: {constants.WORKING_DIRECTORY}\n }}"
    )
    formatted_message: str = f"Folder not found: {message}"
    return formatted_message


def parse_command_line_arguments(cwd: str) -> argparse.ArgumentParser:
    """Generate command line parser and all info about the different options
    there are.

    Args:
        cwd (str): Current working directory

    Returns:
        argparse.ArgumentParser: All arguments needed.
    """
    parser = argparse.ArgumentParser(
        description="Rename two folders automatically, back and forth while preserving content."
    )
    parser.add_argument("folder", help="Target folder to rename", type=str)
    parser.add_argument(
        "-p",
        "--path",
        help=(
            f"Path where target folder is [absolute or relative]. Default 'working directory' {cwd}"
        ),
        type=str,
    )
    parser.add_argument(
        "-j",
        "--join",
        help="Joining character between folder. Choose between _ - or #. Default _",
        type=str,
        choices=["_", "-", "#"],
    )
    parser.add_argument(
        "-d",
        "--default",
        help="Surname append for original folder. Default 'original'",
        type=str,
    )
    parser.add_argument(
        "-a",
        "--alternative",
        help="Surname append for new folder. Default 'alt'",
        type=str,
    )
    return parser


if __name__ == "__main__":
    FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=20, format=FORMAT, datefmt="%Y/%m/%d %H:%M:%S")
    current_working_directory: str = os.getcwd()
    parse_arguments = parse_command_line_arguments(current_working_directory)
    settings: Constants = Constants().new(
        arg_parser=parse_arguments, cwd=current_working_directory
    )
    try:
        logging.info(RenameFolder(settings).rename_folder())
    except FileNotFoundError:
        log_message = error_message(settings)
        logging.error(log_message)
