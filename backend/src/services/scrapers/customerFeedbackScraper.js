const extractNumber = (text) => {
  const match = text.match(/\d+(\.\d+)?/)
  return match ? parseFloat(match[0]) : null
}

// Custom delay function
const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

const scrapeCustomerFeedback = async(page) => {
  const SELECTORS = {
    FEEDBACK_SECTION: 'section.card.aim.-mtm',
    OVERALL_RATING: 'div.-fs29.-yl5.-pvxs span.-b',
    TOTAL_RATINGS: 'p.-fs16.-pts',
    RATING_BREAKDOWN: 'ul.-ptxs.-mts.-pbm li',
    REVIEW_ITEMS: 'article.-pvs.-hr._bet',
    SEE_ALL_LINK:'a.btn._def._ti.-mhs.-fsh0[href*="/catalog/productratingsreviews/"]',
    REVIEW_DATE_AUTHOR: 'div.-pvs',
    VERIFIED_PURCHASE: 'div.-df.-i-ctr.-gn5.-fsh0'
  }

  try {
    const feedbackSection = await page.$(SELECTORS.FEEDBACK_SECTION)
    if (!feedbackSection) {
      console.log('Feedback section not found.')
      return null
    }
    const result = {
      overallRating: null,
      totalRatings: null,
      ratingBreakdown: {},
      reviews: [],
      seeAllUrl: null
    }

    // Scrape overall rating and total ratings
    result.overallRating = await page.$eval(SELECTORS.OVERALL_RATING, el => {
      const extractNumber = (text) => {
	const match = text.match(/\d+(\.\d+)?/)
	return match ? parseFloat(match[0]) : null
      }
      return extractNumber(el.textContent)
    })
      
    result.totalRatings = await page.$eval(SELECTORS.TOTAL_RATINGS, el => {
      const extractNumber = (text) => {
	const match = text.match(/\d+(\.\d+)?/)
	return match ? parseFloat(match[0]) : null
      }
      return extractNumber(el.textContent)
    })
      
  
    // Scrape rating breakdown
    result.ratingBreakdown = await page.$$eval(SELECTORS.RATING_BREAKDOWN, items => {
	    const extractNumber = (text) => {
		    const match = text.match(/\d+(\.\d+)?/)
		    return match ? parseFloat(match[0]) : null
	    }
	return Array.from(items).reduce((acc, item) => {
		const [stars, countElement] = item.querySelectorAll('svg, p.-gy5.-mw-34.-r')
		const key = stars.previousSibling.textContent.trim()
		const count = extractNumber(countElement.textContent)
		acc[key] = count
		return acc
	}, {})    
    })   
    
    const reviews = await page.$$eval(SELECTORS.REVIEW_ITEMS, (items, SELECTORS) => {
	    const extractNumber = (text) => {
		    const match = text.match(/\d+(\.\d+)?/)
		    return match ? parseFloat(match[0]) : null
	    }
	    const extractReviewData = (review) => {
		    try {
			    const dateAuthorElement = review.querySelector(SELECTORS.REVIEW_DATE_AUTHOR)
			    const dateSpan = dateAuthorElement.querySelector('span.-prs')
			    const authorSpan = dateAuthorElement.querySelector('span:last-child')
			    return {
				    rating: extractNumber(review.querySelector('div.stars._m._al').textContent),
				    title: review.querySelector('h3.-m.-fs16.-pvs').textContent.trim(),
				     content: review.querySelector('p.-pvs').textContent.trim(),
				     date: dateSpan ? dateSpan.textContent.trim() : null,
				     author: authorSpan ? authorSpan.textContent.replace('by ', '').trim() : null,
				     verifiedPurchase: !!review.querySelector(`${SELECTORS.VERIFIED_PURCHASE} svg.ic.-f-gn5`)
			     }
		     } catch (error) {
			     console.error(`Error extracting review data:`, error)
			     return null
		     }
	    }

	    return items.map(review => extractReviewData(review)).filter(Boolean)
    }, SELECTORS)
    result.reviews.push(...reviews)

    // Check for "See All" link
    const seeAllLink = await page.$(SELECTORS.SEE_ALL_LINK)
    if (seeAllLink) {
      result.seeAllUrl = await page.evaluate(link => {
	      const relativeUrl = link.getAttribute('href')
	      return new URL(relativeUrl, window.location.origin).href
      }, seeAllLink)
      console.log(`Found "See All" link: ${result.seeAllUrl}`)

      // Handle pagination for "See All" reviews
      if (result.seeAllUrl) {
	console.log(`Navigating to "See All" page: ${result.seeAllUrl}`)
	await page.goto(result.seeAllUrl, { waitUntil: 'networkidle0'})

	// Add a delay after initial navigation
        await delay(3000) // 3 second delay

        let hasNextPage = true
	let pageCount = 1

	while (hasNextPage) {
	  console.log(`Scraping page ${pageCount}`)
	  const pageReviews  = await page.$$eval(SELECTORS.REVIEW_ITEMS, (items, SELECTORS) => {
		  const extractNumber = (text) => {
			  const match = text.match(/\d+(\.\d+)?/)
			  return match ? parseFloat(match[0]) : null
		  }

		  const extractReviewData = (review) => {
		    try {
			    const dateAuthorElement = review.querySelector(SELECTORS.REVIEW_DATE_AUTHOR)
			    const dateSpan = dateAuthorElement.querySelector('span.-prs')
			    const authorSpan = dateAuthorElement.querySelector('span:last-child')
			    return {
				    rating: extractNumber(review.querySelector('div.stars._m._al').textContent),
				    title: review.querySelector('h3.-m.-fs16.-pvs').textContent.trim(),
				     content: review.querySelector('p.-pvs').textContent.trim(),
				     date: dateSpan ? dateSpan.textContent.trim() : null,
				     author: authorSpan ? authorSpan.textContent.replace('by ', '').trim() : null,
				     verifiedPurchase: !!review.querySelector(`${SELECTORS.VERIFIED_PURCHASE} svg.ic.-f-gn5`)
			     }
		     } catch (error) {
			     console.error(`Error extracting review data:`, error)
			     return null
		     }
	    }
	    return items.map(review => extractReviewData(review)).filter(Boolean)
          }, SELECTORS)
	  console.log(`Found ${pageReviews.length} reviews on page ${pageCount}`)
	  result.reviews.push(...pageReviews)

	  // Check for next page button
	  const nextButton = await page.$('a.pg[aria-label="Next Page"]')
	  if (nextButton) {
	    console.log(`Moving to next page (${pageCount + 1})`)
	    await nextButton.click()
	    await page.waitForNavigation({ waitUntil: 'networkidle0'})

	    // Add a delay after each page navigation
            await delay(2000) // 2 second delay
	  } else {
	    console.log('No more pages left to scrape')
	    hasNextPage = false
	  }
	  // Add a delay between processing each page
          await delay(1000) // 1 second delay
	}
      } else {
	      console.log('Found "See All" link, but unable to extract URL')
      }
    } else {
	    console.log('No "See All" link found')
    }

    console.log(`Total reviews scraped: ${result.reviews.length}`)
    return result
  } catch(error) {
    console.log('Error scraping customer feedback:', error)
    return null
  }
} 
export const scrapeCustomerFeedbackString = `${scrapeCustomerFeedback.toString()}`
export default scrapeCustomerFeedback
