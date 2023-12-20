"""Streamlit dashboard for plant data"""

# [TODO] Get live data
#       Visualise live data (wireframe?)
#       Graph latest temperature and moisture for each plant
#       Get graphs from old data
#       Ext: Make these graphs overlap? (Past and present temperature and moisture?)

import streamlit as st
import altair as alt
from os import environ
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy.sql import text
from sqlalchemy import create_engine


def get_db_connection():
    """Connects to the remote database"""

    engine = create_engine(
        f"mssql+pymssql://{environ['DB_USER']}:{environ['DB_PASSWORD']}@{environ['DB_HOST']}/plants")
    conn = engine.connect()

    return conn


if __name__ == "__main__":

    load_dotenv()
    conn = get_db_connection()

    custom_background = """
    <style>
    body {
        background-color: #fff0f5;
    }
    .stApp {
        background-color: #fff0f5;
    }
    .stTextArea {
        background-color: white;
    }
    </style>
    """

    with conn:
        # need .head(38) because the reading table contains a jumble of data right now
        reading_data = pd.read_sql(
            'SELECT * FROM s_gamma.reading;', conn).head(38)

        st.markdown(custom_background, unsafe_allow_html=True)
        st.title("Plant Dashboard - LMNH")

        reading_data['soil_moisture'] = reading_data['soil_moisture'].astype(
            int)

        print(reading_data['soil_moisture'])

        reading_data['temperature'] = reading_data['temperature'].astype(
            int)

        st.subheader("Raw data on readings")
        st.dataframe(reading_data)

        st.subheader("Latest moisture readings for each plant")
        moisture_chart = alt.Chart(reading_data).mark_bar().encode(
            x='plant_id', y='soil_moisture')
        st.altair_chart(moisture_chart, use_container_width=True)

        st.subheader("Latest temperature readings for each plant")
        temp_chart = alt.Chart(reading_data).mark_bar().encode(
            x='plant_id', y='temperature')
        st.altair_chart(temp_chart, use_container_width=True)

        # cols = st.columns(2)
