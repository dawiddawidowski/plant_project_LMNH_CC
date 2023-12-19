from datetime import datetime
from os import environ

import boto3
from dotenv import load_dotenv


def write_to_bucket():

    load_dotenv()
    aws_access_key_id = environ["AWS_ACCESS_KEY_ID"]
    aws_secret_access_key = environ["AWS_SECRET_ACCESS_KEY"]

    s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id,
                             aws_secret_access_key=aws_secret_access_key)

    bucket_name = 'c9-beetle-lmnh-plant-data'

    current_date = datetime.now()
    year_month_day = current_date.strftime('%Y/%M/%d')

    csv_file_name = 'transformed_data.csv'
    s3_object_key = f'{year_month_day}/{csv_file_name}'

    s3_client.upload_file(csv_file_name, bucket_name, s3_object_key)


if __name__ == "__main__":

    write_to_bucket()
