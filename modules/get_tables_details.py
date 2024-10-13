
import sqlalchemy
from sqlalchemy import text  # Import text for executing raw SQL
from sqlalchemy import create_engine, inspect

import pandas as pd


class GetTabelsDetails:
    def __init__(self):
        self.user = 'root'
        self.password = 'mmm_321478910'
        self.host = 'localhost'
        self.db_name = 'FAIRPRICEKE'.lower()
   
        # Create engine without specifying the database to create it if necessary
        self.engine = sqlalchemy.create_engine(
                f'mysql+pymysql://{self.user}:{self.password}@{self.host}/{self.db_name}'
                ) 
    def analyze_jumia_table(self):
        # # Create a connection to the database
        # engine = sqlalchemy.create_engine(
        #     f'mysql+pymysql://{self.user}:{self.password}@{self.host}/{self.db_name}')
       # Create a connection to the database
        connection = self.engine.connect()

        try:
            # 1. Get table structure using SQLAlchemy's inspector
            inspector = inspect(self.engine)
            table_name = 'jumia'
            columns = inspector.get_columns(table_name)

            # Create a formatted string representing the table structure
            table_structure = "jumia Table Structure:\n"
            for col in columns:
                table_structure += f"{col['name']}: {col['type']}\n"

            # 2. Get unique brand names grouped by category
            query_product_name = """
            SELECT Category, GROUP_CONCAT(DISTINCT Brand ORDER BY Brand SEPARATOR ', ') AS Brand
            FROM jumia
            GROUP BY Category
            ORDER BY Category;
            """

            # Execute the query and load data into a DataFrame
            data = pd.read_sql(text(query_product_name), connection)

            # Format the results in the specified format
            result = ""
            for category, terms in data.itertuples(index=False):
                terms_list = terms.split(", ")
                result += f"Category {category} includes:\n"
                for term in terms_list:
                    result += f"    - {term}\n"
                result += "\n"  # Add a newline between categories
                

            
            return table_structure , result

        finally:
            # Close the connection
            connection.close()


    def get_phone_place_kenya_data(self):
        # Create engine to connect to the MySQL database
        # engine = sqlalchemy.create_engine(
        #     f'mysql+pymysql://{self.user}:{self.password}@{self.host}/{self.db_name}')

        
        
        # Open a connection to the database
        connection = self.engine.connect()
        try:
            # Use SQLAlchemy inspector to get the table structure
            inspector = inspect(self.engine)
            table_name = 'phoneplacekenya'
            columns = inspector.get_columns(table_name)

            # Create a formatted string representing the table structure
            table_structure = "phoneplacekenya Table Structure:\n"
            for col in columns:
                table_structure += f"{col['name']}: {col['type']}\n"
                
            query_product_name = """
            SELECT Category, GROUP_CONCAT(DISTINCT Brand ORDER BY Brand SEPARATOR ', ') AS Brand
            FROM phoneplacekenya
            GROUP BY Category
            ORDER BY Category;
            """

            # Execute the query and load data into a DataFrame
            data = pd.read_sql(text(query_product_name), connection)

            # Format the results in the specified format
            result = ""
            for category, terms in data.itertuples(index=False):
                terms_list = terms.split(", ")
                result += f"Category {category} incloud:\n"
                for term in terms_list:
                    result += f"    - {term}\n"
                result += "\n"  # Add a newline between categories
            
            # Return the table structure
            return table_structure , result

        finally:
            # Close the connection after processing
            connection.close()
    

if __name__ == "__main__":
    # Create an instance of GetTabelsDetails class
    obj = GetTabelsDetails()
    
    # Analyze Jumia table
    jumia_table_report  , df_product_name= obj.analyze_jumia_table()
    print('jumia_table_report == ' , jumia_table_report)
    print( df_product_name)
    
    
    # Get Phone Place Kenya data
    phone_place_kenya_data , res = obj.get_phone_place_kenya_data()
    print( 'phone_place_kenya_data = ' ,phone_place_kenya_data)
    print( res)