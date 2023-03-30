from __future__ import annotations

import numpy as np
import pygame
from pygame import Vector2

from cardumen import utils
from cardumen.display import Display
from cardumen.geometry import PosRotScale, rad2deg
from cardumen.projection import Projection


class Polygon:
    def __init__(self, prs: PosRotScale, local_points: list[Vector2],
                 fill_color: tuple = (0, 0, 0, 0), line_color: tuple = (0, 0, 0, 0)):
        """
        Create polygon from points.
        Points are given in local coordinate system.
        The origin of the polygon in local coordinates is (0,0).
        The origin of the polygon in the global coordinate system is given by the PRS position.
        PRS controls the rotation and scale of the polygon.

        :param prs: position, rotation, scale
        :param local_points: list of points
        :param fill_color: fill color
        :param line_color: line color
        """
        self.prs = prs
        self._local_points = local_points  # local coordinates
        self.fill_color = fill_color
        self.line_color = line_color
        self._initial_fill_color = fill_color
        self._initial_line_color = line_color

    def render(self, display: Display) -> None:
        """
        Render polygon.

        :param display: display to render to
        :return:
        """
        display.draw_polygon(self.points, self.fill_color, self.line_color)

    def clone(self) -> Polygon:
        """
        Clone polygon.

        :return: new polygon
        """
        return self.__class__(self.prs.clone(), self.local_points, self.fill_color, self.line_color)

    def clone_at(self, pos: Vector2) -> Polygon:
        """
        Clone polygon at a new position.

        :param pos: new position
        :return: new polygon
        """
        poly = self.clone()
        poly.prs.pos = pos
        return poly

    def intersects(self, other: Polygon, check_wrap: bool = True) -> bool:
        """
        Check if two polygons intersect.

        :param other: other polygon
        :param check_wrap: check if also copies of the polygons wrapped around the screen
        :return: True if polygons intersect, False otherwise
        """
        if check_wrap:
            for wrap in utils.get_wraps():
                if Intersection.intersect(self.clone_at(self.prs.pos + wrap), other):
                    return True
            return False
        else:
            return Intersection.intersect(self, other)

    def get_surface(self, return_rect=False, local=False) -> pygame.Surface | tuple[pygame.Surface, pygame.Rect]:
        """
        Get pygame surface of the polygon, in global (or local) coordinates.
        Optionally return the bounding box of the polygon.

        :return: pygame surface or (surface, rect)
        """
        points = self.local_points if local else self.points
        rect = utils.get_rect(points)
        surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        offset_points = [(p[0] - rect.x, p[1] - rect.y) for p in points]
        pygame.draw.polygon(surface, self.fill_color[:3], offset_points)
        pygame.draw.lines(surface, self.fill_color[:3], True, offset_points, 1)
        if return_rect:
            return surface, rect
        return surface

    def set_color(self, fill: tuple = None, line: tuple = None) -> None:
        if fill:
            self.fill_color = fill
        if line:
            self.line_color = line

    def reset_color(self) -> None:
        self.fill_color = self._initial_fill_color
        self.line_color = self._initial_line_color

    @property
    def local_points(self) -> list[Vector2]:
        """
        Get points in local coordinates.

        :return: list of points
        """
        return [p for p in self._local_points]

    @property
    def points(self) -> list[Vector2]:
        """
        Get points in global coordinates.

        :return: list of points
        """
        return [(self.prs.scale * p.rotate(-self.prs.rot_deg) + self.prs.pos) for p in self._local_points]


class ConvexQuad(Polygon):
    def __init__(self, prs: PosRotScale, local_points: list[Vector2],
                 fill_color: tuple = (0, 0, 0, 0), line_color: tuple = (0, 0, 0, 0)):
        if len(local_points) != 4:
            raise ValueError("ConvexQuad must have 4 points")
        if not utils.check_convex_polygon(local_points):
            raise ValueError("ConvexQuad must be convex")
        super().__init__(prs, local_points, fill_color, line_color)

        self._define_projection()

    def _define_projection(self):
        points = self.local_points
        # largest side of the polygon
        max_side = max([p.distance_to(q) for p, q in zip(points, points[1:] + [points[0]])])
        # define projection to square
        rect = utils.get_rect(points)
        points = [Vector2(p[0] - rect.x, p[1] - rect.y) for p in points]
        self._projection = Projection(points, output_size=(max_side, max_side))

    def project(self, surf_local: pygame.Surface) -> np.ndarray:
        """
        Project the polygon onto a square.

        :param surf_local: surface to project to
        :return:
        """
        arr = utils.surf2arr(surf_local)
        return self._projection(arr)


class Intersection:

    @staticmethod
    def intersect(poly1: Polygon, poly2: Polygon) -> bool:
        """
        Check if two polygons intersect.

        :param poly1: polygon 1
        :param poly2: polygon 2
        :return: True if polygons intersect, False otherwise
        """
        tris1 = Intersection._get_tris(poly1)
        tris2 = Intersection._get_tris(poly2)
        for tri1 in tris1:
            for tri2 in tris2:
                if Intersection._tris_intersect(tri1, tri2):
                    return True
        return False

    @staticmethod
    def intersect_point(poly: Polygon, point: Vector2) -> bool:
        """
        Check if a point is inside a polygon.

        :param poly: polygon
        :param point: point
        :return: True if point is inside polygon, False otherwise
        """
        tris = Intersection._get_tris(poly)
        for tri in tris:
            if Intersection._point_in_tri(point, tri):
                return True
        return False

    @staticmethod
    def _get_tris(poly: Polygon) -> list[tuple[Vector2, Vector2, Vector2]]:
        """
        Get triangles of the polygon.
        Only works for convex polygons.
        Points are given in global coordinates.

        :param poly: polygon
        :return: list of triangles (3-tuples of points)
        """
        points = poly.points
        tris = []
        for i in range(len(points) - 2):
            tris.append((points[0], points[i + 1], points[i + 2]))
        return tris

    @staticmethod
    def _tris_intersect(tri1: tuple[Vector2, Vector2, Vector2], tri2: tuple[Vector2, Vector2, Vector2]) -> bool:
        """
        Check if two 2D triangles intersect.

        :param tri1: triangle 1 as a 3-tuple of points
        :param tri2: triangle 2 as a 3-tuple of points
        :return: True if triangles intersect, False otherwise
        """
        # https://stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect
        for i in range(3):
            for j in range(3):
                p1 = tri1[i]
                p2 = tri1[(i + 1) % 3]
                p3 = tri2[j]
                p4 = tri2[(j + 1) % 3]
                denom = (p4.y - p3.y) * (p2.x - p1.x) - (p4.x - p3.x) * (p2.y - p1.y)
                if denom == 0:
                    continue
                u_a = ((p4.x - p3.x) * (p1.y - p3.y) - (p4.y - p3.y) * (p1.x - p3.x)) / denom
                u_b = ((p2.x - p1.x) * (p1.y - p3.y) - (p2.y - p1.y) * (p1.x - p3.x)) / denom
                if 0 <= u_a <= 1 and 0 <= u_b <= 1:
                    return True
        return False

    @staticmethod
    def _point_in_tri(point: Vector2, tri: tuple[Vector2, Vector2, Vector2]) -> bool:
        """
        Check if point is contained in a 2D triangle.

        :param point: point global coordinates
        :param tri: triangle as a 3-tuple of points
        :return: True if point is contained in triangle, False otherwise
        """
        # http://totologic.blogspot.com/2014/01/accurate-point-in-triangle-test.html
        v0 = tri[2] - tri[0]
        v1 = tri[1] - tri[0]
        v2 = point - tri[0]

        dot00 = v0.dot(v0)
        dot01 = v0.dot(v1)
        dot02 = v0.dot(v2)
        dot11 = v1.dot(v1)
        dot12 = v1.dot(v2)

        inv_denom = 1 / (dot00 * dot11 - dot01 * dot01)
        u = (dot11 * dot02 - dot01 * dot12) * inv_denom
        v = (dot00 * dot12 - dot01 * dot02) * inv_denom
        return u >= 0 and v >= 0 and u + v < 1

    # BY CHATGPT

    # @staticmethod
    # def segment_intersect(p1, q1, p2, q2):
    #     """Returns True if line segment p1-q1 intersects with line segment p2-q2."""
    #
    #     def orientation(p, q, r):
    #         """Returns the orientation of the triplet (p,q,r)."""
    #         val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    #         if val == 0:
    #             return 0
    #         elif val > 0:
    #             return 1
    #         else:
    #             return 2
    #
    #     o1 = orientation(p1, q1, p2)
    #     o2 = orientation(p1, q1, q2)
    #     o3 = orientation(p2, q2, p1)
    #     o4 = orientation(p2, q2, q1)
    #
    #     if o1 != o2 and o3 != o4:
    #         return True
    #
    #     if o1 == 0 and Intersection.on_segment(p1, p2, q1):
    #         return True
    #
    #     if o2 == 0 and Intersection.on_segment(p1, q2, q1):
    #         return True
    #
    #     if o3 == 0 and Intersection.on_segment(p2, p1, q2):
    #         return True
    #
    #     if o4 == 0 and Intersection.on_segment(p2, q1, q2):
    #         return True
    #
    #     return False
    #
    # @staticmethod
    # def on_segment(p, q, r):
    #     """Returns True if point q lies on line segment pr."""
    #     if (q[0] <= max(p[0], r[0])) and (q[0] >= min(p[0], r[0])) and \
    #             (q[1] <= max(p[1], r[1])) and (q[1] >= min(p[1], r[1])):
    #         return True
    #     return False
    #
    # @staticmethod
    # def get_line_segments(poly):
    #     """Returns a list of line segments for the given polygon."""
    #     segments = []
    #     for i in range(len(poly)):
    #         segments.append((poly[i], poly[(i + 1) % len(poly)]))
    #     return segments
    #
    # @staticmethod
    # def bbox_intersect(poly1, poly2):
    #     """Returns True if the bounding boxes of poly1 and poly2 intersect."""
    #     bbox1 = (min(p[0] for p in poly1), min(p[1] for p in poly1),
    #              max(p[0] for p in poly1), max(p[1] for p in poly1))
    #     bbox2 = (min(p[0] for p in poly2), min(p[1] for p in poly2),
    #              max(p[0] for p in poly2), max(p[1] for p in poly2))
    #     if bbox1[2] < bbox2[0] or bbox1[0] > bbox2[2] or bbox1[3] < bbox2[1] or bbox1[1] > bbox2[3]:
    #         return False
    #     else:
    #         return True
    #
    # @staticmethod
    # def polygon_intersection(poly1, poly2):
    #     """Returns True if polygon poly1 intersects with polygon poly2."""
    #
    #     # Get the line segments for each polygon
    #     segments1 = Intersection.get_line_segments(poly1)
    #     segments2 = Intersection.get_line_segments(poly2)
    #
    #     # Check if the bounding boxes intersect
    #     if not Intersection.bbox_intersect(poly1, poly2):
    #         return False
    #
    #     # Check if any line segment from poly1 intersects with any line segment from poly2
    #     for segment1 in segments1:
    #         for segment2 in segments2:
    #             if Intersection.segment_intersect(segment1[0], segment1[1], segment2[0], segment2[1]):
    #                 return True
    #
    #     # If we reach this point, the polygons do not intersect
    #     return False
