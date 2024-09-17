import BaseScraper from './baseScraper.js';

export class JumiaScraper extends BaseScraper {
  /* url: 'https://www.jumia.co.ke/' */
  constructor () {
    super();
    this.url = 'https://www.jumia.co.ke/';
  }

  async scrape (browser, category) {
    let page;
    page = await browser.newPage();
    console.log(`Navigating to ${this.url}...`);
    try {
      //  ensure pages are fully loaded before scraping.
      await page.goto(this.url, { waitUntil: 'networkidle0', timeout: 60000 });

      // Checkpoint 1: Verify homepage loaded
      await this.verifyCheckpoint(page, `a[href="/${category}/"]`, 'Homepage loaded successfully');

      // Get all brand links in the Best Sellers SmartPhones section
      const brandLinks = await this.getBrandLinks(page)
      /* console.log(`Found ${brandLinks.length} brands in Best Sellers Smartphones`); */

      await this.saveCheckpoint('brandLinks.json', brandLinks);
      console.log('Brand links saved');



      if (brandLinks.length === 0) {
        console.log('No brands found. Exiting scraper.');
        return
      }

      console.log('Brands found. Starting to scrape individual brand pages...')
      let allProductData = []

      // This is where we would start scraping individual brand pages
      // For now, let's just log that we've reached this point
      console.log('Ready to start scraping individual brand pages');
      for (const brand of brandLinks) {
        console.log(`Would scrape brand: ${brand.name} at URL: ${brand.url}`);
        const brandData = await this.scrapeBrandPage(browser, brand.url)
        allProductData.push(...brandData)
      }

      await this.saveCheckpoint('allProductData.json', allProductData)
      console.log(`Scraped ${allProductData.length} products in total.`)

      return allProductData
    } catch (error) {
      console.error('An error occurred during scraping:', error);
    } finally {
      console.log('Closing browser...');
      if (page) {
        await page.close();
      }

      await browser.close();
      console.log('Browser closed. Scraper finished');
    }
  }

  async getBrandLinks(page) {
    return page.evaluate(() => {
        // Array.from method creates a new, shallow-copied Array instance from an iterable object
        const bestSellerSection = Array.from(document.querySelectorAll('.sub .cat')).find(
          cat => cat.querySelector('.tit')?.textContent.trim() === 'Best Sellers Smartphones'
        );
        if (!bestSellerSection) {
          console.log('Best Sellers Smartphones section not found');
          return [];
        }

        const links = Array.from(bestSellerSection.querySelectorAll('.s-itm')).map(link => ({
          name: link.textContent.trim(),
          url: link.href
        }));
        console.log(`Found ${links.length} brands in Best Sellers Smartphones`);
        return links;
      });
  }

  async scrapeBrandPage(browser, url) {
    let page = await browser.newPage()
    console.log(`navigating to ${url}...`)
    await page.goto(url, { waitUntil: 'networkidle0'})
    let scrapedData = []

    async function scrapeCurrentPage() {
      await page.waitForSelector('section.card.-fh')
      console.log('Waiting for the section containing the articles')

      let productLinks = await page.evaluate('article.prd._fb.col.c-prd', products => {
        return products.map(product => product.querySelector('a.core').href)
      })

      let pagePromise = (link) => new Promise(async(resolve, reject) => {
        let dataObj = {}
        let newPage = await browser.newPage()
        await newPage.goto(link)
        try {
          dataObj.productName = await newPage.$eval('h1.-fs20 -pts -pbxs', el => el.textContent.trim())
        } catch (error) {
          console.log(`Error scraping product ${link}: ${e.message}`)
        }

        resolve(dataObj)
        await newPage.close()
      })

      for (link of productLinks) {
        let currentPageData = await pagePromise(link)
        scrapeData.push(currentPageData)
      }

      let nextButtonExist = false
      try {
        const nextButton = await page.$eval('a.pg[aria-label="Next Page"]', a => a.textContent)
        nextButtonExist = nextButton.includes('Next')
      } catch (err) {
        nextButtonExist = false
      }

      if (nextButtonExist) {
        await page.click('a.pg[aria-label="Next Page"]')
        return scrapeCurrentPage()
      }

      return scrapeData
    }

    let data = await scrapeCurrentPage()
    await page.close()
    return data
  }
}


