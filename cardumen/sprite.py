import pygame

from cardumen.geometry import rad2deg


def rotate_surface(surface: pygame.Surface, angle: float) -> pygame.Surface:
    """
    Rotate surface w.r.t. its center.

    :param surface: pygame.Surface to be rotated
    :param angle: angle of the rotation, in radians
    :return: pygame.Surface rotated
    """
    return pygame.transform.rotate(surface, rad2deg(angle))


def scale_surface(surface: pygame.Surface, scale: float) -> pygame.Surface:
    """
    Scale surface.

    :param surface: pygame.Surface to be scaled
    :param scale: magnitude of the scale
    :return: pygame.Surface scaled
    """
    # return pygame.transform.scale(surface, (surface.get_width() * scale, surface.get_height() * scale))  # aliasing
    return pygame.transform.smoothscale(surface, (surface.get_width() * scale, surface.get_height() * scale))


def rotate_scale_surface(surface: pygame.Surface, angle: float, scale: float) -> pygame.Surface:
    """
    Apply rotation and scaling of the surface. Optimized to keep good image quality.

    :param surface: pygame.Surface to be transformed
    :param angle: angle of the rotation, in radians
    :param scale: magnitude of the scale
    :return: pygame.Surface transformed
    """
    if scale < 1.0:
        rotated = rotate_surface(surface, angle)
        transformed = scale_surface(rotated, scale)
    else:
        scaled = scale_surface(surface, scale)
        transformed = rotate_surface(scaled, angle)
    return transformed


class Sprite:
    def __init__(self, path: str, rot: float = 0, scale: float = 1, alpha: int = 255):
        """
        Create a rectangular sprite from an image.

        :param path: path to image, string
        :param rot: rotation to be applied to the image when imported, angle in radians, optional
        :param scale: scaling to be applied to the image when imported, optional
        :param alpha: alpha channel of the sprite, int ranging from 0(transparent) to 255(solid), 255 by default
        """
        loaded_img_surf = pygame.image.load(path)
        loaded_img_surf.set_alpha(alpha)
        self._image = loaded_img_surf

        self._rot = rot
        self._scale = scale

    def apply_transform(self, rot: float = 0, scale: float = 1) -> None:
        """
        Apply rotation and scaling to the sprite.

        :param rot: angle of the rotation, in radians
        :param scale: magnitude of the scale
        :return:
        """
        self._rot += rot
        self._scale *= scale

    def get_transformed(self, rot: float = 0, scale: float = 1) -> pygame.Surface:
        """
        Apply rotation and scaling to the sprite.

        :param rot: angle of the rotation, in radians
        :param scale: magnitude of the scale
        :return:
        """
        return rotate_scale_surface(self._image, self._rot + rot, self._scale * scale)

    @property
    def width(self) -> int:
        return self.get_transformed().get_width()

    @property
    def height(self) -> int:
        return self.get_transformed().get_height()
