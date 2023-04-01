from cardumen.config import Config
from cardumen.design_patterns import singleton


@singleton
class Handler:
    def __init__(self):
        self._config = None
        self._scene = None
        self._db = None

    def set_config(self, config: Config):
        self._config = config

    def set_scene(self, scene):
        self._scene = scene

    def set_db(self, db):
        self._db = db

    @property
    def config(self) -> Config:
        return self._config

    @property
    def scene(self):
        return self._scene

    @property
    def db(self):
        return self._db
