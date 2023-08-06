import functools
from contextlib import contextmanager

from pyminitouch.logger import logger
from pyminitouch.connection import MNTConnection, MNTServer


def connection_wrapper(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        operation = func(self, *args, **kwargs)
        logger.info('send operation: {}'.format(operation.replace('\n', '\linesep')))
        self.connection.send(operation)
    return wrapper


class MNTDevice(object):
    def __init__(self, device_id):
        self.device_id = device_id

        # prepare for connection
        server = MNTServer(device_id)
        # real connection
        connection = MNTConnection(server.port)

        self.server = server
        self.connection = connection

    def __del__(self):
        self.connection.disconnect()
        self.server.stop()

    stop = __del__

    @staticmethod
    def _merge_action(old_action, new_action):
        return old_action + 'c\n' + new_action

    @staticmethod
    def _end_action(action):
        return action + 'c\n'

    @connection_wrapper
    def tap(self, x, y, pressure, delay=None):
        # operation str
        operation_str = 'd 0 {} {} {}\n'.format(x, y, pressure)
        # if pause
        if delay:
            self._merge_action(operation_str, 'w {}\n'.format(delay))
        operation_str = self._merge_action(operation_str, 'u 0\n')
        operation_str = self._end_action(operation_str)
        return operation_str


@contextmanager
def safe_device(device_id):
    device = MNTDevice(device_id)
    yield device
    device.stop()


if __name__ == '__main__':
    _DEVICE_ID = '3d33076e'

    # option1:
    device = MNTDevice(_DEVICE_ID)

    device.tap(800, 900, 50)
    device.tap(600, 900, 50)
    device.tap(400, 900, 50)

    device.stop()

    # option2:
    with safe_device(_DEVICE_ID) as device:
        device.tap(800, 900, 50)
        device.tap(600, 900, 50)
        device.tap(400, 900, 50)
