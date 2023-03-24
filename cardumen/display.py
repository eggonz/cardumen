import pygame
from pygame import Vector2

from cardumen.geometry import PosRotScale
from cardumen.sprite import Sprite


class Display:
    def __init__(self, screen_size: tuple):
        self.screen_size = screen_size
        self.screen = pygame.display.set_mode(screen_size)

    def _get_wrap_repeats(self, min_x, min_y, max_x, max_y):
        width, height = Vector2(*self.screen_size)
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

    def draw_sprite(self, sprite: Sprite, prs: PosRotScale):
        img = sprite.get_transformed(prs.rot, prs.scale)
        center = Vector2(sprite.width, sprite.height) / 2  # sprite centered in location

        # wrap
        img_size = Vector2(sprite.width, sprite.height)
        min_x, min_y = prs.pos - img_size/2
        max_x, max_y = prs.pos + img_size/2
        for neighbor in self._get_wrap_repeats(min_x, min_y, max_x, max_y):
            self.screen.blit(img, prs.pos - center + neighbor)

        self.screen.blit(img, prs.pos - center)

    def draw_polygon(self, points: Vector2, color: tuple):
        # wrap
        lx, ly = zip(*points)
        for neighbor in self._get_wrap_repeats(min(lx), min(ly), max(lx), max(ly)):
            pygame.draw.polygon(self.screen, color, [p + neighbor for p in points])

        pygame.draw.polygon(self.screen, color, points)
