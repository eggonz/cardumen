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

        Handler().set_config(config)

        pygame.init()

        self.running = False
        if config.RENDER:
            log.info("Rendering enabled")
            self._render_thread = threading.Thread(target=self._run_render)
            self.display = Display(config.WINDOW_SIZE)
        else:
            log.info("Rendering disabled")

        if config.TESTING and os.path.exists(config.DB_PATH):
            os.remove(config.DB_PATH)
        self.db = Database(config.DB_PATH, config.DB_BUFFER_SIZE)
        Handler().set_db(self.db)
        self.db.connect()

        self.scene = PlaygroundScene()
        Handler().set_scene(self.scene)

    def run(self) -> None:
        """
        Run app by starting update and render threads and running main loop to handle user input.
        Update and render are performed asynchronously.

        :return:
        """
        log.info("Running app")
        self.running = True
        if Handler().config.RENDER:
            self._render_thread.start()

        try:
            pygame.fastevent.init()
            update_timer = pygame.time.get_ticks()
            last_update = pygame.time.get_ticks()
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
                if pygame.time.get_ticks() - update_timer >= 1000 / Handler().config.UPDATE_RATE:
                    update_timer += 1000 / Handler().config.UPDATE_RATE
                    # update game state
                    dt = (pygame.time.get_ticks() - last_update) / 1000
                    self.scene.update(dt)
                    last_update = pygame.time.get_ticks()

                    # control check
                    control_ups.append(dt)
                    control_nu += 1
                if control_nu >= 100:
                    log.debug(f"Average updates per second: {round(len(control_ups) / sum(control_ups), 2)} "
                              f"(target: {Handler().config.UPDATE_RATE})")
                    control_ups = []
                    control_nu = 0

                time.sleep(last_update / 1000 + 1 / Handler().config.UPDATE_RATE - pygame.time.get_ticks() / 1000)
        except KeyboardInterrupt:
            log.info("App interrupted")
        finally:
            self.running = False
            if Handler().config.RENDER:
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
            clock.tick(Handler().config.FPS)


if __name__ == '__main__':
    app = App()
    app.run()
