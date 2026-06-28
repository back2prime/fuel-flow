import { useState } from 'react'
import { Link } from 'react-router-dom'
import client from '../api/client'

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState('')
  const [sent, setSent] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      await client.post('/auth/forgot-password', { email })
      setSent(true)
    } catch (e) {
      const detail = e.response?.data?.detail
      setError(detail || 'Something went wrong. Please try again.')
    }
  }

  if (sent) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4">
        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8 w-full max-w-md text-center">
          <p className="text-4xl mb-4">📬</p>
          <h1 className="text-2xl font-bold text-gray-900 mb-2">Check your email</h1>
          <p className="text-gray-400 text-sm">We sent a password reset link to <strong>{email}</strong>. The link expires in 15 minutes.</p>
          <Link to="/login" className="block mt-6 text-[#FF385C] hover:underline text-sm font-medium">Back to login</Link>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4">
      <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8 w-full max-w-md">
        <h1 className="text-2xl font-bold text-gray-900 mb-1">Forgot password?</h1>
        <p className="text-gray-400 text-sm mb-6">Enter your email and we'll send you a reset link</p>
        {error && <p className="text-red-500 text-sm mb-4">{error}</p>}
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <div>
            <label className="text-xs text-gray-400 mb-1 block">Email</label>
            <input
              type="email"
              className="w-full border border-gray-200 px-4 py-3 rounded-xl outline-none focus:ring-2 focus:ring-[#FF385C] text-gray-900"
              placeholder="your@email.com"
              value={email}
              onChange={e => setEmail(e.target.value)}
            />
          </div>
          <button
            type="submit"
            className="bg-[#FF385C] hover:bg-[#e0314f] text-white font-semibold py-3 rounded-xl transition"
          >
            Send reset link
          </button>
        </form>
        <p className="text-gray-400 text-sm mt-4 text-center">
          <Link to="/login" className="text-[#FF385C] hover:underline font-medium">Back to login</Link>
        </p>
      </div>
    </div>
  )
}