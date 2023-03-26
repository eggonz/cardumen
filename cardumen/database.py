import sqlite3

import numpy as np

from cardumen.logger import log


class BinaryConverter:
    def __init__(self, dtype: type):
        self._dtype = dtype

    def to_bytes(self, arr: np.ndarray) -> bytes:
        if not isinstance(arr, np.ndarray):
            raise TypeError(f"Cannot convert {type(arr)} to binary")
        arr_bytes = arr.astype(self._dtype).tobytes()
        return arr_bytes

    def from_bytes(self, arr_bytes: bytes) -> np.ndarray:
        arr = np.frombuffer(arr_bytes, dtype=self._dtype)
        return arr


class Database:
    def __init__(self, path: str, buffer_size: int = 1):
        self.path = path
        self._conn = None
        self._cursor = None
        self._buffer_size = buffer_size
        self._buffer_items = 0

    def connect(self):
        log.debug(f"Connecting to database at {self.path}")
        self._conn = sqlite3.connect(self.path)
        self._cursor = self._conn.cursor()

    def cursor(self):
        return self._cursor

    def commit(self, force: bool = False):
        """Commit the database if the buffer is full."""
        self._buffer_items += 1
        if force or self._buffer_items >= self._buffer_size:
            log.debug(f"Committing {self._buffer_items} items")
            self._conn.commit()
            self._buffer_items = 0

    def close(self):
        # commit remaining items
        log.debug(f"Committing {self._buffer_items} items")
        self._conn.commit()
        self._buffer_items = 0

        # close connection
        log.debug(f"Closing database connection")
        self._cursor.close()
        self._conn.close()
        self._conn = None

    def execute(self, query, params=()):
        self._conn.execute(query, params)


class Table:
    def __init__(self, db: Database, name: str):
        self._db = db
        self.name = name
        self._bin_converter = BinaryConverter(dtype=np.float32)

    def create(self):
        log.debug(f"Creating table {self.name}")
        self._db.execute(f'CREATE TABLE IF NOT EXISTS {self.name} (time FLOAT, state BLOB)')
        self._db.commit(force=True)

    def add(self, time: float, state: np.ndarray):
        bin_arr = self._bin_converter.to_bytes(state)
        self._db.execute(f'INSERT INTO {self.name} (time, state) VALUES (?, ?)', (time, bin_arr))
        self._db.commit()

    def _format_items(self, items: list[tuple[float, bytes]]) -> list[tuple[float, np.ndarray]]:
        return [(time, self._bin_converter.from_bytes(state)) for time, state in items]

    def get_all(self):
        log.debug(f"Getting all items from table {self.name}")
        cur = self._db.cursor()
        cur.execute(f'SELECT time, state FROM {self.name}')
        return self._format_items(cur.fetchall())

    def get_timerange(self, start_time: float, end_time: float):
        log.debug(f"Getting items from table {self.name} between {start_time} and {end_time}")
        cur = self._db.cursor()
        cur.execute(f'SELECT time, state FROM {self.name} WHERE time BETWEEN ? AND ?', (start_time, end_time))
        return self._format_items(cur.fetchall())
