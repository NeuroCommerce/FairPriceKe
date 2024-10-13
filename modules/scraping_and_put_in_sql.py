import pandas as pd
import sqlalchemy
from sqlalchemy import text  # Import text for executing raw SQL
from get_jumia_phones_data import *  
from get_phones_kenya_data import PhonePlaceKenyaScraping
from clean_phone_kenya_data import PhoneKenyaDataCleaner
from clean_jumia_data import JumiaDataCleaner
from sqlalchemy import create_engine, inspect


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
                # Use text() for raw SQL
                conn.execute(
                    text(f"CREATE DATABASE IF NOT EXISTS {self.db_name}"))
                # Use text() for raw SQL
                conn.execute(text(f"USE {self.db_name}"))

            # Update the engine to connect to the new database
            self.engine = sqlalchemy.create_engine(
                f'mysql+pymysql://{self.user}:{self.password}@{self.host}/{self.db_name}')
        except sqlalchemy.exc.SQLAlchemyError as e:
            print(f"Error creating database: {e}")
            
    def convert(self, df: pd.DataFrame, table_name: str):
        # Create table and insert data
        try:
            df.to_sql(table_name, con=self.engine,
                      if_exists='replace', index=False)
            print(f"Data inserted into table {table_name}")
        except sqlalchemy.exc.SQLAlchemyError as e:
            print(f"Error inserting data into table {table_name}: {e}")
            
    def run(self):
        ppk = PhonePlaceKenyaScraping()
        df = ppk.run()
        ppk_clean = PhoneKenyaDataCleaner(df)
        df_cleaned = ppk_clean.clean_data()
        # Convert DataFrame to SQL table and create the database if it doesn't exist
        converter = ConvertDfToSQL(
            user=self.user, password=self.password, host=self.host, db_name=self.db_name)
        converter.convert(df_cleaned, 'PhonePlaceKenya'.lower())

        #############################################################
        
        
        cleaner = JumiaDataCleaner(
            r'data\Jumia\2024-10-03_all_brands_products.json')
        # Get the cleaned DataFrame
        cleaned_df = cleaner.get_cleaned_data()
        cleaned_df.Key_Features = cleaned_df.Key_Features.apply(
            lambda x: json.dumps(x))
        cleaned_df.jumia_stock = cleaned_df.jumia_stock.apply(
            lambda x: json.dumps(x))

        converter = ConvertDfToSQL()
        converter.convert(cleaned_df, 'jumia'.lower())


# Example usage
if __name__ == "__main__":
    
    x = ConvertDfToSQL()
    x.run()
    # print(x.analyze_jumia_table())