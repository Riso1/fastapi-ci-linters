import logging
import sys


class LevelFileHandler(logging.Handler):
    """
    Обработчик, который записывает сообщения в файл,
    соответствующий уровню логирования.
    """

    LEVEL_TO_FILE = {
        logging.DEBUG: "calc_debug.log",
        logging.INFO: "calc_info.log",
        logging.WARNING: "calc_warning.log",
        logging.ERROR: "calc_error.log",
        logging.CRITICAL: "calc_critical.log",
    }

    def emit(self, record: logging.LogRecord) -> None:
        """
        Записывает лог в файл, соответствующий его уровню.
        """
        log_filename = self.LEVEL_TO_FILE.get(record.levelno)

        if log_filename is None:
            return

        log_message = self.format(record)

        with open(log_filename, "a", encoding="utf-8") as log_file:
            log_file.write(log_message + "\n")


def get_logger(name):
    """
    Создает и возвращает логгер с двумя обработчиками:
    - вывод в stdout;
    - запись в файл по уровню сообщения.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        fmt="%(levelname)s | %(name)s | %(asctime)s | %(lineno)d | %(message)s"
    )

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)

    level_file_handler = LevelFileHandler()
    level_file_handler.setLevel(logging.DEBUG)
    level_file_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.addHandler(level_file_handler)

    return logger