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
                            You are an expert shopping assistant specializing in helping users find the best deals on mobile phones from **Jumia** and **Phone Kenya**. You have access to product price data, historical trends, and reviews from both e-commerce platforms in Kenya. Your goal is to answer user questions by identifying the best phone deals today and comparing them across the two websites.

                When responding to user questions, follow these guidelines:

                1. **Best Deal Identification**:  
                - Analyze current prices, price drops, discounts, and promotions for the phone the user is asking about.
                - Identify which phone offers the best deal today by comparing prices and overall value between Jumia and Phone Kenya.
                - Mention ongoing promotions, special offers, or significant price changes on either platform.

                2. **Phone Comparison**:  
                - If the user asks for a comparison between phones, evaluate price differences, reviews, features, and any added benefits (e.g., warranty, accessories, etc.).
                - Use historical price data to predict whether the prices of competing phones are likely to drop soon, helping users decide whether to buy now or wait.

                3. **Recommendation**:  
                - Recommend the best phone based on price, features, reviews, and value across the two platforms.
                - Explain why this phone is the best choice today. If waiting for a potential price drop is more advantageous, suggest waiting.
                
                4. **Platform-specific Insights**:  
                - Highlight differences between the two platforms, such as shipping speed, customer reviews, or return policies that might impact the user's decision.

                **Context of the product search**:  
                - Users are focused on finding the best phone deals available today across Jumia and Phone Kenya.
                - Time is a factor, so they need clear, concise, and reliable recommendations to make informed decisions without having to manually compare products on both sites.

                User question: {question}  

                Phone data from Jumia: {Jumia_data}  
                Phone data from Phone Kenya: {Phone_Kenya_data}  

                Based on this data, provide the best deal, relevant comparisons, and a recommendation.
        """

    def prepare(self, question, Jumia_data , Phone_Kenya_data):
        """
        Prepares the question and product data for the LLM chain.
        
        :param question: The question the user wants to ask.
        :param product_data: The product data to be analyzed for the best deal.
        :return: Dictionary with 'question' and 'Product_data' keys.
        """
        if self.verbose:
            print("Preparing the inputs for the LLM chain...")
        return {'question': question, 'Jumia_data': Jumia_data , 'Phone_Kenya_data' : Phone_Kenya_data}

    def run(self, question, Jumia_data , Phone_Kenya_data):
        """
        Runs the LLM chain with the prepared inputs.
        
        :param inputs: Dictionary containing the question and product data.
        :return: Response from the LLM model.
        """
        if self.verbose:
            print("Running the LLM chain...")

        inputs = self.prepare(question, Jumia_data , Phone_Kenya_data)
        prompt = PromptTemplate(
            input_variables=['question', 'Product_data'],
            template=self.prompt_template
        )
        chain = LLMChain(llm=self.llm, prompt=prompt)
        return chain.run(question=inputs['question'], Jumia_data=inputs['Jumia_data'] , Phone_Kenya_data =inputs['Phone_Kenya_data']  )

    def test(self, question, Jumia_data , Phone_Kenya_data):
        """
        Test function to demonstrate the use of the assistant.
        
        :param question: The question to ask the assistant.
        :param product_data: The product data for analysis.
        :return: The result of running the LLM chain.
        """
        inputs = self.prepare(question, Jumia_data ,  Phone_Kenya_data)
        result = self.run(inputs)
        if self.verbose:
            print(f"Test Result: {result}")
        return result


if __name__ == "__main__":
    load_dotenv()  # Load environment variables
    google_api_key = os.getenv("GEMINI_KEY")  # Load API key from environment
    llm = GoogleGenerativeAI(model="gemini-1.5-flash-latest", google_api_key=google_api_key, temperature=0)
    
    # Initialize the ShoppingAssistant with verbosity
    shopping_assistant = ShoppingAssistant(llm=llm, verbose=1)

    csv_file_path = r'D:\Projects\FairPriceKe\FairPriceKe\data\Phone Place Kenya Scraping\row\scraped_phones_with_datetime.csv'
    phone_k_cleaner = PhoneKenyaDataCleaner(csv_file_path)
    phone_k_df = phone_k_cleaner.clean_data()
    
    # Create an instance of the class
    jumai_cleaner = JumiaDataCleaner(r'D:\Projects\FairPriceKe\FairPriceKe\data\Jumia\2024-10-03_all_brands_products.json')

    # Get the cleaned DataFrame
    jumai_df = jumai_cleaner.get_cleaned_data()

    # # Display the cleaned data
    # print(cleaned_df.head())

    # Test with a question and filtered data
    question = 'What is the best deal for today?'
    # product_data = df[df['Brands'] == 'Samsung']

    # Run the test
    res = shopping_assistant.run(question, phone_k_df ,  jumai_df)
    print(res)