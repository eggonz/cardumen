from schooling.config import RunConfig
from schooling.entities import Entity, BackgroundEntity
from schooling.utils.geometry import LocRotScale
from schooling.utils.graphics import Sprite


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


class Fish(Entity):
    def __init__(self, position: LocRotScale, *, eid: str = None):
        super().__init__(
            position,
            Sprite.from_image('res/fish1.png', apply_rotation=-90, apply_scale=.08),
            eid=eid,
        )
