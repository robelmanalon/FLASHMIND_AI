<script setup>
import logoUrl from '../../assets/logo.svg'
</script>

<template><div class="mesh-bg flex min-h-screen items-center justify-center px-5 py-10"><div class="w-full max-w-md"><RouterLink to="/" class="mx-auto flex w-fit items-center gap-3 text-lg font-bold text-white"><img :src="logoUrl" alt="FlashMind AI" class="h-10 w-10 rounded-xl" />FlashMind <span class="text-cyan-300">AI</span></RouterLink><div class="glass mt-8 rounded-3xl p-7 sm:p-9"><slot /></div><p class="mt-7 text-center text-xs text-slate-500">By continuing, you agree to our Terms and Privacy Policy.</p></div></div></template>