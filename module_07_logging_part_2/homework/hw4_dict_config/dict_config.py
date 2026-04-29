import sys


dict_config = {
    "version": 1,
    "disable_existing_loggers": False,

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
            "stream": sys.stdout,
        },
        "level_file_handler": {
            "()": "logger_helper.LevelFileHandler",
            "level": "DEBUG",
            "formatter": "default_formatter",
        },
    },

    "loggers": {
        "app": {
            "level": "DEBUG",
            "handlers": ["stdout_handler", "level_file_handler"],
            "propagate": False,
        },
        "utils": {
            "level": "DEBUG",
            "handlers": ["stdout_handler", "level_file_handler"],
            "propagate": False,
        },
    }
}