<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import AuthLayout from './AuthLayout.vue'
import { login } from '../../services/api'
import { useAuthStore } from '../../stores/auth'
import { useUiStore } from '../../stores/ui'
import PasswordInput from '../../components/PasswordInput.vue'
import LogoLoader from '../../components/LogoLoader.vue'

const router = useRouter()
const auth = useAuthStore()
const ui = useUiStore()
const form = ref({ email: '', password: '' })
const loading = ref(false)
const error = ref('')
async function submit() {
	loading.value = true; error.value = ''
	const start = Date.now()
	try {
		const result = await login(form.value)
		const elapsed = Date.now() - start
		if (elapsed < 1500) await new Promise((r) => setTimeout(r, 1500 - elapsed))
		auth.setSession(result)
		await auth.refreshProfile().catch(() => {})
		ui.toast('Welcome back!', 'success'); router.push('/dashboard')
	} catch (cause) { error.value = cause.message; ui.toast(cause.message, 'error') } finally { loading.value = false }
}
</script>

<template><LogoLoader v-if="loading" /><AuthLayout><p class="text-sm font-semibold text-cyan-300">Welcome back</p><h1 class="mt-2 text-3xl font-bold text-white">Sign in to your workspace</h1><p class="mt-3 text-sm text-slate-400">Pick up where your learning left off.</p><form class="mt-8 space-y-5" @submit.prevent="submit"><label class="block text-sm font-semibold text-slate-300">Email address<input v-model="form.email" required type="email" autocomplete="email" placeholder="you@example.com" class="mt-2 w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-white outline-none placeholder:text-slate-600 focus:border-cyan-300/60"></label><label class="block text-sm font-semibold text-slate-300">Password<PasswordInput v-model="form.password" autocomplete="current-password" /></label><div class="flex justify-end"><RouterLink to="/forgot-password" class="text-xs font-semibold text-cyan-300">Forgot password?</RouterLink></div><p v-if="error" class="rounded-lg bg-red-400/10 p-3 text-xs text-red-200">{{ error }}</p><button :disabled="loading" class="w-full rounded-xl bg-indigo-500 py-3.5 font-bold text-white shadow-lg shadow-indigo-500/20 disabled:opacity-50">{{ loading ? 'Signing in...' : 'Sign in' }}</button></form><p class="mt-7 text-center text-sm text-slate-500">New to FlashMind? <RouterLink to="/register" class="font-bold text-white">Create an account</RouterLink></p></AuthLayout></template>