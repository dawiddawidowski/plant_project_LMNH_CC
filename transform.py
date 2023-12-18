import pandas as pd


def clean_data(filename: str) -> pd.DataFrame:
    '''Loads in the static data in csv format, cleans the data
    including removing any entries with errors and returns the
    new dataset as a pandas DataFrame.'''

    df = pd.read_csv(filename)

    # Remove any rows containing errors
    df = df[df['error'].isna()]

    # Format soil moisture column to 2dp
    df['soil_moisture'] = df['soil_moisture'].round(2)

    # Format temperature column to 1dp
    df['temperature'] = df['temperature'].round(1)

    # Create new columns containing botanist information
    df['botanist_email'] = df['botanist'].apply(
        eval).apply(lambda x: x.get('email', None))
    df['botanist_name'] = df['botanist'].apply(
        eval).apply(lambda x: x.get('name', None))
    df['botanist_mobile'] = df['botanist'].apply(
        eval).apply(lambda x: x.get('phone', None))

    # df.drop(['botanist'])
    return df


if __name__ == "__main__":

    print(clean_data("test_plant_data.csv"))
