import threading
import time

from schooling.config import RuntimeContext, RunConfig
from schooling.scene import Scene
from schooling.utils.events import EventQueue
from schooling.utils.graphics import Display


class App:
    _FPS = RunConfig.FPS  # frames per sec
    _SPF = 1.0 / _FPS  # sec per frame

    _UPDATE_RATE = 0.01  # sec

    def __init__(self):
        self._update_thread = threading.Thread(target=self._run_update)
        self._render_thread = threading.Thread(target=self._run_render)
        self.running = False

        self.display = Display(RunConfig.WINDOW_SIZE)
        self.scene = Scene()

    def run(self) -> None:
        RuntimeContext.start_time = time.time()
        self.running = True
        self._update_thread.start()
        self._render_thread.start()

        try:
            EventQueue.init()
            while self.running:
                # Read events
                EventQueue.read()

                # Check quit
                if EventQueue.has_quit():
                    self.running = False

                # Stability sleep
                time.sleep(.01)
        except Exception:
            self.running = False
        finally:
            self._update_thread.join()
            self._render_thread.join()
            self.display.quit()

    def _run_update(self) -> None:
        t0 = time.time()
        while self.running:
            # Update scene
            self.scene.update(dt=App._UPDATE_RATE)

            # Loop time management
            time.sleep(max(0.0, App._UPDATE_RATE - time.time() + t0))
            t0 = time.time()

    def _run_render(self) -> None:
        t0 = time.time()
        while self.running:
            # Render scene
            self.display.clear()
            self.scene.render(self.display)
            self.display.show()

            # Loop time management
            time.sleep(max(0.0, App._SPF - time.time() + t0))
            t0 = time.time()


if __name__ == '__main__':
    app = App()
    app.run()
