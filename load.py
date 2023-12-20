"""Script to load clean data onto RDS database."""
from os import environ
from dotenv import load_dotenv

import pandas as pd
from sqlalchemy import create_engine, sql


def get_database_connection(config):
    """Returns a live database connection."""
    return create_engine(f"""mssql+pymssql://{config['DB_USER']}:{config['DB_PASSWORD']}@{config['DB_HOST']}/plants""")


def update_reading(connection, new_data: pd.DataFrame):
    """Function updates RDS database"""

    with connection.connect() as conn:

        plant_data = new_data.values.tolist()

        for reading in plant_data:

            conn.execute(sql.text("USE plants"))

            botanist_id_query = sql.text(
                "SELECT botanist_id FROM s_gamma.botanist WHERE botanist_name = (:botanist_name);")
            botanist_id = conn.execute(botanist_id_query, {
                "botanist_name": reading[6]
            }).fetchone()[0]

            plant_id = reading[0]

            query = sql.text(
                """INSERT INTO s_gamma.reading 
                (plant_id, botanist_id, soil_moisture, temperature, last_watered, recording_taken) 
                VALUES 
                (:plant, :botanist, :moisture, :temperature, :watered_at, :recording_at)""")
            conn.execute(query, {
                "plant": plant_id,
                "botanist": botanist_id,
                "moisture": reading[2],
                "temperature": reading[3],
                "watered_at": reading[4],
                "recording_at": reading[5]
            })
            conn.commit()


if __name__ == "__main__":

    load_dotenv()

    db_conn = get_database_connection(environ)

    cleaned_file = pd.read_csv('transformed_data.csv')

    update_reading(db_conn, cleaned_file)
