from cardumen.display import Display
from cardumen.geometry import PosRotScale
from cardumen.sprite import Sprite


class Entity:
    def __init__(self, prs: PosRotScale, sprite: Sprite):
        """
        Create an Entity.

        :param prs: position, rotation, scale
        :param sprite: sprite to draw
        """
        self.prs = prs
        self.sprite = sprite

    def update(self, dt: float) -> None:
        """
        Update scene.
        :param dt: time since last update
        :return:
        """
        pass

    def render(self, display: Display) -> None:
        """
        Render scene.
        :param display: display to render to
        :return:
        """
        display.draw_sprite(self.sprite, self.prs)
