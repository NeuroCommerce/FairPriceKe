import BaseScraper from './baseScraper.js';
import RateLimiter from './rateLimiter.js';
// Import other necessary modules


export class KilimallScraper extends BaseScraper {
  constructor (userRequestLimit) {
    super()
    this.url = 'https://www.kilimall.co.ke/'
    this.userAgents = [
      'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.3',
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.3',
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.',
      'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.'
    ];
    const maxAllowedRequests = 200;
    this.rateLimiter = new RateLimiter(maxAllowedRequests, userRequestLimit);
    this.brands = ['Samsung', 'XIAOMI', 'itel', 'TECNO', 'Infinix', 'VIVO', 'OPPO', 'Apple']
    this.siteName = 'Kilimall'
  }


  async makeRequest (url, options = {}) {
    await this.rateLimiter.waitForSlot();
    console.log(`Making request to ${url}`);
    // Simulating a request
    await this.delay(500 + Math.random() * 500);
  }

  // Added a delay(ms) method that returns a Promise that resolves after a specified
  // number of milliseconds.
  async delay (ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
    // Selecting a random agent
  getRandomUserAgent () {
    return this.userAgents[Math.floor(Math.random() * this.userAgents.length)];
  }

    // Verifying User Agents Changes
  async setRandomUserAgent (page) {
    const userAgent = this.getRandomUserAgent();
    await page.setUserAgent(userAgent);
    console.log(`Set user agent: ${userAgent}`);
  }

  async scrape(browser, category) {
    const page = await browser.newPage()

    // Set a random user agent
    await this.setRandomUserAgent(page)
    console.log(`Navigating to ${this.url}...`)
    // await browser.close()
    // console.log('Browser closed. Scraper finished')

    try {
      await this.makeRequest(this.url)

      //  ensure pages are fully loaded before scraping.
      await page.goto(this.url, { waitUntil: 'networkidle0', timeout: 60000 });

      console.log('Page loaded successfully')

      /* await this.navigateToPhoneCategory(page) */

      const categories = await this.getCategories(page)
      console.log('Categories found:', categories)

      const phonesCategories = categories.find(cat => cat.name === 'Phones & Accessories')

      if (phonesCategories) {
        console.log('Found Phones & Accessories category. Attempting to naviaget...')
        await this.navigateToCategory(page, phonesCategories.name)

        // Wait to ensure the page loaded
        /* await page.waitForTimeout(2000) */

        await this.delay(2000 + Math.random() * 2000);

        /* // Log the current URL to verify navigation
        const currentUrl = page.url()
        console.log('Current URL after naviagetion:', currentUrl)

        // Apply filters
        await this.applyFilters(page);

        // Extract product information
        const products = await this.extractProducts(page, browser)
        console.log('Extracted products:', products) */


        // Apply filters and scrape brand-wise
        const allProducts = await this.scrapeBrandWise(page, browser);
        console.log('All extracted products:', allProducts);

        // You can save the products to a file or database here
      }


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

    async getCategories(page) {
    console.log('Attempting to get all categories...');

    try {
      await page.waitForSelector('div.van-cell .base-category-item', { timeout: 10000 });

      const categories = await page.evaluate(() => {
        const categoryElements = Array.from(document.querySelectorAll('div.van-cell .base-category-item'));
        return categoryElements.map(cat => ({
          name: cat.querySelector('.category-name')?.textContent.trim() || 'Unknown',
        }));
      });

      console.log('Categories found:', categories);
      return categories;
    } catch (error) {
      console.error('Error getting categories:', error);
      return [];
    }
  }

   async navigateToCategory(page, categoryName) {
    console.log(`Attempting to navigate to category: ${categoryName}`);
    try {
      await page.waitForSelector('div.van-cell .base-category-item', { timeout: 10000 });
      
      // Use evaluate to find the correct element and get its index
      const categoryIndex = await page.evaluate((name) => {
        const categories = Array.from(document.querySelectorAll('div.van-cell .base-category-item'));
        return categories.findIndex(cat => 
          cat.querySelector('.category-name').textContent.trim() === name
        );
      }, categoryName);

      if (categoryIndex !== -1) {
        console.log(`Found "${categoryName}" at index ${categoryIndex}`);
        
        // Click on the category
        const categoryElements = await page.$$('div.van-cell .base-category-item');
        if (categoryElements[categoryIndex]) {
          await categoryElements[categoryIndex].click();
          console.log(`Clicked on "${categoryName}". Waiting for navigation to complete...`);
          
          // Wait for navigation to complete
          await page.waitForNavigation({ waitUntil: 'networkidle0', timeout: 30000 });
          
          // Log the current URL
          const currentUrl = await page.url();
          console.log(`Navigation complete. Current URL: ${currentUrl}`);

          // Optional: Take a screenshot for debugging
          await page.screenshot({ path: `after_${categoryName.replace(/\s+/g, '_')}_click.png` });
        } else {
          console.error(`Found index ${categoryIndex} but couldn't get the element`);
        }
      } else {
        console.log(`Category "${categoryName}" not found`);
        
        // Log all category names for debugging
        const allCategories = await page.evaluate(() => {
          return Array.from(document.querySelectorAll('div.van-cell .base-category-item .category-name'))
            .map(el => el.textContent.trim());
        });
        console.log('All categories found:', allCategories);
      }
    } catch (error) {
      console.error(`Error navigating to category ${categoryName}:`, error)
    }
   }


  /* async applyFilters(page, brand) {
    console.log(`Applying filters for ${brand}...`);
    try {
      // Wait for the filter container to be available
      await page.waitForSelector('.filter-info', { timeout: 15000 });

      let brandFilterClicked = false; // Define the variable outside the evaluate function

      // Implement a retry mechanism
      for (let attempt = 0; attempt < 3; attempt++) {
        brandFilterClicked = await page.evaluate((brandName) => {
          const filters = Array.from(document.querySelectorAll('.filter-value'));
          const brandFilter = filters.find(el => 
            el.textContent.toLowerCase().includes(brandName.toLowerCase())
          );

          if (brandFilter) {
            brandFilter.click();
            return true;
          }
          return false;
        }, brand);

        if (brandFilterClicked) {
          console.log(`Successfully clicked on ${brand} filter`);
          break;
        } else {
          console.log(`Filter for ${brand} not found. Retrying...`);
          await this.delay(2000); // Wait before retrying
        }
      }

      // If still not found, try alternative methods
      // For example, use the search function
      if (!brandFilterClicked) {
        console.log(`Attempting to use search function for ${brand}`);
        await page.type('.search-input', brand);
        await page.click('.search-button');
      }

      await this.delay(2000 + Math.random() * 2000); // Wait for the page to update
    } catch (error) {
      console.error(`Error applying filters for ${brand}:`, error);
    }

    // Whether successful or not, we continue with the scraping process
    console.log(`Continuing with scraping for ${brand}`);
  } */

  /* async applyFilters(page, brand) {
  console.log(`Applying filters for ${brand}...`);
  try {
    // Wait for filter container
    await page.waitForSelector('.filter-info', { timeout: 15000 });

    // First, check if we need to expand the brand list
    const expandBrands = async () => {
      const needsExpansion = await page.evaluate(() => {
        const viewMoreButton = Array.from(document.querySelectorAll('.filter-value'))
          .find(el => el.textContent.trim().toLowerCase() === 'view more');
        if (viewMoreButton) {
          viewMoreButton.click();
          return true;
        }
        return false;
      });

      if (needsExpansion) {
        console.log('Clicked "View More" to expand brand list');
        await this.delay(2000); // Wait for expansion animation
      }
    };

    // Try to expand the brand list first
    await expandBrands();

    // Now try to click the brand filter with retries
    let brandFilterClicked = false;
    for (let attempt = 0; attempt < 3; attempt++) {
      brandFilterClicked = await page.evaluate((brandName) => {
        const filters = Array.from(document.querySelectorAll('.filter-value'));
        const brandFilter = filters.find(el => 
          el.textContent.trim().toLowerCase() === brandName.toLowerCase()
        );
        if (brandFilter) {
          brandFilter.click();
          return true;
        }
        return false;
      }, brand);

      if (brandFilterClicked) {
        console.log(`Successfully clicked on ${brand} filter`);
        break;
      } else {
        console.log(`Filter for ${brand} not found. Attempt ${attempt + 1}/3`);
        await this.delay(2000);
      }
    }

    if (!brandFilterClicked) {
      console.log(`Could not find filter for ${brand} even after expanding`);
      // Log available filters for debugging
      const availableFilters = await page.evaluate(() => {
        return Array.from(document.querySelectorAll('.filter-value'))
          .map(el => el.textContent.trim());
      });
      console.log('Available filters:', availableFilters);
    }

    // Wait for filtered results to load
    await this.delay(3000);

  } catch (error) {
    console.error(`Error applying filters for ${brand}:`, error);
    console.log(`Continuing without filters for ${brand}`);
  }
} */

/*   async applyFilters(page, brand) {
  console.log(`Applying filters for ${brand}...`);
  try {
    // Wait for filter container
    await page.waitForSelector('.filter-info', { timeout: 15000 });

    // First, check if we need to expand the brand list
    const expandBrands = async () => {
      const needsExpansion = await page.evaluate(() => {
        const viewMoreButton = Array.from(document.querySelectorAll('.filter-value'))
          .find(el => {
            const text = el.textContent.trim().toLowerCase();
            console.log('Found button text:', text); // Debug log
            return text === 'view more';
          });
        if (viewMoreButton) {
          viewMoreButton.click();
          return true;
        }
        return false;
      });

      if (needsExpansion) {
        console.log('Clicked "View More" to expand brand list');
        await this.delay(2000); // Wait for expansion animation
      }
    };

    // Try to expand the brand list first
    await expandBrands();

    // Now try to click the brand filter with retries
    let brandFilterClicked = false;
    for (let attempt = 0; attempt < 3; attempt++) {
      // Log all filter values before attempting to match
      const filterDebugInfo = await page.evaluate(() => {
        const filters = Array.from(document.querySelectorAll('.filter-value'));
        return filters.map(el => ({
          text: el.textContent.trim(),
          innerHTML: el.innerHTML,
          classes: el.className
        }));
      });
      console.log('Available filters debug info:', JSON.stringify(filterDebugInfo, null, 2));

      brandFilterClicked = await page.evaluate((brandName) => {
        const filters = Array.from(document.querySelectorAll('.filter-value'));
        // Try different matching strategies
        const brandFilter = filters.find(el => {
          const elementText = el.textContent.trim();
          const searchText = brandName.trim();
          
          // Log each comparison for debugging
          console.log(`Comparing: "${elementText}" with "${searchText}"`);
          
          return (
            elementText.toLowerCase() === searchText.toLowerCase() ||
            elementText.toLowerCase().includes(searchText.toLowerCase()) ||
            searchText.toLowerCase().includes(elementText.toLowerCase())
          );
        });
        
        if (brandFilter) {
          console.log(`Found matching brand filter: ${brandFilter.textContent}`);
          brandFilter.click();
          return true;
        }
        return false;
      }, brand);

      if (brandFilterClicked) {
        console.log(`Successfully clicked on ${brand} filter`);
        break;
      } else {
        console.log(`Filter for ${brand} not found. Attempt ${attempt + 1}/3`);
        
        // Take a screenshot for debugging
        await page.screenshot({ 
          path: `debug_filters_attempt_${attempt + 1}.png`,
          fullPage: true 
        });
        
        await this.delay(2000);
      }
    }

    if (!brandFilterClicked) {
      console.log(`Could not find filter for ${brand} even after expanding`);
      
      // Get full page HTML for debugging
      const pageHtml = await page.evaluate(() => document.body.innerHTML);
      console.log('Full filter section HTML:', pageHtml.match(/<div class="filter-info"[\s\S]*?<\/div>/)?.[0] || 'Not found');
    }

    // Wait for filtered results to load
    await this.delay(3000);

  } catch (error) {
    console.error(`Error applying filters for ${brand}:`, error);
    console.log(`Continuing without filters for ${brand}`);
  }
} */

  async applyFilters(page, brand) {
  console.log(`Applying filters for ${brand}...`);

  try {
    // Wait for filter container
    await page.waitForSelector('.filter-info', { timeout: 15000 });

    // Check if the brand filter is available without clicking "View More"
    const brandFilterElement = await page.evaluate((brandName) => {
      const filters = Array.from(document.querySelectorAll('div[data-v-24abcad7].filter-value'));
      const brandFilter = filters.find(el => el.textContent.trim() === brandName);
      if (brandFilter) {
        brandFilter.click();
        return true;
      }
      return false;
    }, brand);

    if (brandFilterElement) {
      console.log(`Successfully clicked ${brand} filter`);
    } else {
      // If the brand filter was not found, click the "View More" button
      const viewMoreClicked = await page.evaluate(() => {
        const viewMoreButton = document.querySelector('div[data-v-24abcad7].show-more');
        if (viewMoreButton) {
          viewMoreButton.click();
          return true;
        }
        return false;
      });

      if (viewMoreClicked) {
        console.log('Clicked View More button');
        await this.delay(3000); // Increase delay to 3 seconds

        // Try to find and click the brand filter again
        const brandFilterElementAfterViewMore = await page.evaluate((brandName) => {
          const filters = Array.from(document.querySelectorAll('div[data-v-24abcad7].filter-value'));
          const brandFilter = filters.find(el => el.textContent.trim() === brandName);
          if (brandFilter) {
            brandFilter.click();
            return true;
          }
          return false;
        }, brand);

        if (brandFilterElementAfterViewMore) {
          console.log(`Successfully clicked ${brand} filter`);
        } else {
          console.log(`Could not find filter for ${brand}`);

          // Log available filters for debugging
          const availableFilters = await page.evaluate(() => {
            return Array.from(document.querySelectorAll('div[data-v-24abcad7].filter-value'))
              .map(el => el.textContent.trim());
          });
          console.log('Available filters:', availableFilters);
        }
      } else {
        console.log(`Could not find filter for ${brand}`);

        // Log available filters for debugging
        const availableFilters = await page.evaluate(() => {
          return Array.from(document.querySelectorAll('div[data-v-24abcad7].filter-value'))
            .map(el => el.textContent.trim());
        });
        console.log('Available filters:', availableFilters);
      }
    }

    // Wait for filtered results to load
    await this.delay(3000);
  } catch (error) {
    console.error(`Error applying filters for ${brand}:`, error);
    console.log(`Continuing without filters for ${brand}`);
  }
}

  async scrapeBrandWise(page, browser) {
    /* let allProducts = [] */

    for (const brand of this.brands) {
      console.log(`Starting to scrape ${brand} prodcuts...`)

      // Apply filters for the current brand
      await this.applyFilters(page, brand)

      // Extract products for the current brand
      const brandProducts = await this.extractProducts(page, browser, brand)
      console.log(`Extracted ${brandProducts.length} products for ${brand}`)

      // Add brand information to each product
      /* const productsWithBrand = brandProducts.map(product => ({
        ...product,
        brand: brand
      }))

      // Add to the overrall product list
      allProducts = allProducts.concat(brandProducts) */

      // Save the brand data using the new method
      await this.saveTimeSeriesCheckpoint(this.siteName, brand, brandProducts)

      // Remove filters before moving to the next brand
      await this.removeFilters(page)
    }

    return allProducts
  }

  async removeFilters(page) {
    console.log('Removing filters...')
    try {
      await page.evaluate(() => {
        const activeFilters = Array.from(document.querySelectorAll('div[data-v-24abcad7].filter-value-act'));
        activeFilters.forEach(filter => filter.click());
      });
      await this.delay(2000 + Math.random() * 2000)   // Wait for the page to update
    } catch (error) {
      console.error('Error removing filtes:', error)
    }
  }

  async extractProducts(page, browser, brand) {
    console.log('Extracting product information...')

    try {
      await page.waitForSelector('.product-item', { timeout: 1000 })

      const productsLinks = await page.evaluate(() => {
        const products = Array.from(document.querySelectorAll('.product-item'))
        console.log('Number of products found:', products.length)
        return products.map(product => {
          const link = product.querySelector('a')
          console.log('Product link:', link ? link.href : 'No link found')
          return link ? link.href : null
        }).filter(link => link !== null)
      })

      console.log(`Found ${productsLinks.length} products on this page`)
      /* return productsLinks */

      if (productsLinks.length === 0) {
        console.log('No products found. Checking page structure...');
        await page.evaluate(() => {
          console.log('Page title:', document.title);
        });
      }

      const scrapedData = []

      for (const link of productsLinks) {
        try {
          const productData = await this.scrapeProductPage(browser, link, brand)
          await this.delay(500 + Math.random() * 500)
          scrapedData.push(productData)

        } catch (error) {
          console.error(`Error scraping ${link}:`, error)
        }
      }

      return scrapedData
    } catch (error) {
      console.error(`Error extracting products:`, error)
      return []
    }
  }

  async scrapeProductPage(browser, url, brand) {
    const newPage = await browser.newPage()
    await this.setRandomUserAgent(newPage)
    console.log(`Navigating to product page: ${url}`)

    try {
      await this.makeRequest(url)
      await newPage.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 })
      await this.delay(2000 + Math.random() * 2000)

      const dataObj = await newPage.evaluate(() => {
        const getTextContent = (selector) => {
          // Simplifies text extraction and handle cases where element might not exist
          const element = document.querySelector(selector);
          return element ? element.textContent.trim() : 'N/A';
        };

        return {
          productName: getTextContent('.product-title')
        }
      })

      dataObj.brand = brand
      dataObj.url = url
      dataObj.timestamp = new Date().toISOString()

      console.log('Scraped product data:', dataObj)
      return dataObj
    } catch (error) {
      console.log(`Error scraping product ${url}: ${error.message}`)
      return {}
    } finally {
      await newPage.close()
    }
  }
}
