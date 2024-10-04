import db from '../config/database.js'
import bcrypt from 'bcrypt'

export default class User {
  static async create({email, password, first_name, last_name}) {
    const hashedPassword = await bcrypt.hash(password, 10)
    return db.one(`
      INSERT INTO users (email, password_hash, first_name, last_name)
      VALUES ($1, $2, $3, $4)
      RETURNING id, email, first_name, last_name
    `, [email, hashedPassword, first_name, last_name])
  }
}
