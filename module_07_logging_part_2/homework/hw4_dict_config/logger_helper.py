import logging


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