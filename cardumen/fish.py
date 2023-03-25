from __future__ import annotations

from pygame import Vector2

from cardumen.control import Action, Agent
from cardumen.entities import Entity
from cardumen.geometry import PosRotScale, deg2rad, rad2deg
from cardumen.shapes import Shape
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
        self.vel.from_polar((self.speed, -self.prs.rot_deg))

        self._agent = Agent(list(Swim))

        # trapezoid view
        w, h = self.sprite.width, self.sprite.height
        trapezoid = Shape(self.prs, [Vector2(-1, 0), Vector2(1, 0), Vector2(6, 12), Vector2(-6, 12)],
                          fill_color=(255, 255, 255, 100), line_color=(0, 0, 0, 255))
        view = trapezoid.scale_local(h / 2).rot_local(deg2rad(90)).move_local(Vector2(w / 2 + 4, 0))

        # body rect collider
        rect = Shape(self.prs, [Vector2(0, 0), Vector2(w, 0), Vector2(w, h), Vector2(0, h)],
                     fill_color=(0, 255, 0, 100), line_color=(0, 255, 0, 255))
        collider = rect.move_local(Vector2(-w / 2, -h / 2))

        # proximity sense hexagon collider
        l = 100  # side length
        a = l / 2 * (3 ** .5)  # apothem
        hexagon_points = [Vector2(0, -l), Vector2(a, -l / 2), Vector2(a, l / 2), Vector2(0, l),
                          Vector2(-a, l / 2), Vector2(-a, -l / 2)]
        sensor = Shape(self.prs, hexagon_points, fill_color=(0, 0, 255, 100), line_color=(0, 0, 255, 255))

        self._shapes = [view, collider, sensor]

    def update(self, dt: float) -> None:
        action = self._agent.act(self.get_state())
        action.execute(self, dt)
        self.speed = max(self.min_speed, min(self.max_speed, self.speed))
        self.vel.from_polar((self.speed, -self.prs.rot_deg))
        self.prs.pos += self.vel * dt

    def render(self, display) -> None:
        super().render(display)
        for shape in self._shapes:
            shape.render(display)

    def get_state(self) -> list:
        return [tuple(self.prs.pos), tuple(self.vel)]