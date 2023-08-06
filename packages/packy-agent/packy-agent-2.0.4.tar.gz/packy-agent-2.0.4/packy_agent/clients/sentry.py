import logging

import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.flask import FlaskIntegration

import packy_agent
from packy_agent.utils.platforms import is_inside_docker_container
from packy_agent.configuration.settings import settings

logger = logging.getLogger(__name__)


def init_sentry_client(flask_integration=False, packy_agent_sentry_dsn=None, **kwargs):
    if not packy_agent_sentry_dsn:
        packy_agent_sentry_dsn = settings.get_sentry_dsn()

    if packy_agent_sentry_dsn:
        component = settings.get_component()
        # TODO(dmu) MEDIUM: Improve OS/platform reporting
        platform_name = 'Docker' if is_inside_docker_container() else 'non-Docker'
        release = f'[{component}, {platform_name}] Packy Agent 2 v{packy_agent.__version__}'

        integrations = [LoggingIntegration(level=logging.ERROR, event_level=logging.ERROR)]
        if flask_integration:
            integrations.append(FlaskIntegration())

        agent_key = settings.get_agent_key() or ''
        agent_name = settings.get_agent_name() or ''
        kwargs_ = {
            'debug': True,
            'release': release,
            'environment': settings.get_server_base_url() or '',
            'server_name': f'{agent_name} [{agent_key}]',
            'request_bodies': 'medium',
            'integrations': integrations,
        }
        kwargs_.update(kwargs)

        sentry_sdk.init(packy_agent_sentry_dsn, **kwargs_)
    else:
        logger.warning('Sentry DSN is not configured')
