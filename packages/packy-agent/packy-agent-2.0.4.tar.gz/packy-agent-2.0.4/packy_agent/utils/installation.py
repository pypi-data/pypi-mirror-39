import os
import os.path

import packy_agent


def dump_version(filename, variable_name):
    with open(filename, 'w') as f:
        f.write('{}={}\n'.format(variable_name, packy_agent.__version__))


def is_upgrade_in_progress():
    from packy_agent.configuration.settings import settings
    return os.path.isfile(settings.get_upgrade_in_progress_lock_filename())


def remove_upgrade_in_progress_lock():
    from packy_agent.configuration.settings import settings
    try:
        os.remove(settings.get_upgrade_in_progress_lock_filename())
    except OSError:
        pass
