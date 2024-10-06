import db from './config/database.js'

async function createUsersTable() {
  try {
    // Users table
    await db.none(`
      CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        first_name VARCHAR(100),
        last_name VARCHAR(100),
	mobile_number VARCHAR(100),
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
      );
      CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)
      `);
    console.log('Users table created successfully')
  } catch (err) {
    console.error('Error creating schema', err)
    throw error
  }
}

async function createSchema() {
  try {
    await createUsersTable()
    if (await verifyTable('users')) {
      console.log('Users table verified')
    } else {
      throw new Error('Users table not created')
    }
  } catch (error) {
    console.error(`Error in schema creation:`, error)
  } finally {
    await db.$pool.end()  // Close the database connection pool
    console.log('Connection pool closed')
  }
}

async function verifyTable(tableName) {
  try {
    const result = await db.one(`SELECT to_regclass($1) IS NOT NULL AS exists`, [tableName])
    return result.exists
  } catch (error) {
    console.error(`Error verifying ${tableName}:`, error)
    return false
  }
}

createSchema()
