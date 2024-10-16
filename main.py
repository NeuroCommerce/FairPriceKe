from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv
import pandas as pd
from modules.clean_jumia_data import JumiaDataCleaner
from modules.clean_phone_kenya_data import PhoneKenyaDataCleaner
from modules.shopping_assistant_llm import ShoppingAssistant
from modules.get_data_from_sql import GetDataFromSQL
from modules.response_wrapper import Responsewrapper


class MainClass:
    def __init__(self, llm, verbose=0):
        """
        Initializes the MainClass with an LLM model and verbosity level.

        :param llm: The LLM model to use
        :param verbose: Verbosity level (0 for silent, 1 for detailed logs)
        """
        self.llm = llm
        self.verbose = verbose
        self.get_data_from_sql = GetDataFromSQL(self.llm , verbose=1)
        self.response_wrapper = Responsewrapper(self.llm , verbose=1)

    def prepare(self):
        
    
        self.get_data_from_sql.prepare()
        self.response_wrapper.prepare()
        
        

    def run(self, user_question):
        """
        Runs the ShoppingAssistant with cleaned data to answer the user's question.

        :param question: The user’s question about the best deals
        :param phone_kenya_csv_path: Path to the Phone Kenya CSV file
        :param jumia_json_path: Path to the Jumia JSON file
        :return: Response from the ShoppingAssistant
        """

        self.prepare()
    
        # Run the pipeline and get the final answer
        sql_execution_results , queries  = self.get_data_from_sql.run(user_question)
        print("sql_execution_results:")
        print(sql_execution_results)
        print("*" *50)
        print("queries:")
        print(queries)
        

        final_answer =  self.response_wrapper.run(user_question , queries , sql_execution_results)
        
        print("this is the response wrapper =" , final_answer)
        
        return final_answer

    def test(self, user_question):
        pass


if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    google_api_key = os.getenv("GEMINI_KEY")

    # Initialize the LLM model
    llm = GoogleGenerativeAI(
        model="gemini-1.5-flash-latest", google_api_key=google_api_key, temperature=0)


    question = 'What is the best deal for today?'

    # Initialize the MainClass and run the test
    main_class = MainClass(llm=llm, verbose=1)
    main_class.prepare()
    main_class.run(question)
