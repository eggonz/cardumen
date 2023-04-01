from __future__ import annotations

from cardumen.collision import Collider
from cardumen.display import Display
from cardumen.geometry import PosRotScale
from cardumen.handler import Handler
from cardumen.sprite import Sprite


class Entity:
    def __init__(self, prs: PosRotScale, sprite: Sprite = None):
        """
        Create an Entity.

        :param prs: position, rotation, scale
        :param sprite: sprite to draw
        """
        self.prs = prs
        self.sprite = sprite
        self.colliders = []

    def update(self, dt: float) -> None:
        """
        Update entity.
        :param dt:
        :return:
        """
        for collider in self.colliders:
            collider.update(dt)

    def render(self, display: Display) -> None:
        """
        Render entity.
        :param display: display to render to
        :return:
        """
        display.draw_sprite(self.sprite, self.prs)
        if Handler().config.DEBUG:
            for collider in self.colliders:
                collider.render(display)

    def add_colliders(self, *colliders: Collider) -> None:
        self.colliders.extend(colliders)


class WaterBg(Entity):
    def __init__(self):
        screen_size = Handler().config.WINDOW_SIZE
        super().__init__(PosRotScale(screen_size / 2), Sprite("assets/water.png"))
        # fit screen
        self.sprite.apply_transform(scale=max(screen_size.x / self.sprite.width, screen_size.y / self.sprite.height))

    def render(self, display: Display) -> None:
        display.draw_sprite(self.sprite, self.prs, wrap=False)
