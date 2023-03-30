import pytest
from pygame import Vector2

from cardumen import geometry


@pytest.fixture
def pi():
    return 3.141592653589793


def test_rad2deg(pi):
    assert geometry.rad2deg(0) == 0
    assert geometry.rad2deg(pi) == 180
    assert geometry.rad2deg(2 * pi) == 0
    assert geometry.rad2deg(-pi) == 180
    assert geometry.rad2deg(3 * pi) == 180


def test_deg2rad(pi):
    assert geometry.deg2rad(0) == 0
    assert geometry.deg2rad(180) == pi
    assert geometry.deg2rad(360) == 0
    assert geometry.deg2rad(-180) == pi
    assert geometry.deg2rad(540) == pi


def test_posrotscale_init():
    prs = geometry.PosRotScale()
    assert prs.pos == (0, 0)
    assert prs.rot == 0
    assert prs.scale == 1
    prs = geometry.PosRotScale(Vector2(1, 2), 3, 4)
    assert prs.pos == (1, 2)
    assert prs.rot == 3
    assert prs.scale == 4


def test_posrotscale_clone():
    prs1 = geometry.PosRotScale()
    prs2 = prs1.clone()
    assert prs1.pos == prs2.pos
    assert prs1.rot == prs2.rot
    assert prs1.scale == prs2.scale


def test_posrotscale_inverse():
    prs1 = geometry.PosRotScale(Vector2(1, 2), 3, 4)
    prs2 = prs1.inverse()
    assert prs2.pos == (-1, -2)
    assert prs2.rot == -3
    assert prs2.scale == 0.25


def test_posrotscale_apply():
    prs1 = geometry.PosRotScale(Vector2(1, 2), 3, 4)
    prs2 = geometry.PosRotScale(Vector2(5, 6), 7, 8)
    prs1.apply(prs2)
    assert prs1.pos == (1 + 5, 2 + 6)
    assert prs1.rot == 3 + 7
    assert prs1.scale == 4 * 8


def test_posrotscale_properties(pi):
    prs = geometry.PosRotScale()
    # get rot_deg
    assert prs.rot_deg == 0
    prs.rot = pi
    assert prs.rot_deg == 180


def test_posrotscale_magic(pi):
    prs1 = geometry.PosRotScale(Vector2(1, 2), 3, 4)
    prs2 = geometry.PosRotScale(Vector2(1, 2), 3, 4)
    # eq
    assert prs1 is not prs2
    assert prs1 == prs2
    # repr
    assert repr(prs1) == "PosRotScale(pos=[1, 2], rot=3, scale=4)"
