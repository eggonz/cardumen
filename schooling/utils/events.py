from enum import Enum

import pygame


class InputKey(Enum):
    A = pygame.K_a


class EventQueue:
    _queue = []

    @staticmethod
    def init():
        pygame.fastevent.init()

    @staticmethod
    def read() -> None:
        EventQueue._queue = pygame.fastevent.get()

    @staticmethod
    def has_quit() -> bool:
        for event in EventQueue._queue:
            if event.type == pygame.QUIT:
                return True
        return False

    @staticmethod
    def has_key_pressed(key: InputKey) -> bool:
        for event in EventQueue._queue:
            if event.type == pygame.KEYDOWN and event.key == key.value:
                return True
        return False
