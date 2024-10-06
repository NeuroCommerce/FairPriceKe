import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI
from modules.shopping_assistant_llm import ShoppingAssistant
from modules.clean_jumia_data import JumiaDataCleaner
from main import MainClass

# Streamlit App
def main():
    load_dotenv()  # Load environment variables
    google_api_key = os.getenv("GEMINI_KEY")  # Load API key from environment

    st.title("Shopping Assistant LLM")

    # Initialize the LLM
    llm = GoogleGenerativeAI(model="gemini-1.5-flash-latest", api_key=google_api_key, temperature=0)
    
    # Paths to the datasets
    # For Phone Kenya data (CSV)
    phone_kenya_csv_path = os.path.join( 'data', 'Phone Place Kenya Scraping', 'row', 'scraped_phones_with_datetime.csv')

    # For Jumia data (JSON)
    jumia_json_path = os.path.join('data', 'Jumia', '2024-10-03_all_brands_products.json')
    
    # Initialize the MainClass and run the test
    main_class = MainClass(llm=llm, verbose=1)

    # Initialize the ShoppingAssistant with verbosity
    # shopping_assistant = ShoppingAssistant(llm=llm, verbose=1)

    # Sidebar for navigation
    section = st.sidebar.selectbox("Select Section", ["Data Exploration", "💬 Chat with Shopping Assistant"])

    # Load the product data
    phone_k_df = pd.read_csv(phone_kenya_csv_path)
    
    cleaner = JumiaDataCleaner(jumia_json_path)
    jumai_df = cleaner.get_cleaned_data()
    
    # Initialize session state variables for chat history and messages if they don't exist
    if "messages" not in st.session_state:
        st.session_state.messages = []  # Initialize an empty list to store messages

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = pd.DataFrame(columns=["role", "content"])  # Empty dataframe for chat history

    # Data Exploration Section
    if section == "Data Exploration":
        st.header("Data Exploration")

        st.write("Phone Kenya Data Preview:")
        st.dataframe(phone_k_df.head())

        st.write("Jumia Data Preview:")
        st.dataframe(jumai_df.head())

        # # Display products in a grid layout
        # st.subheader("Phone Kenya Products")
        # products_per_row = 3
        # rows = [phone_k_df[i:i + products_per_row] for i in range(0, len(phone_k_df), products_per_row)]

        # for row in rows:
        #     cols = st.columns(products_per_row)
        #     for idx, (_, product) in enumerate(row.iterrows()):
        #         with cols[idx]:
        #             st.image("placeholder_image1.jpg", width=150)  # Placeholder for product image
        #             st.markdown(f"### {product['ProductName']}")
        #             st.write(f"**Price**: {product['Price 1']}")
        #             st.write(f"**RAM**: {product['RAM']}")
        #             st.write(f"**Storage**: {product['Internal Storage']}")
        #             st.write(f"**Battery**: {product['Battery']}")

    # Chat Section
    elif section == "💬 Chat with Shopping Assistant":
        st.header("💬 Chat with Shopping Assistant")
        
        # Display chat history
        for message in st.session_state.messages:
            is_arabic = message["content"][0].isascii() is False  # Check if the first character is non-ASCII (likely Arabic)
            alignment = "right" if is_arabic else "left"  # Align right for Arabic, left for English
            with st.chat_message(message["role"]):
                st.markdown(
                    f"<div style='text-align: {alignment};'>{message['content']}</div>",
                    unsafe_allow_html=True
                )

        # Chat input area at the bottom
        user_input = st.chat_input("Please enter your question here")

        if user_input:
            # Log user message in session_state
            st.session_state.messages.append({"role": "user", "content": user_input})

            # Display user's message in the chat
            st.chat_message("user").markdown(user_input)

            # Log user message in chat history DataFrame
            new_message = pd.DataFrame([{"role": "user", "content": user_input}])
            st.session_state.chat_history = pd.concat([st.session_state.chat_history, new_message], ignore_index=True)

            # Get response from the Shopping Assistant
            response = main_class.run(
                user_input,
                phone_kenya_csv_path, 
                jumia_json_path
            )

            # Log assistant's response in session_state
            st.session_state.messages.append({"role": "assistant", "content": response})

            # Display assistant's response in the chat
            st.chat_message("assistant").markdown(response)

            # Log assistant's response in chat history DataFrame
            new_response = pd.DataFrame([{"role": "assistant", "content": response}])
            st.session_state.chat_history = pd.concat([st.session_state.chat_history, new_response], ignore_index=True)


if __name__ == "__main__":
    main()
