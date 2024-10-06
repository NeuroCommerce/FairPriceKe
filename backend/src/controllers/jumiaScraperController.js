import {scrapeJumiaService} from '../services/jumiaScraperService.js'

export const scrapeJumia = async (req, res) => {
  const { category } = req.body

  try {
	const results = await scrapeJumiaService(category)
	if (results.length === 0) {
		if (category) {
			return res.status(404).json({ error: `No data found for brand: ${category}`})
		} else {
			return res.status(404).json({ error: 'No data found'})
		}
	}
	res.json({ results })
  } catch(error) {
	  console.error('Error during scraping:', error)
	  res.status(500).json({ error: 'An error occurred during scraping'})
  }
}

export const healthCheck = (req, res) => {
  res.status(200).json({ status: 'OK' })
}
