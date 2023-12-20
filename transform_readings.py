"""
Transform script for the Plant Sensor ETL pipeline.
This script cleans data pulled from the plant API,
and puts it into an order ready to load into the database.
"""

import pandas as pd


def get_field(row: str | None, field: str, value_type=str) -> str | None:
    '''Helper function to get a license or image field from a row in the DataFrame.'''
    try:
        return value_type(eval(row).get(field))
    except TypeError:
        return None


def clean_reading_data(df: pd.DataFrame) -> pd.DataFrame:
    '''Loads in the extracted data in the form of a pandas DataFrame,
    cleans the data and returns the new dataset as a pandas DataFrame. 
    Columns in the DataFrame are grouped by which database table they are in.'''

    # Convert the date format
    df['last_watered'] = pd.to_datetime(
        df['last_watered'], format='%a, %d %b %Y %H:%M:%S GMT')

    # Columns for 'reading' table
    df['soil_moisture'] = df['soil_moisture'].round(2)
    df['temperature'] = df['temperature'].round(2)

    # Columns for 'botanist' table
    df['botanist_email'] = df['botanist'].apply(
        lambda x: x.get('email', None) if x is not None else x)
    df['botanist_name'] = df['botanist'].apply(
        lambda x: x.get('name', None) if x is not None else x)
    df['botanist_mobile'] = df['botanist'].apply(
        lambda x: x.get('phone', None) if x is not None else x)
    df.drop('botanist', axis=1, inplace=True)

    # Reordering columns
    order = ['plant_id', 'plant_name', 'soil_moisture', 'temperature',
             'last_watered', 'recording_taken', 'botanist_name',
             'botanist_mobile', 'botanist_email', 'error']

    df = df[order]

    print("Transformed extracted data.")
    return df
