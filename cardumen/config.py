import json

from cardumen.logger import LogLevel


class Config:
    def __init__(self, path: str):
        with open(path, 'r') as f:
            config = json.load(f)

        self.WIDTH = config['width']
        self.HEIGHT = config['height']
        self.TITLE = config['title']
        self.FPS = config['fps']
        self.UPDATE_RATE = config['updateRate']
        self.WINDOW_RESIZABLE = config['windowResizable']  # unused
        self.WINDOW_FULLSCREEN = config['windowFullscreen']  # unused
        self.WINDOW_BORDERLESS = config['windowBorderless']  # unused
        self.WINDOW_WRAP = config['windowWrap']
        self.DB_PATH = config['dbPath']
        self.DB_BUFFER_SIZE = config['dbBufferSize']
        self.LOG_LEVEL = LogLevel[config['logLevel'].upper()]
        self.LOG_FILE = config['logFile']
        self.DEBUG = config['debug']
        self.TESTING = config['testing']
