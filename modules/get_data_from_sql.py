import os
import re
import random
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_core.output_parsers import StrOutputParser
from sqlalchemy import text
import pandas as pd
from .get_tables_details import GetTablesDetails
# from dotenv import load_dotenv


class GetDataFromSQL:
    """
    Class to handle SQL query generation and execution using Google Generative AI models.
    """

    def __init__(self, llm, verbose=1):
        self.llm = llm
        self.verbose = verbose
        self.get_tabels_details = GetTablesDetails()
        self.prompt_template = """
                
                You are part of a system designed to work as a shopping assistant specializing in helping users find the best deals on products from Kenyan e-commerce platforms. In this system, you are an expert in PostgreSQL and database querying. Your main task is to generate SQL queries based on user questions and the database schema, with tables and structures available.

                ### You have two tables in your database:
                1. **Jumia Table**
                2. **PhonePlaceKenya Table**

                #### Jumia Table:
                - **Structure**:
                {jumia_table_structure}

                - **Category and Brand in Jumia Table**:
             
                {jumia_table_details}
              
                - **Sample Rows**:
          
                timestamp	productName	Brand	jumia_productUrl	price	oldPrice	discount	rating	verifiedRatings	stock	Key_Features	Category
                0	2024-10-03 20:35:39	Samsung Galaxy A05	Samsung	https://www.jumia.co.ke/...	11560.0	12500.0	8.0	4.3 out of 5	(51 verified ratings)	["inStock": true, "stockStatus": "87 items lef...	["Display:\u00a06.7\"\u00a0PLS LCD": true, "Re...	Smartphone
                1	2024-10-03 20:35:39	Samsung Galaxy A05	Samsung	https://www.jumia.co.ke/...	12930.0	14000.0	8.0	4.7 out of 5	(7 verified ratings)	["inStock": true, "stockStatus": "In stock", "...	["6.7 inches IPS LCD display": true, "Qualcomm...	Smartphone
             

                #### PhonePlaceKenya Table:
                - **Structure**:
                {phoneplacekenya_table_structure}

                - **Category and Brand in PhonePlaceKenya Table**:
                {phoneplacekenya_table_details}

                - **Sample Rows**:
                timestamp	productName	Brand	PhonePlaceKenya_productLink	price	oldPrice	discount	verifiedRatings	stock	Key_Features	Category
                0	2024-10-12 18:35:57	Nokia C22	Nokia	https://www.phoneplacekenya.com/product/nokia-...	17500.0	18000.0	2.78	0	IN STOCK	["RAM": "4GB", "Storage": "128GB", "Battery": ...]	Nokia Phones
                1	2024-10-12 18:36:06	Nokia C32	Nokia	https://www.phoneplacekenya.com/product/nokia-...	18300.0	18500.0	1.08	0	IN STOCK	["RAM": ", 4GB", "Storage": "64GB,", "Battery"...]	Nokia Phones
                2	2024-10-12 18:36:16	Nokia T21	Nokia	https://www.phoneplacekenya.com/product/nokia-...	28500.0	38500.0	25.97	0	IN STOCK	["RAM": "4GB", "Storage": "64 GB / 128GB", "Ba...]	Nokia Phones

                ### Important Points:
                1. **Filter** tables by **Brand** and **Category** each time. If the user enters an incorrect Brand or Category, correct it for the query.
                2. **Do not merge** the two tables.
                3. Only filter by **Brand** and **Category**, not `productName`.
                4. Always select the following columns: `productName`, `LINK`, `price`, `oldPrice`, `discount`, `rating`, `verifiedRatings`, `stock`, `Key_Features` from each table.
                5. **Do not use** `LIMIT` in queries.
                6. **Return the query only**, using `UNION ALL` to combine the two tables.
                7. When searching for a Category in one table, perform the same search in the other for fair comparison.
                8. If the query includes multiple Brands or Categories, filter both tables accordingly.


                ### Example Query Format:
                ```sql
                SELECT
                    productName,
                    jumia_productLink AS LINK,
                    price,
                    oldPrice,
                    discount,
                    rating,
                    verifiedRatings,
                    stock,
                    Key_Features
                FROM jumia
                WHERE
                    (Brand = 'Oppo' AND Category = 'Smart Phones') OR (Brand = 'Tecno' AND Category = 'Smart Phones')

                UNION ALL

                SELECT
                    productName,
                    PhonePlaceKenya_productLink AS LINK,
                    price,
                    oldPrice,
                    discount,
                    rating,
                    verifiedRatings,
                    stock,
                    Key_Features
                FROM phoneplacekenya
                WHERE
                    (Brand = 'Oppo' AND Category = 'Oppo') OR (Brand = 'Samsung' AND Category = 'Samsung Phones')
                ```


                **Note**: Avoid using `ORDER BY` in each SELECT statement in the `UNION ALL` operation; apply `ORDER BY` only after combining the results.


                USER QUESTION: {question}

        """

    def prepare(self):
        """
        Prepare the prompts and chains 
        """

        # Set up the prompt for SQL query generation
        model_1_prompt_template = PromptTemplate(
            input_variables=['jumia_table_structure', 'jumia_table_details',
                             'phoneplacekenya_table_details', 'phoneplacekenya_table_structure', 'question'],
            template=self.prompt_template
        )
        self.generate_sql_chain = LLMChain(
            llm=self.llm,
            prompt=model_1_prompt_template,
            output_parser=StrOutputParser()
        )

        print(f"Prepared prompts done")

    def extract_query(self, query_text):
        """
        Extract all SQL queries from the generated query text.

        Args:
        - query_text: The text generated by the LLM containing SQL queries.

        Returns:
        - A list of extracted SQL queries or None if no matches found.
        """
        pattern = r"```sql\s*(.*?)\s*```"
        matches = re.findall(pattern, query_text.strip(), re.DOTALL)
        return matches if matches else None

    def run(self, user_question):
        """
        Executes the full pipeline: generates SQL queries, runs each query on the MySQL database,
        and returns the final result for each query.

        Args:
        - user_question: The question from the user.

        Returns:
        - The final answer generated by the LLM and the results of the executed queries.
        """
        # Step 1: Create a database session
        con = self.get_tabels_details.create_chatbot_database_session()

        # Analyze Jumia table
        jumia_table_structure, jumia_table_details = self.get_tabels_details.analyze_jumia_table()

        # Get Phone Place Kenya data
        phoneplacekenya_table_structure, phoneplacekenya_table_details = self.get_tabels_details.get_phone_place_kenya_data()

        query_text = self.generate_sql_chain.run(
            {'jumia_table_structure': jumia_table_structure,
             'jumia_table_details': jumia_table_details,
             'phoneplacekenya_table_structure': phoneplacekenya_table_structure,
             'phoneplacekenya_table_details': phoneplacekenya_table_details,
             'question': user_question}
        )

        print("Generated Query Text:")
        print(query_text)

        # Step 3: Extract all SQL queries
        queries = self.extract_query(query_text)
        if not queries:
            raise ValueError(
                "No valid SQL queries could be extracted from the LLM output.")

        if self.verbose:
            print(f"Extracted {len(queries)} SQL queries: {queries}")

        sql_execution_results = []  # To store results of each query

        # Step 4: Execute each query and collect results
        try:
            for query in queries:
                try:
                    # query=query.replace('\n', ' ')
                    if self.verbose:
                        print(f"Executing query: {query}")
                    response = con.execute(text(query))  # Execute the query
                    result = response.fetchall()  # Fetch the results
                    sql_execution_results.append(result)  # Store the result

                except Exception as e:
                    self.get_tabels_details.try_to_close_connection()
                    print(f"Error executing query: {e}")
                    # Append None if an error occurs
                    sql_execution_results.append(None)

                print(f"Database response: {sql_execution_results}")

        finally:
            self.get_tabels_details.try_to_close_connection()

        return sql_execution_results, queries


# Usage Example
if __name__ == "__main__":
    # Initialize LLM with a Google API key
    # load_dotenv()
    genini_key = os.getenv("GEMINI_KEY")

    llm = GoogleGenerativeAI(
        model='gemini-1.5-flash-latest',
        google_api_key=genini_key)

    get_data_from_sql = GetDataFromSQL(llm, verbose=1)

    # Prepare the prompts for a specific file type (example: "P&L")
    get_data_from_sql.prepare()

    # Example user question and database structures
    user_question = 'Which platform has the lowest price for iphone 15-pro right now?'

    # Run the pipeline and get the final answer
    sql_execution_results, queries = get_data_from_sql.run(user_question)
    print("sql_execution_results:")
    print(sql_execution_results)
    print("*" * 50)
    print("queries:")
    print(queries)
