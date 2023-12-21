"""
Testing suite for the transform script, including base and edge cases
and mocking for all functions in the script.
"""

import unittest
from unittest.mock import patch, MagicMock

import pandas as pd
from pandas.api.types import is_datetime64_any_dtype as is_datetime
import pytest

from transform_readings import clean_reading_data


@pytest.fixture
def fake_df():

    fake_plants = [{
        "botanist": {
            "email": "fake_email_1",
            "name": "fake_name_1",
            "phone": "fake_phone_1"
        },
        "last_watered": "Wed, 20 Dec 2023 14:10:54 GMT",
        "plant_name": "fake_flower_1",
        "plant_id": 1,
        "error": None,
        "recording_taken": "2023-12-21 10:20:34",
        "soil_moisture": 33.95801666242039,
        "temperature": 9.111493582669517
    },
        {
        "botanist": {
            "email": "fake_email_2",
            "name": "fake_name_2",
            "phone": "fake_phone_2"
        },
        "last_watered": "Wed, 20 Dec 2023 14:10:54 GMT",
        "plant_name": "fake_flower_2",
        "plant_id": 2,
        "error": None,
        "recording_taken": "2023-12-21 10:20:34",
        "soil_moisture": 33.95801666242039,
        "temperature": 9.111493582669517
    }]

    return pd.DataFrame(fake_plants)


class TestCleanReadingData():
    """Tests involving clean_reading_data()."""

    def test_last_watered_datetime(self, fake_df):
        """The values in the last_watered column should be converted to a datetime64[ns] type."""

        result_df = clean_reading_data(fake_df)
        print(result_df['last_watered'].dtype)
        assert result_df['last_watered'].dtype == 'datetime64[ns]'
