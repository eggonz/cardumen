from cardumen.config import Config


class Handler:
    def __init__(self):
        self.config = Config()
        self.scene = None
        self.display = None
        self.db = None
