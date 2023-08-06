import pytest
from fixtures import asciiserial, fake
from zaber.serial import AsciiLockstep, AsciiDevice


@pytest.fixture
def device(asciiserial):
    return AsciiDevice(asciiserial, 1)


@pytest.fixture
def lockstep(device):
    return AsciiLockstep(device, lockstep_group=2)


def test_constructor(device):
    a = AsciiLockstep(device, 1)
    assert(a.device is device)
    assert(a.lockstep_group is 1)


def test_can_be_constructed_from_asciidevice(device):
    a = device.lockstep(2)
    assert(a.lockstep_group == 2)


def test_enable(lockstep, fake):
    fake.expect("/1 0 lockstep 2 setup enable 3 4\r\n", "@01 0 OK IDLE -- 0\r\n")
    lockstep.enable(3, 4)
    fake.validate()


def test_disable(lockstep, fake):
    fake.expect("/1 0 lockstep 2 setup disable\r\n", "@01 0 OK IDLE -- 0\r\n")
    lockstep.disable()
    fake.validate()


def test_home(lockstep, fake):
    fake.expect("/1 0 lockstep 2 home\r\n", "@01 0 OK BUSY WR 0\r\n")
    fake.expect("/1 0 lockstep 2 info\r\n", "@01 0 OK IDLE -- 3 4 0 0\r\n")
    fake.expect("/1 3\r\n", "@01 3 OK IDLE -- 0\r\n")
    lockstep.home()
    fake.validate()


def test_info(lockstep, fake):
    fake.expect("/1 0 lockstep 2 info\r\n", "@01 0 OK IDLE -- 3 4 -500 100\r\n")
    info = lockstep.info()
    fake.validate()
    assert info.is_enabled is True
    assert info.axis1 == 3
    assert info.axis2 == 4
    assert info.offset == -500
    assert info.twist == 100


def test_poll_until_idle_will_continue_polling(lockstep, fake):
    fake.expect("/1 0 lockstep 2 info\r\n", "@01 0 OK BUSY -- 3 4 0 0\r\n")
    for i in range(20):
        fake.expect("/1 3\r\n", "@01 3 OK BUSY -- 0\r\n")
    fake.expect("/1 3\r\n", "@01 3 OK IDLE -- 0\r\n")
    lockstep.poll_until_idle()
    fake.validate()


def test_move_abs(lockstep, fake):
    fake.expect("/1 0 lockstep 2 move abs 10234\r\n", "@01 0 OK BUSY -- 0\r\n")
    fake.expect("/1 0 lockstep 2 info\r\n", "@01 0 OK IDLE -- 3 4 0 0\r\n")
    fake.expect("/1 3\r\n", "@01 3 OK IDLE -- 0\r\n")
    lockstep.move_abs(10234)
    fake.validate()


def test_move_rel(lockstep, fake):
    fake.expect("/1 0 lockstep 2 move rel 12312\r\n", "@01 0 OK BUSY -- 0\r\n")
    fake.expect("/1 0 lockstep 2 info\r\n", "@01 0 OK IDLE -- 3 4 0 0\r\n")
    fake.expect("/1 3\r\n", "@01 3 OK IDLE -- 0\r\n")
    lockstep.move_rel(12312)
    fake.validate()


def test_move_vel(lockstep, fake):
    fake.expect("/1 0 lockstep 2 move vel 1005\r\n", "@01 0 OK BUSY -- 0\r\n")
    lockstep.move_vel(1005)
    fake.validate()


def test_stop(lockstep, fake):
    fake.expect("/1 0 lockstep 2 stop\r\n", "@01 0 OK BUSY NI 0\r\n")
    fake.expect("/1 0 lockstep 2 info\r\n", "@01 0 OK IDLE -- 3 4 0 0\r\n")
    fake.expect("/1 3\r\n", "@01 3 OK IDLE -- 0\r\n")
    lockstep.stop()
    fake.validate()


def test_get_status(lockstep, fake):
    fake.expect("/1 0 lockstep 2 info\r\n", "@01 0 OK BUSY -- 3 4 0 0\r\n")
    fake.expect("/1 3\r\n", "@01 3 OK BUSY -- 0\r\n")
    fake.expect("/1 0 lockstep 2 info\r\n", "@01 0 OK IDLE -- 3 4 0 0\r\n")
    fake.expect("/1 3\r\n", "@01 3 OK IDLE -- 0\r\n")
    assert(lockstep.get_status() == "BUSY")
    assert(lockstep.get_status() == "IDLE")
    fake.validate()
