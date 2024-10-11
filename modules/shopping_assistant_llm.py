from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from pydantic import BaseModel
import pandas as pd
import os
from dotenv import load_dotenv
from .clean_jumia_data import JumiaDataCleaner
from .clean_phone_place_kenya import PhoneKenyaDataCleaner


class ShoppingAssistant:
    def __init__(self, llm, verbose=0):
        """
        Initializes the ShoppingAssistant with an LLM model and verbosity level.

        :param llm: The LLM model to use
        :param verbose: Verbosity level (0 for silent, 1 for detailed logs)
        """
        self.llm = llm
        self.verbose = verbose
        self.prompt_template = """
                

                You are an expert shopping assistant specializing in helping users find the best deals on products from **Jumia** and **Phone Kenya** (or other relevant Kenyan e-commerce platforms).

                When responding to user questions, follow these updated guidelines:

                **You will receive JSON files for each platform. Your responses must be based on this data.**

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
                - If a user asks for the **platform with the widest product range** (e.g., for a brand or category), compare the number of unique products listed on each platform and provide a clear recommendation.

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

                ### **Description of the Data:**
                - **timestamp**: The date and time when the data entry was recorded.
                - **productName**: The name of the product being described.
                - **Brand**: The brand of the product (e.g., Samsung).
                - **price**: The current selling price of the product.
                - **oldPrice**: The previous price before discounts or changes.
                - **discount**: The percentage difference between the old and current price.
                - **verifiedRatings**: The number of verified customer ratings.
                - **stock**: The availability status (e.g., IN STOCK, SOLD OUT).
                - **Key_Features**: A dictionary of key features such as RAM, battery capacity, display size, and camera specifications.

                ---

                ### **Example Questions and Expected Responses:**
                1. **Which platform has the lowest price for [specific product] right now?**
                - The model should return the platform name, current price, any discounts, and a link to the product.

                2. **How does the price of [product] compare across the e-commerce sites in Kenya?**
                - Provide a side-by-side comparison of prices, clearly showing the best offer, including any promotions or discounts.

                3. **What are the 5 best deals in the [category] available right now?**
                - Present a list of the top 5 deals based on price reductions, showing current price, old price, and discount percentage.

                4. **What are the current best-selling phones under 20,000 KES?**
                - Retrieve a list of phones under 20,000 KES from multiple platforms, highlighting the best-selling models based on price drops and customer interest.

                User question: {question}  

                 JSON data from Jumia: {Jumia_data}  
                 JSON data from Phone Kenya: {Phone_Kenya_data}  

        """

    def prepare(self, question, Jumia_data, Phone_Kenya_data):
        """
        Prepares the question and product data for the LLM chain.

        :param question: The question the user wants to ask.
        :param product_data: The product data to be analyzed for the best deal.
        :return: Dictionary with 'question' and 'Product_data' keys.
        """
        if self.verbose:
            print("Preparing the inputs for the LLM chain...")
        return {'question': question, 'Jumia_data': Jumia_data, 'Phone_Kenya_data': Phone_Kenya_data}

    def run(self, question, Jumia_data, Phone_Kenya_data):
        """
        Runs the LLM chain with the prepared inputs.

        :param inputs: Dictionary containing the question and product data.
        :return: Response from the LLM model.
        """
        if self.verbose:
            print("Running the LLM chain...")

        inputs = self.prepare(question, Jumia_data, Phone_Kenya_data)
        print(inputs['Jumia_data'].info())

        prompt = PromptTemplate(
            input_variables=['question', 'Product_data'],
            template=self.prompt_template
        )
        chain = LLMChain(llm=self.llm, prompt=prompt)
        
        jumai_json = Jumia_data.to_json(orient='records', date_format='iso')
        Phone_Kenya_json =  Phone_Kenya_data.to_json(orient='records', date_format='iso')
        
        print('jumai_json data:', jumai_json[: 1000])
        
        print('*' * 50)
        print('Phone_Kenya_json data:', Phone_Kenya_json[: 1000] )

        
        

        return chain.run(question=question, Jumia_data= jumai_json, Phone_Kenya_data=Phone_Kenya_json)

    def test(self, question, Jumia_data, Phone_Kenya_data):
        """
        Test function to demonstrate the use of the assistant.

        :param question: The question to ask the assistant.
        :param product_data: The product data for analysis.
        :return: The result of running the LLM chain.
        """
        inputs = self.prepare(question, Jumia_data,  Phone_Kenya_data)
        result = self.run(inputs)
        if self.verbose:
            print(f"Test Result: {result}")
        return result


if __name__ == "__main__":
    load_dotenv()  # Load environment variables
    google_api_key = os.getenv("GEMINI_KEY")  # Load API key from environment
    llm = GoogleGenerativeAI(
        model="gemini-1.5-flash-latest", google_api_key=google_api_key, temperature=0)

    # Initialize the ShoppingAssistant with verbosity
    shopping_assistant = ShoppingAssistant(llm=llm, verbose=1)

    csv_file_path = r'D:\Projects\FairPriceKe\FairPriceKe\data\Phone Place Kenya Scraping\row\scraped_phones_with_datetime.csv'
    phone_k_cleaner = PhoneKenyaDataCleaner(csv_file_path)
    phone_k_df = phone_k_cleaner.clean_data()

    # Create an instance of the class
    jumai_cleaner = JumiaDataCleaner(
        r'D:\Projects\FairPriceKe\FairPriceKe\data\Jumia\2024-10-03_all_brands_products.json')

    # Get the cleaned DataFrame
    jumai_df = jumai_cleaner.get_cleaned_data()

    # # Display the cleaned data
    # print(cleaned_df.head())

    # Test with a question and filtered data
    question = 'What is the best deal for today?'
    # product_data = df[df['Brands'] == 'Samsung']

    # Run the test
    res = shopping_assistant.run(question, phone_k_df,  jumai_df)
    print(res)
