from enum import Enum

import pygame


class Events:
    _queue = []
    _quit = False

    _keys_just_down = {}
    _keys_just_up = {}
    _keys_pressed = {}

    class Key(Enum):
        ARROW_RIGHT = pygame.K_RIGHT
        ARROW_LEFT = pygame.K_LEFT

    _all_keys = [key.value for key in Key]

    @staticmethod
    def init():
        pygame.fastevent.init()

    @staticmethod
    def read() -> None:
        Events._queue = pygame.fastevent.get()
        for event in Events._queue:
            if event.type == pygame.QUIT:
                Events._quit = True

            Events._keys_just_down = {}
            Events._keys_just_up = {}

            if event.type == pygame.KEYDOWN and event.key in Events._all_keys:
                if not Events._keys_pressed.get(event.key, False):
                    Events._keys_just_down[event.key] = True
                Events._keys_pressed[event.key] = True

            elif event.type == pygame.KEYUP and event.key in Events._all_keys:
                if Events._keys_pressed.get(event.key, False):
                    Events._keys_just_up[event.key] = True
                Events._keys_pressed[event.key] = False

    @staticmethod
    def is_quit() -> bool:
        return Events._quit

    @staticmethod
    def is_key_pressed(key: Key) -> bool:
        return Events._keys_pressed.get(key.value, False)
