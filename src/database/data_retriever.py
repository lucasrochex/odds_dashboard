import pandas as pd
import psycopg2
from datetime import datetime, timedelta

db_params = {
    'dbname': 'futebol',
    'user': 'postgres',
    'password': '123',
    'host': 'localhost',
    'port': '5432'
}

def get_odds_48():
    try:
        # Connect to the PostgreSQL database
        connection = psycopg2.connect(**db_params)
        time_threshold = datetime.now() - timedelta(hours=48)
        # Create a SQL query to select all data from the specified table
        query = f"""SELECT * FROM odds_tracker.odds
        WHERE timestamp >= %s
        """

        # Use pandas to read data from the database into a DataFrame
        dataframe = pd.read_sql(query, connection, params=[time_threshold])

        # Close the connection
        connection.close()

        return dataframe

    except (Exception, psycopg2.Error) as error:
        print("Error fetching data:", error)
        return None