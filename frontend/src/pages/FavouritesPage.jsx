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
      .catch(() => setError('Failed to load favourites'))
  }, [navigate])

  const handleRemove = async (stationId) => {
    try {
      await client.delete(`/stations/${stationId}/favourite`)
      setFavourites(prev => prev.filter(f => f.station_id !== stationId))
    } catch {
      setError('Failed to remove station')
    }
  }
  console.log(favourites)
  return (
    <div className="min-h-screen bg-gray-50 text-gray-900">
      <div className="max-w-6xl mx-auto px-8 py-10">
        <h1 className="text-3xl font-bold text-gray-900 mb-1">My Favourites</h1>
        <p className="text-gray-400 text-sm mb-8">Your saved gas stations</p>

        {error && <p className="text-red-500 mb-4">{error}</p>}

        {favourites.length === 0 && !error && (
          <div className="text-center py-20 text-gray-400">
            <p className="text-5xl mb-4">⛽</p>
            <p className="text-lg font-medium text-gray-500">No saved stations yet</p>
            <p className="text-sm mt-1">Search for stations and save your favourites</p>
          </div>
        )}

        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {favourites.map(f => (
            <div key={f.station_id} className="bg-white rounded-2xl p-5 shadow-sm border border-gray-100 hover:shadow-md transition">
              <div className="flex justify-between items-start mb-3">
                <div>
                  <h2 className="font-semibold text-gray-900">{f.name}</h2>
                  <p className="text-gray-400 text-sm">{f.brand}</p>
                </div>
                <span className={`text-xs px-3 py-1 rounded-full font-medium ${f.is_open ? 'bg-green-50 text-green-600' : 'bg-red-50 text-red-500'}`}>
                  {f.is_open ? 'Open' : 'Closed'}
                </span>
              </div>
              <p className="text-gray-500 text-sm mb-4">{f.address}</p>
              <button
                onClick={() => handleRemove(f.station_id)}
                className="w-full border border-red-200 hover:bg-red-50 text-red-400 py-2 rounded-xl transition text-sm font-medium"
              >
                Remove from favourites
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}