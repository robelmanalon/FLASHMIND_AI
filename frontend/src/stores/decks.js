import { defineStore } from 'pinia'
import { deleteDeck, getDeck, getDecks, saveDeck } from '../services/deckApi'

export const useDeckStore = defineStore('decks', {
  state: () => ({ decks: [], current: null, loading: false, saving: false, error: null }),
  actions: {
    async loadDecks() {
      this.loading = true
      this.error = null
      try { this.decks = await getDecks() } catch (error) { this.error = error.message } finally { this.loading = false }
    },
    async loadDeck(id) {
      this.loading = true
      this.error = null
      try { this.current = await getDeck(id) } catch (error) { this.error = error.message } finally { this.loading = false }
    },
    async save(payload) {
      this.saving = true
      try {
        const deck = await saveDeck(payload)
        this.current = deck
        await this.loadDecks()
        return deck
      } finally { this.saving = false }
    },
    async remove(id) {
      await deleteDeck(id)
      this.decks = this.decks.filter((deck) => String(deck.id) !== String(id))
    },
  },
})