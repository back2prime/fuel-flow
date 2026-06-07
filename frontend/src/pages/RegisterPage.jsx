import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import client from '../api/client'

export default function RegisterPage() {
  const [form, setForm] = useState({
    login: '', email: '', password: '', name: '', surname: '', birth_date: ''
  })
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      await client.post('/auth/register', form)
      navigate('/login')
    } catch {
      setError('Registration failed. Please try again.')
    }
  }

  const fields = [
    { key: 'login', label: 'Login', placeholder: 'Your login' },
    { key: 'email', label: 'Email', placeholder: 'your@email.com' },
    { key: 'password', label: 'Password', placeholder: 'Your password', type: 'password' },
    { key: 'name', label: 'First name', placeholder: 'John' },
    { key: 'surname', label: 'Last name', placeholder: 'Doe' },
    { key: 'birth_date', label: 'Date of birth', placeholder: '', type: 'date' },
  ]

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4">
      <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8 w-full max-w-md">
        <h1 className="text-2xl font-bold text-gray-900 mb-1">Create an account</h1>
        <p className="text-gray-400 text-sm mb-6">Join fuel-flow and save your favourite stations</p>
        {error && <p className="text-red-500 text-sm mb-4">{error}</p>}
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          {fields.map(({ key, label, placeholder, type = 'text' }) => (
            <div key={key}>
              <label className="text-xs text-gray-400 mb-1 block">{label}</label>
              <input
                type={type}
                className="w-full border border-gray-200 px-4 py-3 rounded-xl outline-none focus:ring-2 focus:ring-[#FF385C] text-gray-900"
                placeholder={placeholder}
                value={form[key]}
                onChange={e => setForm({ ...form, [key]: e.target.value })}
              />
            </div>
          ))}
          <button
            type="submit"
            className="bg-[#FF385C] hover:bg-[#e0314f] text-white font-semibold py-3 rounded-xl transition mt-2"
          >
            Sign up
          </button>
        </form>
        <p className="text-gray-400 text-sm mt-4 text-center">
          Already have an account?{' '}
          <Link to="/login" className="text-[#FF385C] hover:underline font-medium">Log in</Link>
        </p>
      </div>
    </div>
  )
}