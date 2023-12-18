"""
This is a script to download a sample csv file of plan data.
"""

import csv
import requests


BASE_URL = 'https://data-eng-plants-api.herokuapp.com/plants/'
MAX_PLANT_NUM = 51


def extract_plant_details():
    """"Returns"""

    for plant_id in range(MAX_PLANT_NUM):
        valid_plants_list = []
        error_plants_list = []
        try:
            plant_details = requests.get(
                BASE_URL+str(plant_id), timeout=10).json()
            if 'error' in plant_details:
                print(plant_id, plant_details)
                error_plants_list.append(plant_details)
            else:
                print(plant_id, "valid id")
                valid_plants_list.append(plant_details)

            # print(plant_id, plant_details)
        except requests.exceptions.JSONDecodeError:
            print(plant_id, "plant not found")

        return valid_plants_list, error_plants_list


extract_plant_details()


# 7 {'error': 'plant not found', 'plant_id': 7}

# 15 {'error': 'plant sensor fault', 'plant_id': 15}

# 43 {'error': 'plant on loan to another museum', 'plant_id': 43}


# assume invalid?
# 74 {'error': 'plant sensor fault', 'plant_id': 74}

# 59 {'error': 'plant sensor fault', 'plant_id': 59}

# 76 {'error': 'plant sensor fault', 'plant_id': 76}

# 70 {'error': 'plant sensor fault', 'plant_id': 70}
