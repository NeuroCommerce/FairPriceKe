# Jumia Scraper API

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Requirements](#requirements)
4. [Installation](#installation)
5. [Configuration](#configuration)
6. [Usage](#usage)
7. [API Endpoints](#api-endpoints)
8. [Error Handling](#error-handling)
9. [Rate Limiting](#rate-limiting)
10. [Contributing](#contributing)
11. [License](#license)

## Introduction

The Jumia Scraper API is a Node.js-based web scraping tool designed to extract product information from Jumia, an e-commerce platform. This API allows users to scrape product data for specific brands or all available brands on Jumia.

## Features

- Scrape product data for specific brands
- Option to scrape data for all available brands
- Rate limiting to prevent overloading the target website
- Error handling and logging
- Easy-to-use RESTful API

## Requirements

- Node.js (v14.0.0 or higher)
- npm (v6.0.0 or higher)

## Installation

1. Clone the repository:
   ```
   https://github.com/NeuroCommerce/FairPriceKe.git
   ```

2. Navigate to the project directory:
   ```
   cd backend/
   ```

3. Install the dependencies:
   ```
   npm install
   ```

## Configuration

1. Create a `.env` file in the root directory of the project.
2. Add the following environment variables:
   ```
   PORT=3000
   MAX_REQUESTS_PER_MINUTE=60
   ```
   Adjust these values as needed.

## Usage

To start the server, run:

```
npm run start
```

The server will start running on `http://localhost:3000` (or the port specified in your .env file).

## API Endpoints

### Scrape Jumia Products

- **URL**: `/api/jumia/scrape`
- **Method**: `POST`
- **Data Params**:
  ```json
  {
    "category": "[brand name or 'all']"
  }
  ```
- **Success Response**:
  - **Code**: 200
  - **Content**: `{ "results": [...] }`
- **Error Response**:
  - **Code**: 400 or 500
  - **Content**: `{ "error": "Error message" }`

#### Example Usage

1. Scrape a specific brand:
   ```bash
   curl -X POST http://localhost:3000/api/jumia/scrape -H "Content-Type: application/json" -d '{"category": "infinix"}'
   ```

2. Scrape all brands:
   ```bash
   curl -X POST http://localhost:3000/api/jumia/scrape -H "Content-Type: application/json" -d '{"category": "all"}'
   ```

## Error Handling

The API uses standard HTTP response codes to indicate the success or failure of requests. In case of errors, a JSON response with an error message is returned.

## Rate Limiting

To prevent overwhelming the target website, this API implements rate limiting. The default limit is set to 60 requests per minute, but this can be adjusted in the `.env` file.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

