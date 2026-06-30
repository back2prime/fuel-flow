import client from '../api/client'

import { Link, useNavigate } from 'react-router-dom'

function FuelDropIcon() {
  return (
    <svg width="28" height="28" viewBox="0 0 28 28" fill="none" xmlns="http://www.w3.org/2000/svg">
      {/* Drop shape */}
      <path
        d="M14 3C14 3 7 11.5 7 16.5C7 20.09 10.13 23 14 23C17.87 23 21 20.09 21 16.5C21 11.5 14 3 14 3Z"
        fill="#FF385C"
      />
      {/* Shine */}
      <ellipse cx="11.5" cy="15" rx="1.5" ry="2.5" fill="white" fillOpacity="0.35" transform="rotate(-15 11.5 15)" />
    </svg>
  )
}

export default function Navbar({ isLoggedIn, setIsLoggedIn }) {
  const navigate = useNavigate()

  const handleLogout = async () => {
    await client.post('/auth/logout')
    setIsLoggedIn(false)
    navigate('/login')
  }

  return (
    <nav className="bg-white border-b border-gray-100 px-8 py-4 flex items-center justify-between sticky top-0 z-50 shadow-sm">
      <Link to="/" className="flex items-center gap-2 text-xl font-bold text-[#FF385C]">
        <FuelDropIcon />
        fuel-flow
      </Link>
      <div className="flex gap-4 items-center">
        {isLoggedIn ? (
          <>
            <Link to="/favourites" className="text-gray-600 hover:text-gray-900 font-medium transition">
              My Favourites
            </Link>
            <Link to="/profile" className="text-gray-600 hover:text-gray-900 font-medium transition">
              Profile
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