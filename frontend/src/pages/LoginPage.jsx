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
    } catch {
      setError('Ungültige Anmeldedaten')
    }
  }

  return (
    <div className="min-h-screen bg-gray-950 flex items-center justify-center">
      <div className="bg-gray-900 p-8 rounded-2xl w-full max-w-md">
        <h1 className="text-2xl font-bold text-white mb-6">Anmelden</h1>
        {error && <p className="text-red-400 mb-4">{error}</p>}
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <input
            className="bg-gray-800 text-white px-4 py-3 rounded-lg outline-none focus:ring-2 focus:ring-green-400"
            placeholder="Login"
            value={form.login}
            onChange={e => setForm({ ...form, login: e.target.value })}
          />
          <input
            type="password"
            className="bg-gray-800 text-white px-4 py-3 rounded-lg outline-none focus:ring-2 focus:ring-green-400"
            placeholder="Passwort"
            value={form.password}
            onChange={e => setForm({ ...form, password: e.target.value })}
          />
          <button type="submit" className="bg-green-500 hover:bg-green-400 text-white font-semibold py-3 rounded-lg transition">
            Anmelden
          </button>
        </form>
        <p className="text-gray-400 mt-4 text-sm">
          Noch kein Konto? <Link to="/register" className="text-green-400 hover:underline">Registrieren</Link>
        </p>
      </div>
    </div>
  )
}