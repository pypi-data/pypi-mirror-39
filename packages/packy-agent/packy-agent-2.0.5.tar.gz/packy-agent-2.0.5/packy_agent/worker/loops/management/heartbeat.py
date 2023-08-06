import logging

import packy_agent
from packy_agent.configuration.settings import settings
from packy_agent.worker.loops.base.periodic import PeriodicLoop
from packy_agent.utils.data_usage import get_data_usage
from packy_agent.clients.packy_server import get_packy_server_client
from packy_agent.constants import HEARTBEAT_LOOP
from packy_agent.utils.network import get_actual_ip_address

logger = logging.getLogger(__name__)


def send_heartbeat():
    if not settings.is_worker_heartbeat_enabled():
        logger.debug('Heartbeat is disabled')
        return

    (prev_bytes_sent, prev_bytes_received), (bytes_sent, bytes_received) = get_data_usage()
    try:
        response = get_packy_server_client().update_status(
            version=packy_agent.__version__,
            ip_address=get_actual_ip_address(),
            prev_bytes_sent=prev_bytes_sent,
            prev_bytes_received=prev_bytes_received,
            bytes_sent=bytes_sent,
            bytes_received=bytes_received,
            raise_for_status=False)

        if response is not None:
            if response.status_code == 401:
                logger.debug('Access token is invalid')
                # We do not expect context switch here because we work with RAM only (no IO)
                invalid_access_tokens = settings.get_invalid_access_tokens() or set()
                invalid_access_tokens.add(settings.get_access_token())
                settings.set_runtime('invalid_access_tokens', invalid_access_tokens)
            else:
                response.raise_for_status()
    except Exception:
        logger.warning('Error while sending heartbeat', exc_info=True)


class HeartbeatLoop(PeriodicLoop):

    formal_name = HEARTBEAT_LOOP

    def __init__(self, period):
        super().__init__(period=period, callable_=send_heartbeat)
