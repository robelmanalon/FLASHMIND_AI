<script setup>
defineProps({ title: { type: String, default: '' } })
defineEmits(['close'])
</script>

<template>
  <div class="fixed inset-0 z-[90] grid place-items-center bg-slate-950/70 p-5 backdrop-blur-sm" role="presentation" @click.self="$emit('close')"><section class="glass w-full max-w-lg rounded-2xl p-6" role="dialog" aria-modal="true" :aria-label="title"><div class="flex items-center justify-between"><h2 class="text-lg font-bold text-white">{{ title }}</h2><button class="text-xl text-slate-500 hover:text-white" aria-label="Close dialog" @click="$emit('close')">×</button></div><div class="mt-5"><slot /></div></section></div>
</template>