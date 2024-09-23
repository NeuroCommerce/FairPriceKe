import puppeteer from 'puppeteer-core';

/* Start with browser.js; this file will contain the script that starts your browser. */
async function startBrowser () {
  let browser;
  try {
    console.log('Opening the browser......');

    /* launch() method that launches an instance of a browser.This method returns a Promise */
    browser = await puppeteer.launch({
      executablePath: '/usr/bin/chromium-browser',
      headless: false,
      args: ['--disable-setuid-sandbox'],
      ignoreHTTPSErrors: true
    });
  } catch (err) {
    console.log('Could not create a browser instance => : ', err);
  }
  return browser;
}

export default startBrowser;
