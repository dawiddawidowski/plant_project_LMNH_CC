"""Streamlit dashboard for plant data"""
from os import environ
from datetime import datetime

import pandas as pd
import boto3
import streamlit as st
import altair as alt
from dotenv import load_dotenv
from sqlalchemy import create_engine


CUSTOM_BACKGROUND = """
    <style>
    body {
        background-color: #fff0f5;
    }
    .stApp {
        background-color: #white;
    }
    .stTextArea {
        background-color: white;
    }
    </style>
    """

CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_YEAR = str(datetime.now().year)
BUCKET_NAME = 'c9-beetle-lmnh-plant-data-terraform'


def get_db_connection():
    """Connects to the RDS plants database"""

    return create_engine(
        f"""mssql+pymssql://{environ['DB_USER']}:{environ['DB_PASSWORD']}@{environ['DB_HOST']}/plants""").connect()


def get_object_keys(client, bucket: str, s3_folder: str) -> list[str]:
    """Gets the keys of the objects in the bucket"""

    if not isinstance(bucket, str):
        raise TypeError("bucket must be a string")

    contents = client.list_objects(
        Bucket=bucket, Prefix=s3_folder)["Contents"]

    return [o["Key"] for o in contents]


def load_s3_data(s3_client: boto3.client, bucket: str, key):
    """Loads old plant data from S3 bucket"""

    obj = s3_client.get_object(Bucket=bucket, Key=key)
    return pd.read_csv(obj['Body'])


def show_specific_plant_info(
        plant_data: pd.DataFrame,
        chosen_plant: int,
        plant_filter: str,
        colour: str,
        timeframe: str) -> pd.DataFrame:
    """Returns plant info for a single plant based on specific filter provided"""

    st.subheader(
        f"{plant_filter} readings ({timeframe}) for plant {chosen_plant}")
    moisture_chart = alt.Chart(plant_data).mark_bar(color=colour).encode(
        x='recording_taken',
        y=plant_filter)
    return st.altair_chart(moisture_chart, use_container_width=True)


def create_full_reading_table(all_plant_data, timeframe):
    """Returns a full reading table within timeframe, allowing user to filter plants to see"""

    st.write(f"ALL RAW DATA from {timeframe}")
    unique_plant_numbers = all_plant_data["plant_id"].unique()
    selected_plants = st.multiselect(
        "Select plants to view", unique_plant_numbers, default=unique_plant_numbers)
    readings_data = all_plant_data[(
        all_plant_data['plant_id'].isin(selected_plants))]
    return st.dataframe(readings_data)


if __name__ == "__main__":

    load_dotenv()
    conn = get_db_connection()
    s3 = boto3.client("s3",
                      aws_access_key_id=environ["AWS_ACCESS_KEY_ID"],
                      aws_secret_access_key=environ["AWS_SECRET_ACCESS_KEY"])

    with conn:
        reading_data = pd.read_sql(
            'SELECT * FROM s_gamma.reading;', conn)

        st.set_page_config(page_title="Plant Dashboard - LMNH", layout="wide")

        st.markdown(CUSTOM_BACKGROUND, unsafe_allow_html=True)
        st.title("Plant Dashboard - LMNH")
        cols = st.columns(2)

        # CURRENT DATABASE
        with cols[0]:
            st.header('Most recent data')
            st.write(f"Date: {CURRENT_DATE}")
            st.subheader("Raw data on readings in last 24 hours")

            create_full_reading_table(reading_data, "PAST 24 HOURS")

            selected_plant = st.selectbox(
                "Select to view temperature and moisture for one plant",
                reading_data['plant_id'].unique())

            filtered_plant_data = reading_data[reading_data['plant_id']
                                               == selected_plant]

            show_specific_plant_info(
                filtered_plant_data,
                selected_plant,
                'soil_moisture',
                '#C71585',
                "Latest")

            show_specific_plant_info(
                filtered_plant_data,
                selected_plant,
                'temperature',
                '#C71585',
                "Latest")

        # OLD DATA
        with cols[1]:
            st.header("Old data")
            st.subheader("Raw data on readings across time")
            keys = get_object_keys(
                s3, BUCKET_NAME, f'{CURRENT_YEAR}/')
            selected_key = st.selectbox('Select Data', keys)
            old_data = load_s3_data(
                s3, BUCKET_NAME, selected_key)
            create_full_reading_table(old_data, selected_key)
            selected_plant_old = st.selectbox("Select to view one plant id",
                                              old_data['plant_id'].unique())
            filtered_plant_data_old = old_data[old_data['plant_id']
                                               == selected_plant_old]
            show_specific_plant_info(
                filtered_plant_data_old,
                selected_plant_old,
                'soil_moisture',
                '#8B00FF',
                "Over time"
            )
            show_specific_plant_info(
                filtered_plant_data_old,
                selected_plant_old,
                'temperature',
                '#8B00FF',
                "Over time"
            )
