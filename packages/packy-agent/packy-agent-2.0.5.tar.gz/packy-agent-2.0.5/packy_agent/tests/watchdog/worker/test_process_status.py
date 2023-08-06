import os
from unittest.mock import MagicMock, patch

import pytest

from packy_agent.watchdog.service import WatchdogService


@pytest.mark.usefixtures('activated', 'watchdog_started_long_ago')
def test_process_is_running():
    with patch('packy_agent.watchdog.service.control_manager.get_pid') as get_pid:
        get_pid.return_value = os.getpid()
        service = WatchdogService()

        service.reboot = MagicMock()
        service.restart_worker = MagicMock()
        service.start_worker = MagicMock()

        service.resolve_online_status = MagicMock()
        service.resolve_worker_supervisor_program_status = MagicMock()
        service.resolve_worker_response = MagicMock()

        service.loop_iteration()

        service.start_worker.assert_not_called()
        service.restart_worker.assert_not_called()
        service.reboot.assert_not_called()


@pytest.mark.usefixtures('activated', 'watchdog_started_long_ago')
def test_process_is_not_running():
    with patch('packy_agent.watchdog.service.control_manager.get_pid') as get_pid:
        get_pid.return_value = 9999999999999999999999
        service = WatchdogService()

        service.reboot = MagicMock()
        service.restart_worker = MagicMock()
        service.start_worker = MagicMock()

        service.resolve_online_status = MagicMock()
        service.resolve_worker_supervisor_program_status = MagicMock()
        service.resolve_worker_response = MagicMock()

        service.loop_iteration()

        service.start_worker.assert_not_called()
        service.restart_worker.assert_called()
        service.reboot.assert_not_called()
