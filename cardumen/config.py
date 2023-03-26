import json
from argparse import Namespace


class AppConfig:
    def __init__(self, path: str):
        with open(path, 'r') as f:
            config = json.load(f)

        self.WIDTH = config['width']
        self.HEIGHT = config['height']
        self.TITLE = config['title']
        self.FPS = config['fps']
        self.UPDATE_RATE = config['update_rate']
        self.WINDOW_RESIZABLE = config['window_resizable']
        self.WINDOW_FULLSCREEN = config['window_fullscreen']
        self.WINDOW_BORDERLESS = config['window_borderless']
        self.WINDOW_WRAP = config['window_wrap']
        self.DB_PATH = config['db_path']
        self.DEBUG = config['debug']
        self.TESTING = config['testing']
        self.TESTING_DB_PATH = config['testing_db_path']


class DbConfig:
    def __init__(self, path: str):
        with open(path, 'r') as f:
            config = json.load(f)
        self._tables = config['tables']

        self.BUFFER_SIZE = config['params']['buffer_size']

    def _get_dtype(self, dtype: str):
        if dtype == 'int':
            return int
        elif dtype == 'float':
            return float
        elif dtype == 'str':
            return str
        else:
            raise ValueError(f"Unknown dtype '{dtype}'")

    def __getitem__(self, table_name: str):
        if table_name not in self._tables:
            raise KeyError(f"Table '{table_name}' not found in config")
        table_config = Namespace(**self._tables[table_name])
        table_config.dtype = self._get_dtype(table_config.dtype)
        return table_config
