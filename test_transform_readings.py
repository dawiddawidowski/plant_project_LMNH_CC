"""
Testing suite for the transform script, including base and edge cases
and mocking for all functions in the script.
"""

import pandas as pd
import pytest

from transform_readings import clean_reading_data


@pytest.fixture(name="fake_df")
def df():
    """Fixture for testing valid base cases."""

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
        "soil_moisture": 30.91501666242039,
        "temperature": 9.150493582669517
    }]

    return pd.DataFrame(fake_plants)


@pytest.fixture(name="fake_df_negative_soil_temp")
def df_negative_soil_temp():
    """Fixture for testing negative soil moisture and temperature edge case."""

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
        "soil_moisture": -33.95801666242039,
        "temperature": -9.111493582669517
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
        "soil_moisture": 30.91501666242039,
        "temperature": 9.150493582669517
    }]

    return pd.DataFrame(fake_plants)


@pytest.fixture(name="fake_df_zero_soil_temp")
def df_zero_soil_temp():
    """Fixture for testing zero soil moisture and temperature edge case."""

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
        "soil_moisture": 0,
        "temperature": 0
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
        "soil_moisture": 30.91501666242039,
        "temperature": 9.150493582669517
    }]

    return pd.DataFrame(fake_plants)


@pytest.fixture(name="fake_df_high_soil_temp")
def df_high_soil_temp():
    """Fixture for testing excessively high soil moisture and temperature edge case."""
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
        "soil_moisture": 101,
        "temperature": 41
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
        "soil_moisture": 30.91501666242039,
        "temperature": 9.150493582669517
    }]

    return pd.DataFrame(fake_plants)


@pytest.fixture(name="fake_df_error")
def df_error():
    """Fixture for testing error reading edge cases."""

    fake_plants = [{
        "botanist": None,
        "last_watered": None,
        "plant_name": None,
        "plant_id": 8,
        "error": 'plant not found',
        "recording_taken": None,
        "soil_moisture": None,
        "temperature": None
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
        "soil_moisture": 30.91501666242039,
        "temperature": 9.150493582669517
    }]

    return pd.DataFrame(fake_plants)


def test_last_watered_datetime(fake_df):
    """The values in the last_watered column should be converted to a datetime64[ns] type."""

    result_df = clean_reading_data(fake_df)
    assert result_df['last_watered'].dtype == 'datetime64[ns]'


def test_soil_moisture_rounded(fake_df):
    """The values in the soil_moisture column should be rounded to 2 d.p."""

    result_df = clean_reading_data(fake_df)
    assert result_df['soil_moisture'][0] == 33.96
    assert result_df['soil_moisture'][1] == 30.92


def test_temperature_rounded(fake_df):
    """The values in the temperature column should be rounded to 2 d.p."""

    result_df = clean_reading_data(fake_df)
    assert result_df['temperature'][0] == 9.11
    assert result_df['temperature'][1] == 9.15


def test_extracted_botanist_email_column(fake_df):
    """The botanist column should be flattened to include a botanist_email column."""

    result_df = clean_reading_data(fake_df)
    assert result_df['botanist_email'][0] == "fake_email_1"
    assert result_df['botanist_email'][1] == "fake_email_2"


def test_extracted_botanist_name_column(fake_df):
    """The botanist column should be flattened to include a botanist_name column."""

    result_df = clean_reading_data(fake_df)
    assert result_df['botanist_name'][0] == "fake_name_1"
    assert result_df['botanist_name'][1] == "fake_name_2"


def test_extracted_botanist_mobile_column(fake_df):
    """The botanist column should be flattened to include a botanist_mobile column."""

    result_df = clean_reading_data(fake_df)
    assert result_df['botanist_mobile'][0] == "fake_phone_1"
    assert result_df['botanist_mobile'][1] == "fake_phone_2"


def test_column_order(fake_df):
    """
    The resulting data frame columns should be in a specific order
    for compatibility with load script.
    """

    result_df = clean_reading_data(fake_df)
    assert result_df.columns[0] == 'plant_id'
    assert result_df.columns[1] == 'plant_name'
    assert result_df.columns[2] == 'soil_moisture'
    assert result_df.columns[3] == 'temperature'
    assert result_df.columns[4] == 'last_watered'
    assert result_df.columns[5] == 'recording_taken'
    assert result_df.columns[6] == 'botanist_name'
    assert result_df.columns[7] == 'botanist_mobile'
    assert result_df.columns[8] == 'botanist_email'
    assert result_df.columns[9] == 'error'


def test_negative_soil_moisture(fake_df_negative_soil_temp):
    """A reading (row) with a negative soil_moisture column value should be discarded."""

    result_df = clean_reading_data(fake_df_negative_soil_temp)

    assert result_df["soil_moisture"].get(0) is None
    assert result_df["soil_moisture"][1] == 30.92
    assert len(result_df["soil_moisture"]) == 1


def test_negative_temperature(fake_df_negative_soil_temp):
    """A reading (row) with a negative temperature column value should be discarded."""

    result_df = clean_reading_data(fake_df_negative_soil_temp)

    assert result_df["temperature"].get(0) is None
    assert result_df["temperature"][1] == 9.15
    assert len(result_df["temperature"]) == 1


def test_high_temperature(fake_df_high_soil_temp):
    """A reading (row) with an excessive temperature column value should be discarded."""

    result_df = clean_reading_data(fake_df_high_soil_temp)

    assert result_df["temperature"].get(0) is None
    assert result_df["temperature"][1] == 9.15
    assert len(result_df["temperature"]) == 1


def test_high_soil_moisture(fake_df_high_soil_temp):
    """A reading (row) with an excessive soil_moisture column value should be discarded."""

    result_df = clean_reading_data(fake_df_high_soil_temp)

    assert result_df["soil_moisture"].get(0) is None
    assert result_df["soil_moisture"][1] == 30.92
    assert len(result_df["soil_moisture"]) == 1


def test_zero_temperature(fake_df_zero_soil_temp):
    """A reading (row) with an zero temperature column value should be kept."""

    result_df = clean_reading_data(fake_df_zero_soil_temp)

    assert result_df["temperature"][0] == 0
    assert result_df["temperature"][1] == 9.15
    assert len(result_df["temperature"]) == 2


def test_zero_soil_moisture(fake_df_zero_soil_temp):
    """A reading (row) with an zero soil_moisture column value should be kept."""

    result_df = clean_reading_data(fake_df_zero_soil_temp)

    assert result_df["soil_moisture"][0] == 0
    assert result_df["soil_moisture"][1] == 30.92
    assert len(result_df["soil_moisture"]) == 2


def test_error_reading(fake_df_error):
    """A reading (row) with nan values due to an error reading should remain as nan."""

    result_df = clean_reading_data(fake_df_error)
    test_value = pd.isnull(result_df.at[0, 'soil_moisture'])
    print(test_value)

    assert test_value
    assert result_df["soil_moisture"][1] == 30.92
