# Import relevant libraries
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime
# from clean_jumia_data import clean_jumia_data  # Ensure this module is available


# class PhonePlaceKenyaScraping:
#     def __init__(self):
#         # Initialize the WebDriver (ensure the ChromeDriver is in PATH)
#         self.driver = webdriver.Chrome()
#         self.all_product_data = []

#     def extract_info(self, text):
#         """
#         Helper function to extract information from product details.
#         """
#         lines = text.strip().split('\n')
#         product_info = {}
#         for line in lines:
#             if ':' in line:
#                 key, value = line.split(':', 1)
#                 product_info[key.strip()] = value.strip()
#             else:
#                 if 'Reviews' in line:
#                     product_info['Reviews'] = line.strip()
#                 elif 'IN STOCK' in line:
#                     product_info['Status'] = line.strip()
#                 elif 'Warranty' in line:
#                     product_info['Warranty Info'] = line.strip()
#                 elif line.startswith("East Africa") or line.startswith("UAE"):
#                     product_info['Region'] = line.strip()
#                 elif line.startswith("KSh"):
#                     if 'PhonePlaceKenya_oldPrice' not in product_info:
#                         # First price
#                         product_info['PhonePlaceKenya_oldPrice'] = line.strip()
#                     else:
#                         # Second price
#                         product_info['PhonePlaceKenya_Price'] = line.strip()
#         return product_info

#     def scrape_phones_data(self, phone_type):
#         """
#         Scrapes phone data for a given phone type from PhonePlace Kenya website.
#         """
#         # Base URL
#         url = f"https://www.phoneplacekenya.com/product-category/smartphones/{phone_type}/"

#         self.driver.get(url)

#         try:
#             # Wait for the search results to load
#             phones_grid = WebDriverWait(self.driver, 20).until(
#                 EC.presence_of_all_elements_located(
#                     (By.CLASS_NAME, "product-wrapper"))
#             )

#             # Loop through each product element
#             for i, product in enumerate(phones_grid):
#                 try:
#                     # Re-locate product wrapper in case of stale reference
#                     phones_grid = WebDriverWait(self.driver, 20).until(
#                         EC.presence_of_all_elements_located(
#                             (By.CLASS_NAME, "product-wrapper"))
#                     )

#                     product = phones_grid[i]  # Access product element by index

#                     # Extract the product link before clicking
#                     product_link_element = product.find_element(
#                         By.TAG_NAME, 'a')
#                     product_link = product_link_element.get_attribute('href')

#                     product.click()  # Click on the product

#                     # Wait for the product details to load (single element)
#                     phone_info = WebDriverWait(self.driver, 20).until(
#                         EC.presence_of_element_located(
#                             (By.CLASS_NAME, "product-images-summary"))
#                     )

#                     # Product information
#                     product_name = phone_info.find_element(
#                         By.CSS_SELECTOR, ".product_title.entry-title").text

#                     data = phone_info.find_element(
#                         By.CSS_SELECTOR, ".summary.entry-summary").text

#                     # Extract the information and append to the list
#                     product_data = self.extract_info(data)
#                     # Add product name to the data
#                     product_data['productName'] = product_name

#                     # Add the product link to the data
#                     # New Field
#                     product_data['PhonePlaceKenya_productLink'] = product_link

#                     # Add the current date and time to the product data
#                     product_data['Scrape Date'] = datetime.now().strftime(
#                         "%Y-%m-%d")  # Date
#                     product_data['Scrape Time'] = datetime.now().strftime(
#                         "%H:%M:%S")  # Time

#                     # Extract discount percentage (if available)
#                     try:
#                         discount_percent = phone_info.find_element(
#                             By.CLASS_NAME, "onsale.percent").text

#                         product_data['PhonePlaceKenya_Discount'] = discount_percent
#                     except:
#                         product_data['PhonePlaceKenya_Discount'] = "No Discount"

#                     # Extract verifiedRatings (if available)
#                     try:
#                         verifiedRatings = phone_info.find_element(
#                             By.CLASS_NAME, "review-count").text

#                         product_data['PhonePlaceKenya_verifiedRatings'] = verifiedRatings
#                     except:
#                         product_data['PhonePlaceKenya_verifiedRatings'] = 0

#                     self.all_product_data.append(product_data)

#                     time.sleep(2)  # Pause before navigating back
#                     self.driver.back()  # Go back to the previous page
#                     time.sleep(2)

#                 except Exception as e:
#                     print(f"Error occurred on product {i+1}: {e}")

#         except TimeoutException as e:
#             print(f"Failed to load product grid: {e}")

#     def reorder_columns(self):
#         """
#         Reorders the DataFrame columns as per the required format.
#         """
#         df = pd.DataFrame(self.all_product_data)

#         # Required columns in specific order
#         ordered_columns = ['Scrape Date',
#                            'Scrape Time', 'productName', 'PhonePlaceKenya_productLink']  # Added link here

#         # Add other columns except 'Price 1' and 'Price 2'
#         other_columns = [col for col in df.columns if col not in [
#             'Scrape Date', 'Scrape Time', 'productName', 'PhonePlaceKenya_oldPrice', 'PhonePlaceKenya_Price', 'PhonePlaceKenya_Discount', 'PhonePlaceKenya_verifiedRatings', 'PhonePlaceKenya_productLink']]

#         # Add 'Price 1' and 'Price 2' at the end
#         ordered_columns += other_columns + \
#             ['PhonePlaceKenya_verifiedRatings', 'PhonePlaceKenya_oldPrice', 'PhonePlaceKenya_Price',
#              'PhonePlaceKenya_Discount', 'PhonePlaceKenya_productLink']  # Ensure link is included

#         # Reorder the DataFrame
#         df_reordered = df[ordered_columns]
#         return df_reordered

#     def save_data_to_csv(self, df, file_path):
#         """
#         Saves the DataFrame to a CSV file.
#         """
#         df.to_csv(file_path, index=False)
#         print(f"Data successfully saved to {file_path}")

#     def close_driver(self):
#         """
#         Closes the WebDriver instance.
#         """
#         self.driver.quit()


# # Example usage
# if __name__ == "__main__":
#     # Create an instance of the class
#     scraper = PhonePlaceKenyaScraping()

#     # List of phone types to scrape
#     phone_types = ["samsung", "iphone", "infinix-phones-in-kenya", "google", "itel", "nokia",
#                    "oppo", "oneplus", "realme", "tecno", "vivo", "xiaomi"]

#     # Loop through the phone types and scrape data
#     for phone in phone_types:
#         scraper.scrape_phones_data(phone)

#     # Reorder the columns and get the final DataFrame
#     final_df = scraper.reorder_columns()
#     print(final_df.sample(3))

#     # Save the DataFrame to CSV
#     scraper.save_data_to_csv(
#         final_df, r'D:\freelance\FairPriceKe-add_llm\FairPriceKe\FairPriceKe\data\Phone Place Kenya Scraping\row\scraped_phones_with_datetime.csv')

#     # Close the browser after scraping
#     scraper.close_driver()
class PhonePlaceKenyaScraping:
    def __init__(self):
        # Initialization and other methods remain the same...
        # Initialize the WebDriver (ensure the ChromeDriver is in PATH)
        self.driver = webdriver.Chrome()
        self.all_product_data = []

    def reorder_columns(self):
        """
        Reorders the DataFrame columns as per the required format.
        """
        df = pd.DataFrame(self.all_product_data)

        # Required columns in specific order
        ordered_columns = ['Scrape Date',
                           'Scrape Time', 'productName', 'PhonePlaceKenya_productLink']  # Added link here

        # Add other columns except 'Price 1' and 'Price 2'
        other_columns = [col for col in df.columns if col not in [
            'Scrape Date', 'Scrape Time', 'productName', 'PhonePlaceKenya_oldPrice', 'PhonePlaceKenya_Price', 'PhonePlaceKenya_Discount', 'PhonePlaceKenya_verifiedRatings', 'PhonePlaceKenya_productLink']]

        # Add 'Price 1' and 'Price 2' at the end
        ordered_columns += other_columns + \
            ['PhonePlaceKenya_verifiedRatings', 'PhonePlaceKenya_oldPrice', 'PhonePlaceKenya_Price',
             'PhonePlaceKenya_Discount']  # Ensure link is included

        # Reorder the DataFrame
        df_reordered = df[ordered_columns]
        return df_reordered

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
                    if 'PhonePlaceKenya_oldPrice' not in product_info:
                        # First price
                        product_info['PhonePlaceKenya_oldPrice'] = line.strip()
                    else:
                        # Second price
                        product_info['PhonePlaceKenya_Price'] = line.strip()
        if product_info == {}:
            product_info = text

        return product_info

    def scrape_phones_data(self, category):
        """
        Scrapes product data dynamically for a given phone type from PhonePlace Kenya website.
        The category is scraped directly from the webpage.
        """
        # Base URL
        if category in ["samsung", "apple", "mobile-phone-accessories", "audio", "gaming"]:
            url = f"https://www.phoneplacekenya.com/product-brand/{category}/"
        else:
            url = f"https://www.phoneplacekenya.com/product-category/smartphones/{category}/"

        self.driver.get(url)

        try:
            # Wait for the search results to load
            phones_grid = WebDriverWait(self.driver, 20).until(
                EC.presence_of_all_elements_located(
                    (By.CLASS_NAME, "product-wrapper"))
            )

            # Loop through each product element
            for i, product in enumerate(phones_grid):
                try:
                    # Re-locate product wrapper in case of stale reference
                    phones_grid = WebDriverWait(self.driver, 20).until(
                        EC.presence_of_all_elements_located(
                            (By.CLASS_NAME, "product-wrapper"))
                    )

                    product = phones_grid[i]  # Access product element by index

                    # Extract the product link before clicking
                    product_link_element = product.find_element(
                        By.TAG_NAME, 'a')
                    product_link = product_link_element.get_attribute('href')

                    product.click()  # Click on the product

                    # Wait for the product details to load (single element)
                    phone_info = WebDriverWait(self.driver, 20).until(
                        EC.presence_of_element_located(
                            (By.CLASS_NAME, "product-images-summary"))
                    )

                    # Product information
                    product_name = phone_info.find_element(
                        By.CSS_SELECTOR, ".product_title.entry-title").text

                    data = phone_info.find_element(
                        By.CSS_SELECTOR, ".summary.entry-summary").text

                    # Extract the information and append to the list
                    product_data = self.extract_info(data)
                    # Add product name to the data
                    product_data['productName'] = product_name

                    # Add the product link to the data
                    product_data['PhonePlaceKenya_productLink'] = product_link

                    # Add the current date and time to the product data
                    product_data['Scrape Date'] = datetime.now().strftime(
                        "%Y-%m-%d")  # Date
                    product_data['Scrape Time'] = datetime.now().strftime(
                        "%H:%M:%S")  # Time

                    # Scrape the category from the page (breadcrumb or tag section)
                    try:
                        category_element = phone_info.find_element(
                            By.CSS_SELECTOR, ".cat-links a").text
                        # Add the scraped category
                        product_data['Category'] = category_element
                        if category_element.lower() == category:
                            product_data['Category'] = f"{category_element} Phones"

                    except:
                        # If category is not found
                        product_data['Category'] = "Unknown"

                    # Extract discount percentage (if available)
                    try:
                        discount_percent = phone_info.find_element(
                            By.CLASS_NAME, "onsale.percent").text

                        product_data['PhonePlaceKenya_Discount'] = discount_percent
                    except:
                        product_data['PhonePlaceKenya_Discount'] = "No Discount"

                    # Extract verifiedRatings (if available)
                    try:
                        verifiedRatings = phone_info.find_element(
                            By.CLASS_NAME, "review-count").text

                        product_data['PhonePlaceKenya_verifiedRatings'] = verifiedRatings
                    except:
                        product_data['PhonePlaceKenya_verifiedRatings'] = 0

                    self.all_product_data.append(product_data)

                    time.sleep(2)  # Pause before navigating back
                    self.driver.back()  # Go back to the previous page
                    time.sleep(2)

                except Exception as e:
                    print(f"Error occurred on product {i+1}: {e}")

        except TimeoutException as e:
            print(f"Failed to load product grid: {e}")

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

    def run(self):
        categorys = ["nokia"]
        for category in categorys:
            self.scrape_phones_data(category)

        final_df = self.reorder_columns()

        self.close_driver()

        return final_df

    # Reorder columns, save data to CSV, and other methods remain the same...


# Example usage
if __name__ == "__main__":
    # Create an instance of the class
    scraper = PhonePlaceKenyaScraping()

    # List of phone types to scrape (you no longer need to define the category manually)
    categorys = ["nokia"]

    # Loop through the product types and scrape data
    for category in categorys:
        scraper.scrape_phones_data(category)

    # Reorder the columns and get the final DataFrame
    final_df = scraper.reorder_columns()
    print(final_df.sample(3))

    # Save the DataFrame to CSV
    scraper.save_data_to_csv(
        final_df, r'D:\freelance\FairPriceKe-add_llm\FairPriceKe\FairPriceKe\data\Phone Place Kenya Scraping\row\scraped_phones_with_datetime2.csv')

    # Close the browser after scraping
    scraper.close_driver()
