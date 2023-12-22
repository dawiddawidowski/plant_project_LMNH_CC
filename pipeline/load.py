"""
Load script for the Plant Sensor ETL pipeline.
Script to load clean data onto RDS database, connecting to
the database and sending INSERT queries to the database.
"""

from os import environ

import pandas as pd
from sqlalchemy import create_engine, sql


def get_database_connection():
    """Returns a live database connection."""
    return create_engine(f"""mssql+pymssql://{environ['DB_USER']}:{environ['DB_PASSWORD']}@{environ['DB_HOST']}/plants""")


def update_reading(connection, new_data: pd.DataFrame) -> None:
    """Function to insert records of plant health for each plant into the
    reading table in the plant database."""

    with connection.connect() as conn:

        plant_data = new_data.values.tolist()

        for reading in plant_data:

            plant_id = reading[0]

            conn.execute(sql.text("USE plants"))

            botanist_id_query = sql.text(
                "SELECT botanist_id FROM s_gamma.botanist WHERE botanist_name = (:botanist_name);")

            fetched_botanist_query = conn.execute(botanist_id_query,
                                                  {"botanist_name": reading[6]}).fetchone()

            error = reading[-1]
            try:
                # Do not insert erroneous transactions
                if not error:
                    botanist_id = fetched_botanist_query[0]
                    insert_query = sql.text(
                        """INSERT INTO s_gamma.reading
                        (plant_id, botanist_id, soil_moisture,
                          temperature, last_watered, recording_taken)
                        VALUES (:plant, :botanist, :moisture,
                          :temperature, :watered_at, :recording_at)""")
                    conn.execute(insert_query, {
                        "plant": plant_id,
                        "botanist": botanist_id,
                        "moisture": reading[2],
                        "temperature": reading[3],
                        "watered_at": reading[4],
                        "recording_at": reading[5]
                    })
                    conn.commit()
            except Exception:
                continue
