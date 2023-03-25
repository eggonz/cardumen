from collections import defaultdict

from pygame import Vector2

from cardumen.display import Display
from cardumen.entities import Entity, WaterBg
from cardumen.fish import Fish
from cardumen.geometry import PosRotScale, deg2rad
from cardumen.sprite import Sprite


class PlaygroundScene:

    def __init__(self, screen_size: tuple):
        self._screen_size = Vector2(screen_size)

        self.layers = defaultdict(list)

        water = WaterBg(self._screen_size)
        fish1 = Fish(PosRotScale(self._screen_size/2))

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

                # wrap every entity position
                if entity.prs.pos.x > self._screen_size.x:
                    entity.prs.pos.x -= self._screen_size.x
                elif entity.prs.pos.x < 0:
                    entity.prs.pos.x += self._screen_size.x
                if entity.prs.pos.y > self._screen_size.y:
                    entity.prs.pos.y -= self._screen_size.y
                elif entity.prs.pos.y < 0:
                    entity.prs.pos.y += self._screen_size.y

    def render(self, display: Display) -> None:
        """
        Render scene.
        :param display: display to render to
        :return:
        """
        for layer in sorted(self.layers, reverse=True):
            for entity in self.layers[layer]:
                entity.render(display)
