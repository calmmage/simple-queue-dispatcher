import os

import pytest

from simple_queue_dispatcher.core.app_config import DatabaseConfig, AppConfig


@pytest.fixture
def setup_environment():
    os.environ['DATABASE_CONN_STR'] = 'test_conn_str'
    os.environ['DATABASE_NAME'] = 'test_name'
    os.environ['TELEGRAM_BOT_TOKEN'] = 'test_token'
    yield
    del os.environ['DATABASE_CONN_STR']
    del os.environ['DATABASE_NAME']
    del os.environ['TELEGRAM_BOT_TOKEN']


def test_database_config(setup_environment):
    database = DatabaseConfig()
    assert database.conn_str == 'test_conn_str'
    assert database.name == 'test_name'


def test_app_config(setup_environment):
    app_config = AppConfig()
    assert app_config
