import requests
from connectors.core.connector import get_logger, ConnectorError
from .constants import *
from .utils import invoke_rest_endpoint

logger = get_logger(LOGGER_NAME)


def send_to_arcanna(config, params, *args, **kwargs):
    logger.info("Start sending.")

    job_id = params.get('jobId')
    title = params.get("title")
    body = params.get('body')
    caseId = params.get("caseId", None)

    data = {
        "job_id": int(job_id),
        "title": title,
        "raw_body": body
    }

    endpoint = EVENTS_ENDPOINT
    if not caseId:
        endpoint = endpoint + str(caseId)

    request_body = data

    api_response = invoke_rest_endpoint(config, endpoint, 'POST', request_body)

    api_response.update({'status': 'ok', "value": endpoint})
    return api_response
