export function getApiUrl() {
  return localStorage.getItem('flashmind-api-url') || import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'
}

export function setApiUrl(url) {
  localStorage.setItem('flashmind-api-url', url)
}

function authHeaders() {
  const token = localStorage.getItem('flashmind-token')
  return token ? { Authorization: `Bearer ${token}` } : {}
}

function handleSessionExpired() {
  localStorage.removeItem('flashmind-token')
  localStorage.removeItem('flashmind-user')
  if (!window.location.pathname.startsWith('/login')) {
    window.location.href = '/login'
  }
}

async function request(path, options = {}) {
  const headers = { ...authHeaders(), ...options.headers }
  const controller = new AbortController()
  const timer = setTimeout(() => controller.abort(), 30000)
  let response
  try {
    response = await fetch(`${getApiUrl()}${path}`, { ...options, headers, signal: controller.signal })
  } catch (err) {
    if (err.name === 'AbortError') throw new Error('Request timed out. Please try again.')
    throw new Error('Cannot connect to server. Please check if the backend is running.')
  } finally {
    clearTimeout(timer)
  }
  const payload = await response.json().catch(() => null)
  if (!response.ok) {
    if (response.status === 401 && headers.Authorization) handleSessionExpired()
    throw new Error(payload?.detail || `Request failed (${response.status})`)
  }
  return payload
}

export { request }

export function login(credentials) { return request('/auth/login', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(credentials) }) }
export function register(credentials) { return request('/auth/register', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(credentials) }) }

export function getProfile() { return request('/profile') }
export function updateProfile(data) { return request('/profile', { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) }) }

export async function getHealth() {
  const response = await fetch(`${getApiUrl()}/health`)
  if (!response.ok) throw new Error('API is unavailable')
  return response.json()
}

export async function generateStudyMaterials(file, options = {}) {
  const body = new FormData()
  body.append('file', file)
  body.append('flashcard_count', String(options.flashcardCount || 10))
  body.append('quiz_count', String(options.quizCount || 10))
  const response = await fetch(`${getApiUrl()}/ai/generate`, { method: 'POST', body })
  const payload = await response.json()
  if (!response.ok) throw new Error(payload.detail || 'Could not generate study materials')
  return payload
}

export async function recordStudyReview(flashcardId, rating, responseTimeSeconds = null) {
  const response = await fetch(`${getApiUrl()}/study/review`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ flashcard_id: flashcardId, rating, response_time_seconds: responseTimeSeconds }),
  })
  const payload = await response.json()
  if (!response.ok) throw new Error(payload.detail || 'Could not save review')
  return payload
}