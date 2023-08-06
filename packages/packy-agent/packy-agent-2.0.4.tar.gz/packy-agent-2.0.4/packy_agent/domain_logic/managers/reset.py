import logging

from packy_agent.domain_logic.managers.control import control_manager
from packy_agent.domain_logic.managers.network import network_manager
from packy_agent.configuration.settings import settings
from packy_agent.clients.packy_server import packy_server_client


logger = logging.getLogger(__name__)


class ResetManager:

    def reset_network_configuration(self, reboot=True, reboot_delay_seconds=5):
        if network_manager.is_network_configuration_supported():
            network_manager.restore_configuration(
                reboot=reboot, reboot_delay_seconds=reboot_delay_seconds)

    def deactivate(self, reboot=False, delay_seconds=5):
        packy_server_client.deactivate_agent()
        settings.deactivate()

        if reboot:
            control_manager.reboot(delay_seconds=delay_seconds)
        else:
            control_manager.restart_all(delay_seconds=delay_seconds)

    def full_reset(self, delay_seconds=5):
        self.deactivate(delay_seconds=delay_seconds)
        self.reset_network_configuration(reboot=True, reboot_delay_seconds=delay_seconds)


reset_manager = ResetManager()
