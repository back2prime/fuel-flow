import axios from 'axios'

const client = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  withCredentials: true,
})

client.interceptors.response.use(
  (response) => response,
  (error) => {
    const isAuthCheck =
      error.config?.url?.includes('/users/me') && error.config?.method === 'get'

    if (error.response?.status === 401 && !isAuthCheck && window.location.pathname !== '/login') {
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default client