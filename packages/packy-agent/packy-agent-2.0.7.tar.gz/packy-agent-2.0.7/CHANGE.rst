Version 2.0.7
-------------
* FIX: Installation fixes

Version 2.0.6
-------------
* FEATURE: Restart agent once a day to defend from potential memory leaks
* FEATURE: Watchdog checks Console health and restarts it if needed (including nginx)
* FEATURE: Watchdog reports on exhausting disk space
* FEATURE: "Reset and reboot" button on "Network Configuration" form if configuration was changed
* IMPROVEMENT: Docker images size reduced from 700Mb to 235Mb (by 66%)
* IMPROVEMENT: Extra measures to avoid too often restarts and reboots by Watchdog
* IMPROVEMENT: If user changes IP address in network configuration then `Back` button redirects
  to the new address
* FIX: Non-printable characters in logs are ignored for `/debug/` instead showing empty log

Version 2.0.5
-------------
* IMPROVEMENT: Added 2Gb swapfile for Raspberry Pi and Orange Pi platforms
* IMPROVEMENT: More details on platform reporting for Sentry
* IMPROVEMENT: Improved greenlet-multitasking safety
* CHANGE: Do not distinguish point versions on of Raspbian since they are bug fixes
* FIX: Fix for handling too many agents error during agent activation

Version 2.0.4
-------------
* IMPROVEMENT: More accurate RTT measurement in case of concurrent traceroute running at the same time
* IMPROVEMENT: Does not store empty hops for UDP and ICMP traceroute in case of unreachable host
* IMPROVEMENT: Faster ICMP traceroute in case of unreachable host
* BACKPORTED: Send more detailed information about platform in User-Agent
* FIX: Concurrent trace (and ping) module tasks compatibility with gevent
* FIX: Trace module better validates host replies structure to avoid exceptions
* FIX: Fixed packy-agent-ping, packy-agent-traceroute and packy-agent-http CLI tools
* FIX: Packy logo size fix for Packy Agent Console

Version 2.0.3
-------------
* FIX: Fix upgrade from Console and Worker

Version 2.0.2
-------------
* FIX: SSL support for connection to Packy Communication on `test01` and `production`

Version 2.0.1
-------------
* IMPROVEMENT: More automated build and deploy of Python package and Docker image
* FIX: Alpine support bug fix

Version 2.0.0
-------------
* FEATURE: Measurements are no longer lost if Packy Server is down. Collected and submitted later
* FEATURE: Much more sophisticated Watchdog: properly handles unavailabilty of Packy Server, checks
  supervisor program status for Worker, checks OS-level process status, check Worker process
  status over HTTP, checks actual workflow and data processing inside Worker, less aggressive
  reboot policy, sentry messages throttling
* FEATURE: Worker status available over HTTP (includes stats on Worker internal loops activity)
* FEATURE: Worker tasks periods are configurable with cron-like syntax
* FEATURE: packy-agent-settings CLI tool
* FEATURE: Refresh tokens support
* IMPROVEMENT: Celery-based architecture is replaced with WAMP(Crossbar)-based architecture:
  easier to support, better source code maintainability, less points of failure, less built-in
  limitations, better server-side scalability, less RAM consumption, less network data usage
* IMPROVEMENT (security): Agent with its own access token can access to only what belongs to it
* IMPROVEMENT: More flexible settings subsystem: introduction sqlite3-based key value storage,
  multilayer settings with dictionary key override (local RAM, command line, environment variables,
  server, cached, local storage, settings file,  defaults)
* IMPROVEMENT: Better naming and structure of agent settings
* IMPROVEMENT: Officially supported platforms: Armbian Bionic mainline kernel 4.14.y,
  Raspbian Stretch Lite October 2018, Ubuntu Server 16.04 LTS, Ubuntu Server 18.04 LTS,
  Docker (guest: Alpine 3.8.1)
* IMPROVEMENT: Migrated to pipenv
* IMPROVEMENT: Introduced pyenv
* IMPROVEMENT: Manual tests (Behave/BDD-based)
* IMPROVEMENT: Unittests with code coverage calculation
* IMPROVEMENT: Code quality and refactoring (better naming and more maintainable structure)
* UPGRADE: Upgraded and migrated to Python 3.7.1
* UPGRADE: Upgraded to Alpine 3.8
* CHANGE: Packy Agent Control Server renamed to Packy Agent Console
* CHANGE: The component that actually runs measuring tasks is now named Packy Agent Worker
* PORTED: Ping module support
* PORTED: Trace (traceroute) module support
* PORTED: Speedtest module support
* PORTED: HTTP module support
* PORTED: Management features of Packy Agent Worker: update settings (reload), restart, reboot,
  heartbeat, upgrade
* PORTED: All features of Packy Agent Console: activation, deactivation, login, logout,
  index (status) page,  network configuration (with refactoring), reset (with refactoring),
  start/stop/restart/reboot, upgrade, debug page
* PORTED: Packy Agent Watchdog
* PORTED: packy-agent-activate CLI tool
* PORTED: packy-agent-welcome CLI tool
* PORTED: packy-agent-traceroute CLI tool
* PORTED: Not activated agent notifies server with its Console URL for activation
* PORTED: Integration with Sentry (also migrated to sentry-sdk from legacy raven library)
* PORTED: Ansible-based installation/upgrade scripts
* PORTED: Build and deploy automation
* PORTED: Smooth upgrade from previous version
