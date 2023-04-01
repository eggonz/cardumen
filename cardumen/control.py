"""
In this module we define the class that controls the movement of the fish in the scene.
Fish have two possible actions tilt right and tilt left.
"""
import random

import numpy as np


class Agent:
    def __init__(self, num_labels: int):
        self.num_labels = num_labels

    def act(self, state: list[np.ndarray]) -> int:
        """
        Get action from agent.

        :param state: current state
        :return: action label
        """
        return random.randint(0, self.num_labels - 1)
