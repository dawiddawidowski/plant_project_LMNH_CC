'''Script to extract the readings information for each plant and stores
this in a pandas DataFrame.'''

from time import perf_counter
from multiprocessing import Pool
import requests

import pandas as pd


BASE_URL = 'https://data-eng-plants-api.herokuapp.com/plants/'
MAX_PLANT_NUM = 51


def extract_changing_plant_details(plant_id: int) -> dict:
    """
    Extracts only the necessary information for each plant reading
    at a fixed point in time and stores this in a dictionary.
    """

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
    except requests.exceptions.JSONDecodeError as errj:
        print(plant_id, "Error, Plant not found" + errj)
    except requests.exceptions.HTTPError as errh:
        print("An Http Error occurred:" + repr(errh))
    except requests.exceptions.ConnectionError as errc:
        print("An Error Connecting to the API occurred:" + repr(errc))
    except requests.exceptions.Timeout as errt:
        print("A Timeout Error occurred:" + repr(errt))
    except requests.exceptions.RequestException as err:
        print("An Unknown Error occurred" + repr(err))

    print("Extracted plant information from API.")
    return plant_dict


def extract_all_plant_details() -> pd.DataFrame:
    """
    Top level function which implements multiprocessing and returns a Data Frame
    containing all plant details.
    """
    plants_list = []

    # Implement multiprocessing
    with Pool(4) as p:
        result_list = p.map(extract_changing_plant_details,
                            range(MAX_PLANT_NUM))
        plants_list.extend(result_list)

    # Turn into data frame
    return pd.DataFrame(plants_list)


if __name__ == '__main__':
    start_time = perf_counter()
    df_plants = extract_all_plant_details()
    end_time = perf_counter()
    print(f"Time taken: {end_time - start_time} seconds")
    print(df_plants.shape)
