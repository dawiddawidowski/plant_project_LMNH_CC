"""
Testing suite for the transform script, including base and edge cases
and mocking for all functions in the script.
"""

import unittest
from unittest.mock import patch, MagicMock

import pandas as pd
import pytest

from transform_readings import clean_reading_data


@pytest.fixture
def fake_df():

    fake_plant = {
        "botanist": {
            "email": "fake_email_1",
            "name": "fake_name_1",
            "phone": "fake_phone_1"
        },
        "last_watered": "Wed, 20 Dec 2023 14:10:54 GMT",
        "name": "fake_flower_1",
        "origin_location": [
            "7.65649",
            "4.92235",
            "fake_location_1",
            "fake_country_code_1",
            "fake_region_1"
        ],
        "plant_id": 1,
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
        "name": "fake_flower_2",
        "origin_location": [
            "7.65649",
            "4.92235",
            "fake_location_2",
            "fake_country_code_2",
            "fake_region_2"
        ],
        "plant_id": 2,
        "recording_taken": "2023-12-21 10:20:34",
        "soil_moisture": 33.95801666242039,
        "temperature": 9.111493582669517
    }

    return pd.DataFrame([fake_plant])


class TestCleanReadingData():
    """Tests involving clean_reading_data()."""

    def test_(self, fake_df):

        assert "plant_id" in fake_df.columns
