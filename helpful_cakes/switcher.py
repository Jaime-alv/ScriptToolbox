# Copyright (C) 2022 Jaime Alvarez
# MIT License
"""Kube forwarder script."""
import filecmp
import os
from pathlib import Path
from typing import NamedTuple


class Constants(NamedTuple):
    """Constants."""

    # original file created by kubernetes
    ORIGIN: str = ".kube/config"
    # file kube forwarder read
    DESTINY: str = ".kube/config_abs"
    # absolute path to WSL2
    WSL_PATH: str = r"\\wsl$\Ubuntu"
    # folder location in WSL2
    HOME: str = "HOME"


class Switcher:
    """Main script."""

    def __init__(self, constant: Constants):
        """Conform absolute paths."""
        self.constant = constant
        self.path: str = constant.WSL_PATH
        self.home = self.__get_home_directory(self.constant.HOME)
        self.origin: Path = self.__absolute_path(self.constant.ORIGIN)
        self.destiny: Path = self.__absolute_path(self.constant.DESTINY)
        self.origin_file: list[str] = []

    def __call__(self) -> str:
        """Populate destiny file with correct path."""
        if not self.__make_checks():
            return "Failed operation."
        try:
            self.origin_file: list[str] = self.read_text(self.origin)
        except FileNotFoundError:
            return "Origin file not found."

        return self.populate_new_data()

    def __repr__(self) -> str:
        """Show result from operation."""
        return self.__call__()

    def __absolute_path(self, folder_path: str) -> Path:
        """Return absolute Path item for a folder.

        Args:
            folder_path (str): folder to work with

        Returns:
            Path: path item
        """
        return Path(f"{self.home}/{folder_path}")

    @staticmethod
    def __get_home_directory(home: str) -> str:
        """Get base directory to work from.

        Args:
            home (str): UNIX directory

        Returns:
            str: absolute path
        """
        return str(os.getenv(home))

    def __make_checks(self) -> bool:
        """Validate integrity and check everything is OK.

        Returns:
            bool: boolean value
        """
        checks: list[bool] = [
            self.check_existence(self.destiny),
            self.check_integrity(self.destiny),
            self.check_same_data(self.destiny),
        ]
        return all(checks)

    @staticmethod
    def check_existence(file: Path) -> bool:
        """Check if file exists and create a new one if needed at set path.

        Args:
            file (Path): where the file is

        Returns:
            bool: boolean value
        """
        if not file.exists():
            file.touch()
        return True

    @staticmethod
    def compare_files(file1: Path, file2: Path) -> bool:
        """Compare both files and their content.

        Args:
            file1 (Path): Path to file 1
            file2 (Path): Path to file to compare against

        Returns:
            bool: boolean value
        """
        return filecmp.cmp(file1, file2)

    @staticmethod
    def read_text(file: Path) -> list[str]:
        """Read text from file in path and split it in lines.

        Args:
            file (Path): file path

        Returns:
            list[str]: content from file
        """
        return file.read_text(encoding="utf-8").splitlines()

    def get_new_data(self, to_file: list[str]) -> list[str]:
        """Populate file with new metadata.

        Avoid overwrite of certificates

        Args:
            to_file (list[str]): file content from destiny file

        Returns:
            list[str]: new content metadata
        """
        avoid: tuple[str, str, str] = (
            "certificate-authority",
            "client-certificate",
            "client-key",
        )

        for index, line in enumerate(self.origin_file):
            if to_file[index] != line and not line.strip().startswith(avoid):
                to_file[index] = line

        return to_file

    def check_same_data(self, destiny_path: Path) -> bool:
        """Check data against file.

        Args:
            destiny_path (Path): path to file

        Returns:
            bool: boolean value
        """
        if not self.compare_files(self.origin, destiny_path):
            destiny: list[str] = self.read_text(destiny_path)
            data: list[str] = self.get_new_data(destiny)
            self.write_data(self.join_one_line(data), destiny_path)
        return True

    @staticmethod
    def write_data(data: str, to_file: Path) -> None:
        """Clear data and write new data to file.

        Args:
            data (str): data to write
            to_file (Path): path to file
        """
        to_file.write_text("")
        to_file.write_text(data)

    def check_length(self, file2: Path) -> bool:
        """Compare length of two files and check if its higher than zero.

        Args:
            file2 (Path): path to file

        Returns:
            bool: boolean value
        """
        return 0 < self.get_text_length(self.origin) == self.get_text_length(file2)

    def check_integrity(self, file2: Path) -> bool:
        """Check if there are any errors in file.

        Args:
            file2 (Path): file to write to

        Returns:
            bool: boolean value
        """
        if not self.check_length(file2):
            origin_data = self.origin.read_text(encoding="utf-8")
            self.write_data(origin_data, file2)
        return True

    def get_text_length(self, file: Path) -> int:
        """Return length of file.

        Args:
            file (Path): file path

        Returns:
            int: number of lines in file
        """
        return len(self.read_text(file))

    @staticmethod
    def get_current_windows_path() -> str:
        """Conform a valid windows path for kube forwarder.

        Returns:
            str: valid address
        """
        return str(Path.resolve(Path(""))).replace("/", "\\")

    def get_key(self, current_path: str) -> dict[str, str]:
        """Write key dictionary with certificates and a valid windows path.

        Returns:
            dict[str, str]: certificate path
        """
        full_path: str = f"{self.path}{current_path}"
        keys: dict[str, str] = {
            "certificate-authority": f"{full_path}\\.minikube\\ca.crt",
            "client-certificate": f"{full_path}\\.minikube\\profiles\\minikube\\client.crt",
            "client-key": f"{full_path}\\.minikube\\profiles\\minikube\\client.key",
        }
        return keys

    def set_wsl_path(self, destiny: list[str], key: dict[str, str]) -> list[str]:
        """Set the new certificates with windows paths.

        Args:
            destiny (list[str]): destiny file content
            key (dict[str, str]): certificate with valid paths

        Returns:
            list[str]: new file
        """
        # fmt: off
        for index, line in enumerate(self.origin_file):
            if self.strip_line(line, "certificate-authority"):
                destiny[index] = f"    certificate-authority: {key['certificate-authority']}"
            if self.strip_line(line, "client-certificate"):
                destiny[index] = f"    client-certificate: {key['client-certificate']}"
            if self.strip_line(line, "client-key"):
                destiny[index] = f"    client-key: {key['client-key']}"

        return destiny

    @staticmethod
    def strip_line(line: str, start: str) -> bool:
        """Strip white spaces and check starting string.

        Args:
            line (str): string to clean and check
            start (str): starting string

        Returns:
            bool: boolean value
        """
        return line.strip().startswith(start)

    @staticmethod
    def join_one_line(data: list[str]) -> str:
        """Join list of strings to conform a valid string to write.

        Args:
            data (list[str]): list to join

        Returns:
            str: valid text
        """
        return "\n".join(data)

    def populate_new_data(self) -> str:
        """Logic component, build new data.

        Returns:
            str: result of operation
        """
        destiny_file: list[str] = self.read_text(self.destiny)
        current_path: str = self.get_current_windows_path()
        keys: dict[str, str] = self.get_key(current_path)
        data = self.set_wsl_path(destiny_file, keys)
        self.write_data(self.join_one_line(data), self.destiny)
        return "Success"


if __name__ == "__main__":
    print(Switcher(constant=Constants()))
