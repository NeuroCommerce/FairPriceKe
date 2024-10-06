// The main application file where you set up your Express app.

import express from 'express';
import db from './config/database.js'
import userRoutes from './routes/userRoutes.js'
import jumiaScraperRoutes from './routes/jumiaScraperRoutes.js'

const app = express();
const port = process.env.PORT || 3000;

app.use(express.json());

app.get('/', (req, res) => {
  res.json({ message: 'Welcome to FairPriceKe API' });
});
app.use('/api/users', userRoutes);
app.use('/api/jumia', jumiaScraperRoutes)
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});

// app.get('/test-db', async (req, res) => {
//   try {
//     const result = await db.query('SELECT NOW()')
//     res.json({
//       message: 'Database connected successfully', 
//       currentTime: result.rows[0].now
//     })
//   } catch (err) {
//     console.error('Database connection error', err.stack)
//     res.status(500).json({ message: 'Database connection error' });
//   }
// })
//
// // In src/app.js
//
// app.get('/create-test-table', async (req, res) => {
//   try {
//     await db.query(`
//       CREATE TABLE IF NOT EXISTS test_table (
//         id SERIAL PRIMARY KEY,
//         name VARCHAR(100) NOT NULL,
//         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
//       )
//     `);
//     res.json({ message: 'Test table created successfully' });
//   } catch (err) {
//     console.error('Error creating test table', err.stack);
//     res.status(500).json({ message: 'Error creating test table' });
//   }
// });
