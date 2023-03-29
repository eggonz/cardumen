"""
Module containing the main application
"""
import os
import threading
import time

import pygame

from cardumen.config import Config
from cardumen.database import Database
from cardumen.display import Display
from cardumen.handler import Handler
from cardumen.logger import log, set_log_level, set_log_file
from cardumen.scene import PlaygroundScene


class App:
    """Class for the main application to be run"""

    def __init__(self, config_path: str = 'config_dev.json'):
        """
        Start app by initializing display and scene.
        Defines update and rendering threads.
        """
        config = Config(config_path)

        set_log_level(config.LOG_LEVEL)
        set_log_file(config.LOG_FILE)
        log.info("Starting app")

        self._handler = Handler(config)

        pygame.init()

        self.running = False
        if config.RENDER:
            log.info("Rendering enabled")
            self._render_thread = threading.Thread(target=self._run_render)
            self.display = Display(self._handler, config.WINDOW_SIZE)
        else:
            log.info("Rendering disabled")

        if config.TESTING and os.path.exists(config.DB_PATH):
            os.remove(config.DB_PATH)
        self.db = Database(config.DB_PATH, config.DB_BUFFER_SIZE)
        self._handler.db = self.db
        self.db.connect()

        self.scene = PlaygroundScene(self._handler)
        self._handler.scene = self.scene

    def run(self) -> None:
        """
        Run app by starting update and render threads and running main loop to handle user input.
        Update and render are performed asynchronously.

        :return:
        """
        log.info("Running app")
        self.running = True
        if self._handler.config.RENDER:
            self._render_thread.start()

        try:
            pygame.fastevent.init()
            update_timer = pygame.time.get_ticks()
            control_ups = []
            control_nu = 0
            while self.running:
                # Read events
                queue = pygame.fastevent.get()
                for event in queue:
                    if event.type == pygame.QUIT:
                        log.info("App quit")
                        self.running = False
                if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    log.info("App quit")
                    self.running = False
                if not self.running:
                    break

                # update the scene every UPDATE_RATE seconds
                current_time = pygame.time.get_ticks()
                dt = (current_time - update_timer) / 1000
                if dt >= 1 / self._handler.config.UPDATE_RATE:
                    # update game state
                    self.scene.update(dt)
                    # reset update timer
                    update_timer = current_time

                    # control check
                    control_ups.append(dt)
                    control_nu += 1
                if control_nu >= 100:
                    log.debug(f"Average updates per second: {round(len(control_ups) / sum(control_ups), 2)} "
                              f"(target: {self._handler.config.UPDATE_RATE})")
                    control_ups = []
                    control_nu = 0

                # Stability sleep
                time.sleep(.01)
        except KeyboardInterrupt:
            log.info("App interrupted")
        finally:
            self.running = False
            if self._handler.config.RENDER:
                self._render_thread.join()
            self.db.close()
            pygame.quit()
            log.info("App closed")

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
            clock.tick(self._handler.config.FPS)


if __name__ == '__main__':
    app = App()
    app.run()
