from unittest.mock import MagicMock, patch

import pytest

from packy_agent.watchdog.service import WatchdogService


@pytest.mark.usefixtures('activated', 'watchdog_started_long_ago')
def test_program_is_running():
    with patch('packy_agent.watchdog.service.control_manager.is_running') as is_running:
        is_running.return_value = True
        service = WatchdogService()

        service.reboot = MagicMock()
        service.restart_worker = MagicMock()
        service.start_worker = MagicMock()

        service.resolve_online_status = MagicMock()
        service.resolve_worker_process_status = MagicMock()
        service.resolve_worker_response = MagicMock()

        service.loop_iteration()

        service.start_worker.assert_not_called()
        service.restart_worker.assert_not_called()
        service.reboot.assert_not_called()


@pytest.mark.usefixtures('activated', 'watchdog_started_long_ago')
def test_program_is_not_running():
    with patch('packy_agent.watchdog.service.control_manager.is_running') as is_running:
        is_running.return_value = False
        service = WatchdogService()

        service.reboot = MagicMock()
        service.restart_worker = MagicMock()
        service.start_worker = MagicMock()

        service.resolve_online_status = MagicMock()
        service.resolve_worker_process_status = MagicMock()
        service.resolve_worker_response = MagicMock()

        service.loop_iteration()

        service.start_worker.assert_called()
        service.restart_worker.assert_not_called()
        service.reboot.assert_not_called()
