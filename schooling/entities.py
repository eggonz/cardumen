from __future__ import annotations

import uuid
from abc import ABC
from typing import Callable

from schooling.config import RunConfig
from schooling.utils.geometry import LocRotScale, Box
from schooling.utils.graphics import Display, Sprite, Colors, Color

_ENTITIES_BY_EID = {}


class EntityManager:
    def __init__(self):
        self._layers = {}

    def add_entity(self, entity: Entity, layer: int) -> None:
        if not self._layers.get(layer):
            self._layers[layer] = []
        self._layers[layer].append(entity)

    def update(self, dt: float) -> None:
        for layer in sorted(self._layers.keys()):
            for entity in self._layers[layer]:
                entity.update(dt)

    def render(self, display: Display) -> None:
        for layer in sorted(self._layers.keys()):
            for entity in self._layers[layer]:
                entity.render(display)

    def apply_to_all(self, func: Callable) -> None:
        for layer in self._layers.values():
            for entity in layer:
                func(entity)


class Entity(ABC):
    def __init__(self, position: LocRotScale, sprite: Sprite, bound_box: Box = None, *, eid: str = None):
        self._eid = str(uuid.uuid4()) if eid is None else eid
        _ENTITIES_BY_EID[self._eid] = self
        self.position = position
        self.sprite = sprite
        self.bound_box = Box(*sprite.get_size()) if bound_box is None else bound_box

        self._debug_color = Colors.RED
        self._enabled = True
        self._visible = True
        self._collider_enabled = True

    def __del__(self):
        _ENTITIES_BY_EID.pop(self._eid)

    def update(self, dt: float) -> None:
        if RunConfig.WRAP:
            fish = Entity.get_by_eid('fish')
            width, height = RunConfig.WINDOW_SIZE
            if fish.position.x > width:
                fish.position.x = fish.position.x - width
            elif fish.position.x < 0:
                fish.position.x = fish.position.x + width
            if fish.position.y > height:
                fish.position.y = fish.position.y - height
            elif fish.position.y < 0:
                fish.position.y = fish.position.y + height

    def render(self, display: Display) -> None:
        if RunConfig.DEBUG_MODE:
            if self.is_collider_enabled():
                display.draw_rect(self.bound_box, self._debug_color, self.position)
        if self.is_visible():
            display.draw_img(self.sprite, self.position)

    @classmethod
    def get_by_eid(cls, eid: str) -> Entity:
        return _ENTITIES_BY_EID[eid]

    def is_enabled(self) -> bool:
        return self._enabled

    def is_visible(self) -> bool:
        return self._enabled and self._visible

    def is_collider_enabled(self) -> bool:
        return self._enabled and self._collider_enabled

    def set_enabled(self, value: bool) -> None:
        self._enabled = value

    def set_visible(self, value: bool) -> None:
        self._visible = value

    def set_collider_enabled(self, value: bool) -> None:
        self._collider_enabled = value

    def set_debug_color(self, value: Color) -> None:
        self._debug_color = value
