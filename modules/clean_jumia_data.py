import json
import pandas as pd
import numpy as np


class JumiaDataCleaner:
    def __init__(self, json_file_path):
        self.json_file_path = json_file_path
        self.df = None

    def load_json(self):
        # Load the JSON file
        with open(self.json_file_path, 'r', encoding='utf-8') as f:
            jumia_json = json.load(f)
        self.df = pd.DataFrame(jumia_json)

    def clean_data(self):
        # Select relevant columns
        self.df = self.df[['productName', 'price', 'oldPrice', 'discount', 'rating',
                            'verifiedRatings', 'stock', 'specifications', 'timestamp']]

        # Convert 'timestamp' column to datetime format
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'], errors='coerce')

        # Drop rows where 'productName' is NaN
        self.df = self.df.dropna(subset=['productName'])

        # Extract the product name and assign brand
        self.df['productName'] = self.df['productName'].str.extract(
            r'^(.*?)(,|$)', expand=False)[0]
        self.df['Brand'] = self.df['productName'].str.split(' ', n=1).str[0]

        # Clean the 'price', 'oldPrice', and 'discount' columns
        def clean_currency(value):
            try:
                # Remove currency symbols and commas
                return float(value.replace('KSh', '').replace(',', '').strip())
            except ValueError:
                # Return NaN if conversion fails
                return np.nan

        self.df['price'] = self.df['price'].apply(clean_currency)
        self.df['oldPrice'] = self.df['oldPrice'].apply(clean_currency)

        # Handle 'discount' column and convert to a float
        def clean_discount(value):
            try:
                # Remove percentage symbol
                return float(value.strip('%'))
            except (ValueError, AttributeError):
                # Return NaN if conversion fails
                return np.nan

        self.df['discount'] = self.df['discount'].apply(clean_discount)

        # Rename the specified columns by adding 'jumia_' prefix
        columns_to_rename = ['price', 'oldPrice', 'discount', 'rating', 'verifiedRatings', 'stock']
        self.df.rename(
            columns={col: 'jumia_' + col for col in columns_to_rename}, inplace=True)

        # Extract 'Key Features' from 'specifications'
        self.df['Key_Features'] = self.df['specifications'].apply(
            lambda x: x.get('Key Features') if isinstance(x, dict) else None)

        # Drop the 'specifications' column
        self.df = self.df.drop('specifications', axis=1)

        # Add the 'Category' column
        self.df['Category'] = 'Smart Phones'


    def reorder_columns(self):
        # Reorder the columns
        new_column_order = [
            'timestamp', 'productName', 'Brand', 'jumia_price', 'jumia_oldPrice',
            'jumia_discount', 'jumia_rating', 'jumia_verifiedRatings',
            'jumia_stock', 'Key_Features', 'Category'
        ]
        self.df = self.df[new_column_order]

    def get_cleaned_data(self):
        # Load, clean, and return the cleaned DataFrame
        self.load_json()
        self.clean_data()
        self.reorder_columns()
        return self.df


if __name__ == '__main__':
    # Create an instance of the class
    cleaner = JumiaDataCleaner(
        r'D:\Projects\FairPriceKe\FairPriceKe\data\Jumia\2024-10-03_all_brands_products.json')

    # Get the cleaned DataFrame
    cleaned_df = cleaner.get_cleaned_data()

    # Display the cleaned data
    print(cleaned_df.head())


    
    print(cleaned_df.info())
