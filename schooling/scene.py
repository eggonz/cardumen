import math
from random import random, randint

from schooling.background import Water
from schooling.config import RunConfig
from schooling.entities import EntityManager
from schooling.fish import Fish
from schooling.utils.geometry import LocRotScale
from schooling.utils.graphics import Display


class Scene:
    def __init__(self):
        self._entity_manager = EntityManager()

        self._init_entities()

    def _init_entities(self) -> None:

        # Background
        bg = Water(LocRotScale(RunConfig.WINDOW_SIZE[0]/2, RunConfig.WINDOW_SIZE[1]/2))
        self._entity_manager.add_entity(bg, 0)

        # Fish
        fish = Fish(LocRotScale(randint(0, 800), randint(0, 400), math.pi * random()), eid='fish')
        self._entity_manager.add_entity(fish, 1)

    def update(self, dt: float):
        self._entity_manager.update(dt)

    def render(self, display: Display):
        self._entity_manager.render(display)
