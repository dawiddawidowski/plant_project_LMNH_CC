"""Seeds the database with initial static data"""

import os
from os import environ
import requests
import csv
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text


load_dotenv()
BASE_URL = 'https://data-eng-plants-api.herokuapp.com/plants/'
DATABASE_URI = f"mssql+pymssql://{environ['DB_USER']}:{environ['DB_PASSWORD']}@{environ['DB_HOST']}/plants"
MAX_PLANT_NUM = 51


def get_db_connection():
    """Connects to the remote database"""

    engine = create_engine(
        f"mssql+pymssql://{environ['DB_USER']}:{environ['DB_PASSWORD']}@{environ['DB_HOST']}/plants")
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

            plant_dict['plant_name'] = plant_details.get('name')
            if plant_details.get('scientific_name'):
                plant_dict['scientific_name'] = plant_details.get(
                    'scientific_name')[0]
            else:
                plant_dict['scientific_name'] = None

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
            if plant_images is not None:
                plant_dict['medium_url'] = plant_images['medium_url'] \
                    if 'medium_url' in plant_images.keys() else None
                plant_dict['regular_url'] = plant_images['regular_url'] \
                    if 'regular_url' in plant_images.keys() else None
                plant_dict['original_url'] = plant_images['original_url'] \
                    if 'original_url' in plant_images.keys() else None
                plant_dict["small_url"] = plant_images['small_url'] \
                    if 'small_url' in plant_images.keys() else None
                plant_dict["thumbnail"] = plant_images['thumbnail'] \
                    if 'thumbnail' in plant_images.keys() else None
            else:
                plant_dict['medium_url'] = None
                plant_dict['regular_url'] = None
                plant_dict['original_url'] = None
                plant_dict['small_url'] = None
                plant_dict['thumbnail'] = None
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


def populate_db_table(table: str, column_list: list[str], data: str) -> None:
    '''Seeds a specified table in the database, with the specified table columns.'''

    # Get the data
    df = pd.read_csv(data)
    rows = df[column_list].drop_duplicates().values.tolist()

    # Remove invalid rows
    rows = [lst for lst in rows if not all(
        isinstance(item, float) for item in lst)]

    # Get ready to insert data
    engine = create_engine(DATABASE_URI)
    metadata = MetaData(schema='s_gamma')
    Session = sessionmaker(bind=engine)
    session = Session()
    db_table = Table(table, metadata, autoload_with=engine)

    # Insert the data into the database table
    for row in rows:
        row_dict = {column: row[index]
                    for index, column in enumerate(column_list)}
        insert_statement = db_table.insert().values(**row_dict)
        session.execute(insert_statement)

    # End the session once finished
    session.commit()
    session.close()


def populate_plant_table(table: str, column_list: list[str], data: str) -> None:
    '''Seeds a specified table in the database, with the specified table columns.'''

    # Get the data
    df = pd.read_csv(data)
    rows = df[column_list].drop_duplicates().values.tolist()

    for row in rows:
        if isinstance(row[1], float):
            row[1] = None
        if isinstance(row[0], float):
            row[0] = None

    # Get ready to insert data
    engine = create_engine(DATABASE_URI)
    metadata = MetaData(schema='s_gamma')
    Session = sessionmaker(bind=engine)
    session = Session()
    db_table = Table(table, metadata, autoload_with=engine)

    # Insert the data into the database table
    for row in rows:
        row_dict = {column: row[index]
                    for index, column in enumerate(column_list)}
        insert_statement = db_table.insert().values(**row_dict)
        session.execute(insert_statement)

    # End the session once finished
    session.commit()
    session.close()


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


def license_id_in_image_table() -> None:
    '''Inserts all license_ids into the image table.'''

    pairs = []
    for plant_id in range(MAX_PLANT_NUM):
        try:
            plant_details = requests.get(BASE_URL+str(plant_id),
                                         timeout=10).json()

            if 'images' in plant_details.keys():
                if 'license_name' in plant_details['images'].keys() \
                        and 'medium_url' in plant_details['images'].keys():
                    pairs.append([plant_details['images']['license_name'],
                                 plant_details['images']['medium_url']])

        except requests.exceptions.JSONDecodeError:
            continue
        except AttributeError:
            continue

    # remove duplicates
    pairs = [list(item) for item in set(tuple(row) for row in pairs)]
    new_pairs = []
    conn = get_db_connection()

    with conn:
        query = text(
            '''select license_id from s_gamma.license where license_name = :value''')
        for pair in pairs:
            res = conn.execute(query, {'value': pair[0]})
            for row in res:
                new_pairs.append([row[0], pair[1]])

        for pair in new_pairs:

            query = text(
                '''update s_gamma.image set license_id = :new_value where medium_url = :condition_value''')
            params = {'new_value': pair[0], 'condition_value': pair[1]}
            res = conn.execute(query, params)
            conn.commit()


def image_id_in_plant_table() -> None:
    '''Inserts all image_ids into the plant table.'''

    pairs = []
    for plant_id in range(MAX_PLANT_NUM):
        try:
            plant_details = requests.get(BASE_URL+str(plant_id),
                                         timeout=10).json()

            if 'images' in plant_details.keys():
                if 'license_name' in plant_details['images'].keys() \
                        and 'medium_url' in plant_details['images'].keys():
                    pairs.append([plant_details['name'],
                                 plant_details['images']['medium_url']])

        except requests.exceptions.JSONDecodeError:
            continue
        except AttributeError:
            continue

    # remove duplicates
    pairs = [list(item) for item in set(tuple(row) for row in pairs)]
    new_pairs = []

    conn = get_db_connection()

    with conn:
        query = text(
            '''select image_id from s_gamma.image where medium_url = :value''')
        for pair in pairs:
            res = conn.execute(query, {'value': pair[1]})
            for row in res:

                new_pairs.append([row[0], pair[0]])
        for pair in new_pairs:
            query = text(
                '''update s_gamma.plant set image_id = :new_value where plant_name = :condition_value''')
            params = {'new_value': pair[0], 'condition_value': pair[1]}
            res = conn.execute(query, params)
            conn.commit()


def origin_id_in_plant_table() -> None:
    '''Inserts all origin_ids into the plant table.'''

    triples = []
    for plant_id in range(MAX_PLANT_NUM):
        try:
            plant_details = requests.get(BASE_URL+str(plant_id),
                                         timeout=10).json()

            plant_name = plant_details.get("name", None)
            latitude = plant_details.get("origin_location", [None])[0]
            longitude = plant_details.get("origin_location", [None, None])[1]

            triples.append([plant_name, latitude, longitude])

        except requests.exceptions.JSONDecodeError:
            continue
        except AttributeError:
            continue

    # remove duplicates
    triples = [list(item) for item in set(tuple(row) for row in triples)]
    new_pairs = []

    conn = get_db_connection()

    with conn:
        query = text(
            '''select origin_id from s_gamma.origin where latitude = :value1 and longitude = :value2''')
        for triple in triples:
            res = conn.execute(
                query, {'value1': triple[1], 'value2': triple[2]})
            for row in res:
                new_pairs.append([row[0], triple[0]])

        for pair in new_pairs:

            query = text(
                '''update s_gamma.plant set origin_id = :new_value where plant_name = :condition_value''')
            params = {'new_value': pair[0], 'condition_value': pair[1]}
            res = conn.execute(query, params)
            conn.commit()


def main():
    '''Seeds all the data in the database tables.'''

    # populate_db_table('origin', ['country_code', 'latitude',
    #                   'longitude', 'location', 'region'], 'master_plant.csv')

    # populate_db_table(
    #     'botanist', ['botanist_name', 'botanist_phone', 'botanist_email'], 'master_plant.csv')

    # populate_db_table(
    #     'license', ['license_name', 'license_url', 'license'], 'master_plant.csv')

    # populate_db_table(
    #     'image', ['medium_url', 'regular_url', 'original_url',
    #               'small_url', 'thumbnail'], 'master_plant.csv')

    # license_id_in_image_table()

    # populate_plant_table(
    #     'plant', ['plant_name', 'scientific_name'], 'master_plant.csv')

    # image_id_in_plant_table()

    # print(origin_id_in_plant_table())


if __name__ == "__main__":

    load_dotenv()
    # write_to_csv(get_raw_data(), 'master_plant.csv')

    # print(image_id_in_plant_table())
