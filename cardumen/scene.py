from collections import defaultdict

from pygame import Vector2

from cardumen.display import Display
from cardumen.entities import Entity
from cardumen.geometry import PosRotScale, deg2rad
from cardumen.sprite import Sprite


class PlaygroundScene:

    def __init__(self, screen_size: tuple):
        self._screen_size = screen_size

        self.layers = defaultdict(list)

        screen_center = Vector2(*self._screen_size)/2
        water = Entity(PosRotScale(screen_center), Sprite("assets/water.png"))
        # fit screen
        water.sprite.apply_transform(scale=max(screen_size[0] / water.sprite.width, screen_size[1] / water.sprite.height))
        fish1 = Entity(PosRotScale(screen_center), Sprite("assets/fish1.png", rot=deg2rad(90), scale=0.05))

        self.layers[0].append(water)
        self.layers[-1].append(fish1)

    def update(self, dt: float) -> None:
        """
        Update scene.
        :param dt: time since last update
        :return:
        """
        for layer in sorted(self.layers, reverse=True):
            for entity in self.layers[layer]:
                entity.update(dt)

    def render(self, display: Display) -> None:
        """
        Render scene.
        :param display: display to render to
        :return:
        """
        for layer in sorted(self.layers, reverse=True):
            for entity in self.layers[layer]:
                entity.render(display)
