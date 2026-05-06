from logging.handlers import TimedRotatingFileHandler


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
            "stream": "ext://sys.stdout",
        },

        "level_file_handler": {
            "()": "logger_helper.LevelFileHandler",
            "level": "DEBUG",
            "formatter": "default_formatter",
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
            "handlers": ["utils_file_handler"],
            "propagate": False,
        },
    }
}