import requests
import json
import time
import schedule
from datetime import datetime


class JumiaScraper:
    def __init__(self, url, category, headers, max_retries=5, retry_delay=60):
        self.url = url
        self.category = category
        self.headers = headers
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def save_to_file(self, results):
        # Get the current timestamp to create a unique file name
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'D:\freelance\FairPriceKe-add_llm\FairPriceKe\FairPriceKe\data\Jumia\row\jumia_scraped_data_{self.category}_{timestamp}.json'

        # Save the results to a JSON file
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=4)

        print(f"Data saved to {filename}")

    def scrape(self):
        # A dictionary to hold the overall result
        response_data = {
            'category': self.category,
            'status': None,
            'error': None,
            'products': [],
            'total_scraped': 0
        }

        data = {'category': self.category}
        for attempt in range(self.max_retries):
            try:
                # Send POST request
                response = requests.post(
                    self.url, headers=self.headers, data=json.dumps(data))

                # Check for successful response
                if response.status_code == 200:
                    results = response.json().get('results', [])
                    response_data['status'] = 'success'
                    response_data['products'] = results
                    response_data['total_scraped'] = len(results)

                    # Print the products for feedback
                    print(f"Scraped {len(results)} products:")

                    # for product in results:
                    #     print(product)

                    # Save results to a file
                    self.save_to_file(response_data)
                    break  # Exit the loop on success

                # Handle rate limiting (429 status code)
                elif response.status_code == 429:
                    print(
                        f"Rate limit exceeded. Retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)

                # Handle other errors
                else:
                    error_message = response.json().get('error', 'Unknown error')
                    response_data['status'] = 'error'
                    response_data['error'] = f"Error {response.status_code}: {error_message}"
                    print(f"Error {response.status_code}: {error_message}")
                    break

            except requests.exceptions.RequestException as e:
                response_data['status'] = 'error'
                response_data['error'] = f"RequestException: {str(e)}"
                print(f"An error occurred: {e}")
                break
        else:
            response_data['status'] = 'error'
            response_data['error'] = "Max retries exceeded. Please try again later."

        return response_data


# Job to run every 24 hours
def run_scraper(category):
    # Create an instance of the scraper
    scraper = JumiaScraper(
        url='http://localhost:3000/api/jumia/scrape',
        category=category,
        headers={'Content-Type': 'application/json'}
    )
    # Call the scrape method and get the JSON response
    result = scraper.scrape()
    return json.dumps(result)


# Schedule the scraper to run every 24 hours
schedule.every(24).hours.do(run_scraper, 'all')

if __name__ == "__main__":
    result = run_scraper('all')
    print(json.dumps(result, indent=4))  # Print the result in a formatted way
