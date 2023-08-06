import pytest

from zaber.serial import AsciiLockstepInfo


def test_parsing_enabled():
    a = AsciiLockstepInfo("1 2 -500 2")
    assert(a.is_enabled is True)
    assert(a.axis1 == 1)
    assert(a.axis2 == 2)
    assert(a.offset == -500)
    assert(a.twist == 2)


def test_parsing_disabled():
    a = AsciiLockstepInfo("disabled")
    assert(a.is_enabled is False)


def test_str():
    a = AsciiLockstepInfo("1 2 -500 2")
    assert str(a) == "Axis1=1,Axis2=2,Offset=-500,Twist=2"
    a = AsciiLockstepInfo("disabled")
    assert str(a) == "Disabled"
