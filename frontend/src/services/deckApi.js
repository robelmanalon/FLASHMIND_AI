import { request } from './api'

export async function getDecks() {
  return request('/decks')
}

export async function getDeck(id) {
  return request(`/decks/${id}`)
}

export async function saveDeck(payload) {
  if (payload && payload.id && payload.id !== 'new') {
    return request(`/decks/${payload.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })
  }
  return request('/decks', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ...payload, id: undefined }),
  })
}

export async function deleteDeck(id) {
  return request(`/decks/${id}`, { method: 'DELETE' })
}