import pygame
from pygame import Vector2

from cardumen.geometry import PosRotScale
from cardumen.handler import Handler
from cardumen.sprite import Sprite


class Display:
    def __init__(self, handler: Handler, screen_size: tuple):
        self._handler = handler
        self.screen_size = Vector2(screen_size)
        self.screen = pygame.display.set_mode(screen_size)

    def _get_wrap_repeats(self, min_x, min_y, max_x, max_y):
        width, height = self.screen_size
        under_x = min_x < 0
        over_x = max_x > width
        under_y = min_y < 0
        over_y = max_y > height

        repeats = []
        if under_x and under_y:
            repeats.append(Vector2(width, height))
        if under_x:
            repeats.append(Vector2(width, 0))
        if under_x and over_y:
            repeats.append(Vector2(width, -height))
        if under_y:
            repeats.append(Vector2(0, height))
        if over_y:
            repeats.append(Vector2(0, -height))
        if over_x and under_y:
            repeats.append(Vector2(-width, height))
        if over_x:
            repeats.append(Vector2(-width, 0))
        if over_x and over_y:
            repeats.append(Vector2(-width, -height))
        return repeats

    def draw_sprite(self, sprite: Sprite, prs: PosRotScale, wrap=True):
        img = sprite.get_transformed(prs.rot, prs.scale)
        if wrap and self._handler.config.WINDOW_WRAP:
            img_size = Vector2(img.get_size())
            min_x, min_y = prs.pos - img_size / 2
            max_x, max_y = prs.pos + img_size / 2
            for neighbor in self._get_wrap_repeats(min_x, min_y, max_x, max_y):
                self.screen.blit(img, img.get_rect(center=prs.pos + neighbor))
        self.screen.blit(img, img.get_rect(center=prs.pos))

    def draw_polygon(self, points: list[Vector2], fill_color: tuple = (0, 0, 0, 0), line_color: tuple = (0, 0, 0, 0),
                     wrap=True):
        surf = pygame.Surface(self.screen_size + Vector2(2, 2), pygame.SRCALPHA)
        if wrap and self._handler.config.WINDOW_WRAP:
            lx, ly = zip(*points)
            for neighbor in self._get_wrap_repeats(min(lx), min(ly), max(lx), max(ly)):
                npoints = [p + neighbor for p in points]
                pygame.draw.polygon(surf, fill_color, npoints)
                pygame.draw.lines(surf, line_color, True, npoints)
        pygame.draw.polygon(surf, fill_color, points)
        pygame.draw.lines(surf, line_color, True, points)
        self.screen.blit(surf, (0, 0))
