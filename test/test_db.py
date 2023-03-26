from cardumen.config import DbConfig
from cardumen.database import Database, Table

import pytest


@pytest.fixture
def db():
    db_config = DbConfig('../db_config.json')
    db = Database("../test.db", db_config)
    db.connect()
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
