import cv2
import numpy as np
from pygame import Vector2


class Projection:
    def __init__(self, src_points: list[Vector2], output_size: tuple[int, int]):
        self.output_size = int(output_size[0]), int(output_size[1])

        # Compute the projective transformation matrix
        self._M = Projection._homography(src_points, self.output_size)

    def __call__(self, arr: np.ndarray) -> np.ndarray:
        # Apply the projective transformation
        return cv2.warpPerspective(arr, self._M, self.output_size)

    @staticmethod
    def _homography(src_points: list[Vector2], output_size: tuple[int, int]) -> np.ndarray:
        width, height = output_size
        dst_points = np.array([[0, 0], [width, 0], [width, height], [0, height]])
        H, _ = cv2.findHomography(np.array(src_points), dst_points)
        return H
