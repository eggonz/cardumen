from __future__ import annotations

import math

from pygame import Vector2


def rad2deg(rad: float) -> float:
    """
    Utility function to convert angles from radians to degrees.

    :param rad: angle in radians
    :return: angle in degrees
    """
    rad %= 2 * math.pi
    return rad * 360 / 2.0 / math.pi


def deg2rad(deg: float) -> float:
    """
    Utility function to convert angles from degrees to radians.

    :param deg: angle in degrees
    :return: angle in radians
    """
    deg %= 360
    return deg * 2.0 * math.pi / 360


class PosRotScale:
    """
    Class to represent position, rotation and scale of an object.
    """

    def __init__(self, pos: Vector2 = Vector2(0, 0), rot: float = 0, scale: float = 1):
        """
        Create a new PosRotScale object.

        :param pos: position of the object
        :param rot: rotation of the object, in radians, positive counterclockwise
        :param scale: scale of the object
        """
        self.pos = pos
        self.rot = rot
        self.scale = scale

    def clone(self) -> PosRotScale:
        """
        Create a copy of this object.

        :return: copy of this object
        """
        return PosRotScale(self.pos.copy(), self.rot, self.scale)

    def inverse(self) -> PosRotScale:
        """
        Create a new PosRotScale object representing the inverse transformation of this object.

        :return: inverse transformation
        """
        return PosRotScale(-self.pos, -self.rot, 1 / self.scale)

    def apply(self, prs: PosRotScale) -> None:
        """
        Apply the transformation represented by another PosRotScale object to this object.

        :param prs: transformation to apply
        """
        self.pos += prs.pos
        self.rot += prs.rot
        self.scale *= prs.scale

    @property
    def rot_deg(self) -> float:
        """
        Rotation of the object, in degrees, positive counterclockwise.

        :return: rotation angle
        """
        return rad2deg(self.rot)

    def __eq__(self, other):
        return self.pos == other.pos and self.rot == other.rot and self.scale == other.scale

    def __repr__(self):
        return f'PosRotScale(pos={self.pos}, rot={self.rot}, scale={self.scale})'
