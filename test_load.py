"""
Testing suite for the load script, including base and edge cases
and mocking functions in the script.
"""


import unittest
from unittest.mock import patch, MagicMock

import pandas as pd
import pytest
from sqlalchemy import create_engine, sql

from load import update_reading


@pytest.fixture(name="fake_df")
def df():
    """Fixture for testing valid base cases."""

    fake_plants = [{
        "plant_id": 1,
        "plant_name": "fake_flower_1",
        "soil_moisture": 33.95801666242039,
        "temperature": 9.111493582669517,
        "last_watered": "Wed, 20 Dec 2023 14:10:54 GMT",
        "recording_taken": "2023-12-21 10:20:34",
        "botanist_name": "fake_name_1",
        "botanist_mobile": "fake_phone_1",
        "botanist_email": "fake_email_1",
        "error": None
    }]

    return pd.DataFrame(fake_plants)


@pytest.fixture(name="fake_df_new_botanist")
def df_new_botanist():
    """Fixture for testing valid base cases."""

    fake_plants = [{
        "plant_id": 1,
        "plant_name": "fake_flower_1",
        "soil_moisture": 33.95801666242039,
        "temperature": 9.111493582669517,
        "last_watered": "Wed, 20 Dec 2023 14:10:54 GMT",
        "recording_taken": "2023-12-21 10:20:34",
        "botanist_name": "fake_name_1_new",
        "botanist_mobile": "fake_phone_1_new",
        "botanist_email": "fake_email_1_new",
        "error": None
    }]

    return pd.DataFrame(fake_plants)


@patch('load.create_engine')
def test_add_new_botanist_if_not_exist(mock_create_engine, fake_df_new_botanist):
    """update_reading() should insert a new botanist into the database if one doesn't exist."""

    mock_connection = MagicMock()
    mock_execute = mock_connection.execute
    mock_execute.fetchone.return_value = None

    # Mock the connect method of the create_engine result
    mock_engine = mock_create_engine.return_value
    mock_engine.connect.return_value.__enter__.return_value = mock_connection

    result = update_reading(mock_engine, fake_df_new_botanist)

    assert result == fake_df_new_botanist
