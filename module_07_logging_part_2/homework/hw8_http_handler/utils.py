import logging
from typing import Union, Callable
from operator import sub, mul, truediv, add

logger = logging.getLogger("utils")

OPERATORS = {
    "+": add,
    "-": sub,
    "*": mul,
    "/": truediv,
}

Numeric = Union[int, float]


def string_to_operator(value: str) -> Callable[[Numeric, Numeric], Numeric]:
    logger.info("Converting operator: %s", value)

    if not isinstance(value, str):
        logger.error("Wrong operator type: %s", value)
        raise ValueError("wrong operator type")

    if value not in OPERATORS:
        logger.error("Wrong operator value: %s", value)
        raise ValueError("wrong operator value")

    return OPERATORS[value]