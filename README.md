# Shopping Assistant LLM

This project implements a Shopping Assistant using a Large Language Model (LLM) to help users explore product data and engage in conversations about products. It uses the Google Generative AI model via the `langchain_google_genai` library to interact with the product data from Phone Kenya and Jumia platforms.

## Features

- **Data Exploration**: Users can view and explore product data from Phone Kenya and Jumia.
- **Chat with Shopping Assistant**: Users can chat with the shopping assistant to ask questions about the products, with the chat history being saved during the session.

## Requirements

- Python 3.11+
- Dependencies listed in `requirements.txt`

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-repository/shopping-assistant-llm.git
cd shopping-assistant-llm
```

### 2. Set Up a Virtual Environment (optional but recommended)

To isolate dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install Dependencies

You can install all the required Python packages by running:

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

The app uses the Google Generative AI API for LLM capabilities, so you'll need to set up the environment variable for the API key:

- Create a `.env` file in the project root and add the following:

```
GEMINI_KEY=your-google-generative-ai-api-key
```

Replace `your-google-generative-ai-api-key` with your actual API key.

### 5. Data Scraping

## 1. Configure Database Credentials

      Go to the modules folder and open the files scraping_and_put_in_sql.py and get_tables_details.py.

      Update the database connection details in both files:

      ```bash
      self.user = 'your_database_user'
      self.password = 'your_database_password'
      self.host = 'your_database_host'
      ```
      Replace these values with your actual database information.

## 2. Run the Scraping Script

      Navigate to the modules folder in your terminal.
      Run the scraping script:

      ```bash

      python scraping_and_put_in_sql.py
      ```

      This step will begin scraping data and creating tables for both Jumia and Phone Kenya platforms. It also creates a history table to log updates or changes in the future.

## 3. Verify Data Tables

    Upon completing the scraping, the following tables should be present in your database:

    Jumia table
    Phone Kenya table
    Jumia History table
    Phone Kenya History table

### Running the Shopping Assistant

## Start the Chat Interface

     To interact with the shopping assistant, run the following command in your terminal:

    ```bash
    streamlit run llm_bot.py
    ```

    This will launch a Streamlit-based user interface, allowing you to chat with the assistant and explore product data.

## How to Use

### 1. Data Exploration

- From the sidebar, select **"Data Exploration"**.
- This will display previews of the Phone Kenya and Jumia product datasets, allowing you to explore the available data.

### 2. Chat with the Shopping Assistant

- Select **"💬 Chat with Shopping Assistant"** from the sidebar.
- Use the chat input box at the bottom to ask questions about the products.
- The assistant responds based on the provided data, and both your inputs and the assistant’s responses will be logged in the session.

### Example Questions:

- "What is the best phone available on Phone Kenya?"
- "Which product has the largest discount on Jumia?"

## Modules

- `shopping_assistant_llm`: Contains the logic for interacting with the LLM model.
- `clean_jumia_data`: Cleans and processes the Jumia dataset for use in the application.
- `main`: The main class that orchestrates interactions between the datasets and the LLM model.

## Customizing the Application

If you want to add more datasets or change the logic of how the assistant processes queries, you can modify the `ShoppingAssistant` or `MainClass` in the `main.py` file.
