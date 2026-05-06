import logging
import logging.config

from dict_config import dict_config
from utils import string_to_operator

logger = logging.getLogger("app")


def configure_logging() -> None:
    """
    Конфигурирует логирование с помощью словаря.
    """
    logging.config.dictConfig(dict_config)


def calc(args):
    logger.info("Arguments: %s", args)

    num_1 = args[0]
    operator = args[1]
    num_2 = args[2]

    try:
        num_1 = float(num_1)
    except ValueError:
        logger.exception("Error while converting number 1")
        return

    try:
        num_2 = float(num_2)
    except ValueError:
        logger.exception("Error while converting number 2")
        return

    operator_func = string_to_operator(operator)
    result = operator_func(num_1, num_2)

    logger.info("Result: %s", result)
    logger.info("%s %s %s = %s", num_1, operator, num_2, result)


if __name__ == "__main__":
    configure_logging()
    calc(["2", "+", "3"])