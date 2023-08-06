import os


def get_available_disk_space(path):
    statvfs = os.statvfs(path)
    return statvfs.f_frsize * statvfs.f_bavail
