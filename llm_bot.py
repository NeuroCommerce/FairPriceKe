import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI
from modules.shopping_assistant_llm import ShoppingAssistant

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
    uploaded_file = st.file_uploader("Choose a product data CSV file", type="csv")

    if uploaded_file:
        # Load the product data into a DataFrame
        df = pd.read_csv(uploaded_file)
        st.write("Product Data Preview:")
        st.dataframe(df.head())

        # Allow the user to select the brand they are interested in
        brands = df['Brands'].unique()
        selected_brand = st.selectbox("Select a brand:", brands)

        # Filter the data based on the selected brand
        product_data = df[df['Brands'] == selected_brand]

        # Ask user to input a question
        question = st.text_input("Ask a question about deals:", "What is the best deal for today?")

        # Button to run the LLM
        if st.button("Get Best Deal"):
            # Run the ShoppingAssistant with the user's question and filtered product data
            result = shopping_assistant.run(question, product_data.to_dict(orient='records'))
            st.write("Result:")
            st.write(result)
        # Display each product in a card-like format in a grid layout
        st.subheader(f"Products from {selected_brand}")

        # Define how many products per row
        products_per_row = 3
        rows = [product_data[i:i + products_per_row] for i in range(0, len(product_data), products_per_row)]

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
