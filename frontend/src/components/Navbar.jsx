import { Link, useNavigate } from 'react-router-dom'

export default function Navbar() {
  const navigate = useNavigate()
  const token = localStorage.getItem('access_token')

  const handleLogout = () => {
    localStorage.removeItem('access_token')
    navigate('/login')
  }

  return (
    <nav className="bg-white border-b border-gray-100 px-8 py-4 flex items-center justify-between sticky top-0 z-50 shadow-sm">
      <Link to="/" className="flex items-center gap-2 text-xl font-bold text-[#FF385C]">
        ⛽ fuel-flow
      </Link>
      <div className="flex gap-4 items-center">
        {token ? (
          <>
            <Link to="/favourites" className="text-gray-600 hover:text-gray-900 font-medium transition">
              My Favourites
            </Link>
            <button
              onClick={handleLogout}
              className="bg-[#FF385C] hover:bg-[#e0314f] text-white font-medium px-5 py-2 rounded-full transition"
            >
              Log out
            </button>
          </>
        ) : (
          <>
            <Link to="/login" className="text-gray-600 hover:text-gray-900 font-medium transition">
              Log in
            </Link>
            <Link
              to="/register"
              className="bg-[#FF385C] hover:bg-[#e0314f] text-white font-medium px-5 py-2 rounded-full transition"
            >
              Sign up
            </Link>
          </>
        )}
      </div>
    </nav>
  )
}