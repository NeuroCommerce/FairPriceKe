import requests
import json
import time
import schedule


class JumiaScraper:
    def __init__(self, url, category, headers, max_retries=5, retry_delay=60):
        self.url = url
        self.category = category
        self.headers = headers
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def scrape(self):
        data = {'category': self.category}
        for attempt in range(self.max_retries):
            try:
                # Send POST request
                response = requests.post(
                    self.url, headers=self.headers, data=json.dumps(data))

                # Check for successful response
                if response.status_code == 200:
                    results = response.json().get('results', [])
                    print(f"Scraped {len(results)} products:")
                    for product in results:
                        print(product)
                    break  # Exit the loop on success

                # Handle rate limiting (429 status code)
                elif response.status_code == 429:
                    print(
                        f"Rate limit exceeded. Retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)

                # Handle other errors
                else:
                    error_message = response.json().get('error', 'Unknown error')
                    print(f"Error {response.status_code}: {error_message}")
                    break

            except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")
                break
        else:
            print("Max retries exceeded. Please try again later.")

# Job to run every 24 hours


def run_scraper(category):
    # Create an instance of the scraper
    scraper = JumiaScraper(
        url='http://localhost:3000/api/jumia/scrape',
        category=category,
        headers={'Content-Type': 'application/json'}
    )
    # Call the scrape method
    scraper.scrape()


# Schedule the scraper to run every 24 hours
schedule.every(24).hours.do(run_scraper)

if __name__ == "__main__":
    # Run the scheduled tasks
    print("Starting the scraper. It will run every 24 hours.")
    while True:
        schedule.run_pending('infinix')
        time.sleep(60)  # Wait 1 minute before checking again
