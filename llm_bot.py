import streamlit as st
import pandas as pd
import os
import json
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI
from modules.shopping_assistant_llm import ShoppingAssistant
from modules.clean_jumia_data import JumiaDataCleaner


# Streamlit App
def main():
    load_dotenv()  # Load environment variables
    google_api_key = os.getenv("GEMINI_KEY")  # Load API key from environment

    st.title("Shopping Assistant LLM")

    # Initialize the LLM
    llm = GoogleGenerativeAI(model="gemini-1.5-flash-latest", api_key=google_api_key, temperature=0)

    # Initialize the ShoppingAssistant with verbosity
    shopping_assistant = ShoppingAssistant(llm=llm, verbose=1)

    # Upload CSV file for product data
    # uploaded_file = st.file_uploader("Choose a product data CSV file", type="csv")

    # if uploaded_file:
        # Load the product data into a DataFrame
    phone_k_df = pd.read_csv(r"data\Phone Place Kenya Scraping\scraped_phones_data.csv")
    
    # Create an instance of the class
    cleaner = JumiaDataCleaner(r'D:\Projects\FairPriceKe\FairPriceKe\data\Jumia\2024-10-03_all_brands_products.json')
    # Get the cleaned DataFrame
    
    jumai_df = cleaner.get_cleaned_data()
    
    # json_file_path = r'data\Jumia\2024-10-03_all_brands_products.json'
    # with open(json_file_path, 'r', encoding='utf-8') as f:
    #         jumia_json = json.load(f)
    # jumai_df = pd.DataFrame(jumia_json)
    
    st.write("phone kenya Data Preview:")
    st.dataframe(phone_k_df.head())
    
    st.write("jumai Data Preview:")
    st.dataframe(jumai_df.head())

    # # Allow the user to select the brand they are interested in
    # brands = df['Brands'].unique()
    # selected_brand = st.selectbox("Select a brand:", brands)

    # # Filter the data based on the selected brand
    # product_data = df[df['Brands'] == selected_brand]

    # Ask user to input a question
    question = st.text_input("Ask a question about deals:", "What is the best deal for today?")

    # Button to run the LLM
    if st.button("Get Best Deal"):
        # Run the ShoppingAssistant with the user's question and filtered product data
        result = shopping_assistant.run(question, phone_k_df.to_dict(orient='records') ,  jumai_df.to_dict(orient='records'))
        st.write("Result:")
        st.write(result)
    # Display each product in a card-like format in a grid layout
    # st.subheader(f"Products from {selected_brand}")

    # Define how many products per row
    products_per_row = 3
    rows = [phone_k_df[i:i + products_per_row] for i in range(0, len(phone_k_df), products_per_row)]

    # Iterate through each row and display products
    for row in rows:
            cols = st.columns(products_per_row)
            for idx, (_, product) in enumerate(row.iterrows()):
                with cols[idx]:
                    with st.container():
                        st.image("placeholder_image1.jpg", width=150)  # Placeholder for product image
                        st.markdown(f"### {product['Product Name']}")
                        st.write(f"**Price**: {product['Price 1']}")
                        st.write(f"**RAM**: {product['RAM']}")
                        st.write(f"**Storage**: {product['Internal Storage']}")
                        st.write(f"**Battery**: {product['Battery']}")
                        # st.write(f"**Main Camera**: {product['Main camera']}")
                        # st.write(f"**Front Camera**: {product['Front camera']}")
                        # st.write(f"**Display**: {product['Display']}")
                        # st.write(f"**Processor**: {product['Processor']}")
                        # st.write(f"**Color**: {product['Colors']}")
                        # st.write(f"**Operating System**: {product['OS']}")

        

if __name__ == "__main__":
    main()
