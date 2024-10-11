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
                You are an expert shopping assistant specializing in helping users find the best deals on  products from **Jumia** and **Phone Kenya**. 

                When responding to user questions, follow these guidelines:

                I WILL GIVE YOU JSON FILE FOR EACH PLATEFORM 

                1. **Best Deal Identification**:  
                - Analyze current prices, price drops, discounts, and promotions for the products the user is asking about.
                - Identify which products offers the best deal today by comparing prices and overall value between Jumia and products Kenya.
                - Mention ongoing promotions, special offers, or significant price changes on either platform.

                2. **products Comparison**:  
                - If the user asks for a comparison between products, evaluate price differences, reviews, features, and any added benefits (e.g., warranty, accessories, etc.).
                - Use historical price data to predict whether the prices of competing products are likely to drop soon, helping users decide whether to buy now or wait.

                3. **Recommendation**:  
                - Recommend the best products based on price, features, reviews, and value across the two platforms.
                - Explain why this products is the best choice today. If waiting for a potential price drop is more advantageous, suggest waiting.
                
                4. **Platform-specific Insights**:  
                - Highlight differences between the two platforms, such as shipping speed, customer reviews, or return policies that might impact the user's decision.

                **Context of the product search**:  
                - Users are focused on finding the best products deals available from data across Jumia and products Kenya.
                - Time is a factor, so they need clear, concise, and reliable recommendations to make informed decisions without having to manually compare products on both sites.
                
                IMPORTANT IN OUTPUT :
                1.YOU PREFEAR GET PRICE AND OLD PRICE OF PRODUCT FROM JSON DATA AND SHOW PRICE AND DISCOUT FOR CUSTOMER 
                2.Perform a deep and thorough search of all available data before providing an answer. 
                3.Ensure your response is accurate, complete, and addresses the user's question specifically without missing any important details.
                4.end answer with recommendation questions 

                discribtion of data :
                        timestamp: The date and time when the data entry was recorded.
                        productName: The name of the products model being described.
                        Brand: The brand of the products (e.g., Samsung).
                        price: The current selling price of the products.
                        oldPrice: The previous price of the products before any discounts or changes.
                        discount: The percentage difference between the old price and the current price, representing the discount applied.
                        verifiedRatings: The number of verified customer ratings for the product.
                        stock: The availability status of the products (e.g., IN STOCK, SOLD OUT).
                        Key_Features: A dictionary of the key features of the products, such as RAM, battery capacity, display size, connectivity options, and camera specifications.
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

        return chain.run(question=question, Jumia_data=Jumia_data.to_json(orient='records', date_format='iso', indent=4), Phone_Kenya_data=Phone_Kenya_data.to_json(orient='records', date_format='iso', indent=4))

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
