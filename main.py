from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv
import pandas as pd
from modules.clean_jumia_data import JumiaDataCleaner
from modules.clean_phone_place_kenya import PhoneKenyaDataCleaner
from modules.shopping_assistant_llm import ShoppingAssistant


class MainClass:
    def __init__(self, llm, verbose=0):
        """
        Initializes the MainClass with an LLM model and verbosity level.

        :param llm: The LLM model to use
        :param verbose: Verbosity level (0 for silent, 1 for detailed logs)
        """
        self.llm = llm
        self.verbose = verbose
        self.shopping_assistant = ShoppingAssistant(llm=llm, verbose=verbose)

    def load_clean_phone_kenya_data(self, phone_kenya_csv_path):
        """
        Loads and cleans Phone Kenya data using PhoneKenyaDataCleaner.

        :param phone_kenya_csv_path: Path to the Phone Kenya CSV file
        :return: Cleaned DataFrame
        """
        if self.verbose:
            print("Cleaning Phone Kenya data...")
        phone_k_cleaner = PhoneKenyaDataCleaner(phone_kenya_csv_path)
        phone_k_df = phone_k_cleaner.clean_data()
        return phone_k_df

    def load_clean_jumia_data(self, jumia_json_path):
        """
        Loads and cleans Jumia data using JumiaDataCleaner.

        :param jumia_json_path: Path to the Jumia JSON file
        :return: Cleaned DataFrame
        """
        if self.verbose:
            print("Cleaning Jumia data...")
        jumia_cleaner = JumiaDataCleaner(jumia_json_path)
        jumia_df = jumia_cleaner.get_cleaned_data()
        return jumia_df

    def run(self, question, phone_kenya_csv_path, jumia_json_path):
        """
        Runs the ShoppingAssistant with cleaned data to answer the user's question.

        :param question: The user’s question about the best deals
        :param phone_kenya_csv_path: Path to the Phone Kenya CSV file
        :param jumia_json_path: Path to the Jumia JSON file
        :return: Response from the ShoppingAssistant
        """
        # Load and clean data
        phone_k_df = self.load_clean_phone_kenya_data(phone_kenya_csv_path)
        jumia_df = self.load_clean_jumia_data(
            jumia_json_path)
        # jumia_df.to_csv('asd.csv', index=False)
        # print("jumia_df is saved")

        # Run the ShoppingAssistant model
        result = self.shopping_assistant.run(question, jumia_df, phone_k_df)
        return result

    def test(self, phone_kenya_csv_path, jumia_json_path):
        """
        Test method to demonstrate how the MainClass works.

        :param phone_kenya_csv_path: Path to the Phone Kenya CSV file
        :param jumia_json_path: Path to the Jumia JSON file
        :return: The result of running the ShoppingAssistant with a sample question
        """
        question = 'What is the best deal for today?'
        result = self.run(question, phone_kenya_csv_path, jumia_json_path)
        if self.verbose:
            print(f"Test Result: {result}")
        return result


if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    google_api_key = os.getenv("GEMINI_KEY")

    # Initialize the LLM model
    llm = GoogleGenerativeAI(
        model="gemini-1.5-flash-latest", google_api_key=google_api_key, temperature=0)

    # Paths to the datasets
    phone_kenya_csv_path = r'D:\Projects\FairPriceKe\FairPriceKe\data\Phone Place Kenya Scraping\row\scraped_phones_with_datetime.csv'
    jumia_json_path = r'D:\Projects\FairPriceKe\FairPriceKe\data\Jumia\2024-10-03_all_brands_products.json'

    # Initialize the MainClass and run the test
    main_class = MainClass(llm=llm, verbose=1)
    main_class.test(phone_kenya_csv_path, jumia_json_path)
