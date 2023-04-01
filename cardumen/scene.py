from collections import defaultdict
from random import random

from pygame import Vector2

from cardumen.display import Display
from cardumen.entities import WaterBg
from cardumen.fish import Fish
from cardumen.geometry import PosRotScale
from cardumen.handler import Handler


class PlaygroundScene:

    def __init__(self):
        self.layers = defaultdict(list)

        water = WaterBg()
        self.layers[0].append(water)
        for i in range(0, Handler().config.n_fish):
            w, h = Handler().config.WINDOW_SIZE
            fish = Fish(PosRotScale(Vector2(w * random(), h * random())), cat=i % 7 + 1)
            self.layers[-1].append(fish)

    def update(self, dt: float) -> None:
        """
        Update scene.
        :param dt: time since last update
        :return:
        """
        for layer in sorted(self.layers, reverse=True):
            width, height = Handler().config.WINDOW_SIZE
            for entity in self.layers[layer]:
                entity.update(dt)

                # wrap every entity position
                if entity.prs.pos.x > width:
                    entity.prs.pos.x -= width
                elif entity.prs.pos.x < 0:
                    entity.prs.pos.x += width
                if entity.prs.pos.y > height:
                    entity.prs.pos.y -= height
                elif entity.prs.pos.y < 0:
                    entity.prs.pos.y += height

    def render(self, display: Display) -> None:
        """
        Render scene.
        :param display: display to render to
        :return:
        """
        for layer in sorted(self.layers, reverse=True):
            for entity in self.layers[layer]:
                entity.render(display)
        if Handler().config.DEBUG:
            display.draw_grid()
