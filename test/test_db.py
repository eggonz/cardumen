import os

from cardumen.database import Database, Table

import pytest
import numpy as np
import time


@pytest.fixture
def db_path():
    return "../test.db"


@pytest.fixture
def table_name():
    return 'test_data'


@pytest.fixture
def db(db_path, table_name):
    if os.path.exists(db_path):
        os.remove(db_path)
    db = Database(db_path, 1)
    db.connect()
    table = Table(db, table_name)
    table.create()
    table.add(time.time(), np.array([[1, 2, 3], [4, 5, 6]]).astype(np.float32))
    yield db
    db.close()
    os.remove(db_path)


@pytest.fixture
def table(db, table_name):
    table = Table(db, table_name)
    yield table


def test_get_all(table):
    items = table.get_all()
    print()
    for it in items:
        print(it)
