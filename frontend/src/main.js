import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

// Keep global state, routing, and the persisted theme available before the first render.
const app = createApp(App)
const pinia = createPinia()
app.use(pinia).use(router).mount('#app')
document.documentElement.dataset.theme = localStorage.getItem('flashmind-theme') || 'dark'
