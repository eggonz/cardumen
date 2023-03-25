from __future__ import annotations

from pygame import Vector2

from cardumen.control import Action, Agent
from cardumen.entities import Entity
from cardumen.geometry import PosRotScale, deg2rad, rad2deg
from cardumen.sprite import Sprite


class Swim(Action):
    NONE = 0
    RIGHT = -1
    LEFT = 1
    RIGHTx3 = -3
    LEFTx3 = 3
    FASTER = 0, 1.1
    SLOWER = 0, 0.9

    def __init__(self, tilt_sign: float, vel_multiplier: float = 1):
        self._tilt_sign = tilt_sign
        self._vel_multiplier = vel_multiplier

    def execute(self, fish: Fish, dt: float) -> None:
        fish.prs.rot += self._tilt_sign * dt * fish.tilt_speed
        fish.speed *= self._vel_multiplier


class Fish(Entity):
    def __init__(self, prs: PosRotScale):
        super().__init__(prs, Sprite("assets/fish1.png", rot=deg2rad(-90), scale=.05))

        base_speed = 200
        self.min_speed = base_speed * .25
        self.max_speed = base_speed * 4
        self.speed = base_speed
        self.tilt_speed = .5
        self.vel = Vector2()
        self.vel.from_polar((self.speed, -rad2deg(self.prs.rot)))

        self._agent = Agent(list(Swim))

    def update(self, dt: float) -> None:
        action = self._agent.act(self.get_state())
        action.execute(self, dt)
        self.speed = max(self.min_speed, min(self.max_speed, self.speed))
        self.vel.from_polar((self.speed, -rad2deg(self.prs.rot)))
        self.prs.pos += self.vel * dt

    def get_state(self) -> list:
        return [tuple(self.prs.pos), tuple(self.vel)]
