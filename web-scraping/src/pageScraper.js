// creates a new page instance in the browser, and these page instances can
// do quite a few things.
// created a page instance and then used the page.goto() method to navigate to the url
const scraperObject = {
  url: 'https://www.jumia.co.ke/mlp-samsung-shop/',
  async scraper (browser) {
    const page = await browser.newPage();
    console.log(`Navigating to ${this.url}...`);
    await page.goto(this.url);

    // WAit for the required DOM to be rendered
    await page.waitForSelector('section.card.-fh', { timeout: 120000 });

    /* Get the details of all samsung smartphones within the specific section */
    const productList = await page.$$eval('section.card.-fh article.prd._fb.col.c-prd', products => {
      return products.map(product => ({
        name: product.querySelector('.name')?.innerText.trim(),
        price: product.querySelector('.prc')?.innerText.trim(),
        link: product.querySelector('a.core')?.href
      }));
    });
    console.log('Products found: `${productList.length}`');
    console.log(JSON.stringify(productList, null, 2));
    /* await browser.close() */
  }
};

export default scraperObject;
