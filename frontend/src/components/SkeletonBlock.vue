<script setup>
defineProps({ className: { type: String, default: 'h-4 w-full' } })
</script>

<template><div :class="['animate-pulse rounded-lg bg-white/10', className]" aria-hidden="true"></div></template>