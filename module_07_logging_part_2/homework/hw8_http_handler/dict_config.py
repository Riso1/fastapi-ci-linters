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

        "http_handler": {
            "class": "logging.handlers.HTTPHandler",
            "level": "INFO",
            "host": "127.0.0.1:5000",
            "url": "/log",
            "method": "POST",
        },
    },

    "loggers": {
        "app": {
            "level": "DEBUG",
            "handlers": ["stdout_handler", "http_handler"],
            "propagate": False,
        },

        "utils": {
            "level": "DEBUG",
            "handlers": ["http_handler"],
            "propagate": False,
        },
    }
}