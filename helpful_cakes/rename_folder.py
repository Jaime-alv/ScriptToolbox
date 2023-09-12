# Copyright (C) 2023 Jaime Alvarez
# MIT License
"""Rename two folders automatically back and forth."""
import view.rename_folder_view as rfv
from model.rename_folder_model import Constants, RenameFolder
from utils.common_functions import get_cwd
from view.logger import set_logger

if __name__ == "__main__":
    set_logger()
    current_working_directory: str = get_cwd()
    parse_arguments = rfv.parse_command_line_arguments(current_working_directory)
    settings: Constants = Constants().new(
        arg_parser=parse_arguments, cwd=current_working_directory
    )

    try:
        rfv.success(RenameFolder(settings).rename_folder())
    except FileNotFoundError:
        rfv.failure(settings)
