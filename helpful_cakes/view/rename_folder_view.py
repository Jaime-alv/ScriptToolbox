# Copyright (C) 2023 Jaime Alvarez
# MIT License
"""Text display in CLI"""
import argparse
import logging

from model.rename_folder_model import Constants


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


def error_message(folder: str, file_path: str) -> str:
    """Format a human readable message.
    Outputs a message with folder and path names so user can
    take necessary actions.

    Args:
        folder (str): folder name
        file_path (str): folder path

    Returns:
        str: formatted message
    """
    # fmt:off
    message: str = (
        f"\n {{\n    folder: {folder},\n    path: {file_path}\n }}"
    )
    formatted_message: str = f"Folder not found: {message}"
    return formatted_message


def success(folder: str) -> None:
    """Logs success operation.

    Args:
        folder (str): success message.
    """
    logging.info(folder)


def failure(settings: Constants) -> None:
    """Logs error message to user.

    Args:
        settings (Constants): Current settings. Looks specifically
        for folder name and path.
    """
    log_message = error_message(settings.FOLDER, settings.WORKING_DIRECTORY)
    logging.error(log_message)
