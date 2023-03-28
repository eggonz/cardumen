"""
Collision detection and response.
"""
from __future__ import annotations

from collections import defaultdict

from cardumen.display import Display
from cardumen.shapes import Polygon


class Collider:
    """
    A collider is a polygon that can be used to detect collisions.
    """
    _TAG_INDEX = defaultdict(set)
    _ENTITY_INDEX = defaultdict(set)

    def __init__(self, entity, poly: Polygon, tag: str, detect: str = None):
        """
        Create a collider.

        :param entity: entity that owns this collider
        :param poly: polygon
        :param tag: tag of this collider
        :param detect: tag of colliders to detect
        """
        self._entity = entity
        self.poly = poly
        self.tag = tag
        self._detect = detect
        self._TAG_INDEX[tag].add(poly)
        self._ENTITY_INDEX[entity].add(poly)

        self._colliding = False

    def get_colliding(self) -> list[Polygon]:
        """
        Get colliding polygons.

        :return: list of colliding polygons
        """
        if self._detect is None:
            return []
        for poly in self._TAG_INDEX[self._detect]:
            if poly != self.poly and poly not in self._ENTITY_INDEX[self._entity]:
                if self.poly.intersects(poly):
                    yield poly

    def is_colliding(self) -> bool:
        """
        Check if this collider is colliding with any other collider.

        :return: True if colliding, False otherwise
        """
        return any(self.get_colliding())

    def update(self, dt: float) -> None:
        """
        Update collider.

        :param dt: time since last update
        :return:
        """
        self.poly.update(dt)
        if self.is_colliding():
            if not self._colliding:
                self._colliding = True
                self.on_collision_start()
            self.on_collision()
        else:
            if self._colliding:
                self._colliding = False
                self.on_collision_end()

    def render(self, display: Display) -> None:
        """
        Render collider.

        :param display: display to render to
        :return:
        """
        self.poly.render(display)

    def on_collision(self) -> None:
        """
        Called when this collider is colliding with another collider.

        :return:
        """
        pass

    def on_collision_start(self) -> None:
        """
        Called when this collider starts colliding with another collider.

        :return:
        """
        pass

    def on_collision_end(self) -> None:
        """
        Called when this collider stops colliding with another collider.

        :return:
        """
        pass
