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


def scale_points(points: list[Vector2], scale: float) -> list[Vector2]:
    """
    Scale points by scale around the origin.

    :param points:
    :param scale:
    :return:
    """
    return [p * scale for p in points]


def rotate_points(points: list[Vector2], angle: float) -> list[Vector2]:
    """
    Rotate points by angle around the origin.
    Angle is in radians and positive is counterclockwise.

    :param points:
    :param angle:
    :return:
    """
    return [p.rotate(-rad2deg(angle)) for p in points]


def move_points(points: list[Vector2], offset: Vector2) -> list[Vector2]:
    """
    Move points by offset.

    :param points:
    :param offset:
    :return:
    """
    return [p + offset for p in points]


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

    def relative_to(self, other: PosRotScale) -> PosRotScale:
        """
        Get the transformation of this object relative to another PosRotScale object.

        :param other: other object
        :return: transformation of this object relative to the other object
        """
        return PosRotScale(
            # default Vector2 in clockwise rotation
            (self.pos - other.pos).rotate(other.rot_deg) / other.scale,
            self.rot - other.rot,
            self.scale / other.scale
        )

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
