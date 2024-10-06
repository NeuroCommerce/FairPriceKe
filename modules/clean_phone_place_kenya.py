import pandas as pd
import numpy as np


class PhoneKenyaDataCleaner:
    def __init__(self, csv_file):
        # Initialize with the CSV file path
        self.csv_file = csv_file
        self.df = pd.read_csv(self.csv_file)

        # Strip any leading or trailing spaces from the column names
        self.df.columns = self.df.columns.str.strip()
        # print("Stripped Columns:", self.df.columns.tolist())

    def combine_date_time(self):
        # Combine 'Scrape Date' and 'Scrape Time' into a single 'timestamp' column
        self.df['timestamp'] = pd.to_datetime(
            self.df['Scrape Date'] + ' ' + self.df['Scrape Time'])

    def clean_prices(self):
        # Clean price and old price by removing the currency symbol and commas, then convert to float
        self.df['PhonePlaceKenya_Price'] = self.df['PhonePlaceKenya_Price'].str.replace(
            'KSh', '').str.replace(',', '').astype(float)
        self.df['PhonePlaceKenya_oldPrice'] = self.df['PhonePlaceKenya_oldPrice'].str.replace(
            'KSh', '').str.replace(',', '').astype(float)

    def calculate_discount(self):
        # Calculate the discount if both prices exist and round it to 2 decimal places
        self.df['discount'] = ((self.df['PhonePlaceKenya_oldPrice'] -
                               self.df['PhonePlaceKenya_Price']) / self.df['PhonePlaceKenya_oldPrice']) * 100
        self.df['discount'] = self.df['discount'].round(2)

    def extract_verified_ratings(self):
        # Extract 'verifiedRatings' from the Reviews column and convert to numerical values
        self.df['verifiedRatings'] = self.df['Reviews'].str.extract(
            r'(\d+)').fillna(0).astype(int)

    def consolidate_key_features(self):
        # Consolidate all columns that contain product information into 'Key_Features'
        product_info_columns = [
            'RAM', 'Storage', 'Battery', 'Camera', 'Selfie', 'Display', 'Processor',
            'Connectivity', 'Colors', 'OS', 'Network', 'Display Size', 'Resolution',
            'Operating System', 'Main Camera', 'Secondary Camera', 'Color', 'Main camera',
            'Front camera', 'Internal Storage', 'Selfie Camera', 'Tags'
        ]
        self.df['Key_Features'] = self.df[product_info_columns].apply(
            lambda x: x.dropna().to_dict(), axis=1)

    def set_stock_status(self):
        # Set stock status (IN STOCK or SOLD OUT)
        self.df['stock'] = np.where(
            self.df['Status'] == 'IN STOCK', 'IN STOCK', 'SOLD OUT')

    def reorder_columns(self):
        # Extract the brand from the product name
        self.df['Brand'] = self.df['productName'].apply(lambda x: x.split()[0])

        # Rename the columns to match the expected names
        self.df.rename(columns={
            'PhonePlaceKenya_Price': 'price',
            'PhonePlaceKenya_oldPrice': 'oldPrice',
        }, inplace=True)

        # Ensure that you have stripped and renamed columns correctly
        # print("Final Columns:", self.df.columns.tolist())

        # Reorder columns
        new_column_order = [
            'timestamp', 'productName', 'Brand', 'price', 'oldPrice',
            'discount', 'verifiedRatings', 'stock', 'Key_Features'
        ]
        self.df_cleaned = self.df[new_column_order]

    def clean_data(self):
        # Call the necessary methods to clean the data
        self.combine_date_time()
        self.clean_prices()
        self.calculate_discount()
        self.extract_verified_ratings()
        self.consolidate_key_features()
        self.set_stock_status()
        self.reorder_columns()

        # Return the cleaned DataFrame
        return self.df_cleaned


# Usage example
if '__main__' == __name__:
    csv_file_path = r'D:\Projects\FairPriceKe\FairPriceKe\data\Phone Place Kenya Scraping\row\scraped_phones_with_datetime.csv'
    cleaner = PhoneKenyaDataCleaner(csv_file_path)
    cleaned_df = cleaner.clean_data()

    # # Save to CSV
    # output_path = r'D:\freelance\FairPriceKe-add_llm\FairPriceKe\FairPriceKe\data\Phone Place Kenya Scraping\cleaned\phone_place_kenya.csv'
    # cleaned_df.to_csv(output_path, index=False)
    print(cleaned_df)
