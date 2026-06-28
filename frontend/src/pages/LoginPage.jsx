import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import client from '../api/client'

export default function LoginPage() {
  const [form, setForm] = useState({ login: '', password: '' })
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      const res = await client.post('/auth/login', form)
      localStorage.setItem('access_token', res.data.access_token)
      navigate('/')
    } catch (e) {
      if (e.response?.status === 429) {
        setError(e.response?.data?.error || 'Too many attempts. Please wait a minute.')
      } else if (e.response?.status === 401) {
        setError('Invalid login or password')
      } else {
        setError('Something went wrong. Please try again.')
      }
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4">
      <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8 w-full max-w-md">
        <h1 className="text-2xl font-bold text-gray-900 mb-1">Welcome back</h1>
        <p className="text-gray-400 text-sm mb-6">Log in to your fuel-flow account</p>
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
            <label className="text-xs text-gray-400 mb-1 block">Password</label>
            <input
              type="password"
              className="w-full border border-gray-200 px-4 py-3 rounded-xl outline-none focus:ring-2 focus:ring-[#FF385C] text-gray-900"
              placeholder="Your password"
              value={form.password}
              onChange={e => setForm({ ...form, password: e.target.value })}
            />
            <div className="text-right mt-1">
              <Link to="/forgot-password" className="text-xs text-[#FF385C] hover:underline">
                Forgot password?
              </Link>
            </div>
          </div>
          <button
            type="submit"
            className="bg-[#FF385C] hover:bg-[#e0314f] text-white font-semibold py-3 rounded-xl transition mt-2"
          >
            Log in
          </button>
        </form>
        <p className="text-gray-400 text-sm mt-4 text-center">
          Don't have an account?{' '}
          <Link to="/register" className="text-[#FF385C] hover:underline font-medium">Sign up</Link>
        </p>
      </div>
    </div>
  )
}