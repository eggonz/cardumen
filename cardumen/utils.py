import numpy as np
import pygame
from matplotlib import pyplot as plt
from pygame import Vector2

from cardumen.handler import Handler


def get_rect(points: list[Vector2]) -> pygame.Rect:
    lx, ly = zip(*points)
    return pygame.Rect(min(lx), min(ly), max(lx) - min(lx), max(ly) - min(ly))


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


def check_convex_polygon(points: list[Vector2]) -> bool:
    # cv2.isContourConvex, scipy.spatial.ConvexHull, etc. are too slow/heavy
    if len(points) < 3:
        return False
    for i in range(len(points)):
        a, b, c = points[i - 1], points[i], points[(i + 1) % len(points)]
        if (b - a).cross(c - b) < 0:
            return False
    return True


def surf2arr(surf: pygame.Surface) -> np.ndarray:
    return np.transpose(pygame.surfarray.array3d(surf), (1, 0, 2))


def plot_arr(arr: np.ndarray):
    plt.imshow(arr)
    plt.axis('off')
    plt.show()
