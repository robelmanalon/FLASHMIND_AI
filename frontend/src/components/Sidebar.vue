<script setup>
import { useRoute } from 'vue-router'
import logoUrl from '../assets/logo.svg'

const route = useRoute()
const menu = [
  ['Dashboard', '/dashboard', '⌂'], ['My Decks', '/decks', '▦'], ['AI Generator', '/generator', '✦'],
  ['Quiz', '/quiz', '✓'], ['Study Session', '/study', '◷'], ['Progress', '/progress', '↗'], ['Settings', '/settings', '⚙'],
]
</script>

<template>
  <aside class="fixed inset-y-0 left-0 z-40 hidden w-72 border-r border-white/10 bg-[#0c0f1c]/95 p-6 backdrop-blur-xl lg:block">
    <RouterLink to="/" class="flex items-center gap-3 text-lg font-bold text-white"><img :src="logoUrl" alt="FlashMind AI" class="h-10 w-10 rounded-xl" /><span>FlashMind <span class="text-cyan-300">AI</span></span></RouterLink>
    <p class="mb-3 mt-12 px-3 text-[11px] font-bold uppercase tracking-[.2em] text-slate-500">Workspace</p>
    <nav class="space-y-1" aria-label="Primary navigation">
      <RouterLink v-for="item in menu" :key="item[1]" :to="item[1]" class="flex items-center gap-3 rounded-xl px-3 py-3 text-sm font-semibold text-slate-400 transition hover:bg-white/5 hover:text-white" :class="{ 'bg-indigo-500/15 text-indigo-200 ring-1 ring-indigo-400/20': route.path === item[1] }"><span class="grid h-6 w-6 place-items-center text-base text-cyan-300">{{ item[2] }}</span>{{ item[0] }}</RouterLink>
    </nav>
    <div class="absolute bottom-7 left-6 right-6 rounded-2xl border border-indigo-400/20 bg-gradient-to-br from-indigo-500/15 to-cyan-400/5 p-4"><div class="flex items-center justify-between"><p class="text-xs font-semibold text-slate-300">Weekly goal</p><span class="text-xs font-bold text-cyan-300">74%</span></div><div class="mt-3 h-1.5 rounded-full bg-white/10"><div class="h-full w-3/4 rounded-full bg-cyan-300"></div></div><p class="mt-3 text-xs text-slate-500">3 of 4 sessions complete</p></div>
  </aside>
</template>
