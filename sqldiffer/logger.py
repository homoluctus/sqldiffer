import logging
from typing import Union


def get_logger(
        name: str = __name__,
        level: Union[str, int] = logging.INFO) -> logging.Logger:
    """Get logger

    Args:
        name (str, optional): Defaults to __name__.
        level (Union[str, int], optional): Defaults to logging.INFO.

    Returns:
        logging.Logger:
    """

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger
