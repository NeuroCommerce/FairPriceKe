import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine, text
from .get_jumia_phones_data import *
from .get_phones_kenya_data import PhonePlaceKenyaScraping
from .clean_phone_kenya_data import PhoneKenyaDataCleaner
from .clean_jumia_data import JumiaDataCleaner
import os
import json


def standardize_dataframes(df1, default_link="https://www.jumia.co.ke/?gad_source=1&gclid=CjwKCAjwjsi4BhB5EiwAFAL0YO0ItBXwhDXa2-8ANqkP7xaIs-g5Z7l1Bn8te1d8g7qNUxXCJ-7D0xoCcvAQAvD_BwE"):
    df1 = df1.rename(columns={
        'jumia_price': 'price',
        'jumia_oldPrice': 'oldPrice',
        'jumia_discount': 'discount',
        'jumia_verifiedRatings': 'verifiedRatings',
        'jumia_stock': 'stock',
        'jumia_rating': 'rating'
    })
    df1['jumia_productLink'] = default_link
    return df1


class ConvertDfToSQL:
    def __init__(self):
        self.user = 'postgres'
        self.password = '1234'
        self.host = 'localhost'
        self.port = '1234'
        self.db_name = 'fairpriceke'

        # Create the initial engine to connect to the PostgreSQL server
        self.engine = create_engine(
            f'postgresql+psycopg://{self.user}:{self.password}@{self.host}:{self.port}/postgres')
        self.create_database()

    def create_database(self):
        try:
            # Use AUTOCOMMIT to avoid transaction block issues
            with self.engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
                conn.execute(text(f"CREATE DATABASE {self.db_name} WITH OWNER = {
                             self.user} ENCODING = 'UTF8' CONNECTION LIMIT = -1"))
            print(f"Database {self.db_name} created successfully.")

            # Reconfigure the engine to connect to the newly created database
            self.engine = create_engine(
                f'postgresql+psycopg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}')
        except sqlalchemy.exc.SQLAlchemyError as e:
            print(f"Error creating database: {e}")

    def convert(self, df: pd.DataFrame, table_name: str, mode='replace'):
        try:
            df.to_sql(table_name, con=self.engine, if_exists=mode, index=False)
            print(f"Data inserted into table {table_name}")
        except sqlalchemy.exc.SQLAlchemyError as e:
            print(f"Error inserting data into table {table_name}: {e}")

    def append_to_history(self, df: pd.DataFrame, history_table_name: str):
        try:
            df.to_sql(history_table_name, con=self.engine,
                      if_exists='append', index=False)
            print(f"Data appended to history table {history_table_name}")
        except sqlalchemy.exc.SQLAlchemyError as e:
            print(f"Error appending data to history table {
                  history_table_name}: {e}")

    def run(self):
        # Get data from PhonePlaceKenya and clean it
        # ppk = PhonePlaceKenyaScraping()
        # df = ppk.run()
        # ppk_clean = PhoneKenyaDataCleaner(df)
        # df_cleaned = ppk_clean.clean_data()
        df_cleaned = pd.read_csv(
            r"D:\freelance\FairPriceKe-add_llm\FairPriceKe\FairPriceKe\data\Phone Place Kenya Scraping\cleaned\phone_place_kenya.csv")

        # Insert cleaned PhonePlaceKenya data
        self.convert(df_cleaned, 'phoneplacekenya', mode='replace')
        self.append_to_history(df_cleaned, 'phoneplacekenya_history')

        # Load and clean Jumia data
        jumia_data = os.path.join(
            'data', 'Jumia', 'row', 'today_jumia_data.json')
        cleaner = JumiaDataCleaner(jumia_data)
        cleaned_df = cleaner.get_cleaned_data()
        cleaned_df.Key_Features = cleaned_df.Key_Features.apply(
            lambda x: json.dumps(x))
        cleaned_df.stock = cleaned_df.stock.apply(lambda x: json.dumps(x))
        print(cleaned_df.info())
        print(cleaned_df)

        # Insert cleaned Jumia data
        self.convert(cleaned_df, 'jumia', mode='replace')
        self.append_to_history(cleaned_df, 'jumia_history')


if __name__ == "__main__":
    x = ConvertDfToSQL()
    x.run()
