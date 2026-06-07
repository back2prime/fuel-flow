import { Link, useNavigate } from 'react-router-dom'

export default function Navbar() {
  const navigate = useNavigate()
  const token = localStorage.getItem('access_token')

  const handleLogout = () => {
    localStorage.removeItem('access_token')
    navigate('/login')
  }

  return (
    <nav className="bg-gray-900 text-white px-6 py-4 flex items-center justify-between">
      <Link to="/" className="text-xl font-bold text-green-400">⛽ fuel-flow</Link>
      <div className="flex gap-4 items-center">
        {token ? (
          <>
            <Link to="/favourites" className="hover:text-green-400 transition">Favoriten</Link>
            <button onClick={handleLogout} className="hover:text-red-400 transition">Abmelden</button>
          </>
        ) : (
          <>
            <Link to="/login" className="hover:text-green-400 transition">Anmelden</Link>
            <Link to="/register" className="hover:text-green-400 transition">Registrieren</Link>
          </>
        )}
      </div>
    </nav>
  )
}