<script setup>
import { useUiStore } from '../stores/ui'

const ui = useUiStore()
</script>

<template>
  <div class="fixed right-4 top-4 z-[100] flex w-[min(22rem,calc(100vw-2rem))] flex-col gap-3" aria-live="polite"><div v-for="toast in ui.toasts" :key="toast.id" class="glass flex items-start gap-3 rounded-xl p-4 shadow-2xl" role="status"><span class="mt-0.5" :class="toast.type === 'error' ? 'text-red-300' : toast.type === 'success' ? 'text-emerald-300' : 'text-cyan-300'">{{ toast.type === 'error' ? '!' : toast.type === 'success' ? '✓' : 'i' }}</span><p class="flex-1 text-sm text-slate-200">{{ toast.message }}</p><button class="text-slate-500 hover:text-white" aria-label="Dismiss notification" @click="ui.dismissToast(toast.id)">×</button></div></div>
</template>