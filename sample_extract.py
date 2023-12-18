"""
This is a script to download a sample csv file of plan data.
"""

import csv
import requests
from time import perf_counter


BASE_URL = 'https://data-eng-plants-api.herokuapp.com/plants/'
MAX_PLANT_NUM = 51


def extract_plant_details():
    """"Returns all raw data about plants"""

    plants_list = []
    for plant_id in range(MAX_PLANT_NUM):
        try:
            plant_details = requests.get(
                BASE_URL+str(plant_id), timeout=10).json()
            plants_list.append(plant_details)
            # extract only relevant values/ keys
            # soil moisture, last_water, recording_taken, botanist, temperature
        except requests.exceptions.JSONDecodeError:
            print(plant_id, "plant not found")

    return plants_list


def extract_changing_plant_details():
    """
    Extracts only the changing plant information
    soil moisture, last_water, recording_taken, botanist, temperature
    """

    plants_list = []
    for plant_id in range(MAX_PLANT_NUM):
        try:
            plant_dict = {}
            plant_details = requests.get(
                BASE_URL+str(plant_id), timeout=10).json()
            plant_dict["soil_moisture"] = plant_details.get("soil_moisture")
            plant_dict["last_water"] = plant_details.get("last_water")
            plant_dict["recording_taken"] = plant_details.get(
                "recording_taken")
            plant_dict["botanist"] = plant_details.get("botanist")
            plant_dict["temperature"] = plant_details.get("temperature")
            plant_dict["error"] = plant_details.get("error")
            plant_dict["plant_id"] = plant_id
            plants_list.append(plant_dict)
            # extract only relevant values/ keys
            # soil moisture, last_water, recording_taken, botanist, temperature
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


if __name__ == "__main__":
    start_time = perf_counter()
    plants = extract_changing_plant_details()
    write_to_csv(plants, "test_plant_data.csv")
    end_time = perf_counter()

    print(f"Time take for extract: {end_time - start_time} seconds.")
