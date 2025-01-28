import axios from 'axios'
import { toast } from 'react-hot-toast'

const api = axios.create({
  baseURL: '/api'
})

// Request interceptor
api.interceptors.request.use((config) => {
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
  }
  return config
}, (error) => {
  return Promise.reject(error)
})

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    const message = error.response?.data?.message || 'An error occurred'
    
    // Handle authentication errors
    if (error.response?.status === 401 || error.response?.status === 403) {
      localStorage.removeItem('token')
      window.location.href = '/'
      toast.error('Session expired. Please login again.')
    }
    
    return Promise.reject(error)
  }
)

export default api

