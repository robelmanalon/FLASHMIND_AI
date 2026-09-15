const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

function authHeaders() {
  const token = localStorage.getItem('flashmind-token')
  return token ? { Authorization: `Bearer ${token}` } : {}
}

async function request(path, options = {}) {
  const headers = { ...authHeaders(), ...options.headers }
  const response = await fetch(`${API_URL}${path}`, { ...options, headers })
  const payload = await response.json()
  if (!response.ok) throw new Error(payload.detail || 'Request failed')
  return payload
}

export { request }

export function login(credentials) { return request('/auth/login', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(credentials) }) }
export function register(credentials) { return request('/auth/register', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(credentials) }) }

export function getProfile() { return request('/profile') }
export function updateProfile(data) { return request('/profile', { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) }) }

export async function getHealth() {
  const response = await fetch(`${API_URL}/health`)
  if (!response.ok) throw new Error('API is unavailable')
  return response.json()
}

export async function generateStudyMaterials(file, options = {}) {
  const body = new FormData()
  body.append('file', file)
  body.append('flashcard_count', String(options.flashcardCount || 10))
  body.append('quiz_count', String(options.quizCount || 10))
  const response = await fetch(`${API_URL}/ai/generate`, { method: 'POST', body })
  const payload = await response.json()
  if (!response.ok) throw new Error(payload.detail || 'Could not generate study materials')
  return payload
}

export async function recordStudyReview(flashcardId, rating, responseTimeSeconds = null) {
  const response = await fetch(`${API_URL}/study/review`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ flashcard_id: flashcardId, rating, response_time_seconds: responseTimeSeconds }),
  })
  const payload = await response.json()
  if (!response.ok) throw new Error(payload.detail || 'Could not save review')
  return payload
}