export const checkProductStock = () => {
  const DEFAULT_STATUS = 'Status unknown'
  const DEFAULT_UNITS = null

  const stockInfo = { inStock: false, stockStatus: DEFAULT_STATUS, unitsLeft: DEFAULT_UNITS}
  const selectors = [
    { selector: 'p.-df.-i-ctr.-fs12.-pbs.-gy5', type: 'status'},
    { selector: 'span.-fsh0.-prs.-fs12', type: 'units'},	// Class during offers
    { selector: 'p.-fs12.-pbs.-gy5', type: 'status'},
    { selector: '.-df.-i-ctr.-fs12.-pbs.-rd5', type: 'units' }
  ]

  // Loop through selectors to check stock information
  for (const {selector, type} of selectors) {
    const element = document.querySelector(selector)
    if (!element) continue  // Skip if element is not found

    const textContent = element.textContent.trim().toLowerCase()

    if (type === 'status') {
      if (textContent === 'in stock') {
	stockInfo.inStock = true
	stockInfo.stockStatus = 'In stock'
	return stockInfo  // Early return for in stock
      } else if (textContent === 'out of stock') {
	stockInfo.stockStatus = 'Out of Stock'
	return stockInfo  // Early return for out of stock
      } else {
      stockInfo.stockStatus = textContent // Handle other statuses
      }
    } else if (type === 'units') {
      // Check units left
      const match = textContent.match(/(\d+)\s+(?:items?|units?)\s+left/i)
      if (match) {
	stockInfo.inStock = true
        stockInfo.unitsLeft = parseInt(match[1], 10)
        stockInfo.stockStatus = textContent
        return stockInfo	//  Early return after finding units left
      }
    }
  }

  return stockInfo
}

// Exporting the function's string representation
export const checkProductStockString = checkProductStock.toString()
