/**
 * Keep-Alive service to prevent Render free tier from sleeping
 * Pings the backend every 10 minutes to keep it warm
 */

const PING_INTERVAL = 10 * 60 * 1000 // 10 minutes
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5001/api'

let pingInterval = null

export const startKeepAlive = () => {
  // Don't run on localhost
  if (API_URL.includes('localhost')) {
    console.log('[KeepAlive] Running on localhost, skipping keep-alive')
    return
  }

  // Clear any existing interval
  if (pingInterval) {
    clearInterval(pingInterval)
  }

  console.log('[KeepAlive] Starting keep-alive service...')

  // Ping immediately on start
  pingBackend()

  // Then ping every 10 minutes
  pingInterval = setInterval(() => {
    pingBackend()
  }, PING_INTERVAL)
}

export const stopKeepAlive = () => {
  if (pingInterval) {
    clearInterval(pingInterval)
    pingInterval = null
    console.log('[KeepAlive] Keep-alive service stopped')
  }
}

const pingBackend = async () => {
  try {
    const response = await fetch(`${API_URL}/produtos?per_page=1`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    })

    if (response.ok) {
      console.log('[KeepAlive] Backend is awake ✓')
    } else {
      console.warn('[KeepAlive] Backend responded with status:', response.status)
    }
  } catch (error) {
    console.warn('[KeepAlive] Failed to ping backend:', error.message)
  }
}
