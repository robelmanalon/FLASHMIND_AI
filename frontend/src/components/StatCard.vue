<script setup>
defineProps({ label: String, value: String, detail: String, icon: String, tone: String })
</script>

<template><div class="glass rounded-2xl p-5"><div class="flex items-start justify-between"><p class="text-sm text-slate-400">{{ label }}</p><span :class="['grid h-8 w-8 place-items-center rounded-lg', tone === 'cyan' ? 'bg-cyan-400/10 text-cyan-300' : tone === 'purple' ? 'bg-purple-400/10 text-purple-300' : 'bg-indigo-400/10 text-indigo-300']">{{ icon }}</span></div><p class="mt-4 text-2xl font-bold text-white">{{ value }}</p><p class="mt-1 text-xs text-slate-500">{{ detail }}</p></div></template>
