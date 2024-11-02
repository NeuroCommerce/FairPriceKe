import pandas as pd
import sqlalchemy
from sqlalchemy import text
from get_jumia_phones_data import *
from get_phones_kenya_data import PhonePlaceKenyaScraping
from clean_phone_kenya_data import PhoneKenyaDataCleaner
from clean_jumia_data import JumiaDataCleaner
import os
import json  # Importing JSON module for handling JSON data


class ConvertDfToSQL:
    def __init__(self):
        self.user = 'postgres'
        self.password = '1234'
        self.host = 'localhost'
        self.port = 1234    # Specify your PostgreSQL port here
        self.db_name = 'fairpriceke'

        # Create engine for PostgreSQL with specified port
        self.engine = sqlalchemy.create_engine(
            f'postgresql+psycopg://{self.user}:{
                self.password}@{self.host}:{self.port}'
        )
        self.create_database()

    def create_database(self):
        try:
            with self.engine.connect() as conn:
                conn.execute(text(f"CREATE DATABASE {self.db_name}"))
                # Terminate any existing connections to the database before dropping
                conn.execute(text(
                    f"SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = '{self.db_name}'"))
            # Update engine to connect to the newly created database
            self.engine = sqlalchemy.create_engine(
                f'postgresql+psycopg2://{self.user}:{self.password}@{
                    self.host}:{self.port}/{self.db_name}'
            )
            print(f"Database '{self.db_name}' created successfully.")
        except sqlalchemy.exc.SQLAlchemyError as e:
            print(f"Error creating database: {e}")

    def convert(self, df: pd.DataFrame, table_name: str, mode='replace'):
        try:
            df.to_sql(table_name, con=self.engine, if_exists=mode, index=False)
            print(f"Data inserted into table '{
                  table_name}' with mode '{mode}'")
        except sqlalchemy.exc.SQLAlchemyError as e:
            print(f"Error inserting data into table '{table_name}': {e}")

    def append_to_history(self, df: pd.DataFrame, history_table_name: str):
        try:
            df.to_sql(history_table_name, con=self.engine,
                      if_exists='append', index=False)
            print(f"Data appended to history table '{history_table_name}'")
        except sqlalchemy.exc.SQLAlchemyError as e:
            print(f"Error appending data to history table '{
                  history_table_name}': {e}")

    def run(self):
        # Scraping and cleaning for PhonePlaceKenya
        ppk = PhonePlaceKenyaScraping()
        df = ppk.run()
        ppk_clean = PhoneKenyaDataCleaner(df)
        df_cleaned= ppk_clean.clean_data()

        self.convert(df_cleaned, 'phoneplacekenya', mode='replace')
        self.append_to_history(df_cleaned, 'phoneplacekenya_history')

        # Scraping and cleaning for Jumia
        jumia_data = os.path.join(
            'data', 'Jumia', 'row', 'today_jumia_data.json')
        cleaner = JumiaDataCleaner(jumia_data)
        cleaned_df = cleaner.get_cleaned_data()

        # Ensure Key_Features and stock are stored as JSON strings
        cleaned_df['Key_Features'] = cleaned_df['Key_Features'].apply(
            lambda x: json.dumps(x))
        cleaned_df['stock'] = cleaned_df['stock'].apply(
            lambda x: json.dumps(x))

        print(cleaned_df.info())
        print(cleaned_df)

        self.convert(cleaned_df, 'jumia', mode='replace')
        self.append_to_history(cleaned_df, 'jumia_history')


if __name__ == "__main__":
    x = ConvertDfToSQL()
    x.run()
