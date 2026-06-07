import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import client from '../api/client'

export default function RegisterPage() {
  const [form, setForm] = useState({
    login: '', email: '', password: '', name: '', surname: '', birth_date: ''
  })
  const [confirmPassword, setConfirmPassword] = useState('')
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (form.password !== confirmPassword) {
      setError('Passwords do not match')
      return
    }
    try {
      await client.post('/auth/register', form)
      navigate('/login')
    } catch (e) {
      const detail = e.response?.data?.detail
      setError(detail || 'Registration failed. Please try again.')
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4">
      <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8 w-full max-w-md">
        <h1 className="text-2xl font-bold text-gray-900 mb-1">Create an account</h1>
        <p className="text-gray-400 text-sm mb-6">Join fuel-flow and save your favourite stations</p>
        {error && <p className="text-red-500 text-sm mb-4">{error}</p>}
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">

          <div>
            <label className="text-xs text-gray-400 mb-1 block">Login</label>
            <input
              className="w-full border border-gray-200 px-4 py-3 rounded-xl outline-none focus:ring-2 focus:ring-[#FF385C] text-gray-900"
              placeholder="Your login"
              value={form.login}
              onChange={e => setForm({ ...form, login: e.target.value })}
            />
          </div>

          <div>
            <label className="text-xs text-gray-400 mb-1 block">Email</label>
            <input
              type="email"
              className="w-full border border-gray-200 px-4 py-3 rounded-xl outline-none focus:ring-2 focus:ring-[#FF385C] text-gray-900"
              placeholder="your@email.com"
              value={form.email}
              onChange={e => setForm({ ...form, email: e.target.value })}
            />
          </div>

          <div>
            <label className="text-xs text-gray-400 mb-1 block">Password</label>
            <input
              type="password"
              className="w-full border border-gray-200 px-4 py-3 rounded-xl outline-none focus:ring-2 focus:ring-[#FF385C] text-gray-900"
              placeholder="Your password"
              value={form.password}
              onChange={e => setForm({ ...form, password: e.target.value })}
            />
          </div>

          <div>
            <label className="text-xs text-gray-400 mb-1 block">Confirm password</label>
            <input
              type="password"
              className={`w-full border px-4 py-3 rounded-xl outline-none focus:ring-2 focus:ring-[#FF385C] text-gray-900 ${
                confirmPassword && form.password !== confirmPassword
                  ? 'border-red-300'
                  : 'border-gray-200'
              }`}
              placeholder="Repeat your password"
              value={confirmPassword}
              onChange={e => setConfirmPassword(e.target.value)}
            />
            {confirmPassword && form.password !== confirmPassword && (
              <p className="text-red-400 text-xs mt-1">Passwords do not match</p>
            )}
          </div>

          <div>
            <label className="text-xs text-gray-400 mb-1 block">First name</label>
            <input
              className="w-full border border-gray-200 px-4 py-3 rounded-xl outline-none focus:ring-2 focus:ring-[#FF385C] text-gray-900"
              placeholder="John"
              value={form.name}
              onChange={e => setForm({ ...form, name: e.target.value })}
            />
          </div>

          <div>
            <label className="text-xs text-gray-400 mb-1 block">Last name</label>
            <input
              className="w-full border border-gray-200 px-4 py-3 rounded-xl outline-none focus:ring-2 focus:ring-[#FF385C] text-gray-900"
              placeholder="Doe"
              value={form.surname}
              onChange={e => setForm({ ...form, surname: e.target.value })}
            />
          </div>

          <div>
            <label className="text-xs text-gray-400 mb-1 block">Date of birth</label>
            <input
              type="date"
              className="w-full border border-gray-200 px-4 py-3 rounded-xl outline-none focus:ring-2 focus:ring-[#FF385C] text-gray-900"
              value={form.birth_date}
              onChange={e => setForm({ ...form, birth_date: e.target.value })}
            />
          </div>

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