import pytest
from threading import Thread
from zaber.serial.portlock import PortLock

canAcquireRead = None
canAcquireWrite = None
canAcquire = None
lock = None


def setup_function(function):
    global canAcquireRead
    global canAcquireWrite
    global canAcquire
    global lock

    canAcquireRead = None
    canAcquireWrite = None
    canAcquire = None

    lock = PortLock()


def teardown_function(function):
    global lock

    lock = None


def test_locking_locks_both_locks():
    def tryAcquireThread():
        global canAcquireRead
        global canAcquireWrite

        canAcquireRead = lock.read_lock.acquire(blocking=False)
        canAcquireWrite = lock.write_lock.acquire(blocking=False)

    thread = Thread(target=tryAcquireThread)

    with lock:
        thread.start()
        thread.join()

    # neither can be acquired
    assert canAcquireRead is False
    assert canAcquireWrite is False


def test_acquire_returns_false_when_locked_by_other_thread():
    def tryAcquireThread():
        global canAcquire

        canAcquire = lock.acquire(blocking=False)

    thread = Thread(target=tryAcquireThread)

    with lock:
        thread.start()
        thread.join()

    # acquire returned false because lock was locked
    assert canAcquire is False


def test_acquire_does_not_lock_read_lock_if_write_lock_cannot_be_acquired():
    def tryAcquireThread():
        global canAcquire

        canAcquire = lock.acquire(blocking=False)

    thread = Thread(target=tryAcquireThread)

    with lock.write_lock:
        thread.start()
        thread.join()

    # can acquire read lock (it was not taked by other thread)
    assert lock.read_lock.acquire(blocking=False)
    lock.read_lock.release()

    assert canAcquire is False


def test_acquire_does_not_lock_write_lock_if_read_lock_cannot_be_acquired():
    def tryAcquireThread():
        global canAcquire

        canAcquire = lock.acquire(blocking=False)

    thread = Thread(target=tryAcquireThread)

    with lock.read_lock:
        thread.start()
        thread.join()

    # can acquire write lock (it was not taked by other thread)
    assert lock.write_lock.acquire(blocking=False)
    lock.write_lock.release()

    assert canAcquire is False
