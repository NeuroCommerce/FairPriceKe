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

### 5. Prepare Data

Ensure the required data files are available in the correct directories:

- Phone Kenya CSV file: `data/Phone Place Kenya Scraping/row/scraped_phones_with_datetime.csv`
- Jumia JSON file: `data/Jumia/2024-10-03_all_brands_products.json`

Place the files in these locations or update the file paths in the `llm_bot.py` script accordingly.

## Running the Application

To run the app, use Streamlit:

```bash
streamlit run llm_bot.py
```

This will open the app in your browser.

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



