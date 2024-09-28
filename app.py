import streamlit as st
import pandas as pd
from modules.phone_place_kenya_scraping import PhonePlaceKenyaScraping  # Import your scraping class

# Streamlit App Setup
st.title('Phone Scraper - PhonePlace Kenya')

# Instructions
st.write("""
    Select the phone types you want to scrape from PhonePlace Kenya.
    After selecting, click 'Scrape' to begin.
""")

# List of phone types
phone_types = ["samsung", "iphone", "infinix-phones-in-kenya", 
               "google", "itel", "nokia", 
               "oppo", "oneplus", "realme", 
               "tecno", "vivo", "xiaomi"]

# Multiselect for phone types
selected_phones = st.multiselect("Select phone types to scrape:", phone_types)

# Button to start scraping
if st.button('Scrape'):
    # Check if any phone types are selected
    if selected_phones:
        # Create an instance of the scraper class
        scraper = PhonePlaceKenyaScraping()
        
        # Display a progress message
        st.info(f"Scraping data for: {', '.join(selected_phones)}... This might take a few minutes.")
        
        # Perform scraping for each selected phone type
        for phone in selected_phones:
            scraper.scrape_phones_data(phone)
        
        # Reorder columns and get the final DataFrame
        scraped_df = scraper.reorder_columns()
        
        # Close the WebDriver
        scraper.close_driver()

        # Display the DataFrame in Streamlit
        st.write("Scraping completed successfully. Here's the data:")
        st.dataframe(scraped_df)

        # Option to download the DataFrame as CSV
        csv = scraped_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='scraped_phones_data.csv',
            mime='text/csv'
        )
    else:
        st.warning("Please select at least one phone type to scrape.")
