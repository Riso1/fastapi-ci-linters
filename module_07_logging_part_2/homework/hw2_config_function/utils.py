from module_07_logging_part_2.homework.hw3_level_file_handler.logger_helper import get_logger
from typing import Union, Callable
from operator import sub, mul, truediv, add

logger = get_logger(__name__)

OPERATORS = {
    '+': add,
    '-': sub,
    '*': mul,
    '/': truediv,
}

Numeric = Union[int, float]


def string_to_operator(value: str) -> Callable[[Numeric, Numeric], Numeric]:
    """
    Convert string to arithmetic function
    :param value: basic arithmetic operator
    """
    if not isinstance(value, str):
        logger.error("Wrong operator type: %s", value)
        raise ValueError("wrong operator type")

    if value not in OPERATORS:
        logger.error("Wrong operator value: %s", value)
        raise ValueError("wrong operator value")

    return OPERATORS[value]