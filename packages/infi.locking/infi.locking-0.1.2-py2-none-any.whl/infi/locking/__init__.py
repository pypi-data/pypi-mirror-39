from __future__ import absolute_import
from logging import getLogger
from infi.pyutils.decorators import wraps
from infi.pyutils.contexts import contextmanager

log = getLogger(__name__)


@contextmanager
def locking_context(lock_filepath):
    """
    inter-process file-based locking context
    :lock_filepath: requires full filepath for the lock file
    """
    from lockfile import AlreadyLocked
    from lockfile.pidlockfile import PIDLockFile
    from os import path
    lock = PIDLockFile(lock_filepath, timeout=0)

    while True:
        try:
            if lock.i_am_locking():  # our PID has already acquired the lock
                log.info("poll process already holds the pid lock file")
                break
            lock.acquire(0)
            break  # successfully acquired the lock
        except AlreadyLocked:
            locking_pid = lock.read_pid()  # either None or int
            if locking_pid is not None and path.exists("/proc/{}".format(locking_pid)):
                log.error("another poll process (pid {}) is still running and did not release the lock file"
                          .format(locking_pid))
                raise SystemExit(1)
            # pid file is left over by a dead process, break the lock and re-acquire
            log.info("detected lock left over of a dead poll process ({}), breaking lock".format(locking_pid))
            lock.break_lock()

    try:
        yield
    finally:
        lock.release()


def lock_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with locking_context(func.__name__):
            return func(*args, **kwargs)
    return wrapper
