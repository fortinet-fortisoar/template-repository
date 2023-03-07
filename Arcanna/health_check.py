from .utils import invoke_rest_endpoint
from connectors.core.connector import get_logger, ConnectorError
from .constants import *

logger = get_logger(LOGGER_NAME)
from .utils import invoke_rest_endpoint

def health_check(config=None, *args, **kwargs):
    auth_endpoint = HEALTH_ENDPOINT
    logger.info("Calling healthcheck")
    invoke_rest_endpoint(config, auth_endpoint, 'GET')

    return 'Connector is Available'
