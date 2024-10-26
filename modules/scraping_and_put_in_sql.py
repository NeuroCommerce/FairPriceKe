import pandas as pd
import sqlalchemy
from sqlalchemy import text  # Import text for executing raw SQL
from get_jumia_phones_data import *
from get_phones_kenya_data import PhonePlaceKenyaScraping
from clean_phone_kenya_data import PhoneKenyaDataCleaner
from clean_jumia_data import JumiaDataCleaner
from sqlalchemy import create_engine, inspect


def standardize_dataframes(df1, default_link="https://www.jumia.co.ke/?gad_source=1&gclid=CjwKCAjwjsi4BhB5EiwAFAL0YO0ItBXwhDXa2-8ANqkP7xaIs-g5Z7l1Bn8te1d8g7qNUxXCJ-7D0xoCcvAQAvD_BwE"):
    # Step 1: Rename columns to match between df1 and df2
    df1 = df1.rename(columns={
        'jumia_price': 'price',
        'jumia_oldPrice': 'oldPrice',
        'jumia_discount': 'discount',
        'jumia_verifiedRatings': 'verifiedRatings',
        'jumia_stock': 'stock',
        'jumia_rating': 'rating'
    })

    # Step 2: Add PhonePlaceKenya_productLink to df1 with default value
    df1['jumia_productLink'] = default_link

    # Step 4: Return both standardized dataframes
    return df1


class ConvertDfToSQL:
    def __init__(self):
        self.user = 'root'
        self.password = 'mmm_321478910'
        self.host = 'localhost'
        self.db_name = 'FAIRPRICEKE'.lower()

        # Create engine without specifying the database to create it if necessary
        self.engine = sqlalchemy.create_engine(
            f'mysql+pymysql://{self.user}:{self.password}@{self.host}')
        self.create_database()

    def create_database(self):
        # Create the database if it doesn't exist
        try:
            with self.engine.connect() as conn:
                conn.execute(
                    text(f"CREATE DATABASE IF NOT EXISTS {self.db_name}"))
                conn.execute(text(f"USE {self.db_name}"))

            # Update the engine to connect to the new database
            self.engine = sqlalchemy.create_engine(
                f'mysql+pymysql://{self.user}:{self.password}@{self.host}/{self.db_name}')
        except sqlalchemy.exc.SQLAlchemyError as e:
            print(f"Error creating database: {e}")

    def convert(self, df: pd.DataFrame, table_name: str, mode='replace'):
        # Create table and insert data
        try:
            df.to_sql(table_name, con=self.engine, if_exists=mode, index=False)
            print(f"Data inserted into table {table_name}")
        except sqlalchemy.exc.SQLAlchemyError as e:
            print(f"Error inserting data into table {table_name}: {e}")

    def append_to_history(self, df: pd.DataFrame, history_table_name: str):
        # Append data to the history table
        try:
            df.to_sql(history_table_name, con=self.engine,
                      if_exists='append', index=False)
            print(f"Data appended to history table {history_table_name}")
        except sqlalchemy.exc.SQLAlchemyError as e:
            print(
                f"Error appending data to history table {history_table_name}: {e}")

    def run(self):
        # Scraping for PhonePlaceKenya
        ppk = PhonePlaceKenyaScraping()
        df = ppk.run()
        ppk_clean = PhoneKenyaDataCleaner(df)
        df_cleaned = ppk_clean.clean_data()

        # Replace old data in PhonePlaceKenya table and append to history
        self.convert(df_cleaned, 'PhonePlaceKenya'.lower(), mode='replace')
        self.append_to_history(df_cleaned, 'PhonePlaceKenya_history'.lower())

        #############################################################

        # Scraping and cleaning for Jumia
        cleaner = JumiaDataCleaner(
            r'D:\Projects\FairPriceKe\v2\FairPriceKe\data\Jumia\2024-10-25_string_products.json')
        cleaned_df = cleaner.get_cleaned_data()
        cleaned_df.Key_Features = cleaned_df.Key_Features.apply(
            lambda x: json.dumps(x))
        cleaned_df.stock = cleaned_df.stock.apply(
            lambda x: json.dumps(x))
        # cleaned_df = standardize_dataframes(cleaned_df)
        print(cleaned_df.info())
        print(cleaned_df)
        # Replace old data in jumia table and append to history
        self.convert(cleaned_df, 'jumia'.lower(), mode='replace')
        self.append_to_history(cleaned_df, 'jumia_history'.lower())


# Example usage
if __name__ == "__main__":
    x = ConvertDfToSQL()
    x.run()
