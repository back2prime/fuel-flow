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
      setError('Registrierung fehlgeschlagen')
    }
  }

  const fields = [
    { key: 'login', placeholder: 'Login' },
    { key: 'email', placeholder: 'E-Mail' },
    { key: 'password', placeholder: 'Passwort', type: 'password' },
    { key: 'name', placeholder: 'Vorname' },
    { key: 'surname', placeholder: 'Nachname' },
    { key: 'birth_date', placeholder: 'Geburtsdatum', type: 'date' },
  ]

  return (
    <div className="min-h-screen bg-gray-950 flex items-center justify-center">
      <div className="bg-gray-900 p-8 rounded-2xl w-full max-w-md">
        <h1 className="text-2xl font-bold text-white mb-6">Registrieren</h1>
        {error && <p className="text-red-400 mb-4">{error}</p>}
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          {fields.map(({ key, placeholder, type = 'text' }) => (
            <input
              key={key}
              type={type}
              className="bg-gray-800 text-white px-4 py-3 rounded-lg outline-none focus:ring-2 focus:ring-green-400"
              placeholder={placeholder}
              value={form[key]}
              onChange={e => setForm({ ...form, [key]: e.target.value })}
            />
          ))}
          <button type="submit" className="bg-green-500 hover:bg-green-400 text-white font-semibold py-3 rounded-lg transition">
            Registrieren
          </button>
        </form>
        <p className="text-gray-400 mt-4 text-sm">
          Bereits ein Konto? <Link to="/login" className="text-green-400 hover:underline">Anmelden</Link>
        </p>
      </div>
    </div>
  )
}