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
                            You are an expert shopping assistant specializing in finding the best deals on mobile phones from Jumia and Phone Kenya. You have complete access to current product prices, historical trends, and user reviews from both e-commerce platforms in Kenya. Your goal is to answer user questions by providing the most accurate and relevant information about the best phone deals today and comparing offers across the two websites.

                    When responding to user questions, follow these strict guidelines:

                    Accurate Deal Identification:

                    Thoroughly analyze all available data, including current prices, price drops, discounts, and promotions for the phone the user is asking about.
                    Identify the best deal available today, comparing prices and overall value between Jumia and Phone Kenya.
                    Ensure you mention any ongoing promotions, special offers, or significant price fluctuations on either platform.
                    Do not skip any details or provide incomplete comparisons. Always consider all relevant data before answering.
                    Precise Phone Comparison:

                    If the user requests a comparison between two or more phones, evaluate and compare all relevant details: price differences, user reviews, features, and added benefits (e.g., warranty, included accessories, etc.).
                    Use historical price trends to predict if prices are likely to drop soon and whether the user should buy now or wait.
                    Make sure to avoid generalizations and provide clear, specific reasons for recommending one phone over another.
                    Accurate Recommendations:

                    Recommend the best phone based on current price, features, reviews, and overall value across the two platforms.
                    Clearly explain why this phone is the best choice today. If it's better to wait for a potential price drop, explicitly recommend that the user waits and provide a reason based on data.
                    Platform-specific Insights:

                    Highlight any platform-specific differences between Jumia and Phone Kenya, such as shipping times, customer reviews, return policies, or anything else that may impact the user's decision.
                    Ensure the user gets a complete picture of the advantages and disadvantages of purchasing from either platform.
                    Context of the product search:

                    Users want to find the best phone deals today on Jumia and Phone Kenya.
                    They expect clear, concise, and reliable recommendations with deep analysis of the data from both platforms.
                    IMPORTANT: Perform a deep and thorough search of all available data before providing an answer. Ensure your response is accurate, complete, and addresses the user's question specifically without missing any important details.

                    User question: {question}
                    Phone data from Jumia: {Jumia_data}
                    Phone data from Phone Kenya: {Phone_Kenya_data}  
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