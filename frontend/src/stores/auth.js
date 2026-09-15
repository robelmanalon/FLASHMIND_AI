import { defineStore } from 'pinia'
import { getProfile } from '../services/api'

const savedUser = localStorage.getItem('flashmind-user')

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: savedUser ? JSON.parse(savedUser) : null,
    token: localStorage.getItem('flashmind-token') || '',
  }),
  getters: { isAuthenticated: (state) => Boolean(state.token && state.user) },
  actions: {
    setSession(payload) {
      const returningUser = Boolean(this.user)
      this.user = { ...payload.user, lastActiveAt: returningUser ? new Date().toISOString() : null }
      this.token = payload.access_token
      localStorage.setItem('flashmind-user', JSON.stringify(this.user))
      localStorage.setItem('flashmind-token', payload.access_token)
    },
    updateUserData(data) {
      this.user = { ...this.user, ...data }
      localStorage.setItem('flashmind-user', JSON.stringify(this.user))
    },
    async refreshProfile() {
      const data = await getProfile()
      this.updateUserData({ name: data.name, avatar_url: data.avatar_url })
    },
    logout() {
      this.user = null
      this.token = ''
      localStorage.removeItem('flashmind-user')
      localStorage.removeItem('flashmind-token')
    },
  },
})