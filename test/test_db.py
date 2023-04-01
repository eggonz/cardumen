import os
import time

import numpy as np
import pytest

from cardumen.config import DataConfig
from cardumen.database import Database, Table
from cardumen.handler import Handler
from cardumen.logger import set_log_level, LogLevel

# set logging level to debug for tests
set_log_level(LogLevel.DEBUG)


@pytest.fixture
def mock_db_path():
    return "../test.db"


@pytest.fixture
def mock_table_name():
    return 'test_data'


@pytest.fixture
def mock_data_config():
    return DataConfig("../data_config.json")


@pytest.fixture
def mock_db(mock_db_path, mock_table_name, mock_data_config):
    if os.path.exists(mock_db_path):
        os.remove(mock_db_path)
    db = Database(mock_db_path, 1)
    db.connect()
    table = Table(db, mock_table_name, mock_data_config)
    table.create()
    table.add(time.time(), [np.array([[1, 2, 3], [4, 5, 6]]).astype(np.float32)])
    yield db
    db.close()
    os.remove(mock_db_path)


@pytest.fixture
def mock_table(mock_db, mock_table_name, mock_data_config):
    table = Table(mock_db, mock_table_name, mock_data_config)
    yield table


def test_get_all(mock_table):
    items = mock_table.get_all()
    for it in items:
        print(it)


def test_data_get_all(mock_data_config):
    db_path = "../cardumen_dev.db"
    table_name = 'fish1'
    db = Database(db_path, 1)
    db.connect()
    table = Table(db, table_name, mock_data_config)
    items = table.get_all()
    print(items[0])
    print(items[0][1].shape)
    print(items[0][2].shape)
    db.close()
