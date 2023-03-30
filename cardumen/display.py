import pygame
from pygame import Vector2

from cardumen import utils
from cardumen.geometry import PosRotScale
from cardumen.handler import Handler
from cardumen.sprite import Sprite


class Display:
    def __init__(self, screen_size: tuple):
        self.screen_size = Vector2(screen_size)
        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption(Handler().config.TITLE)

    def draw_sprite(self, sprite: Sprite, prs: PosRotScale, wrap=True):
        img = sprite.get_transformed(prs.rot, prs.scale)
        rect = img.get_rect(center=prs.pos)
        if wrap and Handler().config.WRAP:
            for neighbor in utils.get_wraps(rect):
                self.screen.blit(img, img.get_rect(center=prs.pos + neighbor))
        else:
            self.screen.blit(img, rect)

    def draw_polygon(self, points: list[Vector2], fill_color: tuple = (0, 0, 0, 0), line_color: tuple = (0, 0, 0, 0),
                     wrap=True):
        surf = pygame.Surface(self.screen_size, pygame.SRCALPHA)
        lx, ly = zip(*points)
        rect = pygame.Rect(min(lx), min(ly), max(lx) - min(lx), max(ly) - min(ly))
        if wrap and Handler().config.WRAP:
            for neighbor in utils.get_wraps(rect):
                npoints = [p + neighbor for p in points]
                pygame.draw.polygon(surf, fill_color, npoints)
                pygame.draw.lines(surf, line_color, True, npoints)
        else:
            pygame.draw.polygon(surf, fill_color, points)
            pygame.draw.lines(surf, line_color, True, points)
        self.screen.blit(surf, (0, 0))
