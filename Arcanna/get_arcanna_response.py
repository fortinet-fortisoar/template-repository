from connectors.core.connector import get_logger, ConnectorError
from .constants import *
from .utils import invoke_rest_endpoint
logger = get_logger(LOGGER_NAME)


def get_arcanna_response(config, params, *args, **kwargs):
    event_id = params.get('eventId')
    job_id = params.get('jobId')
    endpoint = EVENT_STATUS_FORMAT.format(job_id, event_id)
    api_response = invoke_rest_endpoint(config, endpoint, 'GET', {})
    logger.info("RESPONSE={}".format(api_response))
    return api_response
