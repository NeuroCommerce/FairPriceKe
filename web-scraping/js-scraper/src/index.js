
import startBrowser from './browser.js';

import scrapeController from './pageController.js';
// Start the browser and create a browser instance
const browserInstance = await startBrowser();

// Pass the browser instance to the scraper controller
scrapeController(browserInstance);
