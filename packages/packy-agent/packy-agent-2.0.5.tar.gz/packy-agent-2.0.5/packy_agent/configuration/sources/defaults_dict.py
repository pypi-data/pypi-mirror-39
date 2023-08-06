# Having it in a separate file to be able to access from Ansible scripts without unnecessary imports
# Please, be Python 2 compatible

defaults = {

    # Paths
    'settings_filename': '/etc/packy-agent-settings.yaml',
    'database_filename': None,
    'upgrade_in_progress_lock_filename': '/tmp/packy-upgrade-in-progress.lock',
    'packy_run_install_script_filename': '/tmp/packy-run-install-script.sh',
    'interfaces_configuration_filename': '/etc/network/interfaces',
    'configurable_network_interface': None,

    # URLs
    'server_base_url': None,
    'communication_url': None,
    'sentry_dsn': None,

    # Names
    'cached_settings_tablename': 'cached_settings',
    'local_settings_tablename': 'local_settings',

    # Flags
    'debug_mode': False,
    'activated': False,
    'reboot_enabled': True,
    'upgrade_enabled': True,
    'network_configuration_enabled': True,

    # Auth
    'client_id': None,
    'access_token': None,
    'refresh_token': None,
    'agent_key': None,
    'agent_name': None,

    # Timeouts/periods
    'http_timeout_seconds': 5,
    'process_status_check_period_seconds': 1,
    'process_stop_timeout_seconds': 10,
    'process_restart_timeout_seconds': 10,
    'sigterm_timeout_seconds': 10,

    # Misc
    'component': None,
    'minimum_disk_space_bytes': 1024 * 1024 * 512,  # 512Mb
    'vendored_hardware': False,

    'communication_roles': {
        'roles': {
            'subscriber': {},
            'publisher': {},
            'callee': {
                'shared_registration': True,
            },
            'caller': {},
        },
        'authmethods': ['ticket'],
        'authid': '*'
    },

    # Supervisor
    'supervisor': {
        'configuration_filename': '/etc/packy-supervisord.conf',
        'log_filename': '/var/log/packy/supervisor/supervisor.log',
        'run_directory': '/var/run/packy/supervisor',
    },

    # Console
    'console': {
        'flask': {},
        'uwsgi': {
            'configuration_filename': '/etc/packy-uwsgi.conf',
            'pid_filename': 'var/run/packy-uwsgi.pid',
        },
        'nginx': {
            'configuration_filename': '/etc/nginx/sites-enabled/packy-agent.conf'
        },
        'http_port': 8001,
        'stdout_log_filename': '/var/log/packy/console/standard.log',
        'stderr_log_filename': '/var/log/packy/console/error.log',
        'version_dump_filename': '/etc/packy-agent-console-version',
        'version_dump_variable_name': 'PACKY_AGENT_CONSOLE_VERSION',
    },

    # Worker
    'worker': {
        'pid': None,  # TODO(dmu) MEDIUM: should we rather use /var/run/packy-agent-worker.pid ?

        'stopped': False,
        'heartbeat_enabled': True,
        'heartbeat_period_seconds': 5,
        'guard_period_seconds': 5,
        'loops': ['ping_module', 'trace_module', 'speedtest_module', 'http_module', 'consumer',
                  'submitter', 'purger', 'communication', 'heartbeat', 'guard', 'status'],

        'consumer_loop_timeout': 1,
        'results_submission_period_seconds': 10,
        'results_submission_pause_seconds': 0.5,
        'purge_period_seconds': 300,
        'periodic_task_jitter_factor': 0.1,

        'stdout_log_filename': '/var/log/packy/worker/standard.log',
        'stderr_log_filename': '/var/log/packy/worker/error.log',
        'version_dump_filename': '/etc/packy-agent-worker-version',
        'version_dump_variable_name': 'PACKY_AGENT_WORKER_VERSION',

        'activation_notify_period_seconds': 10,  # Server throttles anything more than 10 r/minute
        'started_check_period_seconds': 5,
        'packy_communication_retry_period': 30,
        'packy_communication_heartbeat_timeout_seconds': 60,

        'offline_to_restart_seconds': 120,
        'restart_wait_seconds': 120,
        'offline_to_reboot_seconds': 300,
        'reboot_wait_seconds': 300,

        'http_bind_address': '127.0.0.1',
        'http_port': 5000,
        'expected_http_response_time_seconds': 1,
    },

    # Watchdog
    'watchdog': {
        'check_period_seconds': 30,
        'relax_period_seconds': 60,
        'warmup_period_seconds': 30,

        'warning_report_period': 600,
        'error_report_period': 300,

        'stdout_log_filename': '/var/log/packy/watchdog/standard.log',
        'stderr_log_filename': '/var/log/packy/watchdog/error.log',
        'version_dump_filename': '/etc/packy-agent-watchdog-version',
        'version_dump_variable_name': 'PACKY_AGENT_WATCHDOG_VERSION',
    },

    # logging
    'log_level': 'WARNING',
    'logging': {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s %(levelname)s %(name)s %(message)s'
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
            },
        },
        'loggers': {
            'packy_agent': {
                'propagate': True,
            },
            'sqlitedict': {
                'level': 'WARNING',
                'propagate': True,
            },
            'urllib3':  {
                'level': 'WARNING',
                'propagate': True,
            },
            'sentry_sdk':  {
                'level': 'WARNING',
                'propagate': True,
            },
        },
        'root': {
            'level': 'WARNING',
            'handlers': ['console'],
        }
    }
}
