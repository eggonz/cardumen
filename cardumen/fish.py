from __future__ import annotations

import time

import numpy as np
import pygame
from pygame import Vector2

from cardumen import utils
from cardumen.collision import Collider
from cardumen.control import Action, Agent
from cardumen.database import Table
from cardumen.entities import Entity
from cardumen.geometry import PosRotScale, deg2rad, scale_points, rotate_points, move_points
from cardumen.handler import Handler
from cardumen.projection import Projection
from cardumen.shapes import Polygon, ConvexQuad
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
    def __init__(self, prs: PosRotScale, cat: int = 1):
        if not 1 <= cat <= 7:
            raise ValueError("cat must be in [1, 7]")
        super().__init__(prs, Sprite(f"assets/fish{cat}.png", rot=deg2rad(-90), scale=.05))
        self.cat = cat

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
        points = [Vector2(2, 0), Vector2(6, 12), Vector2(-6, 12), Vector2(-2, 0)]
        points = scale_points(points, h / 2)
        points = rotate_points(points, deg2rad(90))
        points = move_points(points, Vector2(0.75 * w / 2, 0))
        view = ConvexQuad(self.prs, points, fill_color=(255, 255, 255, 50), line_color=(0, 0, 0, 255))
        self.view = Collider(self, view, 'fish view', detect='fish body')
        self.view_projection = Projection.from_convex_quad(view)

        # body rect collider
        points = [Vector2(0, 0), Vector2(w, 0), Vector2(w, h), Vector2(0, h)]
        points = move_points(points, Vector2(-w / 2, -h / 2))
        body = Polygon(self.prs, points, fill_color=(0, 255, 0, 50), line_color=(0, 255, 0, 255))
        self.body = Collider(self, body, 'fish body')

        # proximity sense hexagon collider
        l = 100  # side length
        a = l / 2 * (3 ** .5)  # apothem
        points = [Vector2(0, -l), Vector2(a, -l / 2), Vector2(a, l / 2), Vector2(0, l), Vector2(-a, l / 2),
                  Vector2(-a, -l / 2)]
        sensor = Polygon(self.prs, points, fill_color=(0, 0, 255, 50), line_color=(0, 0, 255, 255))
        self.sensor = Collider(self, sensor, 'fish sensor', detect='fish body')

        self.add_colliders(self.view, self.body, self.sensor)

        # collision callbacks
        self.view.on_collision_start = lambda _: self.view.poly.set_color(fill=(255, 0, 0, 50))
        self.view.on_collision_end = lambda _: self.view.poly.reset_color() if not self.view.is_colliding() else None
        self.sensor.on_collision_start = lambda _: self.sensor.poly.set_color(fill=(255, 0, 0, 50))
        self.sensor.on_collision_end = lambda \
                _: self.sensor.poly.reset_color() if not self.sensor.is_colliding() else None

        def add_to_detection_canvas(other: Collider):
            for rep in utils.get_wraps():
                poly2 = other.poly.clone_at(other.poly.prs.pos + rep)
                poly2.prs = poly2.prs.relative_to(self.view.poly.prs)
                body_surf, body_rect = poly2.get_surface(return_rect=True)
                view_rect = utils.get_rect(self.view.poly.local_points)
                topleft = Vector2(body_rect.topleft) - Vector2(view_rect.topleft)
                self.view_detect.blit(body_surf, topleft)

        self.view.on_collision = add_to_detection_canvas

        self.view_detect = None
        self.view_state = np.empty((*self.view_projection.output_size, 3))

        # database
        self.db_table = Table(Handler().db, f'fish{cat}', Handler().config.DATA_CONFIG)
        self.db_table.create()

    def update(self, dt: float) -> None:
        # choose action
        action = self._agent.act(self.get_state())
        action.execute(self, dt)

        # update position
        self.speed = max(self.min_speed, min(self.max_speed, self.speed))
        self.vel.from_polar((self.speed, -self.prs.rot_deg))
        self.prs.pos += self.vel * dt

        # update colliders
        view_rect = utils.get_rect(self.view.poly.local_points)
        self.view_detect = pygame.Surface(view_rect.size, pygame.SRCALPHA)
        for collider in self.colliders:
            collider.update(dt)
        if self.view.is_colliding() and self.cat == 1:
            self.view_state = self.view_projection(utils.surf2arr(self.view_detect))
            if Handler().config.plot_collider:
                utils.plot_arr(self.view_state)

        # update database
        self.db_table.add(time.time(), self.get_state())

    def get_state(self) -> list[np.ndarray]:
        return [np.array([*self.prs.pos, *self.vel]), self.view_state]

    def __repr__(self):
        return f'Fish(cat={self.cat})'
