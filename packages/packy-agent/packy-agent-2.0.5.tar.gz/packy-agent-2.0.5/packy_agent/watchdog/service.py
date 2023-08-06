import time
import logging
from collections import defaultdict, OrderedDict
from threading import Condition

from psutil import Process, NoSuchProcess
from requests.exceptions import ConnectionError as RequestsConnectionError, HTTPError
from sentry_sdk import capture_message, capture_exception

from packy_agent.configuration.settings import settings
from packy_agent.domain_logic.constants import WORKER_COMPONENT
from packy_agent.clients.packy_server import get_packy_server_client
from packy_agent.clients.packy_agent_worker import get_packy_agent_worker_client
from packy_agent.constants import MODULE_LOOP_SUFFIX
from packy_agent.domain_logic.managers.control import control_manager
from packy_agent.utils.datetime import get_croniter


logger = logging.getLogger(__name__)


MESSAGE_KEY_LEN = 10
MAX_THROTTLE_DICT_SIZE = 1024
FAILOVER_CHECK_PERIOD_SECONDS = 30
ROOT_PID = 1
START = 'restart'
RESTART = 'restart'
REBOOT = 'reboot'
ERROR = 'error'
WARNING = 'warning'
UNKNOWN = 'unknown'
OK = 'ok'


def get_loop_deadline(loop_props):
    now_ts = time.time()
    loop_type = loop_props.get('loop_type')
    if loop_type in ('scheduled', 'scheduled_producer'):
        schedule = loop_props.get('schedule')
        if schedule:
            croniter = get_croniter(schedule)
            return croniter.get_next()
    elif loop_type == 'periodic':
        period = loop_props.get('period')
        if period is not None:
            return now_ts + period


class WatchdogService:

    def __init__(self, raven_client=None):
        self.raven_client = raven_client

        self._graceful_stop = False
        self.condition = Condition()

        self.known_activated_time = None
        self.last_restart_time = None
        self.last_known_online_time = None

        self.last_known_online_ts = None

        self.has_reported_not_activated = False
        self.has_reported_stopped = False

        self.collected_counter = None
        self.collected_counter_ts = None
        self.collected_counter_deadline_ts = None
        self.submitted_counter = None
        self.submitted_counter_ts = None
        self.submitted_counter_deadline_ts = None
        self.purged_records = None
        self.purged_records_ts = None

        self.loop_stats = defaultdict(dict)

        self.report_throttle = OrderedDict()

    def graceful_stop(self):
        self._graceful_stop = True
        with self.condition:
            self.condition.notify_all()

    def throttle(self, message, period):
        now_ts = time.time()

        message_key = message[:MESSAGE_KEY_LEN]
        last_reported_ts = self.report_throttle.get(message_key)
        if last_reported_ts and time.time() < last_reported_ts + period:
            logger.debug('Message has been throttled: %s', message)
            return True
        else:
            self.report_throttle[message_key] = now_ts
            if len(self.report_throttle) > MAX_THROTTLE_DICT_SIZE:
                self.report_throttle.popitem(last=False)
            return False

    def report_warning(self, message):
        logger.warning(message)
        if not self.throttle(message, settings.get_watchdog_warning_report_period()):
            capture_message(message, level='warning')

    def report_error(self, message):
        logger.error(message)
        if not self.throttle(message, settings.get_watchdog_error_report_period()):
            capture_message(message, level='error')

    def handle_console(self):
        # TODO(dmu) LOW: Implement handling running status of Packy Agent Console
        pass

    def start_worker(self):
        self.report_warning('Watchdog requested Worker start')
        control_manager.start(WORKER_COMPONENT)

    def restart_worker(self):
        self.report_warning('Watchdog requested Worker restart')
        control_manager.restart(WORKER_COMPONENT)

    def reboot(self):
        self.report_warning('Watchdog requested reboot')
        control_manager.reboot()

    def resolve_online_status(self):
        logger.debug('Resolving agent online status...')
        now_ts = time.time()

        if not settings.get_worker_heartbeat_enabled():
            logger.debug('Heartbeat is disabled, so we do not expect agent to be online')
            return UNKNOWN

        try:
            is_online = get_packy_server_client().is_agent_online()
        except Exception:
            logger.debug('Could not get agent online status. Maybe Packy Server is not available')
            return UNKNOWN

        if is_online is None:
            logger.debug('Could not get agent online status. Maybe there is an issue with '
                         'Packy Server')
            return UNKNOWN
        elif is_online:
            self.last_known_online_ts = now_ts

        if self.last_known_online_ts is None:
            return UNKNOWN
        else:
            offline_period_seconds = now_ts - self.last_known_online_ts

            # If we have been offline long enough and rebooted long ago then go reboot
            if (offline_period_seconds >= settings.get_worker_offline_to_reboot_seconds() and
                    now_ts >= (settings.get_rebooted_at_ts() or 0) +
                               settings.get_worker_reboot_wait_seconds()):
                return REBOOT
            # If we have been offline long enough and started long ago then go restart
            elif (offline_period_seconds >= settings.get_worker_offline_to_restart_seconds() and
                  now_ts >= (settings.get_worker_started_at_ts() or 0) +
                             settings.get_worker_restart_wait_seconds()):
                return RESTART

        return OK

    def resolve_worker_supervisor_program_status(self):
        logger.debug('Resolving Worker running status (supervisor)...')
        if control_manager.is_running(WORKER_COMPONENT):
            logger.debug('Worker is running (supervisor)')
            return OK
        elif not (control_manager.is_starting(WORKER_COMPONENT) or
                  control_manager.is_stopping(WORKER_COMPONENT)):
            logger.debug('Worker is NOT running (supervisor)')
            return START
        else:
            return UNKNOWN

    def resolve_worker_process_status(self):
        pid = control_manager.get_pid(WORKER_COMPONENT)

        try:
            Process(pid)
            return OK
        except NoSuchProcess:
            return RESTART

    def resolve_loops_activity(self, loops):
        result = None
        
        now_ts = time.time()
        relax_period = settings.get_watchdog_relax_period_seconds()

        for loop_name, loop_props in loops.items():
            new_counter = loop_props.get('counter')
            current_counter = (self.loop_stats.get(loop_name) or {}).get('counter')
            if new_counter == current_counter:
                change_deadline_ts = self.loop_stats[loop_name].get('change_deadline_ts')
                if change_deadline_ts is not None:
                    relaxed_change_deadline_ts = change_deadline_ts + relax_period
                    if now_ts >= relaxed_change_deadline_ts:
                        result = WARNING
                        counter_ts = self.loop_stats[loop_name].get('counter_ts')
                        self.report_warning(
                            f'{loop_name} counter is stale on {current_counter} at '
                            f'{counter_ts:.3f} (change expected before '
                            f'{relaxed_change_deadline_ts:.3f})')
                        self.loop_stats[loop_name][
                            'change_deadline_ts'] = get_loop_deadline(loop_props)
            else:
                self.loop_stats[loop_name]['counter'] = new_counter
                self.loop_stats[loop_name]['counter_ts'] = now_ts

                logger.debug('%s updated counter from %s to %s at %.3f', loop_name,
                             current_counter, new_counter, now_ts)

                self.loop_stats[loop_name][
                    'change_deadline_ts'] = get_loop_deadline(loop_props)

        return result
    
    def resolve_workflow(self, status):

        # Filter out measurement loops
        running_measurement_loops = {k: v for k, v in (status.get('loops') or {}).items()
                                     if k.endswith(MODULE_LOOP_SUFFIX)}
        if not running_measurement_loops:
            logger.debug('No active measurement loops found')
            return  # No measurement loops, so we should not expect counters increment

        deadline_ts = min(
            list(filter(None, (get_loop_deadline(loop_props) for loop_name, loop_props
                               in running_measurement_loops.items()))) or (None,))
        logger.debug('Workflow deadline is calculated as %s', deadline_ts)

        result = None
        relax_period = settings.get_watchdog_relax_period_seconds()
        now_ts = time.time()

        collected_counter = status.get('collected_counter')
        if self.collected_counter == collected_counter:
            logger.debug('Collected counter did not change (value: %s)', self.collected_counter)
            if (self.collected_counter_deadline_ts and
                    now_ts >= (self.collected_counter_deadline_ts + relax_period)):
                result = WARNING
                self.report_warning(f'Measurement collection is stale on {self.collected_counter} '
                                    f'at {self.collected_counter_ts:.3f}')
                self.collected_counter_deadline_ts = deadline_ts
        else:
            self.collected_counter = collected_counter
            self.collected_counter_ts = now_ts
            self.collected_counter_deadline_ts = deadline_ts

        submitted_counter = status.get('submitted_counter')
        if self.submitted_counter == submitted_counter:
            logger.debug('Submitted counter did not change (value: %s)', self.submitted_counter)
            if (self.submitted_counter_deadline_ts and
                    now_ts >= self.submitted_counter_deadline_ts + relax_period):
                result = WARNING
                self.report_warning(f'Measurement submission is stale on {self.submitted_counter} '
                                    f'at {self.submitted_counter_ts:.3f}')
                self.submitted_counter_deadline_ts = deadline_ts
        else:
            self.submitted_counter = submitted_counter
            self.submitted_counter_ts = now_ts
            self.submitted_counter_deadline_ts = deadline_ts

        purged_records = status.get('purged_records')
        if self.purged_records == purged_records:
            purge_period = settings.get_worker_purge_period_seconds() + relax_period
            if self.purged_records_ts and now_ts >= self.purged_records_ts + purge_period:
                result = WARNING
                self.report_warning(f'Measurement purging is stale on {self.purged_records} '
                                    f'at {self.purged_records_ts:.3f}')

        else:
            self.purged_records = purged_records
            self.purged_records_ts = now_ts

        return result

    def resolve_worker_response(self):
        start = time.time()
        try:
            status = get_packy_agent_worker_client().get_status()
            finish = time.time()
        except RequestsConnectionError:
            logger.debug('Could not get Worker status over HTTP')
            return RESTART
        except HTTPError as ex:
            self.report_error(f'Packy Agent Worker returned HTTP{ex.response.status_code}: {ex!r}')
            return ERROR

        result = OK

        actual_duration = finish - start
        expected_duration = settings.get_worker_expected_http_response_time_seconds()
        if actual_duration > expected_duration:
            result = WARNING
            self.report_warning(f'It took {actual_duration:.3g} seconds for Packy Agent Worker '
                                f'to respond while it was expected to take only '
                                f'{expected_duration:.3g}')

        loops = status.get('loops')
        if loops:
            loops_result = self.resolve_loops_activity(loops)
            if loops_result:
                result = loops_result
        else:
            result = WARNING
            self.report_warning('Worker did not return running loops')

        workflow_result = self.resolve_workflow(status)
        if workflow_result:
            result = workflow_result

        return result

    def handle_worker(self):
        if not settings.is_activated():
            if not self.has_reported_not_activated:
                self.has_reported_not_activated = True
                logger.info('Worker is not activated')

            return
        self.has_reported_not_activated = False

        if settings.is_stopped():
            if not self.has_reported_stopped:
                self.has_reported_stopped = True
                logger.info('Worker is stopped on purpose')

            return
        self.has_reported_stopped = False

        online_status_action = self.resolve_online_status()
        if online_status_action == REBOOT:
            self.reboot()
            return
        elif online_status_action == RESTART:
            self.restart_worker()
            return

        supervisor_program_status = self.resolve_worker_supervisor_program_status()
        if supervisor_program_status == START:
            self.start_worker()
            return

        worker_process_status = self.resolve_worker_process_status()
        if worker_process_status == RESTART:
            # if we reach here it means that supervisor reports Worker as running, but the is
            # actually dead. Not sure if this is possible situation (maybe if supervisor has bug).
            # So we restart, not just start
            self.restart_worker()
            return

        worker_response_status = self.resolve_worker_response()
        if worker_response_status == RESTART:
            self.restart_worker()
            return

    def loop_iteration(self):
        if (time.time() - settings.get_watchdog_started_at_ts() <
                settings.get_watchdog_warmup_period_seconds()):
            logger.debug('Warming up...')
            return

        try:
            self.handle_worker()
        except Exception:
            logger.exception('Error while handling Worker')
            capture_exception()

        try:
            self.handle_console()
        except Exception:
            logger.exception('Error while handling Console')
            capture_exception()

    def run(self):
        logger.info('STARTED Watchdog')
        while not self._graceful_stop:
            start = time.time()
            try:
                self.loop_iteration()
            except Exception:
                logger.exception('Error during loop iteration')
                capture_exception()

            # Configuration may change with time, so we reread it every loop
            try:
                check_period_seconds = settings.get_watchdog_check_period_seconds()
            except Exception:
                check_period_seconds = FAILOVER_CHECK_PERIOD_SECONDS
                logger.exception('Could not get check period seconds from configuration file, '
                                 'using failover value: %s', check_period_seconds)
                capture_exception()

            wait_duration = check_period_seconds - (time.time() - start)
            if wait_duration > 0:
                logger.debug('Waiting for %.3g seconds for next iteration', wait_duration)
                with self.condition:
                    self.condition.wait(wait_duration)

        logger.info('STOPPED Watchdog gracefully')
