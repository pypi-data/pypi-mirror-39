import psutil

from packy_agent.configuration.settings import settings


def get_data_usage():
    prev_bytes_sent = settings.get('bytes_sent')
    prev_bytes_received = settings.get('bytes_received')

    snetio = psutil.net_io_counters(pernic=True, nowrap=True)
    snetio.pop('lo', None)

    bytes_sent = bytes_received = 0
    for value in snetio.values():
        bytes_sent += value.bytes_sent
        bytes_received += value.bytes_recv

    settings.set_runtime('bytes_sent', bytes_sent)
    settings.set_runtime('bytes_received', bytes_received)

    return (prev_bytes_sent, prev_bytes_received), (bytes_sent, bytes_received)
