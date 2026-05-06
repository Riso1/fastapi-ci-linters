dict_config = {
    "version": 1,
    "disable_existing_loggers": False,

    "filters": {
        "ascii_filter": {
            "()": "ascii_filter.AsciiFilter",
        }
    },

    "formatters": {
        "default_formatter": {
            "format": "%(levelname)s | %(name)s | %(asctime)s | %(lineno)d | %(message)s"
        }
    },

    "handlers": {
        "stdout_handler": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "default_formatter",
            "stream": "ext://sys.stdout",
            "filters": ["ascii_filter"],
        },

        "utils_file_handler": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "INFO",
            "formatter": "default_formatter",
            "filename": "utils.log",
            "when": "H",
            "interval": 10,
            "backupCount": 1,
            "encoding": "utf-8",
            "filters": ["ascii_filter"],
        },
    },

    "loggers": {
        "app": {
            "level": "DEBUG",
            "handlers": ["stdout_handler"],
            "propagate": False,
        },

        "utils": {
            "level": "DEBUG",
            "handlers": ["utils_file_handler"],
            "propagate": False,
        },
    }
}