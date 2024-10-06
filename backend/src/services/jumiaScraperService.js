import puppeteer from 'puppeteer'
import { JumiaScraper } from './scrapers/jumiaScraper.js'
// const userRequestLimit = 50
// const jumiaScraper = new JumiaScraper
//
// export const scrapeJumiaService = async (category) => {
//   const browser = await puppeteer.launch({ headless: true })
//   try {
//     const results = await jumiaScraper.scrape(browser, category)
//   } finally {
//     await browser.close()
//   }
// }

// export const scrapeJumiaService = async (category) => {
//   console.log('scrapeJumiaService called with category:', category); // Debug log
// 	
//
//   const browser = await puppeteer.launch({
//     headless: true,
//     args: ['--no-sandbox', '--disable-setuid-sandbox']
//   });
//
//  /*  const scraper = new JumiaScraper(60); // Assuming 100 is your user request limit */
//   const scraper = new JumiaScraper(60); // Assuming 100 is your user request limit
//
//   // Load homepage and find all brands
//   const brands = await scraper.getBrandLinks(); // Function to get brand links
//   try {
//     console.log('Calling scraper.scrape with category:', category); // Debug log
//     const results = await scraper.scrape(browser, category);
//     console.log('Scraper returned results:', results.length); // Debug log
//     return results;
//   } finally {
//     await browser.close();
//   }
// };

// jumiaScraperService.js
// import { JumiaScraper } from './jumiaScraper.js';
//
async function getBrands() {
  const scraper = new JumiaScraper(60);
  /* const browser = await scraper.launchBrowser(); */
  const browser = await puppeteer.launch({ headless: true })
  const page = await browser.newPage();

  await scraper.setRandomUserAgent(page);
  await page.goto(scraper.url, { waitUntil: 'networkidle0', timeout: 60000 });

  const brands = await scraper.getBrandLinks(page);

  await browser.close();
  return brands;
}

async function scrapeBrandProducts(url) {
  const scraper = new JumiaScraper(60);
  /* const browser = await scraper.launchBrowser(); */
	const browser = await puppeteer.launch({ headless: true })
  
  const products = await scraper.scrapeBrandPage(browser, url);
  
  await browser.close();
  return products;
}

export const scrapeJumiaService = async (category) => {
  // Load homepage and find all brands
  const brands = await getBrands();

  let filteredBrands
  // Filter brands based on the provided category
  if (category && category.toLowerCase() !== 'all') {
    filteredBrands = brands.filter(brand => 
      brand.name.toLowerCase() === category.toLowerCase()
    );

    if (filteredBrands.length === 0) {
      console.log(`No brands found for category: ${category}`);
      return [];
    } 
  } else {
    filteredBrands= brands
  }

  let results = [];
  for (const brand of filteredBrands) {
    console.log(`Scraping products for brand: ${brand.name}`);
    const products = await scrapeBrandProducts(brand.url);
    results = results.concat(products);
  }

  return results;
};
