// Database configuration (connection to PostgreSQL).
import pgPromise from 'pg-promise'
import dotenv from 'dotenv'

// Load environment variables from .env files
dotenv.config()

const pgp = pgPromise()	// Initialize pg-promise

/* const pool = new Pool({
  user: process.env.DB_USER,
  host: process.env.DB_HOST,
  database: process.env.DB_NAME,
  password: process.env.DB_PASSWORD,
  port: process.env.DB_PORT,
})

module.exports = {
  query: (text, params) => pool.query(text, params)
} */

const connection = {
  user: process.env.DB_USER,
  host: process.env.DB_HOST,
  database: process.env.DB_NAME,
  password: process.env.DB_PASSWORD,
  port: process.env.DB_PORT,
}

const db = pgp(connection)

export default db
