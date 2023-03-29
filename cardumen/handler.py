from cardumen.config import Config
from cardumen.design_patterns import singleton


@singleton
class Handler:
    def __init__(self, config: Config):
        self.config = config
        self.scene = None
        self.db = None
