from __future__ import annotations

from pygame import Vector2

from cardumen.display import Display
from cardumen.geometry import PosRotScale, rad2deg


class Shape:
    def __init__(self, prs: PosRotScale, points: list[Vector2],
                 fill_color: tuple = (0, 0, 0, 0), line_color: tuple = (0, 0, 0, 0)):
        """
        Create shape from points.
        Points are given in local coordinate system.
        The origin of the shape in local coordinates is (0,0).
        The origin of the shape in the global coordinate system is given by the PRS position.
        PRS controls the rotation and scale of the shape.

        :param prs: position, rotation, scale
        :param points: list if points
        :param fill_color: fill color
        :param line_color: line color
        """
        self.prs = prs
        self._points = points  # local coordinates
        self.fill_color = fill_color
        self.line_color = line_color

    def move_local(self, move: Vector2 = Vector2()) -> Shape:
        """
        Applies displacement to the points in local coordinates.

        :param move: position displacement
        :return:
        """
        self._points = [p + move for p in self._points]
        return self

    def rot_local(self, rot: float = 0) -> Shape:
        """
        Applies rotation to the points in local coordinates w.r.t. the origin ((0,0))

        :param rot: rotation angle, in radians, positive counterclockwise
        :return:
        """
        self._points = [p.rotate(-rad2deg(rot)) for p in self._points]
        return self

    def scale_local(self, scale: float = 1) -> Shape:
        """
        Scales the position of the points in local coordinates w.r.t. the origin ((0,0))

        :param scale: scaling factor
        :return:
        """
        self._points = [scale * p for p in self._points]
        return self

    def render(self, display: Display) -> None:
        """
        Render shape.

        :param display: display to render to
        :return:
        """
        display.draw_polygon(self.points, self.fill_color, self.line_color)

    @property
    def points(self) -> list[Vector2]:
        """
        Get points in global coordinates.

        :return: list of points
        """
        return [(self.prs.scale * p.rotate(-self.prs.rot_deg) + self.prs.pos) for p in self._points]
