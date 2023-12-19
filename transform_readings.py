'''Script to clean data pulled from the plant API,
ready to insert into the database.'''

import pandas as pd


def get_field(row: str | None, field: str, value_type=str) -> str | None:
    '''Helper function to get a license or image field from a row in the DataFrame.'''
    try:
        return value_type(eval(row).get(field))
    except TypeError:
        return None


def clean_reading_data(filename: str) -> pd.DataFrame:
    '''Loads in the static data in csv format, cleans the data
    including removing any entries with errors and returns the
    new dataset as a pandas DataFrame. Columns in the DataFrame
    are grouped by which database table they are in.'''

    df = pd.read_csv(filename)

    # Remove any rows containing errors
    df = df[df['error'].isna()]

    # Columns for 'reading' table
    df['soil_moisture'] = df['soil_moisture'].round(2)
    df['temperature'] = df['temperature'].round(2)

    # Columns for 'botanist' table
    df['botanist_email'] = df['botanist'].apply(
        eval).apply(lambda x: x.get('email', None))
    df['botanist_name'] = df['botanist'].apply(
        eval).apply(lambda x: x.get('name', None))
    df['botanist_mobile'] = df['botanist'].apply(
        eval).apply(lambda x: x.get('phone', None))
    df.drop('botanist', axis=1, inplace=True)

    # Reordering columns
    order = ['plant_id', 'plant_name', 'soil_moisture', 'temperature',
             'last_watered', 'recording_taken', 'botanist_name',
             'botanist_mobile', 'botanist_email']
    df = df[order]
    df.to_csv('transformed_data.csv', index=False)
    return df


if __name__ == "__main__":

    print(clean_reading_data("extracted_readings_data.csv"))
