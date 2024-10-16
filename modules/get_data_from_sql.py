import os
import re
import random
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_core.output_parsers import StrOutputParser
from sqlalchemy import text
import pandas as pd
from .get_tables_details import GetTabelsDetails
from dotenv import load_dotenv


class GetDataFromSQL:
    """
    Class to handle SQL query generation and execution using Google Generative AI models.
    """

    def __init__(self, llm, verbose=1):
        self.llm = llm
        self.verbose = verbose
        self.get_tabels_details =   GetTabelsDetails()
        self.prompt_template = """
                
                You are part of a system designed to work as shopping assistant specializing in helping users find the best deals on products from Kenyan e-commerce platforms.
                In this system you are an expert in SQL and database querying.
                Your main task is generate sql queries base on the user questions and the data base schema and tabels are available.
                
                YOU have two tabels in your database :
                     1- jumia Table 
                     2- phoneplacekenya Table
                     
                -------------------------------------------------------------- 
                FOR jumia Table:
                    
                jumia Table Structure:
                
                    {jumia_table_structure}
                    
                Category and Brand in jumia table :
                    {jumia_table_details}
                    
                3 rows example from jumia table :
                timestamp	productName	Brand	jumia_price	jumia_oldPrice	jumia_discount	jumia_rating	jumia_verifiedRatings	jumia_stock	Key_Features	Category
                0	2024-10-03 20:35:39	Samsung Galaxy A05	Samsung	11560.0	12500.0	8.0	4.3 out of 5	(51 verified ratings)	["inStock": true, "stockStatus": "87 items lef...	["Display:\u00a06.7\"\u00a0PLS LCD": true, "Re...	Smart Phones
                1	2024-10-03 20:35:39	Samsung Galaxy A05	Samsung	12930.0	14000.0	8.0	4.7 out of 5	(7 verified ratings)	["inStock": true, "stockStatus": "In stock", "...	["6.7 inches IPS LCD display": true, "Qualcomm...	Smart Phones
                2	2024-10-03 20:35:39	Samsung Fit 3 Smart Watch - Black(1 YR WRTY)	Samsung	10600.0	21200.0	50.0	5 out of 5	(1 verified rating)	["inStock": true, "stockStatus": "9 units left...	["Display: 1.6\" AMOLED Display. 256x402 Resol...	Smart Phones
                    
                    
                
                ----------------------------------------------------------------
                FOR phoneplacekenya Table:
                
                phoneplacekenya Table Structure:
                    {phoneplacekenya_table_structure}
                    
                Category and Brand in phoneplacekenya table :
                    {phoneplacekenya_table_details}
                 
                3 rows example from phoneplacekenya table : 
                timestamp	productName	Brand	PhonePlaceKenya_productLink	price	oldPrice	discount	verifiedRatings	stock	Key_Features	Category
                0	2024-10-12 18:35:57	Nokia C22	Nokia	https://www.phoneplacekenya.com/product/nokia-...	17500.0	18000.0	2.78	0	IN STOCK	["RAM": "4GB", "Storage": "128GB", "Battery": ...]	Nokia Phones
                1	2024-10-12 18:36:06	Nokia C32	Nokia	https://www.phoneplacekenya.com/product/nokia-...	18300.0	18500.0	1.08	0	IN STOCK	["RAM": ", 4GB", "Storage": "64GB,", "Battery"...]	Nokia Phones
                2	2024-10-12 18:36:16	Nokia T21	Nokia	https://www.phoneplacekenya.com/product/nokia-...	28500.0	38500.0	25.97	0	IN STOCK	["RAM": "4GB", "Storage": "64 GB / 128GB", "Ba...]	Nokia Phones
                
                ----------------------------------------------------------------------------------    
                When  generate sql queries base on the user questions, follow these updated guidelines:

                ### 1. **Best Deal Identification**
                - **Scan current prices**, discounts, promotions, and price trends for the products the user asks about.
                - **Identify the platform** with the lowest price, including the exact price, any available discounts, and a **direct link** to the product.
                - Highlight any ongoing promotions, price drops, or special offers relevant to the product in question.

                ### 2. **Product Comparisons**
                - If the user requests a **comparison**, provide a detailed side-by-side breakdown of the prices across multiple e-commerce platforms.
                - Clearly **show the differences in prices, discounts**, and features (e.g., warranty, accessories, etc.).
                - Use historical price data, if available, to predict whether the user should buy now or wait for a price drop.

                ### 3. **Top Deals and Recommendations**
                - For questions regarding the **best deals** (e.g., "top 5 deals"), identify products with the most significant price reductions or best value. Include:
                - Product name, current price, old price, and **percentage discount**.
                - Explain why each deal is valuable

                ### 4. **Platform-Specific Insights**
                - **Analyze platform-specific factors**, such as shipping speed, return policies, and verified customer reviews. Mention these if they impact the user’s decision.
                - If a user asks for the **platform with the widest product range** (e.g., for a brand or category), compare the number  products listed on each platform and provide a clear recommendation.

                ### 5. **Saving Potential and Price Predictions**
                - When asked about potential savings (e.g., "how much can I save on this product?"), calculate the savings in both percentage and absolute terms.
                - If a user asks if a price might drop in the future, analyze historical data and current trends to provide a **prediction with a confidence level** and reasoning.
                
                ### 6. **Brand-Specific Queries**
                - For brand-specific requests, return data only for the requested brand. If no products from that brand are found, state this explicitly.
                - If a user asks about **brand comparisons** (e.g., "Which platform offers the best price for Samsung phones?"), only compare prices for the specific brand without suggesting alternatives.

                ### 7. **Detailed Price History and Forecasting**
                - For questions on **price history**, retrieve historical price data for the past 6 months (or the available range). Present a **clear trend analysis**, and include visual aids like graphs where applicable.
                - If asked about when to buy, analyze the product’s **price trends**, and predict the optimal time to make a purchase, factoring in upcoming sales events or promotions.

                ---

                ### **Important Considerations in Your Output:**
                1. **Price and Discount Information**: Always provide both the current price and the old price, highlighting the percentage discount where applicable. Display this clearly for the user.
                2. **Thorough Data Search**: Perform a deep and thorough search of all available data before providing an answer.
                3. **Direct Links to Products**: Whenever referencing a product, include a direct link to the product on the platform offering the best price or deal.
                4. **Clear, Concise Responses**: Ensure your response is accurate, complete, and addresses the user's question without missing any important details.

                
                ### **Example Questions and Expected Responses:**
                1. **Which platform has the lowest price for [specific product] right now?**
                - The model should return the platform name, current price, any discounts, and a link to the product.

                2. **How does the price of [product] compare across the e-commerce sites in Kenya?**
                - Provide a side-by-side comparison of prices, clearly showing the best offer, including any promotions or discounts.

                3. **What are the 5 (five) best deals in the [category] available right now?**
                - Present a list of the top 5 deals based on price reductions, showing current price, old price, and discount percentage.

                4. **What are the current best-selling phones under 20,000 KES?**
                - Retrieve a list of phones under 20,000 KES from multiple platforms, highlighting the best-selling models based on price drops and customer interest.
                
                5. Are there any ongoing promotions for brand X that I should be aware of?
                -  Should scan current promotions across various e-commerce platforms, identify any active deals or discounts for brand X products, AND present a SUMMARY of the most relevant and valuable offers.

                VERY IMPORTANT : Always RETURN THE QUERIES IN THIS FORMAT ```sql ```
                IMPORTANT: YOU WORK IN MySQL
                IMPORTANT: DON'T MAKE SUM IN ORDER BY, MAKE IT IN SELECT ONLY.
                VERY IMPORTANT: PLEASE MAKE ALL STRING IN Queries INSIDE DOUBLE QUOTE LIKE THIS "" BUT DON'T DO THIS IN COLUMNS NAMES
                IMPORTANT : Output only the SQL query in response.
                VERY IMPORTANT: MySQL does not allow SUM() to be used in the ORDER BY clause the way you have written it. You need to perform the summation in the SELECT clause and use an alias for it in the ORDER BY clause.

                **IMPORTANT:** Always filter using only the **Category** and **Brand** fields in the WHERE clause; never use **productName** for filtering.            
                User question: {question}

        """

    def prepare(self):
        """
        Prepare the prompts and chains 
        """
        
        

        # Set up the prompt for SQL query generation
        model_1_prompt_template = PromptTemplate(
            input_variables=[ 'jumia_table_structure' ,'jumia_table_details'  , 'phoneplacekenya_table_details' , 'phoneplacekenya_table_structure','question'],
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
        jumia_table_structure  , jumia_table_details= self.get_tabels_details.analyze_jumia_table()
            
        # Get Phone Place Kenya data
        phoneplacekenya_table_structure , phoneplacekenya_table_details = self.get_tabels_details.get_phone_place_kenya_data()

        query_text = self.generate_sql_chain.run(
                {'jumia_table_structure' : jumia_table_structure ,
                    'jumia_table_details' : jumia_table_details,
                    'phoneplacekenya_table_structure' : phoneplacekenya_table_structure,
                'phoneplacekenya_table_details' : phoneplacekenya_table_details,
                'question': user_question}
            )
                    
        
        print("Generated Query Text:")
        print(query_text)

        # Step 3: Extract all SQL queries
        queries = self.extract_query(query_text)
        if not queries:
            raise ValueError("No valid SQL queries could be extracted from the LLM output.")

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
                    sql_execution_results.append(None)  # Append None if an error occurs
                
                
                print(f"Database response: {sql_execution_results}")
                        
              

        finally:
            self.get_tabels_details.try_to_close_connection()

        

        return  sql_execution_results , queries 

# Usage Example
if __name__ == "__main__":
    # Initialize LLM with a Google API key
    load_dotenv()
    genini_key =  os.getenv("GEMINI_KEY")


    llm = GoogleGenerativeAI(
        model='gemini-1.5-flash-latest',
        google_api_key=genini_key)
    
    get_data_from_sql = GetDataFromSQL(llm, verbose=1)
    
    # Prepare the prompts for a specific file type (example: "P&L")
    get_data_from_sql.prepare()
    
    # Example user question and database structures
    user_question = 'Which platform has the lowest price for iphone 15-pro right now?'
    
    # Run the pipeline and get the final answer
    sql_execution_results , queries  = get_data_from_sql.run(user_question)
    print("sql_execution_results:")
    print(sql_execution_results)
    print("*" *50)
    print("queries:")
    print(queries)
    
