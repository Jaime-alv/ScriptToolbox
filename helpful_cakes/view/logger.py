# Copyright (C) 2023 Jaime Alvarez
# MIT License
"""Set logging configuration options."""
import logging

FORMAT: str = "%(asctime)s - %(levelname)s - %(message)s"


def set_logger(level: int = 20) -> None:
    """Set logger format with an adequate level

    Args:
        level (int, optional): logger level. Defaults to 20.
    """
    logging.basicConfig(level=level, format=FORMAT, datefmt="%Y/%m/%d %H:%M:%S")
