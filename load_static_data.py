"""Seeds the database with initial static data"""
import os
from os import environ
import requests
import csv
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, sql, Table, MetaData

BASE_URL = 'https://data-eng-plants-api.herokuapp.com/plants/'
MAX_PLANT_NUM = 51


def get_db_connection():
    """Connects to the remote database"""

    engine = create_engine(
        f"mssql+pymssql://{environ['DB_USER']}:{environ['DB_PASSWORD']}@{environ['DB_HOST']}/?charset=utf8")
    conn = engine.connect()

    return conn


def get_raw_data() -> list[dict]:
    """"Returns all raw data about plants."""

    plants_list = []
    for plant_id in range(MAX_PLANT_NUM):
        try:
            plant_dict = {}
            plant_details = requests.get(
                BASE_URL+str(plant_id), timeout=10).json()
            plant_dict["plant_id"] = plant_details.get("plant_id")

            # Origin
            plant_dict["latitude"] = plant_details.get(
                "origin_location", [''])[0]
            plant_dict["longitude"] = plant_details.get(
                "origin_location", ['', ''])[1]
            plant_dict["location"] = plant_details.get(
                "origin_location", ['', '', ''])[2]
            plant_dict["country_code"] = plant_details.get("origin_location", ['', '', '', ''])[
                3]
            plant_dict["region"] = plant_details.get(
                "origin_location", ['', '', '', '', ''])[4]

            # Botanist
            plant_botanist = plant_details.get("botanist")
            plant_dict["botanist_name"] = plant_botanist.get(
                'name') if isinstance(plant_botanist, dict) else None
            plant_dict["botanist_email"] = plant_botanist.get(
                'email') if isinstance(plant_botanist, dict) else None
            plant_dict["botanist_phone"] = plant_botanist.get(
                'phone') if isinstance(plant_botanist, dict) else None

            # License
            plant_images = plant_details.get("images", {'license': None})
            plant_dict["license"] = plant_images.get(
                'license') if isinstance(plant_images, dict) else None
            plant_dict["license_name"] = plant_images.get(
                'license_name') if isinstance(plant_images, dict) else None
            plant_dict["license_url"] = plant_images.get(
                'license_url') if isinstance(plant_images, dict) else None

            # Images
            plant_dict['medium_url'] = plant_details.get(
                "medium_url") if isinstance(plant_images, dict) else None
            plant_dict['regular_url'] = plant_details.get(
                "regular_url") if isinstance(plant_images, dict) else None
            plant_dict['original_url'] = plant_details.get(
                "original_url") if isinstance(plant_images, dict) else None
            plant_dict["small_url"] = plant_details.get(
                'small_url') if isinstance(plant_images, dict) else None
            plant_dict["thumbnail"] = plant_details.get(
                'thumbnail') if isinstance(plant_images, dict) else None

            plants_list.append(plant_dict)
        except requests.exceptions.JSONDecodeError:
            print(plant_id, "plant not found")

    return plants_list


def write_to_csv(details_list: list, filename: str):
    """
    Writes plant data to a CSV file. Use for both
    valid and error plants.
    """
    possible_headers = set(
        header for entry in details_list for header in entry.keys())

    with open(filename, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=possible_headers)

        writer.writeheader()

        for entry in details_list:
            writer.writerow(entry)


def convert_csv_to_df(filename: str) -> pd.DataFrame:
    """Converts csv to df"""

    df = pd.read_csv(filename)
    return df


def populate_origin_table():
    """Populates origin table"""

    df = convert_csv_to_df('master_plant_csv.csv')

    # botanist_list = df[['country_code', 'latitude', 'longitude',
    #                     'location', 'region']].drop_duplicates().values.tolist()

    origin_list = df[['country_code', 'latitude', 'longitude',
                      'location', 'region']].drop_duplicates().values.tolist()

    conn = get_db_connection()
    conn.execute(sql.text("USE plants;"))

    query = sql.text(
        'INSERT INTO s_gamma.origin (country_code, latitude, longitude, location, region) VALUES (:?,:?,:?,:?,:?)')

    for sublist in origin_list:
        conn.execute(query, sublist)

    return origin_list


""""
    time_zone_name VARCHAR(100) NOT NULL,
    country VARCHAR(50) NOT NULL,
    region VARCHAR(50) NOT NULL,
    latitude DECIMAL(7,5) NOT NULL,
    longitude DECIMAL(8,5) NOT NULL,
"""


# def find_plant_data(data: list[dict]) -> list[list]:
#     """
#     Takes in all raw plant data and finds info for
#     plant table
#     """
#     all_plant_data = []
#     for datum in data:
#         # without plant ids
#         current_plant_data = []
#         current_plant_data.append(datum.get('name', ''))
#         current_plant_data.append(datum.get('scientific_name', ''))
#         # need to crack into this
#         current_plant_data.append(datum.get('origin_location', ''))
#         current_plant_data.append(datum.get('image', ''))

# [TODO] Address difficulty with linking origin to plant in database

# def find_botanist_data(data: list[dict]) -> list[list]:
#     """
#     Takes in all raw plant data and finds info for
#     botanist table
#     """
#     # all_botanist_data = []
#     # for datum in data:
#     pass
if __name__ == "__main__":
    load_dotenv()
    data = get_raw_data()
    write_to_csv(data, 'master_plant_csv.csv')
    populate_origin_table()
