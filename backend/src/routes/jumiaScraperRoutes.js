import express from 'express'
import { scrapeJumia, healthCheck } from '../controllers/jumiaScraperController.js'

const router = express.Router()

router.post('/scrape', scrapeJumia)
router.get('/health', healthCheck)

export default router
