import numpy as np
from pygame import Vector2

from cardumen.projection import Projection


def test_projection():
    src_points = [Vector2(0, 0), Vector2(6, 0), Vector2(6, 6), Vector2(0, 6)]
    output_size = (6, 6)
    projection = Projection(src_points, output_size)
    arr = np.random.rand(6, 6, 3)
    proj_arr = projection(arr)
    assert np.array_equal(proj_arr, arr)

    src_points = [Vector2(0, 0), Vector2(3, 0), Vector2(3, 3), Vector2(0, 3)]
    output_size = (3, 3)
    projection = Projection(src_points, output_size)
    proj_arr = projection(arr)
    assert np.array_equal(proj_arr, arr[:3, :3, :])

