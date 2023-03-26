import json
from argparse import Namespace


class Config:
    def __init__(self, path: str):
        with open(path, 'r') as f:
            config = json.load(f)

        self.WIDTH = config['width']
        self.HEIGHT = config['height']
        self.TITLE = config['title']
        self.FPS = config['fps']
        self.UPDATE_RATE = config['updateRate']
        self.WINDOW_RESIZABLE = config['windowResizable']
        self.WINDOW_FULLSCREEN = config['windowFullscreen']
        self.WINDOW_BORDERLESS = config['windowBorderless']
        self.WINDOW_WRAP = config['windowWrap']
        self.DB_PATH = config['dbPath']
        self.DB_CONFIG_PATH = config['dbConfigPath']
        self.DEBUG = config['debug']
        self.TESTING = config['testing']


class DbConfig:
    def __init__(self, path: str):
        with open(path, 'r') as f:
            config = json.load(f)
        self._data_formats = config['dataFormats']

        self.BUFFER_SIZE = config['params']['bufferSize']

    def _get_dtype(self, dtype: str):
        if dtype == 'int':
            return int
        elif dtype == 'float':
            return float
        elif dtype == 'str':
            return str
        else:
            raise ValueError(f"Unknown dtype '{dtype}'")

    def __getitem__(self, data_format: str):
        if data_format not in self._data_formats:
            raise KeyError(f"Data format '{data_format}' not found in config")
        params = Namespace(
            obj_type=self._data_formats[data_format]['objType'],
            shape=self._data_formats[data_format]['shape'],
            dtype=self._get_dtype(self._data_formats[data_format]['dtype']),
        )
        return params
