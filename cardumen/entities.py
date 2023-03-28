from __future__ import annotations

from pygame import Vector2

from cardumen.collision import Collider
from cardumen.display import Display
from cardumen.geometry import PosRotScale
from cardumen.handler import Handler
from cardumen.sprite import Sprite


class Entity:
    def __init__(self, handler: Handler, prs: PosRotScale, sprite: Sprite = None):
        """
        Create an Entity.

        :param prs: position, rotation, scale
        :param sprite: sprite to draw
        """
        self._handler = handler
        self.prs = prs
        self.sprite = sprite
        self.colliders = []

    def update(self, dt: float) -> None:
        """
        Update scene.
        :param dt: time since last update
        :return:
        """
        for collider in self.colliders:
            collider.update(dt)

    def render(self, display: Display) -> None:
        """
        Render scene.
        :param display: display to render to
        :return:
        """
        display.draw_sprite(self.sprite, self.prs)
        if self._handler.config.DEBUG:
            for collider in self.colliders:
                collider.render(display)

    def add_colliders(self, *colliders: Collider) -> None:
        self.colliders.extend(colliders)


class WaterBg(Entity):
    def __init__(self, handler: Handler, screen_size: Vector2):
        super().__init__(handler, PosRotScale(screen_size / 2), Sprite("assets/water.png"))
        # fit screen
        self.sprite.apply_transform(scale=max(screen_size.x / self.sprite.width, screen_size.y / self.sprite.height))

    def render(self, display: Display) -> None:
        display.draw_sprite(self.sprite, self.prs, wrap=False)
