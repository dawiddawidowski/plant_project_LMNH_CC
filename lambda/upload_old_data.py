"""Script uploads data from reading table over past 24 hours to the S3 bucket"""
from datetime import datetime
from os import environ

import pandas as pd
import boto3
from dotenv import load_dotenv
from sqlalchemy import create_engine, sql


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


def write_to_bucket(s3_client: boto3.client, data: pd.DataFrame) -> None:
    """converts the data into a csv file and writes to S3 bucket
    S3 object path and file name is the current date
    """

    current_date = datetime.now().strftime('%Y/%m/%d')
    csv_format = datetime.now().strftime('%Y-%m-%d')

    csv_file_name = f'{csv_format}.csv'
    data.to_csv(csv_file_name, index=False)

    bucket_name = 'c9-beetle-lmnh-plant-data'

    s3_object_key = f'{current_date}/{csv_file_name}'
    s3_client.upload_file(csv_file_name, bucket_name, s3_object_key)


def lambda_handler(event=None, context=None):

    db_conn = get_database_connection(environ)
    reading_data = get_todays_data(db_conn)

    s3 = boto3.client('s3', aws_access_key_id=environ["AWS_ACCESS_KEY_ID"],
                            aws_secret_access_key=environ["AWS_SECRET_ACCESS_KEY"])
    write_to_bucket(s3, reading_data)


if __name__ == "__main__":
    load_dotenv()
    lambda_handler()
