import BaseScraper from './baseScraper.js';
import RateLimiter from './rateLimiter.js'
import path from 'path'

export class JumiaScraper extends BaseScraper {
  /* url: 'https://www.jumia.co.ke/' */
  constructor (userRequestLimit) {
    super();
    this.url = 'https://www.jumia.co.ke/';
    this.userAgents = [
      'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.3',
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.3',
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.',
      'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.'
    ]
    const maxAllowedRequests = 200
    this.rateLimiter = new RateLimiter(maxAllowedRequests, userRequestLimit)
  }
  async makeRequest(url, options = {}) {
	  await this.rateLimiter.waitForSlot()
	  console.log(`Making request to ${url}`)
	  // Simulating a request
	  await this.delay(500 + Math.random() * 500)
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
      await this.makeRequest(this.url)
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

	// Save checkpoint after each brand is scraped
	const checkpointFilename = path.join('checkpoints', `${brand.name.replace(/\s+/g, '_').toLowerCase()}_products.json`)
	await this.saveCheckpoint(checkpointFilename, brandData)
	console.log(`Saved checkpoint for ${brand.name}`)
	
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
    await this.makeRequest(this.url)
    await page.goto(url, { waitUntil: 'networkidle0'})

    /* await this.delay(2000 + Math.random() * 2000)  */// Random between 2-4 seconds
    let scrapedData = []

    const scrapeCurrentPage = async () => {
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
        try {
         let currentPageData = await this.scrapeProductPage(browser, link)
         // Add a delay between product scrapes
          /* await this.delay(500 + Math.random() * 500); */ 
          scrapedData.push(currentPageData) 
        } catch (error){
          console.error(`Error scraping ${link}:`, error)
        }
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
    await page.close()  // Close the page after scraping to prevent memory leaks
    return scrapedData


  }

  async scrapeProductPage(browser, url) {
    let newPage = await browser.newPage()
    // Set  a random user agent for each product page
    await this.setRandomUserAgent(newPage)
    console.log(`Navigating to product page: ${url}`);
    
    
    try {
      await this.makeRequest(this.url)
      await newPage.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 })
      await this.delay(2000 + Math.random() * 2000)

      // Wait for the product name to be visible
      await newPage.waitForSelector('h1.-fs20.-pts.-pbxs', {timeout: 10000})
      const dataObj = await newPage.evaluate(() => {
        const getTextContent = (selector) => {
          // Simplifies text extraction and handle cases where element might not exist
          const element = document.querySelector(selector)
          return element ? element.textContent.trim() : 'N/A'
        }

        const getAllProductImages = () => {
          const imageLinks = document.querySelectorAll('#imgs a.itm')
          return Array.from(imageLinks).map(link => {
            const img = link.querySelector('img')
            return {
              largeImageUrl: link.href,
              thumbnailUrl: img.dataset.src || img.src,
              alt: img.alt
            }
          })
        }

        const productImages = getAllProductImages()
        return {
          productName: getTextContent('h1.-fs20.-pts.-pbxs'),
          price: getTextContent('span.-b.-ubpt.-tal.-fs24'),
          oldPrice: getTextContent('span.-tal.-gy5.-lthr.-fs16'),
          discount: getTextContent('span.bdg._dsct._dyn.-mls'),
          rating: getTextContent('div.stars._m._al'),
          verifiedRatings: getTextContent('a.-plxs._more'),
          /* imageUrl: getImageSrc('a.itm img.-fw.-fh') */
          images: productImages,
          mainImageUrl: productImages.length > 0 ? productImages[0].thumbnailUrl : ''
        }
      })
      console.log('Scraped product data:', JSON.stringify(dataObj, null, 2))

      // Debugging information
      if (dataObj.productName === 'N/A') console.log('Warning: Unable to scrape product name.')
      if (dataObj.price === 'N/A') console.log('Warning: Unable to scrape price.')
      if (dataObj.oldPrice === 'N/A') console.log('Warning: Unable to scrape old price.')
      if (dataObj.discount === 'N/A') console.log('Warning: Unable to scrape discount.')
      if (dataObj.rating === 'N/A') console.log('Warning: Unable to scrape ratings.')
      if (dataObj.verifiedRatings === 'N/A') console.log('Warning: Unable to scrape verifiedRatings.')
      if (dataObj.imageUrl === 'N/A') console.log('Warning: Unable to scrape image url.')

      return dataObj
    } catch (error) {
      console.log(`Error scraping product ${url}: ${error.message}`)
      if (error.name === `Timeout`) {
        console.log('Attempting to retrieve partial data...')
        try {
          const partialData = await newPage.evaluate(() => {
            const getTextContent = (selector) => {
              // Simplifies text extraction and handle cases where element might not exist
               const element = document.querySelector(selector)
               return element ? element.textContent.trim() : 'N/A'
            }
            return {
              productName: getTextContent('h1.-fs20.-pts.-pbxs'),
              price: getTextContent('span.-b.-ltr.-tal.-fs24'),
              oldPrice: getTextContent('span.-tal.-gy5.-lthr.-fs16'),
              discount: getTextContent('span.bdg._dsct._dyn.-mls'),
              rating: getTextContent('div.stars._m._al'),
              verifiedRatings: getTextContent('a.-plxs._more'),
              imageUrl: getImageSrc('img.-fw.-fw')
              // Add more fields as needed
            }
          })
          console.log('Partial data retrieved:', JSON.stringify(partialData, null, 2))
          return partialData
        } catch (innerError) {
          console.error('Failed to retrieve partial data:', innerError)
        }
      }
      console.log('Page content at time of error:')
      console.log(await newPage.content())
      return {}
    } finally {
      await newPage.close()
      
    }
  }
}


