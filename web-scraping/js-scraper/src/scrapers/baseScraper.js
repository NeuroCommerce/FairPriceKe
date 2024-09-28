import fs from 'fs/promises';
import path from 'path'

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

  async saveTimeSeriesCheckpoint(filename, newData) {
    const fullPath = path.join('time_series_checkpoints', filename)
    let existingData = []

    // Validate newData
    if (!Array.isArray(newData)) {
      throw new Error('newdata must be an array')
    }
    try {
      const fileContent = await fs.readFile(fullPath, 'utf8')
      existingData = JSON.parse(fileContent)
    } catch (error) {
      // File doesn't exist
    }

   /*  const timestamp = new Date().toISOString() */
    const dataWithTimestamp = newData.map(item => ({
      ...item,
      timestamp,
    }))

    const updatedData = [...existingData, ...dataWithTimestamp]
    await fs.writeFile(fullPath, JSON.stringify(updateddata, null, 2))
  }

}


