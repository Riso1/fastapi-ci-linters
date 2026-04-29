import logging


class AsciiFilter(logging.Filter):
    """
    Фильтр пропускает только сообщения,
    состоящие из ASCII-символов.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        message = record.getMessage()
        return message.isascii()