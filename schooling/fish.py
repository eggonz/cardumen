import math

from schooling.entities import Entity
from schooling.utils.events import Events
from schooling.utils.geometry import LocRotScale, deg2rad
from schooling.utils.graphics import Sprite


class Fish(Entity):
    def __init__(self, position: LocRotScale, *, eid: str = None):
        super().__init__(
            position,
            Sprite.from_image('res/fish1.png', apply_rotation=deg2rad(-90), apply_scale=.08),
            eid=eid,
        )
        self.speed = 200.0

    def update(self, dt: float) -> None:
        super().update(dt)
        if Events.is_key_pressed(Events.Key.ARROW_RIGHT):
            self.tilt_right()
        if Events.is_key_pressed(Events.Key.ARROW_LEFT):
            self.tilt_left()
        vx, vy = self.get_speed_vect()
        self.position.x += vx * dt
        self.position.y += vy * dt

    def get_speed_vect(self) -> tuple:
        speed_x = self.speed * math.cos(self.position.angle)
        speed_y = - self.speed * math.sin(self.position.angle)
        return speed_x, speed_y

    def tilt_left(self) -> None:
        self.position.apply_rotation(0.03)

    def tilt_right(self) -> None:
        self.position.apply_rotation(-0.03)
