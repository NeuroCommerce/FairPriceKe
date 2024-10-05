import json
import pandas as pd

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

        # Drop rows where 'productName' is NaN
        self.df = self.df.dropna(subset=['productName'])

        # Extract the product name and assign brand
        self.df['productName'] = self.df['productName'].str.extract(r'^(.*?)(,|$)', expand=False)[0]
        self.df['Brand'] = self.df['productName'].str.split(' ', n=1).str[0]

        # Rename the specified columns by adding 'jumia_' prefix
        columns_to_rename = ['price', 'oldPrice', 'discount', 'rating', 'verifiedRatings', 'stock']
        self.df.rename(columns={col: 'jumia_' + col for col in columns_to_rename}, inplace=True)
        self.df['Key_Features']   = self.df['specifications'].apply(lambda x: x['Key Features'])
        self.df = self.df.drop( 'specifications', axis=1)

    def reorder_columns(self):
        # Reorder the columns
        new_column_order = [
            'timestamp', 'productName', 'Brand', 'jumia_price', 'jumia_oldPrice', 
            'jumia_discount', 'jumia_rating', 'jumia_verifiedRatings', 
            'jumia_stock', 'Key_Features'
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
    cleaner = JumiaDataCleaner(r'D:\Projects\FairPriceKe\FairPriceKe\data\Jumia\2024-10-03_all_brands_products.json')

    # Get the cleaned DataFrame
    cleaned_df = cleaner.get_cleaned_data()

    # Display the cleaned data
    print(cleaned_df.head())