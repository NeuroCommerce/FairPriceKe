from langchain_google_genai import GoogleGenerativeAI  
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from pydantic import BaseModel
import pandas as pd
import os
from dotenv import load_dotenv

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
            You are an expert shopping assistant tasked with helping users find the best deals on products and compare them against other available options. You have access to product price data and historical trends from multiple e-commerce platforms in Kenya. Your goal is to answer user questions by providing the best deal for today and comparing it to other similar products.

            When responding to the user's questions, follow these guidelines:

            1. **Best Deal Identification**: 
               - Look at the current prices, historical price trends, and any ongoing promotions for the product the user is asking about.
               - Identify which product is offering the best deal today by considering price drops, discounts, and overall value.
               - Mention any promotions, discounts, or special offers available.

            2. **Product Comparison**: 
               - If the user asks to compare products, consider price differences, reviews, and any additional benefits or features between products.
               - Use historical price data to predict whether the price of competing products is likely to drop soon.

            3. **Recommendation**: 
               - Recommend the best product based on price, features, and value. Explain why this product is the best choice today.
               - If the user would benefit from waiting for a potential price drop, suggest waiting.

            **Context of the product search:**
            - Users are looking for the best deal today, often on frequently purchased items like groceries, electronics, and household items.
            - Time-consuming price comparison is a major issue for users, and they are concerned about missing out on deals or promotions.
            - Users want to make informed decisions, save time, and trust the pricing information they are receiving.

            User question: {question}

            Product data: {Product_data}

            Based on this data, provide the best deal and relevant product comparisons.
        """

    def prepare(self, question, product_data):
        """
        Prepares the question and product data for the LLM chain.
        
        :param question: The question the user wants to ask.
        :param product_data: The product data to be analyzed for the best deal.
        :return: Dictionary with 'question' and 'Product_data' keys.
        """
        if self.verbose:
            print("Preparing the inputs for the LLM chain...")
        return {'question': question, 'Product_data': product_data}

    def run(self, question, product_data):
        """
        Runs the LLM chain with the prepared inputs.
        
        :param inputs: Dictionary containing the question and product data.
        :return: Response from the LLM model.
        """
        if self.verbose:
            print("Running the LLM chain...")

        inputs = self.prepare(question, product_data)
        prompt = PromptTemplate(
            input_variables=['question', 'Product_data'],
            template=self.prompt_template
        )
        chain = LLMChain(llm=self.llm, prompt=prompt)
        return chain.run(question=inputs['question'], Product_data=inputs['Product_data'])

    def test(self, question, product_data):
        """
        Test function to demonstrate the use of the assistant.
        
        :param question: The question to ask the assistant.
        :param product_data: The product data for analysis.
        :return: The result of running the LLM chain.
        """
        inputs = self.prepare(question, product_data)
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

    # Load the product data
    df = pd.read_csv(r'..\data\Phone Place Kenya Scraping\scraped_phones_data.csv')

    # Test with a question and filtered data
    question = 'What is the best deal for today?'
    product_data = df[df['Brands'] == 'Samsung']

    # Run the test
    res = shopping_assistant.run(question, product_data)
    print(res)