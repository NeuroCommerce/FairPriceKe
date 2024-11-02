import sqlalchemy
from sqlalchemy import text, inspect
from sqlalchemy.orm import sessionmaker
import psycopg  # Adjusted for compatibility with SQLAlchemy
import pandas as pd
from sqlalchemy import text


class GetTablesDetails:
    def __init__(self):
        self.user = 'postgres'
        self.password = '1234'
        self.host = 'localhost'
        self.db_name = 'fairpriceke'
        self.port = '1234'  # Ensure the port is correctly specified

        # Check and create the database if it does not exist
        self.check_and_create_database()

        # Create an engine now pointing to the specific database
        self.engine = sqlalchemy.create_engine(
            f'postgresql+psycopg://{self.user}:{self.password}@{
                self.host}:{self.port}/{self.db_name}'
        )
        # self.rename_column()
        self.chatbot_Session = sessionmaker(bind=self.engine)

    # Function to rename the column in the table

    def check_and_create_database(self):
        # Connect to the default database to check for `fairpriceke`
        conn = psycopg.connect(
            dbname="postgres", user=self.user, password=self.password, host=self.host, port=self.port
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # Check if the database exists
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{
                       self.db_name}';")
        exists = cursor.fetchone()

        if not exists:
            # Database does not exist, so create it
            cursor.execute(
                f"CREATE DATABASE {self.db_name} "
                "WITH OWNER = postgres ENCODING = 'UTF8' CONNECTION LIMIT = -1;"
            )
            print(f"Database '{self.db_name}' created successfully.")
        else:
            print(f"Database '{self.db_name}' already exists.")

        cursor.close()
        conn.close()

    def create_chatbot_database_session(self):
        session = self.chatbot_Session()
        return session

    def analyze_jumia_table(self):
        connection = self.engine.connect()
        try:
            inspector = inspect(self.engine)
            table_name = 'jumia'
            columns = inspector.get_columns(table_name)

            # Structure output
            table_structure = "jumia Table Structure:\n"
            for col in columns:
                table_structure += f"{col['name']}: {col['type']}\n"

            query_product_name = """
            SELECT 
            "Category", 
            STRING_AGG(DISTINCT "Brand", ', ' ORDER BY "Brand") AS Brand
            FROM 
            jumia
            GROUP BY 
            "Category"
            ORDER BY 
            "Category";

            """
            data = pd.read_sql(text(query_product_name), connection)

            result = ""
            for category, terms in data.itertuples(index=False):
                terms_list = terms.split(", ")
                result += f"Category {category} includes:\n"
                for term in terms_list:
                    result += f"    - {term}\n"
                result += "\n"

            return table_structure, result

        finally:
            connection.close()

    def get_phone_place_kenya_data(self):
        connection = self.engine.connect()
        try:
            inspector = inspect(self.engine)
            table_name = 'phoneplacekenya'
            columns = inspector.get_columns(table_name)

            table_structure = "phoneplacekenya Table Structure:\n"
            for col in columns:
                table_structure += f"{col['name']}: {col['type']}\n"

            query_product_name = """
            SELECT 
                "Category", 
                STRING_AGG(DISTINCT "Brand", ', ' ORDER BY "Brand") AS Brand
            FROM 
                phoneplacekenya
            GROUP BY 
                "Category"
            ORDER BY 
                "Category";

            """
            data = pd.read_sql(text(query_product_name), connection)

            result = ""
            for category, terms in data.itertuples(index=False):
                terms_list = terms.split(", ")
                result += f"Category {category} includes:\n"
                for term in terms_list:
                    result += f"    - {term}\n"
                result += "\n"

            return table_structure, result

        finally:
            connection.close()

    def try_to_close_connection(self):
        """Close the database connection if it's open."""
        if self.engine:
            self.engine.dispose()
            print("Database connection closed.")


if __name__ == "__main__":
    obj = GetTablesDetails()

    jumia_table_report, df_product_name = obj.analyze_jumia_table()
    print('Jumia Table Report:\n', jumia_table_report)
    print(df_product_name)

    phone_place_kenya_data, res = obj.get_phone_place_kenya_data()
    print('PhonePlaceKenya Table Structure:\n', phone_place_kenya_data)
    print(res)
