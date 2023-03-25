from __future__ import annotations

from pygame import Vector2

from cardumen.display import Display
from cardumen.geometry import PosRotScale
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

    def update(self, dt: float) -> None:
        """
        Update scene.
        :param dt: time since last update
        :return:
        """
        pass

    def render(self, display: Display) -> None:
        """
        Render scene.
        :param display: display to render to
        :return:
        """
        display.draw_sprite(self.sprite, self.prs)


class WaterBg(Entity):
    def __init__(self, screen_size: Vector2):
        super().__init__(PosRotScale(screen_size/2), Sprite("assets/water.png"))
        # fit screen
        self.sprite.apply_transform(scale=max(screen_size.x / self.sprite.width, screen_size.y / self.sprite.height))

    def render(self, display: Display) -> None:
        display.draw_sprite(self.sprite, self.prs, wrap=False)


