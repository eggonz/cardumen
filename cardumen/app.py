"""
Module containing the main application
"""
import threading
import time

import pygame

from cardumen.display import Display
from cardumen.handler import Handler
from cardumen.scene import PlaygroundScene

FPS = 32  # frames per sec, 64
SPF = 1.0 / FPS  # sec per frame
UPDATE_RATE = 0.01  # sec
WINDOW_SIZE = (1000, 600)


class App:
    """Class for the main application to be run"""

    def __init__(self):
        """
        Start app by initializing display and scene.
        Defines update and rendering threads.
        """
        self._handler = Handler()

        self._update_thread = threading.Thread(target=self._run_update)
        self._render_thread = threading.Thread(target=self._run_render)
        self.running = False

        pygame.init()
        self.display = Display(self._handler, WINDOW_SIZE)
        self._handler.display = self.display
        self.scene = PlaygroundScene(self._handler, WINDOW_SIZE)
        self._handler.scene = self.scene

    def run(self) -> None:
        """
        Run app by starting update and render threads and running main loop to handle user input.
        Update and render are performed asynchronously.

        :return:
        """
        self.running = True
        self._update_thread.start()
        self._render_thread.start()

        try:
            pygame.fastevent.init()
            # loop until the user clicks the close button
            while self.running:
                # Read events
                queue = pygame.fastevent.get()
                for event in queue:
                    if event.type == pygame.QUIT:
                        self.running = False
                # Stability sleep
                time.sleep(.01)
        except:
            self.running = False
        finally:
            self._update_thread.join()
            self._render_thread.join()
            pygame.quit()

    def _run_update(self) -> None:
        """
        Run main update loop.
        The scene is updated at regular intervals of time.

        :return:
        """
        t0 = time.time()
        while self.running:
            # Update scene
            self.scene.update(dt=UPDATE_RATE)

            # Loop time management
            time.sleep(max(0.0, UPDATE_RATE - time.time() + t0))
            t0 = time.time()

    def _run_render(self) -> None:
        """
        Run main render loop.
        The loop period has a lower-bound defined by the FPS rate.
        On each iteration, the display is cleared, the scene rendered again and then showed.

        :return:
        """
        t0 = time.time()
        while self.running:
            # Render scene
            self.display.screen.fill((0, 0, 0))
            self.scene.render(self.display)
            pygame.display.flip()

            # Loop time management
            time.sleep(max(0.0, SPF - time.time() + t0))
            t0 = time.time()


if __name__ == '__main__':
    app = App()
    app.run()
