"""
In this module we define the class that controls the movement of the fish in the scene.
Fish have two possible actions tilt right and tilt left.
"""
import random
from enum import Enum


class Action(Enum):
    def execute(self, *args, **kwargs):
        pass


class Agent:
    def __init__(self, actions: list[Action]):
        self.actions = actions

    def act(self, state: list) -> Action:
        """
        Get action from agent.
        :param state: current state
        :return: action
        """
        return random.choice(self.actions)
