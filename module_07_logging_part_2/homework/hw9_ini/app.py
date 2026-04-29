import logging.config

from dict_config import dict_config

logging.config.dictConfig(dict_config)

logger = logging.getLogger("appLogger")

logger.debug("debug message")
logger.warning("warning message")
logger.error("error message")