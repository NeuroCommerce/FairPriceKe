import pandas as pd

import numpy as np


def cleaning(csv_file):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Strip any leading or trailing spaces from the column names
    df.columns = df.columns.str.strip()

    # Print the column names after stripping spaces
    print("Stripped Columns:", df.columns.tolist())

    # 1. Combine 'Scrape Date' and 'Scrape Time' into a single 'timestamp' column
    df['timestamp'] = pd.to_datetime(
        df['Scrape Date'] + ' ' + df['Scrape Time'])

    # 2. Calculate the 'discount' as a percentage based on the price and old price
    # Clean price and old price by removing the currency symbol and commas
    df['PhonePlaceKenya_Price'] = df['PhonePlaceKenya_Price'].str.replace(
        'KSh', '').str.replace(',', '').astype(float)
    df['PhonePlaceKenya_oldPrice'] = df['PhonePlaceKenya_oldPrice'].str.replace(
        'KSh', '').str.replace(',', '').astype(float)

    # Calculate the discount if both prices exist
    df['discount'] = ((df['PhonePlaceKenya_oldPrice'] -
                      df['PhonePlaceKenya_Price']) / df['PhonePlaceKenya_oldPrice']) * 100
    # Round the discount to 2 decimal places
    df['discount'] = df['discount'].round(2)

    # 3. Extract 'verifiedRatings' from the Reviews column (convert to numerical values)
    df['verifiedRatings'] = df['Reviews'].str.extract(
        r'(\d+)').fillna(0).astype(int)

    # 4. Consolidate all columns that contain product information into 'Key_Features'
    product_info_columns = [
        'RAM', 'Storage', 'Battery', 'Camera', 'Selfie', 'Display', 'Processor',
        'Connectivity', 'Colors', 'OS', 'Network', 'Display Size', 'Resolution',
        'Operating System', 'Main Camera', 'Secondary Camera', 'Color', 'Main camera',
        'Front camera', 'Internal Storage', 'Selfie Camera', 'Tags'
    ]

    # Create 'Key_Features' column containing the product information as a dictionary
    df['Key_Features'] = df[product_info_columns].apply(
        lambda x: x.dropna().to_dict(), axis=1)

    # 5. Stock status (IN STOCK or SOLD OUT)
    df['stock'] = np.where(df['Status'] == 'IN STOCK', 'IN STOCK', 'SOLD OUT')

    # 6. Reorder columns based on the new order
    new_column_order = [
        'timestamp', 'productName', 'Brand', 'price', 'oldPrice',
        'discount', 'verifiedRatings', 'stock', 'Key_Features'
    ]

    # Extract the brand from the product name (assuming the first word of the productName is the brand)
    df['Brand'] = df['productName'].apply(lambda x: x.split()[0])

    # Rename the columns to match your expected names
    df.rename(columns={
        'PhonePlaceKenya_Price': 'price',
        'PhonePlaceKenya_oldPrice': 'oldPrice',
    }, inplace=True)

    # Ensure that you have stripped and renamed columns correctly
    print("Final Columns:", df.columns.tolist())

    # Reorder the DataFrame based on the new column order
    df_cleaned = df[new_column_order]

    return df_cleaned


# Usage example
csv_file_path = r'D:\freelance\FairPriceKe-add_llm\FairPriceKe\FairPriceKe\data\Phone Place Kenya Scraping\cleaned\phone_place_kenya.csv'
input_path = r"D:\freelance\FairPriceKe-add_llm\FairPriceKe\FairPriceKe\data\Phone Place Kenya Scraping\row\scraped_phones_with_datetime.csv"
cleaned_df = cleaning(input_path)
cleaned_df.to_csv(csv_file_path, index=False)
print(cleaned_df)
