import sqlite3
import struct

import numpy as np


class BinaryConverter:
    def __init__(self, obj_type: str):
        if obj_type not in {'array', 'list', 'matrix'}:
            raise NotImplementedError(f"Cannot convert {obj_type} to binary. "
                                      f"Only 'array', 'list' and 'matrix' are supported")
        self._obj_type = obj_type

    def to_binary(self, obj) -> bytes:
        if self._obj_type == 'array':
            return self._array2binary(obj)
        elif self._obj_type == 'list':
            return self._list2binary(obj)
        elif self._obj_type == 'matrix':
            return self._matrix2binary(obj)
        raise TypeError(f"Cannot convert {type(obj)} to binary")

    def from_binary(self, obj_bytes: bytes) -> object:
        if self._obj_type == 'array':
            return self._binary2array(obj_bytes)
        elif self._obj_type == 'list':
            return self._binary2list(obj_bytes)
        elif self._obj_type == 'matrix':
            return self._binary2matrix(obj_bytes)
        raise TypeError(f"Cannot convert binary to {self._obj_type}")

    def _array2binary(self, arr: np.ndarray) -> bytes:
        self._dtype = arr.dtype
        arr_bytes = arr.tobytes()
        return arr_bytes

    def _list2binary(self, lst: list) -> bytes:
        self._size = len(lst)
        lst_bytes = struct.pack('f' * len(lst), *[float(it) for it in lst])
        return lst_bytes

    def _matrix2binary(self, mat: list[list]) -> bytes:
        self._shape = (len(mat), len(mat[0]))
        mat_bytes = struct.pack('f' * len(mat) * len(mat[0]), *[float(item) for row in mat for item in row])
        return mat_bytes

    def _binary2array(self, arr_bytes: bytes) -> np.ndarray:
        arr = np.frombuffer(arr_bytes, dtype=self._dtype)
        return arr

    def _binary2list(self, lst_bytes: bytes) -> list:
        # lst = list(struct.unpack('f' * (len(lst_bytes) // self._size), lst_bytes))
        # lst = list(struct.unpack('f' * len(lst_bytes), lst_bytes))
        lst = list(struct.unpack('f' * self._size, lst_bytes))
        return lst

    def _binary2matrix(self, mat_bytes: bytes) -> list[list]:
        # mat = struct.unpack('f' * len(mat_bytes), mat_bytes)
        mat = struct.unpack('f' * self._shape[0] * self._shape[1], mat_bytes)
        mat = [list(mat[i:i + self._shape[1]]) for i in range(0, len(mat), self._shape[1])]
        return mat


class Database:
    def __init__(self, path: str, bin_converter: BinaryConverter, commit_freq: int = 200):
        self.path = path
        self._db = None
        self._cursor = None
        self._bin_converter = bin_converter

        self._commit_freq = commit_freq
        self._num_items = 0

    def connect(self):
        self._db = sqlite3.connect(self.path)
        self._cursor = self._db.cursor()

    def commit(self):
        self._db.commit()

    def close(self):
        self._db.close()
        self._db = None

    def _execute(self, query, params=()):
        self._db.execute(query, params)

    def create_table(self):
        self._execute(f'CREATE TABLE data (time FLOAT, label INTEGER, arr BLOB)')
        # Unnecessary primary key, slows down item insertion
        # self._execute(f'CREATE TABLE data (id INTEGER PRIMARY KEY, time INTEGER, label INTEGER, arr BLOB)')
        # Creating indices slows down item insertion
        # self._execute(f'CREATE INDEX idx_label ON data (label)')
        # self._execute(f'CREATE INDEX idx_time ON data (time)')

    def add(self, time: float, label: int, arr):
        bin_arr = self._bin_converter.to_binary(arr)
        self._execute('INSERT INTO data (time, label, arr) VALUES (?, ?, ?)', (time, label, bin_arr))
        self._num_items += 1
        if self._num_items % self._commit_freq == 0:
            print(f"Committing to database")
            self.commit()

    def get_all_label(self, label: int):
        self._cursor.execute('SELECT * FROM data WHERE label = ?', (label,))
        rows = self._cursor.fetchall()
        arr = [(row[0], row[1], self._bin_converter.from_binary(row[3])) for i, row in enumerate(rows)]
        return arr

    def get_all_timerange(self, start_time: float, end_time: float):
        self._cursor.execute('SELECT * FROM data WHERE time BETWEEN ? AND ?', (start_time, end_time))
        rows = self._cursor.fetchall()
        arr = [(row[0], row[1], self._bin_converter.from_binary(row[3])) for i, row in enumerate(rows)]
        return arr

    def get_all_label_timerange(self, label: int, start_time: float, end_time: float):
        self._cursor.execute('SELECT * FROM data WHERE label = ? AND time BETWEEN ? AND ?',
                             (label, start_time, end_time))
        rows = self._cursor.fetchall()
        arr = [(row[0], row[1], self._bin_converter.from_binary(row[3])) for i, row in enumerate(rows)]
        return arr
