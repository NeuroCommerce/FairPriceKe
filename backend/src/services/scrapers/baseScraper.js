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


  async saveTimeSeriesCheckpoint(brandName, newData) {
	  // Get current date
	  const now = new Date()
	  const year = now.getFullYear()
	  const month = String(now.getMonth() + 1).padStart(2, '0')
	  const day = String(now.getDate()).padStart(2, '0')
	  const dateString = `${year}-${month}-${day}`

	  // Create brand-specific directory name
	  const brandDir = brandName.replace(/\s+/g, '_').toLowerCase()

	  // Create new filename with date
	  const filename = `${dateString}_${brandDir}_products.json`

	  // Create full path including time_series_checkpoints, brand, and year directories
	  const fullPath = path.resolve('time_series_checkpoints', brandDir, String(year), filename)

	  // Ensure the directory exists
	  await fs.mkdir(path.dirname(fullPath), { recursive: true });

	  // Validate newData
	  if (!Array.isArray(newData)) {
		  throw new Error('newdata must be an array')
	  }  

	  const timestamp = new Date().toISOString()  // Define timestamp here
	  const dataWithTimestamp = newData.map(item => ({
		  ...item,
		  timestamp,
	  }))

	  try {
		  await fs.writeFile(fullPath, JSON.stringify(dataWithTimestamp, null, 2))
		  console.log(`Time series checkpoint saved: ${fullPath}`);
	  }  catch (error) {
		  console.error(`Failed to save time series checkpoint: ${fullPath}`);
		  console.error(error);
	  }
  }
}


