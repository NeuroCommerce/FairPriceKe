import BaseScraper from './baseScraper.js';

export class JumiaScraper extends BaseScraper {
  /* url: 'https://www.jumia.co.ke/' */
  constructor () {
    super();
    this.url = 'https://www.jumia.co.ke/';
    this.userAgents = [
      'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.3',
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.3',
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.',
      'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.'
    ]
  }

  // Selecting a random agent
  getRandomUserAgent() {
    return this.userAgents[Math.floor(Math.random() * this.userAgents.length)]
  }

  // Added a delay(ms) method that returns a Promise that resolves after a specified
  // number of milliseconds.
  async delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms))
  }

  // Verifying User Agents Changes
  async setRandomUserAgent(page) {
    const userAgent = this.getRandomUserAgent()
    await page.setUserAgent(userAgent)
    console.log(`Set user agent: ${userAgent}`)
  }

  async scrape (browser, category) {
    let page;
    page = await browser.newPage();

    // Set a random user agent
    await this.setRandomUserAgent(page)
    console.log(`Navigating to ${this.url}...`);
    try {
      //  ensure pages are fully loaded before scraping.
      await page.goto(this.url, { waitUntil: 'networkidle0', timeout: 60000 });

      // Add a delay after loading the main page
      await this.delay(2000 + Math.random() * 2000) // Random delay betweeb 2-4 seconds

      // Checkpoint 1: Verify homepage loaded
      await this.verifyCheckpoint(page, `a[href="/${category}/"]`, 'Homepage loaded successfully');

      // Get all brand links in the Best Sellers SmartPhones section
      const brandLinks = await this.getBrandLinks(page)
      console.log(`Found ${brandLinks.length} brands in Best Sellers Smartphones`);

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

        // Add a delay between brand scrapes
        await this.delay(3000 + Math.random() * 3000) // Random between 3-6 seconds
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

    // Set a random user agent for each brand
    await this.setRandomUserAgent(page)
    console.log(`navigating to ${url}...`)
    await page.goto(url, { waitUntil: 'networkidle0'})

    await this.delay(2000 + Math.random() * 2000) // Random between 2-4 seconds
    let scrapedData = []

    async function scrapeCurrentPage() {
      console.log('Waiting for the section containing the articles')
      try {
       await page.waitForSelector('section.card.-fh') 
      } catch (error) {
        console.log('Timeout waiting for section.card.-fh. Page might not have loaded correctly.')
        console.log('Current page URL:', page.url())

        // Log the page content for debugging
        const pageContent = await page.content()
        console.log('Page content:', pageContent)

        return  // Exit the function if we can't find the section
      }
      
      

      const productsLinks = await page.evaluate(() => {
        const products = Array.from(document.querySelectorAll('article.prd._fb.col.c-prd'))
        console.log('Number of products found:', products.length)
        return products.map(product => {
          const link = product.querySelector('a.core')
          console.log('Product link:', link ? link.href : 'No link found')
          return link ? link.href : null
        }).filter(link => link !== null)
      })

      console.log(`Found ${productsLinks.length} products on this page`)

      if (productsLinks.length === 0) {
        console.log('No products found. Checking page structure...')
        await page.evaluate(() => {
          console.log('Page title:', document.title)
        })
      }

      for (let link of productsLinks) {
        let currentPageData = await this.scrapeProductPage(browser, link)
        // Add a delay between product scrapes
        await this.delay(500 + Math.random() * 500); 
        scrapedData.push(currentPageData)
      }

      // Check for next page
      let nextButtonExist = false
      try {
        const nextButton = await page.$eval('a.pg[aria-label="Next Page"]', a => a.textContent)
        nextButtonExist = nextButton.includes('Next')
      } catch (err) {
        nextButtonExist = false
      }

      if (nextButtonExist) {
        console.log('Moving to next page...')
        await page.click('a.pg[aria-label="Next Page"]')
        await this.delay(2000 + Math.random() * 2000); // Random delay between 2-4 seconds
        await scrapeCurrentPage()  // call the function recursively
      }
      

     

    }
    await scrapeCurrentPage()
    return scrapedData


  }

  async scrapeProductPage(browser, url) {
    let newPage = await browser.newPage()
    // Set  a random user agent for each product page
    await this.setRandomUserAgent(newPage)
    await newPage.goto(link)
    await this.delay(1000 + Math.random() * 1000)
    try {
      const dataObj = await newPage.evaluate(() => {
        return {
          /* dataObj.productName = await newPage.$eval('h1.-fs20 -pts -pbxs', el => el.textContent.trim()) */
          productName: document.querySelector('h1.-fs20 -pts -pbxs')?.textContent.trim() || 'N/A'
        } 
      })
      console.log('Scraped product data:', dataObj)
      return dataObj
    } catch (error) {
      console.log(`Error scraping product ${url}: ${e.message}`)
      return {}
    } finally {
      await newPage.close()
    }
  }
}


