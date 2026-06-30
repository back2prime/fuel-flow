import { useEffect, useState } from 'react'
import client from '../api/client'

export default function FavouritesPage() {
  const [favourites, setFavourites] = useState([])
  const [error, setError] = useState('')
  const [selectedStation, setSelectedStation] = useState(null)
  const [stationDetail, setStationDetail] = useState(null)
  const [detailLoading, setDetailLoading] = useState(false)
  const [detailError, setDetailError] = useState('')

useEffect(() => {
  client.get('/users/me/favourites')
    .then(res => setFavourites(res.data))
    .catch(() => setError('Failed to load favourites'))
}, [])

  const handleRemove = async (stationId) => {
    try {
      await client.delete(`/stations/${stationId}/favourite`)
      setFavourites(prev => prev.filter(f => f.station_id !== stationId))
      if (selectedStation === stationId) {
        setSelectedStation(null)
        setStationDetail(null)
      }
    } catch {
      setError('Failed to remove station')
    }
  }

  const handleCardClick = async (stationId) => {
    if (selectedStation === stationId) {
      setSelectedStation(null)
      setStationDetail(null)
      return
    }
    setSelectedStation(stationId)
    setStationDetail(null)
    setDetailError('')
    setDetailLoading(true)
    try {
      const res = await client.post(`/stations/${stationId}`)
      setStationDetail(res.data)
    } catch {
      setDetailError('Failed to load station details')
    } finally {
      setDetailLoading(false)
    }
  }

  const formatPrice = (price) =>
    price != null ? `${price.toFixed(3)} €` : '—'

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
            <div key={f.station_id} className="flex flex-col">
              <div
                onClick={() => handleCardClick(f.station_id)}
                className={`bg-white rounded-2xl p-5 shadow-sm border transition cursor-pointer select-none ${
                  selectedStation === f.station_id
                    ? 'border-[#FF385C] shadow-md'
                    : 'border-gray-100 hover:shadow-md'
                }`}
              >
                <div className="flex justify-between items-start mb-3">
                  <div>
                    <h2 className="font-semibold text-gray-900">{f.name}</h2>
                    <p className="text-gray-400 text-sm">{f.brand}</p>
                  </div>
                  <span className="text-xs text-gray-400">
                    {selectedStation === f.station_id ? '▲' : '▼'}
                  </span>
                </div>
                <p className="text-gray-500 text-sm mb-4">{f.address}</p>
                <button
                  onClick={(e) => { e.stopPropagation(); handleRemove(f.station_id) }}
                  className="w-full border border-red-200 hover:bg-red-50 text-red-400 py-2 rounded-xl transition text-sm font-medium"
                >
                  Remove from favourites
                </button>
              </div>

              {selectedStation === f.station_id && (
                <div className="bg-white border border-t-0 border-[#FF385C] rounded-b-2xl px-5 pb-5 -mt-2 pt-4">
                  {detailLoading && (
                    <p className="text-sm text-gray-400">Loading...</p>
                  )}
                  {detailError && (
                    <p className="text-sm text-red-500">{detailError}</p>
                  )}
                  {stationDetail && (
                    <div className="space-y-3">
                      <div className="flex items-center gap-2">
                        <span className={`text-xs px-3 py-1 rounded-full font-medium ${
                          stationDetail.isOpen
                            ? 'bg-green-50 text-green-600'
                            : 'bg-red-50 text-red-500'
                        }`}>
                          {stationDetail.isOpen ? 'Open' : 'Closed'}
                        </span>
                        {stationDetail.wholeDay && (
                          <span className="text-xs px-3 py-1 rounded-full font-medium bg-blue-50 text-blue-500">
                            24h
                          </span>
                        )}
                      </div>

                      <div className="grid grid-cols-3 gap-2 pt-1">
                        {[
                          { label: 'E5', value: stationDetail.e5 },
                          { label: 'E10', value: stationDetail.e10 },
                          { label: 'Diesel', value: stationDetail.diesel },
                        ].map(({ label, value }) => (
                          <div key={label} className="bg-gray-50 rounded-xl p-3 text-center">
                            <p className="text-xs text-gray-400 mb-1">{label}</p>
                            <p className="font-semibold text-gray-900 text-sm">{formatPrice(value)}</p>
                          </div>
                        ))}
                      </div>

                      {stationDetail.openingTimes?.length > 0 && !stationDetail.wholeDay && (
                        <div className="pt-1">
                          <p className="text-xs text-gray-400 mb-2">Opening hours</p>
                          <div className="space-y-1">
                            {stationDetail.openingTimes.map((ot, i) => (
                              <div key={i} className="flex justify-between text-xs text-gray-600">
                                <span>{ot.text || ot.days}</span>
                                <span>{ot.start} – {ot.end}</span>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}