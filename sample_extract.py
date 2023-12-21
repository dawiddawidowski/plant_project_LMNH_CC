'''Script to extract the readings information for each plant and stores
this in a pandas DataFrame.'''

from time import perf_counter
import requests

import pandas as pd


BASE_URL = 'https://data-eng-plants-api.herokuapp.com/plants/'
MAX_PLANT_NUM = 51


def extract_changing_plant_details():
    '''Extracts only the necessary information for each plant reading
    at a fixed point in time and stores this in a pandas DataFrame.'''

    plants_list = []
    for plant_id in range(MAX_PLANT_NUM):
        try:
            plant_dict = {}
            plant_details = requests.get(
                BASE_URL+str(plant_id), timeout=10).json()
            plant_dict["soil_moisture"] = plant_details.get("soil_moisture")
            plant_dict["last_watered"] = plant_details.get("last_watered")
            plant_dict["recording_taken"] = plant_details.get(
                "recording_taken")
            plant_dict["botanist"] = plant_details.get("botanist")
            plant_dict["temperature"] = plant_details.get("temperature")
            plant_dict["error"] = plant_details.get("error")
            plant_dict["plant_id"] = plant_id
            plant_dict["plant_name"] = plant_details.get("name")
            plants_list.append(plant_dict)
        except requests.exceptions.JSONDecodeError as errj:
            print(plant_id, "Error, Plant not found" + repr(errj))
        except requests.exceptions.HTTPError as errh:
            print("An Http Error occurred:" + repr(errh))
        except requests.exceptions.ConnectionError as errc:
            print("An Error Connecting to the API occurred:" + repr(errc))
        except requests.exceptions.Timeout as errt:
            print("A Timeout Error occurred:" + repr(errt))
        except requests.exceptions.RequestException as err:
            print("An Unknown Error occurred" + repr(err))

    print("Extracted plant information from API.")
    return pd.DataFrame(plants_list)


if __name__ == "__main__":

    start_time = perf_counter()
    plants = extract_changing_plant_details()
    end_time = perf_counter()
    print(f"Time take for extract: {end_time - start_time} seconds.")
