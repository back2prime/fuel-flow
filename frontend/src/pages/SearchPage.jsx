import { useState } from 'react'
import client from '../api/client'

const FUEL_TYPES = [
  { value: 'e5', label: 'Super E5' },
  { value: 'e10', label: 'Super E10' },
  { value: 'diesel', label: 'Diesel' },
]

const SORT_TYPES = [
  { value: 'price', label: 'Preis' },
  { value: 'dist', label: 'Entfernung' },
]

export default function SearchPage() {
  const [form, setForm] = useState({ address: '', radius: 5, fuel_type: 'e5', sort_type: 'price' })
  const [stations, setStations] = useState([])
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [added, setAdded] = useState({})

  const handleSearch = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    try {
      const res = await client.post('/stations', form)
      setStations(res.data)
    } catch {
      setError('Fehler bei der Suche')
    } finally {
      setLoading(false)
    }
  }

  const handleFavourite = async (station) => {
    try {
      await client.post(`/stations/${station.id}/favourite`)
      setAdded(prev => ({ ...prev, [station.id]: true }))
    } catch {
      setError('Fehler beim Hinzufügen zu Favoriten')
    }
  }

  return (
    <div className="min-h-screen bg-gray-950 text-white px-6 py-8">
      <h1 className="text-2xl font-bold mb-6">Tankstellen suchen</h1>

      <form onSubmit={handleSearch} className="bg-gray-900 rounded-2xl p-6 flex flex-col gap-4 mb-8 max-w-2xl">
        <input
          className="bg-gray-800 text-white px-4 py-3 rounded-lg outline-none focus:ring-2 focus:ring-green-400"
          placeholder="Adresse (z.B. Berlin Mitte)"
          value={form.address}
          onChange={e => setForm({ ...form, address: e.target.value })}
        />
        <div className="flex gap-4">
          <input
            type="number"
            min={1}
            max={25}
            className="bg-gray-800 text-white px-4 py-3 rounded-lg outline-none focus:ring-2 focus:ring-green-400 w-32"
            placeholder="Radius (km)"
            value={form.radius}
            onChange={e => setForm({ ...form, radius: Number(e.target.value) })}
          />
          <select
            className="bg-gray-800 text-white px-4 py-3 rounded-lg outline-none focus:ring-2 focus:ring-green-400 flex-1"
            value={form.fuel_type}
            onChange={e => setForm({ ...form, fuel_type: e.target.value })}
          >
            {FUEL_TYPES.map(f => <option key={f.value} value={f.value}>{f.label}</option>)}
          </select>
          <select
            className="bg-gray-800 text-white px-4 py-3 rounded-lg outline-none focus:ring-2 focus:ring-green-400 flex-1"
            value={form.sort_type}
            onChange={e => setForm({ ...form, sort_type: e.target.value })}
          >
            {SORT_TYPES.map(s => <option key={s.value} value={s.value}>{s.label}</option>)}
          </select>
        </div>
        <button
          type="submit"
          disabled={loading}
          className="bg-green-500 hover:bg-green-400 disabled:opacity-50 text-white font-semibold py-3 rounded-lg transition"
        >
          {loading ? 'Suche läuft...' : 'Suchen'}
        </button>
      </form>

      {error && <p className="text-red-400 mb-4">{error}</p>}

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {stations.map(s => (
          <div key={s.id} className="bg-gray-900 rounded-2xl p-5">
            <div className="flex justify-between items-start mb-2">
              <h2 className="font-semibold text-lg">{s.name}</h2>
              <span className={`text-sm px-2 py-1 rounded-full ${s.isOpen ? 'bg-green-900 text-green-400' : 'bg-red-900 text-red-400'}`}>
                {s.isOpen ? 'Geöffnet' : 'Geschlossen'}
              </span>
            </div>
            <p className="text-gray-400 text-sm mb-1">{s.brand}</p>
            <p className="text-gray-400 text-sm mb-3">{s.address} · {s.dist} km</p>
            <div className="flex gap-3 mb-4">
              {s.e5 && <span className="bg-gray-800 px-3 py-1 rounded-lg text-sm">E5 {s.e5}€</span>}
              {s.e10 && <span className="bg-gray-800 px-3 py-1 rounded-lg text-sm">E10 {s.e10}€</span>}
              {s.diesel && <span className="bg-gray-800 px-3 py-1 rounded-lg text-sm">Diesel {s.diesel}€</span>}
            </div>
            <button
              onClick={() => handleFavourite(s)}
              disabled={added[s.id]}
              className="w-full bg-green-900 hover:bg-green-800 disabled:opacity-50 text-green-300 py-2 rounded-lg transition text-sm"
            >
              {added[s.id] ? '✓ Gespeichert' : 'Zu Favoriten hinzufügen'}
            </button>
          </div>
        ))}
      </div>
    </div>
  )
}