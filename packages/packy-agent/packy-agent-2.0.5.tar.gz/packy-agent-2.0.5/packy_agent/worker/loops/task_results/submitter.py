import logging

from requests.exceptions import ConnectionError

from packy_agent.constants import (
    PING_MODULE, TRACE_MODULE, SPEEDTEST_MODULE, HTTP_MODULE, SUBMITTER_LOOP)
from packy_agent.worker.loops.base.periodic import PeriodicLoop
from packy_agent.clients.local_storage import get_local_storage, TYPE_MAP
from packy_agent.configuration.settings import settings
from packy_agent.clients.packy_server import get_packy_server_client
from packy_agent.exceptions import CoolDown


MODULE_PUBLIC_IDENTIFIER_MAP = {
    1: PING_MODULE,
    2: TRACE_MODULE,
    3: SPEEDTEST_MODULE,
    4: HTTP_MODULE,
}
assert len(MODULE_PUBLIC_IDENTIFIER_MAP) == len(TYPE_MAP)

logger = logging.getLogger(__name__)


def is_invalid_chronological_order(response):
    if not response.status_code == 400:
        return False

    response_json = response.json()
    if not isinstance(response_json, dict):
        return False

    errors = response_json.get('errors')
    if not isinstance(errors, dict):
        return False

    non_field_errors = errors.get('non_field_errors')
    if not non_field_errors or not isinstance(non_field_errors, list):
        return False

    for item in non_field_errors:
        if item.get('code') == 'invalid-chronological-order':
            return True

    return False


def submit_measurement(measurement_row):
    module_public_identifier = MODULE_PUBLIC_IDENTIFIER_MAP.get(measurement_row.measurement_type)
    if not module_public_identifier:
        logger.warning(f'Unknown measurement type: {measurement_row.measurement_type}')
        return

    value = measurement_row.value
    try:
        response = get_packy_server_client().submit_measurement(
            module_public_identifier, value, raise_for_status=False)
    except ConnectionError as ex:
        logger.warning(f'Could not connect to server to submit measurement of '
                       f'{module_public_identifier} ({ex!r}): {value}')
        get_local_storage().save_measurement_error(
            measurement_row.id, f'Could not connect to server: {ex!r}')
        raise CoolDown()
    except Exception as ex:
        logger.error(f'Error while submitting measurement of {module_public_identifier}: {value}')
        get_local_storage().save_measurement_error(measurement_row.id, repr(ex) or 'Unknown')
        raise CoolDown()

    status_code = response.status_code
    if 200 <= status_code < 300:
        get_local_storage().mark_measurement_as_submitted(measurement_row.id)
        return
    else:
        if status_code >= 500:
            log_method = logger.warning  # because it is server error
        elif status_code >= 400:
            if is_invalid_chronological_order(response):
                logger.warning(f'Server responded with HTTP{status_code}: {response.content}')
                local_storage = get_local_storage()
                local_storage.save_measurement_error(
                    measurement_row.id, f'HTTP{status_code}: {response.content}')
                local_storage.mark_measurement_as_submitted(measurement_row.id)
                return
            else:
                log_method = logger.error  # because it is our error
        else:
            log_method = logger.error  # because it is our error that is never expected

        log_method(f'Server responded with HTTP{status_code}: {response.content}')
        get_local_storage().save_measurement_error(
            measurement_row.id, f'HTTP{status_code}: {response.content}')
        raise CoolDown()


class TaskResultsSubmitter(PeriodicLoop):

    formal_name = SUBMITTER_LOOP

    def __init__(self):
        super().__init__(settings.get_worker_results_submission_period_seconds())
        self.submitted_counter = 0

    def call(self):
        results_submission_pause_seconds = settings.get_worker_results_submission_pause_seconds()
        for measurement_type in MODULE_PUBLIC_IDENTIFIER_MAP.keys():
            for measurement_row in get_local_storage().get_remaining_measurements(measurement_type):
                try:
                    submit_measurement(measurement_row)
                    self.submitted_counter += 1
                except CoolDown:
                    break
                finally:
                    self.sleep(results_submission_pause_seconds)
                    if self.is_stopping or not self.is_running:
                        return
