import time
from dotenv import load_dotenv

from sample_extract import extract_changing_plant_details
from transform_readings import clean_reading_data
from load import get_database_connection, update_reading


def main(connection):

    # Extract
    start_extract_time = time.time()
    plants_df = extract_changing_plant_details()
    end_extract_time = time.time()
    print(f"Extract time: {end_extract_time - start_extract_time}")

    # Transform
    start_transform_time = time.time()
    transformed_df = clean_reading_data(plants_df)
    end_transform_time = time.time()
    print(f"Transform time: {end_transform_time - start_transform_time}")

    # Load
    start_load_time = time.time()
    update_reading(connection, transformed_df)
    end_load_time = time.time()
    print(f"Load time: {end_load_time - start_load_time}")


if __name__ == "__main__":

    load_dotenv()
    db_connection = get_database_connection()

    while True:
        start_time = time.time()
        print(main(db_connection))
        end_time = time.time()

        elapsed_time = end_time - start_time
        print(f"Total time: {elapsed_time} secs")
        if elapsed_time > 60:
            continue
        else:
            time.sleep(60 - elapsed_time)
