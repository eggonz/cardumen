import os

from cardumen.database import Database, Table

import pytest
import numpy as np
import time


@pytest.fixture
def db():
    if os.path.exists('../test.db'):
        os.remove('../test.db')
    db = Database("../test.db", 1)
    db.connect()
    table = Table(db, "fish1")
    table.create()
    table.add(time.time(), np.array([[1, 2, 3], [4, 5, 6]]).astype(np.float32))
    yield db
    db.close()


@pytest.fixture
def table(db):
    table = Table(db, "fish1")
    yield table


def test_get_all(table):
    items = table.get_all()
    print()
    for it in items:
        print(it)
