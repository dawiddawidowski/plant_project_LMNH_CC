"""Script uploads data from reading table over past 24 hours to the S3 bucket"""
from datetime import datetime
from os import environ

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, sql
import s3fs

load_dotenv()


def get_database_connection(config):
    """Returns a live database connection."""
    return create_engine(f"""mssql+pymssql://{config['DB_USER']}:{config['DB_PASSWORD']}@{config['DB_HOST']}/plants""")


def get_todays_data(connection) -> pd.DataFrame:
    """Returns the entries from reading table for current day"""
    with connection.connect() as conn:

        conn.execute(sql.text("USE plants"))

        query = sql.text("""SELECT * FROM s_gamma.reading
                         WHERE CONVERT(DATE, recording_taken) = CONVERT(DATE, GETDATE());""")
        res = conn.execute(query).fetchall()

        query = sql.text("""DELETE FROM s_gamma.reading;""")
        conn.execute(query)
        conn.commit()

        return pd.DataFrame(res)


def write_to_bucket(data: pd.DataFrame) -> None:
    """converts the data into a csv file and writes to S3 bucket
    S3 object path and file name is the current date
    """

    current_date = datetime.now().strftime('%Y/%m/%d')
    csv_format = datetime.now().strftime('%Y-%m-%d')

    csv_file_name = f'{csv_format}.csv'

    bucket_name = 'c9-beetle-lmnh-plant-data-terraform'

    s3 = s3fs.S3FileSystem(anon=False)
    with s3.open(f'{bucket_name}/{current_date}/{csv_file_name}', 'w') as f:
        data.to_csv(f, index=False)


def lambda_handler(event=None, context=None):
    """Function called by Lambda to upload to S3"""
    db_conn = get_database_connection(environ)
    reading_data = get_todays_data(db_conn)

    write_to_bucket(reading_data)
    print("File uploaded")
