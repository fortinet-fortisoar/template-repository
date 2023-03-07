import requests
from connectors.core.connector import get_logger, ConnectorError
from .utils import invoke_rest_endpoint
from .constants import LOGGER_NAME
from .constants import *

logger = get_logger(LOGGER_NAME)


def get_jobs(config, params, *args, **kwargs):
    endpoint = JOBS_ENDPOINT
    request_body = {}

    api_response = invoke_rest_endpoint(config, endpoint, 'GET', request_body)

    logger.info("RESPONSE={}".format(api_response))
    return api_response
