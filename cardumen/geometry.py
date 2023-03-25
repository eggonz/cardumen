import math

from pygame import Vector2


def rad2deg(rad: float) -> float:
    """
    Utility function to convert angles from radians to degrees.

    :param rad: angle in radians
    :return: angle in degrees
    """
    return rad * 360 / 2.0 / math.pi


def deg2rad(deg: float) -> float:
    """
    Utility function to convert angles from degrees to radians.

    :param deg: angle in degrees
    :return: angle in radians
    """
    return deg * 2.0 * math.pi / 360


class PosRotScale:
    """
    Class to represent position, rotation and scale of an object.
    """
    def __init__(self, pos: Vector2 = Vector2(0, 0), rot: float = 0, scale: float = 1):
        """
        Create a new PosRotScale object.

        :param pos: position of the object
        :param rot: rotation of the object
        :param scale: scale of the object
        """
        self.pos = pos
        self.rot = rot
        self.scale = scale

    def __repr__(self):
        return f'PosRotScale(pos={self.pos},rot={self.rot},scale={self.scale})'

