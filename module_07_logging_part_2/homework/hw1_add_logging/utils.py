import logging
from typing import Union, Callable
from operator import sub, mul, truediv, add

logger = logging.getLogger(__name__)

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
    :param value: basic arithmetic function
    """
    if not isinstance(value, str):
        logger.error("wrong operator type: %s", value)
        raise ValueError("wrong operator type")

    if value not in OPERATORS:
        logger.error("wrong operator value: %s", value)
        raise ValueError("wrong operator value")

    return OPERATORS[value]
