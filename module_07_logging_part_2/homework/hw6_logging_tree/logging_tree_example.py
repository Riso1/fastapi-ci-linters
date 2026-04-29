import logging.config

import logging_tree

from dict_config import dict_config


def write_logging_tree_to_file() -> None:
    """
    Применяет конфигурацию логирования
    и записывает дерево логгеров в файл logging_tree.txt.
    """
    logging.config.dictConfig(dict_config)

    tree_output = logging_tree.format.build_description()

    with open("logging_tree.txt", "w", encoding="utf-8") as file:
        file.write(tree_output)


if __name__ == "__main__":
    write_logging_tree_to_file()