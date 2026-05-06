dict_config = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "fileFormatter": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%dT%H:%M:%S",
        },
        "consoleFormatter": {
            "format": "%(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%dT%H:%M:%S",
        },
    },

    "handlers": {
        "consoleHandler": {
            "class": "logging.StreamHandler",
            "level": "WARNING",
            "formatter": "consoleFormatter",
            "stream": "ext://sys.stdout",
        },
        "fileHandler": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "fileFormatter",
            "filename": "logfile.log",
            "encoding": "utf-8",
        },
    },

    "root": {
        "level": "DEBUG",
        "handlers": ["consoleHandler"],
    },

    "loggers": {
        "appLogger": {
            "level": "DEBUG",
            "handlers": ["consoleHandler", "fileHandler"],
            "propagate": False,
        },
    },
}