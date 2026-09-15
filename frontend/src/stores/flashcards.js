import { defineStore } from 'pinia'
import { getDashboardData } from '../services/mockApi'

export const useFlashcardStore = defineStore('flashcards', {
  state: () => ({ data: null, loading: false, error: null }),
  getters: {
    decks: (state) => state.data?.recentDecks || [],
  },
  actions: {
    async loadDashboard() {
      this.loading = true
      this.error = null
      try {
        this.data = await getDashboardData()
      } catch (error) {
        this.error = error.message
      } finally {
        this.loading = false
      }
    },
  },
})