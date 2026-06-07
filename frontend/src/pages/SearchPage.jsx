import { useState, useEffect } from 'react'
import client from '../api/client'

const FUEL_TYPES = [
  { value: 'e5', label: 'Super E5' },
  { value: 'e10', label: 'Super E10' },
  { value: 'diesel', label: 'Diesel' },
]

const SORT_TYPES = [
  { value: 'price', label: 'Price' },
  { value: 'dist', label: 'Distance' },
]

export default function SearchPage() {
  const [form, setForm] = useState({ address: '', radius: 5, fuel_type: 'e5', sort_type: 'price', limit: 10 })
  const [stations, setStations] = useState([])
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [favourites, setFavourites] = useState(new Set())

  useEffect(() => {
    const token = localStorage.getItem('access_token')
    if (!token) return
    client.get('/users/me/favourites')
      .then(res => {
        const ids = new Set(res.data.map(f => f.station_id))
        setFavourites(ids)
      })
      .catch(() => {})
  }, [])

  const handleSearch = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    try {
      const res = await client.post(`/stations?limit=${form.limit}`, form)
      setStations(res.data)
    } catch {
      setError('Something went wrong. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleToggleFavourite = async (station) => {
    const isSaved = favourites.has(station.id)
    try {
      if (isSaved) {
        await client.delete(`/stations/${station.id}/favourite`)
        setFavourites(prev => {
          const next = new Set(prev)
          next.delete(station.id)
          return next
        })
      } else {
        await client.post(`/stations/${station.id}/favourite`)
        setFavourites(prev => new Set(prev).add(station.id))
      }
    } catch {
      setError('Failed to update favourites')
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900">
      <div className="bg-white border-b border-gray-100 px-8 py-12">
        <div className="max-w-3xl mx-auto">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Find gas stations near you</h1>
          <p className="text-gray-500 mb-8">Compare fuel prices across Germany in real time</p>

          <form onSubmit={handleSearch} className="flex flex-col gap-4">
            <input
              className="w-full border border-gray-200 bg-white text-gray-900 px-5 py-4 rounded-2xl outline-none focus:ring-2 focus:ring-[#FF385C] shadow-sm text-base"
              placeholder="Enter address (e.g. Berlin Mitte)"
              value={form.address}
              onChange={e => setForm({ ...form, address: e.target.value })}
            />
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              <div>
                <label className="text-xs text-gray-400 mb-1 block">Radius (km)</label>
                <input
                  type="number"
                  min={1}
                  max={25}
                  className="w-full border border-gray-200 bg-white text-gray-900 px-4 py-3 rounded-xl outline-none focus:ring-2 focus:ring-[#FF385C] shadow-sm"
                  value={form.radius}
                  onChange={e => setForm({ ...form, radius: Number(e.target.value) })}
                />
              </div>
              <div>
                <label className="text-xs text-gray-400 mb-1 block">Results</label>
                <input
                  type="number"
                  min={1}
                  max={50}
                  className="w-full border border-gray-200 bg-white text-gray-900 px-4 py-3 rounded-xl outline-none focus:ring-2 focus:ring-[#FF385C] shadow-sm"
                  value={form.limit}
                  onChange={e => setForm({ ...form, limit: Number(e.target.value) })}
                />
              </div>
              <div>
                <label className="text-xs text-gray-400 mb-1 block">Fuel type</label>
                <select
                  className="w-full border border-gray-200 bg-white text-gray-900 px-4 py-3 rounded-xl outline-none focus:ring-2 focus:ring-[#FF385C] shadow-sm"
                  value={form.fuel_type}
                  onChange={e => setForm({ ...form, fuel_type: e.target.value })}
                >
                  {FUEL_TYPES.map(f => <option key={f.value} value={f.value}>{f.label}</option>)}
                </select>
              </div>
              <div>
                <label className="text-xs text-gray-400 mb-1 block">Sort by</label>
                <select
                  className="w-full border border-gray-200 bg-white text-gray-900 px-4 py-3 rounded-xl outline-none focus:ring-2 focus:ring-[#FF385C] shadow-sm"
                  value={form.sort_type}
                  onChange={e => setForm({ ...form, sort_type: e.target.value })}
                >
                  {SORT_TYPES.map(s => <option key={s.value} value={s.value}>{s.label}</option>)}
                </select>
              </div>
            </div>
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-[#FF385C] hover:bg-[#e0314f] disabled:opacity-50 text-white font-semibold py-4 rounded-2xl transition text-base shadow-sm"
            >
              {loading ? 'Searching...' : 'Search'}
            </button>
          </form>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-8 py-8">
        {error && <p className="text-red-500 mb-4">{error}</p>}
        {stations.length > 0 && (
          <p className="text-gray-400 text-sm mb-4">{stations.length} stations found</p>
        )}
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {stations.map(s => {
            const saved = favourites.has(s.id)
            return (
              <div key={s.id} className="bg-white rounded-2xl p-5 shadow-sm border border-gray-100 hover:shadow-md transition">
                <div className="flex justify-between items-start mb-3">
                  <div>
                    <h2 className="font-semibold text-gray-900">{s.name}</h2>
                    <p className="text-gray-400 text-sm">{s.brand}</p>
                  </div>
                  <span className={`text-xs px-3 py-1 rounded-full font-medium ${s.isOpen ? 'bg-green-50 text-green-600' : 'bg-red-50 text-red-500'}`}>
                    {s.isOpen ? 'Open' : 'Closed'}
                  </span>
                </div>
                <p className="text-gray-500 text-sm mb-4">{s.address} · {s.dist} km</p>
                <div className="flex gap-2 mb-4">
                  {s.e5 && <span className="bg-gray-50 border border-gray-100 px-3 py-1 rounded-lg text-sm font-medium">E5 {s.e5}€</span>}
                  {s.e10 && <span className="bg-gray-50 border border-gray-100 px-3 py-1 rounded-lg text-sm font-medium">E10 {s.e10}€</span>}
                  {s.diesel && <span className="bg-gray-50 border border-gray-100 px-3 py-1 rounded-lg text-sm font-medium">Diesel {s.diesel}€</span>}
                </div>
                <button
                  onClick={() => handleToggleFavourite(s)}
                  className={`w-full py-2 rounded-xl transition text-sm font-medium border ${
                    saved
                      ? 'border-gray-200 bg-gray-50 text-gray-400 hover:border-red-200 hover:text-red-400'
                      : 'border-[#FF385C] text-[#FF385C] hover:bg-[#FF385C] hover:text-white'
                  }`}
                >
                  {saved ? '✓ Saved · click to remove' : '+ Save to favourites'}
                </button>
              </div>
            )
          })}
        </div>
      </div>
    </div>
  )
}