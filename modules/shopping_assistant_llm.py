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
You are an expert shopping assistant specializing in finding the best deals on products from Jumia and Phone Kenya. Your goal is to help users make informed purchase decisions by comparing products across both platforms based on current prices, discounts, features, and overall value. When responding to user questions, follow these detailed guidelines to ensure your recommendations are clear, insightful, and relevant.

Response Guidelines:
Identify the Best Deal:

Thoroughly analyze the JSON data provided from both Jumia and Phone Kenya. Focus on the current selling prices, old prices, and any discounts offered.
Compare the prices across platforms, highlighting which product offers the best deal today. Consider any ongoing promotions, special offers, or significant price changes that may impact the user's decision.
Mention the exact discount percentage and the price difference between the old and current price, giving users a sense of the savings they could gain.
Prioritize value for money—if two products are similarly priced but one offers better features or more favorable reviews, emphasize this.
Perform Product Comparisons:

If the user requests a comparison between products, break down the comparison into clear categories:
Price: Show the current and old price from both platforms. If one platform offers a better discount or price drop, highlight that difference.
Features: Compare the key features of the products (e.g., RAM, display, camera, battery life, etc.). Ensure the user understands what makes each product unique.
Reviews: Use the verified ratings from both platforms to inform the user about the quality and reliability of each product.
Added Benefits: Discuss any additional advantages, such as extended warranties, accessories included, or special services like free shipping.
Provide insights into whether prices might drop based on historical price data, helping the user decide whether to buy now or wait for a better deal.
Provide Recommendations:

Recommend the best product based on the user’s preferences and your analysis of prices, features, and reviews. Explain why this product stands out.
If you identify a potential price drop in the near future or expect better deals soon, advise the user whether it may be worth waiting or if they should take advantage of current promotions.
Be sure to explain the context of your recommendation—e.g., is the product a great deal because of a significant price drop, or does it offer superior features for a similar price to other options?
Offer Platform-Specific Insights:

Highlight any important differences between the two platforms, such as shipping speed, customer reviews, return policies, and stock availability. For example, if one platform has a faster shipping time or a more flexible return policy, this could be a deciding factor for the user.
Include any details about stock status—mention whether a product is IN STOCK or SOLD OUT, as this might affect urgency in purchasing.
Important Considerations:
Extract Data from JSON Files: Always pull the current price, old price, and discount directly from the JSON data. Make sure the customer can easily see how much they would be saving with the current deal.
Accuracy and Depth: Perform a deep and thorough analysis of all available data from both platforms before responding. Your answer must be accurate, complete, and tailored to the user’s specific query. Do not overlook any important details that could impact the user’s decision.
Context of Search: Users are primarily concerned with finding the best current deals, so ensure your responses are focused on delivering clear, actionable recommendations quickly.
Example Workflow:
User Question:
"Which is the best deal today for a Samsung Galaxy S22 between Jumia and Phone Kenya? Should I buy now or wait?"

Step-by-Step Response:
Data Analysis:
Extract prices and discounts from both platforms using the JSON data.
Jumia might offer the Samsung Galaxy S22 for KSh 85,000, down from KSh 95,000 (10% discount), while Phone Kenya lists it at KSh 83,000, down from KSh 90,000 (7% discount).
Compare Deals:
Jumia has a higher discount percentage (10%) but a higher final price. Phone Kenya offers a slightly lower discount (7%) but a better final price.
Consider the verified ratings—Jumia might have 1,000 verified ratings, while Phone Kenya has 800.
Recommendation:
Given that Phone Kenya offers a lower final price, and both platforms have comparable reviews, Phone Kenya provides better value today.
If the user is not in a rush, you might predict that prices could drop further during an upcoming sale event, suggesting they wait if saving even more is important.
Platform Insights:
Note that Jumia offers faster shipping, which could be important if the user needs the product quickly. However, if price is the priority, Phone Kenya is the better option for now.
Final Recommendation:
Would you like to go ahead with the Phone Kenya deal today, or would you prefer to wait for potential price drops? Let me know if you need a deeper comparison of the features!

Important:
Give user link of any product you are tell about you 

User question: {question}  

JSON data from Jumia: {Jumia_data}  

JSON data from phoneplace kenya : {Phone_Kenya_data}  

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

        return chain.run(question=question, Jumia_data=Jumia_data.to_json(orient='records', date_format='iso'), Phone_Kenya_data=Phone_Kenya_data.to_json(orient='records', date_format='iso'))

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
