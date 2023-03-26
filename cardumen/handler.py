from cardumen.config import AppConfig


class Handler:
    def __init__(self, config: AppConfig):
        self.config = config
        self.scene = None
        self.display = None
        self.db = None
