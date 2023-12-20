'''Script to clean data pulled from the plant API,
ready to insert into the database.'''

import pandas as pd


def get_field(row: str | None, field: str, value_type=str) -> str | None:
    '''Helper function to get a license or image field from a row in the DataFrame.'''
    try:
        return value_type(eval(row).get(field))
    except TypeError:
        return None


def clean_data(filename: str) -> pd.DataFrame:
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

    # Columns for 'plant' table
    df['plant_name'] = df['name']
    df['scientific_name'] = df['scientific_name'].apply(
        lambda x: eval(x)[0] if not isinstance(x, float) else None)

    # Columns for 'botanist' table
    df['botanist_email'] = df['botanist'].apply(
        eval).apply(lambda x: x.get('email', None))
    df['botanist_name'] = df['botanist'].apply(
        eval).apply(lambda x: x.get('name', None))
    df['botanist_mobile'] = df['botanist'].apply(
        eval).apply(lambda x: x.get('phone', None))
    df.drop('botanist', axis=1, inplace=True)

    # Columns for 'origin' table
    df['country_code'] = df['origin_location'].apply(
        lambda x: eval(x)[3] if eval(x) else None)
    df['latitude'] = df['origin_location'].apply(
        lambda x: eval(x)[0] if eval(x) else None)
    df['longitude'] = df['origin_location'].apply(
        lambda x: eval(x)[1] if eval(x) else None)
    df['location'] = df['origin_location'].apply(
        lambda x: eval(x)[2] if eval(x) else None)
    df['region'] = df['origin_location'].apply(
        lambda x: eval(x)[-1] if eval(x) else None)

    # Columns for 'license' table
    df['license_name'] = df['images'].apply(
        lambda x: get_field(x, 'license_name'))
    df['license_url'] = df['images'].apply(
        lambda x: get_field(x, 'license_url'))
    df['license_number'] = df['images'].apply(
        lambda x: get_field(x, 'license'))

    # Columns for 'image' table
    df['medium_url'] = df['images'].apply(
        lambda x: get_field(x, 'medium_url'))
    df['regular_url'] = df['images'].apply(
        lambda x: get_field(x, 'regular_url'))
    df['original_url'] = df['images'].apply(
        lambda x: get_field(x, 'original_url'))
    df['small_url'] = df['images'].apply(
        lambda x: get_field(x, 'small_url'))
    df['thumbnail_url'] = df['images'].apply(
        lambda x: get_field(x, 'thumbnail'))

    # Reordering columns
    order = ['soil_moisture', 'temperature', 'last_watered', 'recording_taken',  # Reading table
             'plant_name', 'scientific_name',  # Plant table
             'botanist_name', 'botanist_mobile', 'botanist_email',  # Botanist table
             'country_code', 'latitude', 'longitude', 'location', 'region',  # Origin table
             'license_name', 'license_url', 'license_number',  # License table
             'medium_url', 'regular_url', 'original_url', 'small_url', 'thumbnail_url'  # Image table
             ]
    df = df[order]
    return df


if __name__ == "__main__":

    print(clean_data("RAW_plant_data.csv"))
