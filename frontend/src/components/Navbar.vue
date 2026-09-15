<script setup>
import { ref } from 'vue'
import { useUiStore } from '../stores/ui'
import { useAuthStore } from '../stores/auth'
const profileOpen = ref(false)
const ui = useUiStore()
const auth = useAuthStore()
function logout() { auth.logout(); window.location.href = '/login' }
</script>

<template>
  <header class="flex h-20 items-center justify-between border-b border-white/10 px-5 sm:px-8"><div class="hidden items-center gap-2 text-sm text-slate-500 md:flex"><span>Workspace</span><span>/</span><span class="text-slate-300">Overview</span></div><div class="ml-auto flex items-center gap-2"><button class="grid h-10 w-10 place-items-center rounded-xl border border-white/10 text-lg text-slate-400 hover:bg-white/5" :aria-label="ui.theme === 'dark' ? 'Switch to light theme' : 'Switch to dark theme'" @click="ui.toggleTheme">{{ ui.theme === 'dark' ? '☼' : '☾' }}</button><button class="grid h-10 w-10 place-items-center rounded-xl border border-white/10 text-lg text-slate-400 hover:bg-white/5" aria-label="Notifications">♧<span class="absolute ml-4 mt-[-18px] h-2 w-2 rounded-full bg-cyan-300"></span></button><div class="relative"><button class="flex items-center gap-3 rounded-xl px-2 py-1.5 hover:bg-white/5" :aria-expanded="profileOpen" aria-haspopup="menu" @click="profileOpen = !profileOpen"><img v-if="auth.user?.avatar_url" :src="auth.user.avatar_url" alt="Profile" class="h-9 w-9 rounded-full object-cover" /><span v-else class="grid h-9 w-9 place-items-center rounded-full bg-gradient-to-br from-purple-400 to-indigo-500 text-sm font-bold text-white">{{ auth.user?.name?.slice(0, 2).toUpperCase() || 'AL' }}</span><span class="hidden text-left sm:block"><span class="block text-sm font-bold text-white">{{ auth.user?.name || 'Learner' }}</span><span class="block text-xs text-slate-500">{{ auth.user?.email || 'Guest' }}</span></span><span class="text-slate-500">⌄</span></button><div v-if="profileOpen" class="glass absolute right-0 top-14 z-20 w-44 rounded-xl p-2" role="menu"><RouterLink to="/settings" class="block rounded-lg px-3 py-2 text-sm text-slate-300 hover:bg-white/5">Account settings</RouterLink><button class="block w-full rounded-lg px-3 py-2 text-left text-sm text-slate-300 hover:bg-white/5" @click="logout">Sign out</button></div></div></div></header>
</template>
