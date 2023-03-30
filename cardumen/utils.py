import numpy as np
import pygame
from matplotlib import pyplot as plt
from pygame import Vector2

from cardumen.handler import Handler


def get_wraps(rect: pygame.Rect = None) -> list[Vector2]:
    width, height = Handler().config.WINDOW_SIZE

    if rect is None:
        return [
            Vector2(width, height),
            Vector2(width, 0),
            Vector2(width, -height),
            Vector2(0, height),
            Vector2(0, -height),
            Vector2(-width, height),
            Vector2(-width, 0),
            Vector2(-width, -height),
            Vector2(0, 0)
        ]

    under_x = rect.left < 0
    over_x = rect.right > width
    under_y = rect.top < 0
    over_y = rect.bottom > height

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
    repeats.append(Vector2(0, 0))  # the original rect is the last one, to appear on top
    return repeats


def plot_surf(surf: pygame.Surface):
    arr = pygame.surfarray.array3d(surf)
    arr = np.transpose(arr, (1, 0, 2))
    plt.imshow(arr)
    plt.axis('off')
    plt.show()
