import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import client from '../api/client'

export default function FavouritesPage() {
  const [favourites, setFavourites] = useState([])
  const [error, setError] = useState('')
  const navigate = useNavigate()

  useEffect(() => {
    const token = localStorage.getItem('access_token')
    if (!token) {
      navigate('/login')
      return
    }
    client.get('/users/me/favourites')
      .then(res => setFavourites(res.data))
      .catch(() => setError('Fehler beim Laden der Favoriten'))
  }, [navigate])

  const handleRemove = async (stationId) => {
    try {
      await client.delete(`/stations/${stationId}/favourite`)
      setFavourites(prev => prev.filter(f => f.station_id !== stationId))
    } catch {
      setError('Fehler beim Entfernen')
    }
  }

  return (
    <div className="min-h-screen bg-gray-950 text-white px-6 py-8">
      <h1 className="text-2xl font-bold mb-6">Meine Favoriten</h1>
      {error && <p className="text-red-400 mb-4">{error}</p>}
      {favourites.length === 0 && !error && (
        <p className="text-gray-400">Keine Favoriten gespeichert.</p>
      )}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {favourites.map(f => (
          <div key={f.station_id} className="bg-gray-900 rounded-2xl p-5">
            <div className="flex justify-between items-start mb-2">
              <h2 className="font-semibold text-lg">{f.name}</h2>
              <span className={`text-sm px-2 py-1 rounded-full ${f.is_open ? 'bg-green-900 text-green-400' : 'bg-red-900 text-red-400'}`}>
                {f.is_open ? 'Geöffnet' : 'Geschlossen'}
              </span>
            </div>
            <p className="text-gray-400 text-sm mb-1">{f.brand}</p>
            <p className="text-gray-400 text-sm mb-4">{f.address}</p>
            <button
              onClick={() => handleRemove(f.station_id)}
              className="w-full bg-red-900 hover:bg-red-800 text-red-300 py-2 rounded-lg transition text-sm"
            >
              Aus Favoriten entfernen
            </button>
          </div>
        ))}
      </div>
    </div>
  )
}