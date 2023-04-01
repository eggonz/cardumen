import json
from argparse import Namespace

import numpy as np
from pygame import Vector2

from cardumen.logger import LogLevel


class DataConfig:
    def __init__(self, path: str):
        with open(path, 'r') as f:
            config = json.load(f)

        self.num_features = len(config['features'])
        self.features = []
        for feat in config['features']:
            feat['name'] = feat['name']
            feat['shape'] = tuple(feat['shape'])
            feat['dtype'] = np.dtype(feat['dtype'])
            self.features.append(Namespace(**feat))


class Config:
    def __init__(self, path: str):
        with open(path, 'r') as f:
            config = json.load(f)

        self.WINDOW_SIZE = Vector2(config['width'], config['height'])
        self.TITLE = config['title']
        self.FPS = config['fps']
        self.UPDATE_RATE = config['updateRate']
        self.WINDOW_RESIZABLE = config['windowResizable']  # unused
        self.WINDOW_FULLSCREEN = config['windowFullscreen']  # unused
        self.WINDOW_BORDERLESS = config['windowBorderless']  # unused
        self.WRAP = config['wrap']
        self.DB_PATH = config['dbPath']
        self.DB_BUFFER_SIZE = config['dbBufferSize']
        self.DATA_CONFIG = DataConfig(config['dataConfig'])
        self.LOG_LEVEL = LogLevel[config['logLevel'].upper()]
        self.LOG_FILE = config['logFile']
        self.DEBUG = config['debug']
        self.TESTING = config['testing']
        self.RENDER = config['render']
        self.n_fish = config.get('paramNFish', 2)
        self.plot_collider = config.get('paramPlotCollider', False)
