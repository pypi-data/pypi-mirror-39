import os
import distro


LINUX_MINT = 'linuxmint'
UBUNTU = 'ubuntu'
RASPBIAN = 'raspbian'
ALPINE = 'alpine'

PRETTY_NAMES = {
    LINUX_MINT: 'Linux Mint',
    UBUNTU: 'Ubuntu',
    RASPBIAN: 'Raspbian',
    ALPINE: 'Alpine',
}

LINUX_MINT_18_1 = (LINUX_MINT, '18.1')
UBUNTU_16_04 = (UBUNTU, '16.04')
UBUNTU_18_04 = (UBUNTU, '18.04')
RASPBIAN_9_4 = (RASPBIAN, '9.4')


def get_os_id_and_version():
    return distro.id(), '.'.join(distro.version_parts(best=True)[:2])


def is_inside_docker_container():
    return os.path.isfile('/.dockerenv')
