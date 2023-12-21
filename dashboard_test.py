"""Streamlit dashboard for plant data"""

import boto3
import streamlit as st
import altair as alt
from os import environ
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy.sql import text
from sqlalchemy import create_engine
from datetime import datetime
from io import StringIO


def get_db_connection():
    """Connects to the remote database"""

    engine = create_engine(
        f"mssql+pymssql://{environ['DB_USER']}:{environ['DB_PASSWORD']}@{environ['DB_HOST']}/plants")
    conn = engine.connect()

    return conn


def get_object_keys(s3_client, bucket: str, s3_folder: str) -> list[str]:
    """Gets the keys of the objects in the bucket"""

    if not isinstance(bucket, str):
        raise TypeError("bucket must be a string")

    contents = s3_client.list_objects(
        Bucket=bucket, Prefix=s3_folder)["Contents"]

    return [o["Key"] for o in contents]


def load_s3_data(s3_client, bucket: str, key):
    """Loads old plant data from S3 bucket"""

    obj = s3_client.get_object(Bucket=bucket, Key=key)
    return pd.read_csv(obj['Body'])


if __name__ == "__main__":

    load_dotenv()
    conn = get_db_connection()
    s3_client = boto3.client("s3",
                             aws_access_key_id=environ["AWS_ACCESS_KEY_ID"],
                             aws_secret_access_key=environ["AWS_SECRET_ACCESS_KEY"])

    custom_background = """
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

    with conn:
        reading_data = pd.read_sql(
            'SELECT * FROM s_gamma.reading;', conn)

        st.set_page_config(page_title="Plant Dashboard - LMNH", layout="wide")

        st.markdown(custom_background, unsafe_allow_html=True)
        st.title("Plant Dashboard - LMNH")

        cols = st.columns(2)

        current_date = datetime.now().strftime("%Y-%m-%d")

        # CURRENT DATABASE
        with cols[0]:
            st.header('Most recent data')
            st.write(f"Date: {current_date}")
            st.subheader("Raw data on readings")

            selected_plant = st.number_input(
                "Filter by plant id:", value=None, step=1)

            if selected_plant is not None:
                filtered_plant_data = reading_data[reading_data['plant_id']
                                                   == selected_plant]
                st.dataframe(filtered_plant_data)

                st.subheader(
                    f"Latest moisture readings over 24 hours for plant {selected_plant}")
                moisture_chart = alt.Chart(reading_data).mark_bar(color='#C71585').encode(
                    x='recording_taken',
                    y='soil_moisture')
                st.altair_chart(moisture_chart, use_container_width=True)

                st.subheader(
                    f"Latest temperature readings over 24 hours for plant {selected_plant}")
                temp_chart = alt.Chart(reading_data).mark_bar(color='#C71585').encode(
                    x='recording_taken',
                    y='temperature')
                st.altair_chart(temp_chart, use_container_width=True)

            else:
                st.dataframe(reading_data)

            #     st.subheader("Latest moisture readings for each plant")
            #     moisture_chart = alt.Chart(reading_data).mark_bar(color='#C71585').encode(
            #         x='plant_id',
            #         y='soil_moisture')
            #     st.altair_chart(moisture_chart, use_container_width=True)

            #     st.subheader("Latest temperature readings for each plant")
            #     temp_chart = alt.Chart(reading_data).mark_bar(color='#C71585').encode(
            #         x='plant_id',
            #         y='temperature')
            #     st.altair_chart(temp_chart, use_container_width=True)

        # OLD DATA
        with cols[1]:
            # f-string the year
            st.header("Old data")
            st.subheader("Raw data on readings")
            current_year = str(datetime.now().year)

            keys = get_object_keys(
                s3_client, 'c9-beetle-lmnh-plant-data', f'{current_year}/')
            selected_key = st.selectbox('Select Data', keys)
            old_data = load_s3_data(
                s3_client, 'c9-beetle-lmnh-plant-data', selected_key)

            selected_plant_old = st.number_input(
                "Filter old data by plant id:", value=None, step=1)

            if selected_plant_old is not None:
                filtered_plant_data_old = old_data[old_data['plant_id']
                                                   == selected_plant_old]
                st.write(
                    f"Raw data for {selected_key}, plant {selected_plant_old}")
                st.dataframe(filtered_plant_data_old)

                # Graphing old data - filtered by plant id
                st.subheader(
                    f"Moisture readings for plant {selected_plant_old} over time (old)")
                moisture_chart = alt.Chart(filtered_plant_data_old).mark_bar(color='#8B00FF').encode(
                    x='recording_taken',
                    y='soil_moisture')
                st.altair_chart(moisture_chart, use_container_width=True)

                st.subheader(
                    f"Temperature readings for plant {selected_plant_old} over time (old)")
                temp_chart = alt.Chart(filtered_plant_data_old).mark_bar(color='#8B00FF').encode(
                    x='recording_taken',
                    y='temperature')
                st.altair_chart(temp_chart, use_container_width=True)

            else:
                st.write(f"Raw data for {selected_key}")
                st.dataframe(old_data)

            #     # graphing old data - unfiltered
            #     st.subheader("Previous moisture readings for each plant (old)")
            #     moisture_chart = alt.Chart(old_data).mark_bar(color='#8B00FF').encode(
            #         x='plant_id',
            #         y='soil_moisture')
            #     st.altair_chart(moisture_chart, use_container_width=True)

            #     st.subheader(
            #         "Previous temperature readings for each plant (old)")
            #     temp_chart = alt.Chart(old_data).mark_bar(color='#8B00FF').encode(
            #         x='plant_id',
            #         y='temperature')
            #     st.altair_chart(temp_chart, use_container_width=True)
