from __future__ import annotations

from schooling.config import RunConfig
from schooling.entities import Entity
from schooling.utils.geometry import LocRotScale
from schooling.utils.graphics import Sprite


class BackgroundEntity(Entity):
    def __init__(self, position: LocRotScale, sprite: Sprite, *, eid: str = None):
        super().__init__(
            position,
            sprite,
            eid,
        )
        self._collider_enabled = False

    def set_collider_enabled(self, value: bool) -> None:
        raise AttributeError


class Water(BackgroundEntity):
    def __init__(self, position: LocRotScale, *, eid: str = None):
        sprite = Sprite.from_image('res/water.jpg')
        # min: adjust content to screen
        # max: adjust content to fill screen
        scale = max(RunConfig.WINDOW_SIZE[0]/sprite.get_width(),
                    RunConfig.WINDOW_SIZE[1]/sprite.get_height())
        sprite.apply_transform(apply_scale=scale)
        super().__init__(
            position,
            sprite,
            eid=eid,
        )
