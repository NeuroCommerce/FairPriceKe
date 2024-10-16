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
from .get_data_from_sql import GetDataFromSQL



class Responsewrapper:
    """
    Class to handle SQL query generation and execution using Google Generative AI models.
    """

    def __init__(self, llm, verbose=1):
        self.llm = llm
        self.verbose = verbose
        self.prompt_template = """
                
                You are a smart shopping assistant helping users find the best deals on products from Kenyan e-commerce platforms.

                When answer the user questions, follow these updated guidelines:

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

        Below are the original SQL queries generated based on the user's question, as well as the results from executing those queries.

        ### Original User Question:
        {question}

        ### SQL Queries:
        {queries}

        ### SQL Execution Results:
        {sql_execution_results}

        Based on the queries and results, provide a detailed response to the user in human language that answers the original question. Make sure the response is clear and helpful, including any relevant details like prices, discounts, product names, or recommendations.

        Your response:
        """

    def prepare(self):
        """
        Prepare the prompts and chains .
        
      
        """
        
        # Create the prompt template for final response generation
        final_response_template = PromptTemplate(
            input_variables=['question', 'queries', 'sql_execution_results'],
            template=self.prompt_template
        )

        # Create the LLMChain for generating the final response
        self.final_response_chain = LLMChain(
            llm=self.llm,  # Using the same LLM instance
            prompt=final_response_template
        )
        

        print(f"Prepared Response Wrapper prompts done")

    

    def run(self, user_question , queries , sql_execution_results):
        """
        Executes the full pipeline: generates SQL queries, runs each query on the MySQL database,
        and returns the final result for each query.
        
        Args:
        - user_question: The question from the user.
        
        Returns:
        - The final answer generated by the LLM and the results of the executed queries.
        """
       


        # Run the final response generation
        final_response = self.final_response_chain.run({
            'question': user_question,
            'queries': queries,
            'sql_execution_results': sql_execution_results
        })

        print(f"Final Response:\n{final_response}")

        

        return  final_response

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
    user_question = 'What is the best deal for today'
    
    # Run the pipeline and get the final answer
    sql_execution_results , queries  = get_data_from_sql.run(user_question)
    print("sql_execution_results:")
    print(sql_execution_results)
    print("*" *50)
    print("queries:")
    print(queries)
    
    response_wrapper = Responsewrapper(llm , verbose=1)
    response_wrapper.prepare()
    res =  response_wrapper.run(user_question , queries , sql_execution_results)
    
    print(res)
    
    
