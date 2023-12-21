import pandas as pd



if __name__ == "__main__":

    load_dotenv()

    db_conn = get_database_connection(environ)

    cleaned_file = pd.read_csv('transformed_data.csv')

    update_reading(db_conn, cleaned_file)