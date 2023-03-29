import numpy as np
import pygame
from matplotlib import pyplot as plt
from pygame import Vector2

from cardumen.handler import Handler


def get_wraps(rect: pygame.Rect, wrap: bool = True) -> list[Vector2]:
    if not wrap:
        return [Vector2(0, 0)]

    width, height = Handler().config.WINDOW_SIZE
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
    repeats.append(Vector2(0, 0))
    return repeats


def plot_surf(surf: pygame.Surface):
    arr = pygame.surfarray.array3d(surf)
    arr = np.transpose(arr, (1, 0, 2))
    plt.imshow(arr)
    plt.axis('off')
    plt.show()
