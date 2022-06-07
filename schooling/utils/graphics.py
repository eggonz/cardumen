from __future__ import annotations

import pygame

from schooling.config import RunConfig
from schooling.utils.geometry import LocRotScale, Box, rad2deg


def _rotate_surface(surface: pygame.Surface, angle: float) -> pygame.Surface:
    return pygame.transform.rotate(surface, rad2deg(angle))


def _scale_surface(surface: pygame.Surface, scale: float) -> pygame.Surface:
    return pygame.transform.smoothscale(surface, (surface.get_width() * scale, surface.get_height() * scale))


def _rotate_scale_surface(surface: pygame.Surface, angle: float, scale: float) -> pygame.Surface:
    if scale < 1.0:
        rotated = _rotate_surface(surface, angle)
        transformed = _scale_surface(rotated, scale)
    else:
        scaled = _scale_surface(surface, scale)
        transformed = _rotate_surface(scaled, angle)
    return transformed


class Color:
    def __init__(self, red: int, green: int, blue: int):
        self._rgb = (red, green, blue)

    def get_rgb(self) -> tuple:
        return self._rgb


class Colors:
    BLACK = Color(0, 0, 0)
    WHITE = Color(255, 255, 255)
    RED = Color(255, 0, 0)
    GREEN = Color(0, 255, 0)
    BLUE = Color(0, 0, 255)


class Display:
    def __init__(self, screen_size: tuple = (1000, 600)) -> None:
        pygame.init()
        self._screen = pygame.display.set_mode(screen_size)

    def get_screen_size(self) -> tuple:
        return self._screen.get_size()

    def quit(self) -> None:
        pygame.quit()

    def clear(self, fill_color: Color = Colors.BLACK) -> None:
        self._screen.fill(fill_color.get_rgb())

    def show(self) -> None:
        pygame.display.flip()
        
    def _draw_surface(self, surface: pygame.Surface, center: tuple) -> None:
        self._screen.blit(surface, surface.get_rect(center=center))

        if RunConfig.WRAP:
            x, y = center
            width, height = RunConfig.WINDOW_SIZE
            surf_width, surf_height = surface.get_size()
            if surf_width < width and surf_height < height:
                self._screen.blit(surface, surface.get_rect(center=(x - width, y - height)))
                self._screen.blit(surface, surface.get_rect(center=(x - width, y + height)))
                self._screen.blit(surface, surface.get_rect(center=(x + width, y - height)))
                self._screen.blit(surface, surface.get_rect(center=(x + width, y + height)))
            if surf_width < width:
                self._screen.blit(surface, surface.get_rect(center=(x - width, y)))
                self._screen.blit(surface, surface.get_rect(center=(x + width, y)))
            if surf_height < height:
                self._screen.blit(surface, surface.get_rect(center=(x, y - height)))
                self._screen.blit(surface, surface.get_rect(center=(x, y + height)))

    def draw_img(self, sprite: Sprite, loc_rot_scale: LocRotScale) -> None:
        new_img = _rotate_scale_surface(sprite.image, loc_rot_scale.angle, loc_rot_scale.scale)
        self._draw_surface(new_img, (loc_rot_scale.x, loc_rot_scale.y))

    def draw_rect(self, box: Box, color: Color, loc_rot_scale: LocRotScale) -> None:
        surface = pygame.Surface((loc_rot_scale.scale * box.width,
                                  loc_rot_scale.scale * box.height),
                                 pygame.SRCALPHA)
        rect = pygame.Rect(
            loc_rot_scale.scale * box.offset_x,
            loc_rot_scale.scale * box.offset_y,
            loc_rot_scale.scale * box.width,
            loc_rot_scale.scale * box.height,
        )
        pygame.draw.rect(surface, color.get_rgb(), rect, width=1)
        rotated_surface = _rotate_surface(surface, loc_rot_scale.angle)
        center = (loc_rot_scale.x, loc_rot_scale.y)
        self._draw_surface(rotated_surface, center)


class Sprite:
    def __init__(self, surface: pygame.Surface):
        self._image = surface

    @classmethod
    def from_image(cls, path: str, apply_rotation: float = 0, apply_scale: float = 1.0) -> Sprite:
        loaded_img = pygame.image.load(path)
        surface = _rotate_scale_surface(loaded_img, apply_rotation, apply_scale)
        return cls(surface)

    @classmethod
    def from_color(cls, color: Color, size: tuple) -> Sprite:
        surface = pygame.Surface(size)
        surface.fill(color.get_rgb())
        return cls(surface)

    def apply_transform(self, apply_rotation: float = 0, apply_scale: float = 1.0) -> None:
        self._image = _rotate_scale_surface(self._image, apply_rotation, apply_scale)

    @property
    def image(self) -> pygame.Surface:
        return self._image

    def get_size(self) -> tuple:
        return self._image.get_size()

    def get_width(self) -> int:
        return self._image.get_width()

    def get_height(self) -> int:
        return self._image.get_height()
