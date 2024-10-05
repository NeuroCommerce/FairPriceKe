# Import relevant libraries
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime

class PhonePlaceKenyaScraping:
    def __init__(self):
        # Initialize the WebDriver (ensure the ChromeDriver is in PATH)
        self.driver = webdriver.Chrome()
        self.all_product_data = []

    def extract_info(self, text):
        """
        Helper function to extract information from product details.
        """
        lines = text.strip().split('\n')
        product_info = {}
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                product_info[key.strip()] = value.strip()
            else:
                if 'Reviews' in line:
                    product_info['Reviews'] = line.strip()
                elif 'IN STOCK' in line:
                    product_info['Status'] = line.strip()
                elif 'Warranty' in line:
                    product_info['Warranty Info'] = line.strip()
                elif line.startswith("East Africa") or line.startswith("UAE"):
                    product_info['Region'] = line.strip()
                elif line.startswith("KSh"):
                    if 'Price 1' not in product_info:
                        product_info['Price 1'] = line.strip()  # First price
                    else:
                        product_info['Price 2'] = line.strip()  # Second price
        return product_info

    def scrape_phones_data(self, phone_type):
        """
        Scrapes phone data for a given phone type from PhonePlace Kenya website.
        """
        # Base URL
        url = f"https://www.phoneplacekenya.com/product-category/smartphones/{phone_type}/"
        
        self.driver.get(url)

        try:
            # Wait for the search results to load
            phones_grid = WebDriverWait(self.driver, 20).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "product-wrapper"))
            )

            # Loop through each product element
            for i, product in enumerate(phones_grid):
                try:
                    # Re-locate product wrapper in case of stale reference
                    phones_grid = WebDriverWait(self.driver, 20).until(
                        EC.presence_of_all_elements_located((By.CLASS_NAME, "product-wrapper"))
                    )
                    
                    product = phones_grid[i]  # Access product element by index
                    product.click()  # Click on the product

                    # Wait for the product details to load (single element)
                    phone_info = WebDriverWait(self.driver, 20).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "product-images-summary"))
                    )

                    # Product information
                    product_name = phone_info.find_element(By.CSS_SELECTOR, ".product_title.entry-title").text
                    data = phone_info.find_element(By.CSS_SELECTOR, ".summary.entry-summary").text

                    # Extract the information and append to the list
                    product_data = self.extract_info(data)
                    product_data['Product Name'] = product_name  # Add product name to the data

                    # Add the current date and time to the product data
                    product_data['Scrape Date'] = datetime.now().strftime("%Y-%m-%d")  # Date
                    product_data['Scrape Time'] = datetime.now().strftime("%H:%M:%S")  # Time

                    self.all_product_data.append(product_data)
                    
                    time.sleep(2)  # Pause before navigating back
                    self.driver.back()  # Go back to the previous page
                    time.sleep(2)

                except Exception as e:
                    print(f"Error occurred on product {i+1}: {e}")

        except TimeoutException as e:
            print(f"Failed to load product grid: {e}")
    
    def reorder_columns(self):
        """
        Reorders the DataFrame columns as per the required format.
        """
        df = pd.DataFrame(self.all_product_data)
        
        # Required columns in specific order
        ordered_columns = ['Scrape Date', 'Scrape Time', 'Product Name']
        
        # Add other columns except 'Price 1' and 'Price 2'
        other_columns = [col for col in df.columns if col not in ['Scrape Date', 'Scrape Time', 'Product Name', 'Price 1', 'Price 2']]
        
        # Add 'Price 1' and 'Price 2' at the end
        ordered_columns += other_columns + ['Price 1', 'Price 2']
        
        # Reorder the DataFrame
        df_reordered = df[ordered_columns]
        return df_reordered
    
    def save_data_to_csv(self, df, file_path):
        """
        Saves the DataFrame to a CSV file.
        """
        df.to_csv(file_path, index=False)
        print(f"Data successfully saved to {file_path}")

    def close_driver(self):
        """
        Closes the WebDriver instance.
        """
        self.driver.quit()

# Example usage
if __name__ == "__main__":
    # Create an instance of the class
    scraper = PhonePlaceKenyaScraping()
    
    # List of phone types to scrape
    phone_types = ["samsung", "iphone", "infinix-phones-in-kenya", "google", "itel", "nokia", 
                   "oppo", "oneplus", "realme", "tecno", "vivo", "xiaomi"]
    
    # Loop through the phone types and scrape data
    for phone in phone_types[7]:
        scraper.scrape_phones_data(phone)

    # Reorder the columns and get the final DataFrame
    final_df = scraper.reorder_columns()

    # Save the DataFrame to CSV
    scraper.save_data_to_csv(final_df, r'..\data\Phone Place Kenya Scraping\scraped_phones_with_datetime.csv')

    # Close the browser after scraping
    scraper.close_driver()
