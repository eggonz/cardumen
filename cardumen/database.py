import sqlite3
import struct
import time

import numpy as np

from cardumen.config import DbConfig


class BinaryConverter:
    def __init__(self, obj_type: str, shape: tuple, dtype: type):
        if obj_type not in {'array', 'list', 'matrix'}:
            raise NotImplementedError(f"Cannot convert {obj_type} to binary. "
                                      f"Only 'array', 'list' and 'matrix' are supported")
        self._obj_type = obj_type
        self._shape = tuple(shape)
        self._dtype = dtype

    def check_validity(self, obj) -> None:
        """
        Check if the object is valid for the converter.
        It checks object type, dtype and shape.
        If the object type is 'matrix', it also checks if the matrix is rectangular.

        :param obj: object to check
        :return:
        """
        if self._obj_type == 'array':
            if not isinstance(obj, np.ndarray):
                raise TypeError(f"Invalid type. Expected {np.ndarray}, got {type(obj)}")
            if obj.dtype != self._dtype:
                raise TypeError(f"Invalid dtype. Expected {self._dtype}, got {obj.dtype}")
            if obj.shape != self._shape:
                raise TypeError(f"Invalid shape. Expected {self._shape}, got {obj.shape}")
        elif self._obj_type == 'list':
            if not isinstance(obj, list):
                raise TypeError(f"Invalid type. Expected {list}, got {type(obj)}")
            if not all(isinstance(item, self._dtype) for item in obj):
                raise TypeError(f"Invalid dtype. Expected {self._dtype}, got {type(obj[0])}")
            shape = (len(obj),)
            if shape != self._shape:
                raise TypeError(f"Invalid size. Expected {self._shape}, got {shape}")
        elif self._obj_type == 'matrix':
            if not isinstance(obj, list):
                raise TypeError(f"Invalid type. Expected {list}, got {type(obj)}")
            col_len = len(obj[0])
            for row in obj:
                if not isinstance(row, list):
                    raise TypeError(f"Invalid type. Expected {list}, got {type(row)}")
                if not all(isinstance(item, self._dtype) for item in row):
                    raise TypeError(f"Invalid dtype. Expected {self._dtype}, got {type(row[0])}")
                if len(row) != col_len:
                    raise TypeError(f"Invalid shape. Expected rectangular matrix.")
            shape = (len(obj), col_len)
            if shape != self._shape:
                raise TypeError(f"Invalid shape. Expected {self._shape}, got {shape}")
        else:
            raise TypeError(f"Invalid type. Expected {self._obj_type}, got {type(obj)}")

    def to_bytes(self, obj) -> bytes:  # TODO measure latency of each obj type
        self.check_validity(obj)  # TODO measure latency of validity method
        if self._obj_type == 'array':
            return self._array2binary(obj)
        elif self._obj_type == 'list':
            return self._list2binary(obj)
        elif self._obj_type == 'matrix':
            return self._matrix2binary(obj)
        raise TypeError(f"Cannot convert {type(obj)} to binary")

    def from_bytes(self, obj_bytes: bytes) -> object:
        if self._obj_type == 'array':
            return self._binary2array(obj_bytes)
        elif self._obj_type == 'list':
            return self._binary2list(obj_bytes)
        elif self._obj_type == 'matrix':
            return self._binary2matrix(obj_bytes)
        raise TypeError(f"Cannot convert binary to {self._obj_type}")

    def _array2binary(self, arr: np.ndarray) -> bytes:
        arr_bytes = arr.tobytes()
        return arr_bytes

    def _list2binary(self, lst: list) -> bytes:
        lst_bytes = struct.pack('f' * self._shape[0], *[float(it) for it in lst])
        return lst_bytes

    def _matrix2binary(self, mat: list[list]) -> bytes:
        mat_bytes = struct.pack('f' * self._shape[0] * self._shape[1], *[float(item) for row in mat for item in row])
        return mat_bytes

    def _binary2array(self, arr_bytes: bytes) -> np.ndarray:
        arr = np.frombuffer(arr_bytes, dtype=self._dtype)
        return arr

    def _binary2list(self, lst_bytes: bytes) -> list:
        # lst = list(struct.unpack('f' * (len(lst_bytes) // self._size), lst_bytes))
        # lst = list(struct.unpack('f' * len(lst_bytes), lst_bytes))
        lst = list(struct.unpack('f' * self._shape[0], lst_bytes))
        return lst

    def _binary2matrix(self, mat_bytes: bytes) -> list[list]:
        # mat = struct.unpack('f' * len(mat_bytes), mat_bytes)
        mat = struct.unpack('f' * self._shape[0] * self._shape[1], mat_bytes)
        mat = [list(mat[i:i + self._shape[1]]) for i in range(0, len(mat), self._shape[1])]
        return mat


class Database:
    def __init__(self, path: str, db_config: DbConfig):
        self.path = path
        self._db = None
        self._cursor = None
        self.config = db_config

        self._buffer_items = 0

    def connect(self):
        self._db = sqlite3.connect(self.path)
        self._cursor = self._db.cursor()

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        """Commit the database if the buffer is full."""
        self._buffer_items += 1
        if self._buffer_items >= self.config.BUFFER_SIZE:
            print(f"Committing {self._buffer_items} items")
            self._db.commit()
            self._buffer_items = 0

    def close(self):
        # commit remaining items
        print(f"Committing {self._buffer_items} items")
        self._db.commit()
        self._buffer_items = 0

        # close connection
        self._db.close()
        self._db = None

    def execute(self, query, params=()):
        self._db.execute(query, params)


class Table:
    def __init__(self, db: Database, name: str, data_format: str):
        self._db = db
        self.name = name

        self._bin_converter = BinaryConverter(
            self._db.config[data_format].obj_type,
            self._db.config[data_format].shape,
            self._db.config[data_format].dtype,
        )

        # create table
        self._db.execute(f'CREATE TABLE IF NOT EXISTS {self.name} (time FLOAT, state BLOB)')

        # Unnecessary primary key, slows down item insertion
        # self._execute(f'CREATE TABLE {self.name} (id INTEGER PRIMARY KEY, time FLOAT, state BLOB)')
        # Creating indices slows down item insertion
        # self._execute(f'CREATE INDEX idx_label ON {self.name} (label)')
        # self._execute(f'CREATE INDEX idx_time ON {self.name} (time)')

    def add(self, time: float, state: object):
        bin_arr = self._bin_converter.to_bytes(state)
        self._db.execute(f'INSERT INTO {self.name} (time, state) VALUES (?, ?)', (time, bin_arr))
        self._db.commit()

    def _format_items(self, items: list[tuple[float, object]]) -> list[tuple[float, bytes]]:
        return [(time, self._bin_converter.to_bytes(state)) for time, state in items]

    def get_all(self):
        self._db.cursor.execute(f'SELECT * FROM {self.name}')
        return self._format_items(self._db.cursor.fetchall())  # TODO test gets, use check_validity

    def get_timerange(self, start_time: float, end_time: float):
        self._db.cursor.execute(f'SELECT * FROM {self.name} WHERE time BETWEEN ? AND ?', (start_time, end_time))
        return self._format_items(self._db.cursor.fetchall())  # TODO test gets, use check_validity
