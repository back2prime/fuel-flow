import { useState } from 'react'
import { useNavigate, useSearchParams, Link } from 'react-router-dom'
import client from '../api/client'

export default function ResetPasswordPage() {
  const [searchParams] = useSearchParams()
  const token = searchParams.get('token')
  const [form, setForm] = useState({ new_password: '', confirm: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (form.new_password !== form.confirm) {
      setError('Passwords do not match')
      return
    }
    setLoading(true)
    try {
      await client.post('/auth/reset-password', { token, new_password: form.new_password })
      navigate('/login')
    } catch (e) {
      const detail = e.response?.data?.detail
      setError(detail || 'Something went wrong. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  if (!token) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4">
        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8 w-full max-w-md text-center">
          <p className="text-4xl mb-4">❌</p>
          <h1 className="text-2xl font-bold text-gray-900 mb-2">Invalid link</h1>
          <p className="text-gray-400 text-sm">This reset link is invalid or has expired.</p>
          <Link to="/forgot-password" className="block mt-6 text-[#FF385C] hover:underline text-sm font-medium">Request a new link</Link>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4">
      <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8 w-full max-w-md">
        <h1 className="text-2xl font-bold text-gray-900 mb-1">Reset password</h1>
        <p className="text-gray-400 text-sm mb-6">Enter your new password below</p>
        {error && <p className="text-red-500 text-sm mb-4">{error}</p>}
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <div>
            <label className="text-xs text-gray-400 mb-1 block">New password</label>
            <input
              type="password"
              className="w-full border border-gray-200 px-4 py-3 rounded-xl outline-none focus:ring-2 focus:ring-[#FF385C] text-gray-900"
              placeholder="Your new password"
              value={form.new_password}
              onChange={e => setForm({ ...form, new_password: e.target.value })}
            />
          </div>
          <div>
            <label className="text-xs text-gray-400 mb-1 block">Confirm new password</label>
            <input
              type="password"
              className={`w-full border px-4 py-3 rounded-xl outline-none focus:ring-2 focus:ring-[#FF385C] text-gray-900 ${
                form.confirm && form.new_password !== form.confirm
                  ? 'border-red-300'
                  : 'border-gray-200'
              }`}
              placeholder="Repeat your new password"
              value={form.confirm}
              onChange={e => setForm({ ...form, confirm: e.target.value })}
            />
            {form.confirm && form.new_password !== form.confirm && (
              <p className="text-red-400 text-xs mt-1">Passwords do not match</p>
            )}
          </div>
          <button
            type="submit"
            disabled={loading}
            className="bg-[#FF385C] hover:bg-[#e0314f] disabled:opacity-50 text-white font-semibold py-3 rounded-xl transition"
          >
            {loading ? 'Saving...' : 'Reset password'}
          </button>
        </form>
      </div>
    </div>
  )
}