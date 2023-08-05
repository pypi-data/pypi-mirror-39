import logging
from functools import wraps
import errno
import os
import signal

from nebo_bot import settings


class TimeoutError(Exception):
    pass


def timeout(seconds=10, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            try:
                _timeout = getattr(args[0], '_timeout_%s' % func.__code__.co_name,
                                   getattr(args[0], '_timeout',
                                           getattr(settings, 'TIMEOUT', seconds)
                                           )
                                   )
            except IndexError:
                _timeout = seconds
            signal.alarm(_timeout)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wraps(func)(wrapper)

    return decorator


def mock_send_message(text):
    logging.debug(f'[MockSendMessage]: "{text}"')


class StopBot(BaseException):
    pass
