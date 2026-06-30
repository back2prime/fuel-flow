import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { useState, useEffect } from 'react'
import Navbar from './components/Navbar'
import SearchPage from './pages/SearchPage'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import FavouritesPage from './pages/FavouritesPage'
import ProfilePage from './pages/ProfilePage'
import ForgotPasswordPage from './pages/ForgotPasswordPage'
import ResetPasswordPage from './pages/ResetPasswordPage'
import client from './api/client'

export default function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [authLoading, setAuthLoading] = useState(true)

  useEffect(() => {
    client.get('/users/me')
      .then(() => setIsLoggedIn(true))
      .catch(() => setIsLoggedIn(false))
      .finally(() => setAuthLoading(false))
  }, [])

  if (authLoading) return null

  return (
    <BrowserRouter>
      <Navbar isLoggedIn={isLoggedIn} setIsLoggedIn={setIsLoggedIn} />
      <Routes>
        <Route path="/" element={<SearchPage />} />
        <Route path="/login" element={<LoginPage setIsLoggedIn={setIsLoggedIn} />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/favourites" element={<FavouritesPage />} />
        <Route path="/profile" element={<ProfilePage setIsLoggedIn={setIsLoggedIn} />} />
        <Route path="/forgot-password" element={<ForgotPasswordPage />} />
        <Route path="/reset-password" element={<ResetPasswordPage />} />
      </Routes>
    </BrowserRouter>
  )
}