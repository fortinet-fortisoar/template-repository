from connectors.core.connector import Connector
from connectors.core.connector import get_logger, ConnectorError
from django.utils.module_loading import import_string
from .builtins import *
from .constants import LOGGER_NAME
from .health_check import health_check
logger = get_logger(LOGGER_NAME)

class ArcannaConnector(Connector):

    def dev_execute(self, config, operation, params, *args, **kwargs):
        parent_path = __name__.split('.')[:-1]
        parent_path.extend([operation, operation])
        func = import_string('.'.join(parent_path))
        return func(config, params)

    def execute(self, config, operation, params, *args, **kwargs):
        logger.info("Executing {}".format(operation))
        return supported_operations.get(operation)(config, params)

    def check_health(self, config=None, *args, **kwargs):
        return health_check(config, *args, **kwargs)
