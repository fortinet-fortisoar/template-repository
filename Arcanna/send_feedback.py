from connectors.core.connector import get_logger, ConnectorError
from .constants import *

logger = get_logger(LOGGER_NAME)
from .utils import invoke_rest_endpoint


def send_feedback(config, params, *args, **kwargs):
    logger.info("Start sending feedback")
    job_id = params.get('jobId')
    user = params.get('user')
    event_id = params.get('eventId')
    closing_status = params.get('closingStatus')

    data = {
        "cortex_user": user,
        "feedback": closing_status,
        "closing_notes": ""
    }
    request_body = data
    endpoint = EVENT_FEEDBACK_FORMAT.format(job_id, event_id)
    api_response = invoke_rest_endpoint(config, endpoint, 'PUT', request_body)
    api_response.update({'my_custom_response_key': 'my_custom_value'})
    return api_response
