import math


def rad2deg(rad: float) -> float:
    return rad * 360 / 2.0 / math.pi


class LocRotScale:
    def __init__(self, x: float = 0, y: float = 0, angle: float = 0, scale: float = 1):
        self._orig_x = x
        self._orig_y = y
        self._orig_angle = angle
        self._orig_scale = scale
        self.x = x
        self.y = y
        self.angle = angle
        self.scale = scale

    def apply_translation(self, dx: int, dy: int) -> None:
        self.x += dx
        self.y += dy

    def apply_rotation(self, d_angle: int) -> None:
        self.angle += d_angle

    def apply_scale(self, scale: float) -> None:
        self.scale *= scale

    def reset_translation(self) -> None:
        self.x = self._orig_x
        self.y = self._orig_y

    def reset_rotation(self) -> None:
        self.angle = self._orig_angle

    def reset_scale(self) -> None:
        self.scale = self._orig_scale

    def reset_transform(self) -> None:
        self.x = self._orig_x
        self.y = self._orig_y
        self.angle = self._orig_angle
        self.scale = self._orig_scale

    def __repr__(self) -> str:
        attrs = [f'{a}={self.__dict__[a]}' for a in vars(self) if not a.startswith('_')]
        return f'{self.__class__.__name__}({",".join(attrs)})'


class Box:
    def __init__(self, width: int, height: int, offset_x: int = 0, offset_y: int = 0):
        self._orig_width = width
        self._orig_height = height
        self._orig_offset_x = offset_x
        self._orig_offset_y = offset_y
        self.width = width
        self.height = height
        self.offset_x = offset_x
        self.offset_y = offset_y

    def apply_scale(self, scale: float) -> None:
        self.width *= scale
        self.height *= scale
        self.offset_x *= scale
        self.offset_y *= scale

    def reset_scale(self) -> None:
        self.width = self._orig_width
        self.height = self._orig_height
        self.offset_x = self._orig_offset_x
        self.offset_y = self._orig_offset_y

    def __repr__(self) -> str:
        attrs = [f'{a}={self.__dict__[a]}' for a in vars(self) if not a.startswith('_')]
        return f'{self.__class__.__name__}({",".join(attrs)})'
