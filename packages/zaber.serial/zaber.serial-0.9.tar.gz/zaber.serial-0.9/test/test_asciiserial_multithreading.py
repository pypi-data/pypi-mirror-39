import pytest
from threading import Condition, Thread, Event
from zaber.serial import AsciiSerial, AsciiCommand, AsciiReply, BinaryCommand, TimeoutError
from zaber.serial.portlock import PortLock

TEST_RESPONSE = "@01 0 OK IDLE -- 0"
TEST_COMMAND = "/1 echo TEST"
FAIL_TIMEOUT = 5

port = None


class MockPort(object):
    def __init__(self):
        self._readCondition = Condition()
        self._writeCondition = Condition()

        self._readStarted = Event()
        self._writeStarted = Event()

    def write(self, data):
        with self._writeCondition:
            self._inWriteMethod = True

            self._writeStarted.set()
            self._writeCondition.wait(FAIL_TIMEOUT)

            self._inWriteMethod = False

    def readline(self):
        with self._readCondition:
            self._inReadMethod = True

            self._readStarted.set()
            self._readCondition.wait(FAIL_TIMEOUT)

            self._inReadMethod = False

        return TEST_RESPONSE

    def assertReadAndWriteIsSimultaneous(self):
        self._writeStarted.wait()
        self._readStarted.wait()

        with self._writeCondition, self._readCondition:
            try:
                assert self._inWriteMethod
                assert self._inReadMethod
            finally:
                self._readCondition.notify()
                self._writeCondition.notify()


class AsciiSerialWrapper(AsciiSerial):
    def __init__(self):
        self._ser = MockPort()
        self._lock = PortLock()

    def assertReadAndWriteIsSimultaneous(self):
        self._ser.assertReadAndWriteIsSimultaneous()


def setup_function(function):
    global port

    port = AsciiSerialWrapper()


def teardown_function(function):
    global port

    port = None


def test_allows_simultaneous_read_and_write_access_from_different_threads():
    def writeToPort():
        port.write(AsciiCommand(TEST_COMMAND))

    def readFromPort():
        port.read()

    writeThread = Thread(target=writeToPort)
    readThread = Thread(target=readFromPort)

    writeThread.start()
    readThread.start()

    port.assertReadAndWriteIsSimultaneous()

    writeThread.join()
    readThread.join()
