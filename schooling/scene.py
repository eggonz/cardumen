import math
import time

from schooling.config import RuntimeContext, RunConfig
from schooling.entities import EntityManager, Entity
from schooling.fish import Fish, Water
from schooling.utils.geometry import LocRotScale, rad2deg
from schooling.utils.graphics import Display


class Scene:
    def __init__(self):
        self._entity_manager = EntityManager()

        # Background
        self.bg = Water(LocRotScale(RunConfig.WINDOW_SIZE[0]/2, RunConfig.WINDOW_SIZE[1]/2), eid='water')
        self._entity_manager.add_entity(self.bg, 0)

        # Fish
        fish1 = Fish(LocRotScale(200, 300), eid='fish1')
        self.fish2 = Fish(LocRotScale(400, 300), eid='fish2')
        self._entity_manager.add_entity(fish1, 1)
        self._entity_manager.add_entity(self.fish2, 1)

    def update(self, dt: float):
        self._entity_manager.update(dt)

        # Example1: screen movement changes behaviour
        w = 2.0 * math.pi / 3
        t0 = RuntimeContext.start_time
        fish1 = Entity.get_by_eid('fish1')
        dx1 = dt * 300 * 0.9 * w * math.sin(0.9 * w * (time.time() - t0))
        dy1 = dt * 200 * 1.3 * w * math.sin(1.3 * w * (time.time() - t0) - math.pi / 2)
        fish1.position.apply_translation(int(dx1), int(dy1))

        # Example2: screen movement suddenly changes position but remains
        dx2 = dt * 50 * w * math.cos(w * (time.time() - t0))
        dy2 = dt * 200 * w * math.cos(w * (time.time() - t0) - math.pi / 2)
        self.fish2.position.x = 400 + 50 * math.sin(w * (time.time() - t0))
        self.fish2.position.y = 300 + 200 * math.sin(w * (time.time() - t0) - math.pi / 2)

        fish1.position.angle = rad2deg(math.atan2(-dy1 / dt, dx1 / dt))
        self.fish2.position.angle = rad2deg(math.atan2(-dy2 / dt, dx2 / dt))

    def render(self, display: Display):
        self._entity_manager.render(display)
