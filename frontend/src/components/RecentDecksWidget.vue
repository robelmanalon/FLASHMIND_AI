<script setup>
defineProps({ deck: { type: Object, required: true } })
const accent = { mint: '#22d3ee', gold: '#a78bfa', coral: '#c084fc' }
</script>

<template><article class="glass rounded-2xl p-5 transition hover:-translate-y-1 hover:border-indigo-400/30"><div class="mb-7 flex items-start justify-between"><span class="grid h-10 w-10 place-items-center rounded-xl bg-white/5 text-xl" :style="{ color: accent[deck.color] }">▦</span><button class="text-slate-500 hover:text-white" aria-label="Deck options">•••</button></div><h3 class="font-bold text-white">{{ deck.title }}</h3><p class="mt-2 text-sm text-slate-500">{{ deck.cards }} cards · {{ deck.lastStudied }}</p><div class="mt-5 flex items-center gap-3"><div class="h-1.5 flex-1 rounded-full bg-white/10"><div class="h-full rounded-full bg-gradient-to-r from-indigo-400 to-cyan-300" :style="{ width: `${deck.progress}%` }"></div></div><span class="text-xs font-bold text-slate-400">{{ deck.progress }}%</span></div></article></template>
