import { JumiaScraper } from './scrapers/jumiaScraper.js';
// This part controls the scraping process.
// It uses the browser instance to control the pageScraper.js file, which is
// where all the scraping scripts execute.
async function scrapeAll (browserInstance) {
  let browser;
  try {
    
    browser = await browserInstance;
    let data = {}

    // Instantiate Jumiascraper
    const jumiaScraper = new JumiaScraper(100);
    /* const category = 'phones-tablets' */
    data.phones_tablets = await jumiaScraper.scrape(browser, 'phones-tablets');
    await browser.close()
    console.log(data)
    return data
  } catch (err) {
    console.log('Could not resolve the browser instance => ', err);
  }
}

/* exporting a function that takes a browser instance and passes it to a function */

export default (browserInstance) => scrapeAll(browserInstance);
