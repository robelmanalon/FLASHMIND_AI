import { defineStore } from 'pinia'

export const useUiStore = defineStore('ui', {
  state: () => ({ theme: localStorage.getItem('flashmind-theme') || 'dark', toasts: [], modal: null }),
  actions: {
    toggleTheme() {
      this.theme = this.theme === 'dark' ? 'light' : 'dark'
      localStorage.setItem('flashmind-theme', this.theme)
      document.documentElement.dataset.theme = this.theme
    },
    toast(message, type = 'info') {
      const id = Date.now() + Math.random()
      this.toasts.push({ id, message, type })
      window.setTimeout(() => this.dismissToast(id), 3800)
    },
    dismissToast(id) { this.toasts = this.toasts.filter((toast) => toast.id !== id) },
    openModal(modal) { this.modal = modal },
    closeModal() { this.modal = null },
  },
})