"""
Collision detection and response.
"""
from __future__ import annotations

from collections import defaultdict

from cardumen import utils
from cardumen.display import Display
from cardumen.shapes import Polygon


class Collider:
    """
    A collider is a polygon that can be used to detect collisions.
    """
    # Inverted indices for fast retrieval of colliders
    _TAG_INDEX = defaultdict(list)

    # parent is not type hinted to avoid circular import
    def __init__(self, parent, poly: Polygon, tag: str, detect: str = None, ignore_self: bool = True):
        """
        Create a collider.

        :param parent: entity that owns this collider
        :param poly: polygon
        :param tag: tag of this collider
        :param detect: tag of colliders to detect
        :param ignore_self: ignore self collisions
        """
        self.parent = parent
        self.poly = poly
        self.tag = tag
        self._detect = detect
        self._ignore_self = ignore_self

        Collider._TAG_INDEX[tag].append(self)

        self._colliding = defaultdict(bool)

    def check_collisions(self) -> None:
        """
        Check collisions.

        :return:
        """
        if self._detect is None:
            return

        for other in self._TAG_INDEX[self._detect]:
            if other == self:
                continue
            if self._ignore_self and other.parent == self.parent:
                continue
            if self.poly.intersects(other.poly):
                if not self._colliding[other]:
                    self._colliding[other] = True
                    self.on_collision_start(other)
                self.on_collision(other)
            else:
                if self._colliding[other]:
                    self._colliding.pop(other)  # instead of setting to False, remove key to save memory
                    self.on_collision_end(other)

    def update(self, dt: float) -> None:
        """
        Update collider.

        :param dt: time since last update
        :return:
        """
        self.check_collisions()

    def render(self, display: Display) -> None:
        """
        Render collider.

        :param display: display to render to
        :return:
        """
        self.poly.render(display)

    def is_colliding_with(self, other: Collider) -> bool:
        """
        Check if this collider is colliding with another collider.

        :param other: other collider
        :return: True if colliding, False otherwise
        """
        return self._colliding.get(other, False)

    def is_colliding(self) -> bool:
        """
        Check if this collider is colliding with any other collider.

        :return: True if colliding, False otherwise
        """
        return len(self._colliding) > 0

    def on_collision(self, other: Collider) -> None:
        """
        Called when this collider is colliding with another collider.

        :param other: collider that is colliding
        :return:
        """
        pass

    def on_collision_start(self, other: Collider) -> None:
        """
        Called when this collider starts colliding with another collider.

        :param other: collider that started colliding
        :return:
        """
        pass

    def on_collision_end(self, other: Collider) -> None:
        """
        Called when this collider stops colliding with another collider.

        :param other: collider that stopped colliding
        :return:
        """
        pass
