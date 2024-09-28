import User from '../models/userModel.js'

exports.register = async (req, res) {
  try {
    const { email, password, first_name, last_name } = req.body
    const newUser = await User.create({ email, password, first_name, last_name })
    res.status(201).json(newUser)
  } catch (error) {
    console.error('Error registering user:', error)
    res.status(500).json({ error: 'Failed to register users'})
  }
}
