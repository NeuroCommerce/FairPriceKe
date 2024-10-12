# import pandas as pd
# import sqlalchemy
# from sqlalchemy import text  # Import text for executing raw SQL
# from get_jumia_data_from_api import *
# from phone_place_kenya_scraping import PhonePlaceKenyaScraping
# from clean_phone_place_kenya import PhoneKenyaDataCleaner


# class ConvertDfToSQL:
#     def __init__(self, user, password, host, db_name):
#         self.user = user
#         self.password = password
#         self.host = host
#         self.db_name = db_name

#         # Create engine without specifying the database to create it if necessary
#         self.engine = sqlalchemy.create_engine(
#             f'mysql+pymysql://{user}:{password}@{host}')
#         self.create_database()

#     def create_database(self):
#         # Create the database if it doesn't exist
#         with self.engine.connect() as conn:
#             # Use text() for raw SQL
#             conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {self.db_name}"))
#             conn.execute(text(f"USE {self.db_name}"))  # Use text() for raw SQL

#         # Update the engine to connect to the new database
#         self.engine = sqlalchemy.create_engine(
#             f'mysql+pymysql://{self.user}:{self.password}@{self.host}/{self.db_name}')

#     def convert(self, df: pd.DataFrame, table_name: str):
#         # Create table and insert data
#         df.to_sql(table_name, con=self.engine,
#                   if_exists='replace', index=False)


# # Example usage
# if __name__ == "__main__":
#     # database info
#     user = 'root'
#     password = '1234'
#     host = 'localhost'
#     db_name = 'FAIRPRICEKE'
#     s = PhonePlaceKenyaScraping()
#     df = s.run()
#     sc = PhoneKenyaDataCleaner(df)
#     df_cleaned = sc.clean_data()
#     print(df_cleaned.info())
#     # Convert DataFrame to SQL table and create the database if it doesn't exist
#     converter = ConvertDfToSQL(
#         user='root', password='1234', host=host, db_name=db_name)
#     converter.convert(df_cleaned, 'PhonePlaceKenya')
import pandas as pd
import sqlalchemy
from sqlalchemy import text  # Import text for executing raw SQL
from get_jumia_data_from_api import *
from phone_place_kenya_scraping import PhonePlaceKenyaScraping
from clean_phone_place_kenya import PhoneKenyaDataCleaner
from get_jumia_data_from_api import run_scraper
from clean_jumia_data import JumiaDataCleaner
from sqlalchemy import create_engine, inspect


class ConvertDfToSQL:
    def __init__(self, user, password, host, db_name):
        self.user = user
        self.password = password
        self.host = host
        self.db_name = db_name

        # Create engine without specifying the database to create it if necessary
        self.engine = sqlalchemy.create_engine(
            f'mysql+pymysql://{user}:{password}@{host}')
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

    def analyze_jumia_table(self):
        # Create a connection to the database
        engine = sqlalchemy.create_engine(
            f'mysql+pymysql://{user}:{password}@{host}/{db_name}')
        connection = engine.connect()

        try:
            # 1. Get table structure using SQLAlchemy's inspector
            inspector = inspect(engine)
            table_name = 'jumia'
            columns = inspector.get_columns(table_name)

            # Create a formatted string representing the table structure
            table_structure = "Table Structure:\n"
            for col in columns:
                table_structure += f"{col['name']}: {col['type']}\n"

            # 2. Get unique values for 'productName'
            query_product_name = f"SELECT DISTINCT productName FROM fairpriceke.{table_name};"
            df_product_name = pd.read_sql(text(query_product_name), connection)
            product_name_values = f"\nUnique values in 'productName':\n"
            product_name_values += ', '.join(
                df_product_name['productName'].dropna().tolist())

            # 3. Get unique values for 'Brand'
            query_brand = f"SELECT DISTINCT Brand FROM fairpriceke.{table_name}"
            df_brand = pd.read_sql(text(query_brand), connection)
            brand_values = f"\nUnique values in 'Brand':\n"
            brand_values += ', '.join(df_brand['Brand'].dropna().tolist())

            # 4. Combine table structure and unique values into one text
            full_report = table_structure + product_name_values + "\n" + brand_values
            return full_report

        finally:
            # Close the connection after processing
            connection.close()

    def get_phone_place_kenya_data(user, password, host, db_name):
        # Create engine to connect to the MySQL database
        engine = sqlalchemy.create_engine(
            f'mysql+pymysql://{user}:{password}@{host}/{db_name}')

        # Open a connection to the database
        with engine.connect() as con:
            # Query to get data grouped by Brand and Category, and concatenate productName, price, and other details
            query = f"""
            SELECT Brand, Category, 
                GROUP_CONCAT(productName ORDER BY productName SEPARATOR ', ') AS products,
                GROUP_CONCAT(price ORDER BY productName SEPARATOR ', ') AS prices,
                GROUP_CONCAT(oldPrice ORDER BY productName SEPARATOR ', ') AS old_prices,
                GROUP_CONCAT(discount ORDER BY productName SEPARATOR ', ') AS discounts,
                GROUP_CONCAT(verifiedRatings ORDER BY productName SEPARATOR ', ') AS ratings
            FROM phoneplacekenya
            GROUP BY Brand, Category
            ORDER BY Brand, Category;
            """

            # Execute the query
            res = con.execute(text(query))
            data = res.fetchall()

        # Format the data as requested
        result = ""
        for row in data:
            brand, category, products, prices, old_prices, discounts, ratings = row

            product_list = products.split(", ")
            price_list = prices.split(", ")
            old_price_list = old_prices.split(", ")
            discount_list = discounts.split(", ")
            rating_list = ratings.split(", ")

            result += f"Brand: {brand} | Category: {category}\n"
            for i in range(len(product_list)):
                result += f"    - Product: {product_list[i]}\n"
                result += f"      Price: {price_list[i]}\n"
                result += f"      Old Price: {old_price_list[i]}\n"
                result += f"      Discount: {discount_list[i]}%\n"
                result += f"      Verified Ratings: {rating_list[i]}\n"
            result += "\n"  # Add a newline between brand and category groups

        return result.strip()

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
            r'D:\freelance\FairPriceKe-add_llm\FairPriceKe\FairPriceKe\data\Jumia\2024-10-03_all_brands_products.json')
        # Get the cleaned DataFrame
        cleaned_df = cleaner.get_cleaned_data()
        cleaned_df.Key_Features = cleaned_df.Key_Features.apply(
            lambda x: json.dumps(x))
        cleaned_df.jumia_stock = cleaned_df.jumia_stock.apply(
            lambda x: json.dumps(x))

        converter = ConvertDfToSQL(
            user=user, password=password, host=host, db_name=db_name)
        converter.convert(cleaned_df, 'jumia'.lower())


# Example usage
if __name__ == "__main__":
    # database info
    user = 'root'
    password = '1234'
    host = 'localhost'
    db_name = 'FAIRPRICEKE'.lower()
    x = ConvertDfToSQL(user, password, host, db_name)
    x.run()
    print(x.analyze_jumia_table())
