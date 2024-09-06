const BaseScraper = require('./baseScraper')

class JumiaScraper extends BaseScraper {
	url: 'https://www.jumia.co.ke/'
	constructor() {
		super();
		this.url = 'https://www.jumia.co.ke/'
	}

	async scrape(browser) {
		let page;
		try {
			let page = await browser.newPage();
			console.log(`Navigating to ${this.url}...`)

			//  ensure pages are fully loaded before scraping.
			await page.goto(this.url, {waitUntil: 'networkidle0', timeout: 60000});

			// Checkpoint 1: Verify homepage loaded
			await this.verifyCheckpoint(page, 'a[href="/phones-tablets/"]', 'Homepage loaded successfully');

			// Navigate to phones & Tablets
			await page.hover('a[href="/phones-tablets/"]');

			// Checkpoint 2: Verify popup menu appeared
			await this.verifyCheckpoint(page, '.flyout', 'Popup menu appeared successfully')

			// Get all brand links in the Best Sellers SmartPhones section
			// const brandLinks = await page.$$eval('.flyout .cat:has(.tit:contains("Best Sellers Smartphones")) .s-itm', links => {
			// 	links.map(link => ({ name: link.textContent.trim(), url: link.href}))
			// });
			const brandLinks = await page.evaluate(() => {
				// Array.from method creates a new, shallow-copied Array instance from an iterable object
				const bestSellerSection = Array.from(document.querySelectorAll('.sub .cat')).find(
					cat => cat.querySelector('.tit')?.textContent.trim() === 'Best Sellers Smartphones'
				)
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
			})

			console.log(`Found ${brandLinks.length} brands in Best Sellers Smartphones`)

			await this.saveCheckpoint('brandLinks.json', brandLinks)

			if (brandLinks.length === 0) {
				console.log('No brands found. Exiting scraper.')
			} else {
				console.log('Brands found and saved. Scraping complete.')
			}


		} catch (error) {
			console.error('An error occurred during scraping:', error)
		} finally {
			console.log('Closing browser...')
			if (page) {
				await page.close();
			}

			await browser.close();
			console.log('Browser closed. Scraper finished')
		}
	}
}
