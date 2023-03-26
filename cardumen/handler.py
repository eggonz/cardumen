from cardumen.config import Config


class Handler:
    def __init__(self, config: Config):
        self.config = config
        self.scene = None
        self.display = None
        self.db = None
