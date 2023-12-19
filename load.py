from os import environ
from dotenv import load_dotenv

import pandas as pd
from sqlalchemy import create_engine, sql



def get_database_connection(config):
    """Returns a live database connection."""
    return create_engine(f"mssql+pymssql://{config['DB_USER']}:{config['DB_PASSWORD']}@{config['DB_HOST']}/?charset=utf8")


def update_reading(connection, new_data: pd.DataFrame):
    """Function updates RDS database"""
    # column headers ['soil_moisture', 'temperature', 'last_watered', 'recording_taken',  # Reading table
    #          'plant_name', 'scientific_name',  # Plant table
    #          'botanist_name', 'botanist_mobile', 'botanist_email',  # Botanist table
    #          'country_code', 'latitude', 'longitude', 'location', 'region',  # Origin table
    #          'license_name', 'license_url', 'license_number',  # License table
    #          'medium_url', 'regular_url', 'original_url', 'small_url', 'thumbnail_url'  # Image table
    #          ]

    # Insert data fetched from passed minute into reading table 
    with connection.connect() as conn:

        plant_data = new_data.values.tolist()[:1]

        print(plant_data)
        for reading in data:

            data = [97.33, 13.23, 'Mon, 18 Dec 2023 14:03:04 GMT', '2023-12-18 14:49:04']

            conn.execute(sql.text("USE plants"))

            # id_query = sql.text("SELECT * FROM s_gamma.botanist;")

            botanist_id_query = sql.text("SELECT botanist_id FROM s_gamma.botanist WHERE name = (:botanist_name);")
            botanist_id = conn.execute(botanist_id_query, {
                "botanist_name": reading[6]
            }).fetchone()[0]

            print(botanist_id)
            # plant_id_query = sql.text("SELECT plant_id FROM s_gamma.plant WHERE plant_name = '...';")
            # # plant_id = conn.execute(plant_id_query).fetchone()[0]
            # plant_id = 100

            # query = sql.text("""INSERT INTO s_alpha.reading (plant_id, botanist_id, soil_moisture, temperature, last_watered, recording_taken) VALUES 
            #                  (:plant),(:botanist),(:moisture),(:temperature),(:watered_at),(:recording_at)""")
            # conn.execute(sql.text(query, {
            #     "plant": plant_id,
            #     "botanist": botanist_id,
            #     "moisture": data[0],
            #     "temperature": data[1],
            #     "watered_at": data[2],
            #     "recording_at": data[3]
            # }))

        
            # query = sql.text("SELECT plant_id FROM s_gamma.plant WHERE plant_name = '...';")

            # conn.execute(sql.text("COMMIT;"))

            # res = conn.execute(query).fetchall()
            # print(res)


         
if __name__ == "__main__":

    load_dotenv()

    # engine = create_engine(f"mssql+pymssql://{environ['DB_USER']}:{environ['DB_PASSWORD']}@{environ['DB_HOST']}/?charset=utf8")
    db_conn = get_database_connection(environ)

    cleaned_file = pd.read_csv('transformed_data.csv')

    # print(cleaned_file)

    update_reading(db_conn, cleaned_file)