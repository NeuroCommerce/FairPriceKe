import fs from 'fs/promises';

export default class BaseScraper {
  async verifyCheckpoint (page, selector, message) {
    try {
      await page.waitForSelector(selector, { timeout: 60000 });
      console.log(`Checkpoint passed: ${message}`);
    } catch (error) {
      console.error(`Checkpoint failed: ${message}`);
      console.error(error);
      throw error;	// Re-throw the error to be caught in the main try-catch block
    }
  }

  async saveCheckpoint (filename, data) {
    try {
	            await fs.writeFile(filename, JSON.stringify(data, null, 2));
		    console.log(`Checkpoint data saved: ${filename}`);
	        } catch (error) {
	            console.error(`Failed to save checkpoint data: ${filename}`);
		    console.error(error);
	        }
  }
}


