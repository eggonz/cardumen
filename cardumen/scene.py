from collections import defaultdict
from random import random

from pygame import Vector2

from cardumen.display import Display
from cardumen.entities import WaterBg
from cardumen.fish import Fish
from cardumen.geometry import PosRotScale
from cardumen.handler import Handler


class PlaygroundScene:

    def __init__(self, handler: Handler):
        self._handler = handler

        self.layers = defaultdict(list)

        water = WaterBg(handler, handler.display.screen_size)
        self.layers[0].append(water)
        n = 5
        for i in range(0, n):
            w, h = handler.display.screen_size
            fish = Fish(handler, PosRotScale(Vector2(w * random(), h * random())), cat=i % 7 + 1)
            self.layers[-1].append(fish)

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
                if entity.prs.pos.x > self._handler.display.screen_size.x:
                    entity.prs.pos.x -= self._handler.display.screen_size.x
                elif entity.prs.pos.x < 0:
                    entity.prs.pos.x += self._handler.display.screen_size.x
                if entity.prs.pos.y > self._handler.display.screen_size.y:
                    entity.prs.pos.y -= self._handler.display.screen_size.y
                elif entity.prs.pos.y < 0:
                    entity.prs.pos.y += self._handler.display.screen_size.y

    def render(self, display: Display) -> None:
        """
        Render scene.
        :param display: display to render to
        :return:
        """
        for layer in sorted(self.layers, reverse=True):
            for entity in self.layers[layer]:
                entity.render(display)
