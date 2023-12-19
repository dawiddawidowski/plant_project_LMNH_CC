from os import environ
from dotenv import load_dotenv

import pandas as pd
from sqlalchemy import create_engine, sql



def get_database_connection(config):
    """Returns a live database connection."""
    return create_engine(f"mssql+pymssql://{config['DB_USER']}:{config['DB_PASSWORD']}@{config['DB_HOST']}/?charset=utf8")


def insert_seed(connection, new_data: pd.DataFrame):
    
    with connection.connect() as conn:

        conn.execute(sql.text("USE ..."))

        query = sql.text("INSERT INTO ... ")
        connection.execute()


def update_reading(connection, new_data: pd.DataFrame):
    pass


if __name__ == "__main__":

    load_dotenv()

    db_conn = get_database_connection(environ)
