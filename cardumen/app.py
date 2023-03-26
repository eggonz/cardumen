"""
Module containing the main application
"""
import threading
import time

import pygame

from cardumen.database import Database, BinaryConverter
from cardumen.display import Display
from cardumen.handler import Handler
from cardumen.scene import PlaygroundScene

FPS = 32  # frames per sec, 64
SPF = 1.0 / FPS  # sec per frame
UPDATE_RATE = 1 / 100  # sec
WINDOW_SIZE = (1000, 600)


class App:
    """Class for the main application to be run"""

    def __init__(self):
        """
        Start app by initializing display and scene.
        Defines update and rendering threads.
        """
        self._handler = Handler()

        self._render_thread = threading.Thread(target=self._run_render)
        self.running = False

        pygame.init()

        self.display = Display(self._handler, WINDOW_SIZE)
        self._handler.display = self.display

        self.db = Database(self._handler.config.DATABASE_PATH, BinaryConverter('list'))
        self._handler.db = self.db
        self.db.connect()
        self.db.create_table()

        self.scene = PlaygroundScene(self._handler, WINDOW_SIZE)
        self._handler.scene = self.scene

    def run(self) -> None:
        """
        Run app by starting update and render threads and running main loop to handle user input.
        Update and render are performed asynchronously.

        :return:
        """
        self.running = True
        self._render_thread.start()

        try:
            pygame.fastevent.init()
            update_timer = pygame.time.get_ticks()
            while self.running:
                # Read events
                queue = pygame.fastevent.get()
                for event in queue:
                    if event.type == pygame.QUIT:
                        self.running = False
                if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    self.running = False
                if not self.running:
                    break

                # update the scene every UPDATE_RATE seconds
                current_time = pygame.time.get_ticks()
                if current_time - update_timer >= UPDATE_RATE * 1000:
                    # update game state
                    self.scene.update((current_time - update_timer) / 1000)
                    # reset update timer
                    update_timer = current_time

                # Stability sleep
                time.sleep(.01)
        finally:
            self.running = False
            self._render_thread.join()
            self.db.close()
            pygame.quit()

    def _run_render(self) -> None:
        """
        Run main render loop.
        The loop period has a lower-bound defined by the FPS rate.
        On each iteration, the display is cleared, the scene rendered again and then showed.

        :return:
        """
        clock = pygame.time.Clock()
        while self.running:
            # Render scene
            self.display.screen.fill((0, 0, 0))
            self.scene.render(self.display)
            pygame.display.flip()
            clock.tick(FPS)


if __name__ == '__main__':
    app = App()
    app.run()
