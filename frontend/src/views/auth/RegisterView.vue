<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import AuthLayout from './AuthLayout.vue'
import { register } from '../../services/api'
import { useAuthStore } from '../../stores/auth'
import { useUiStore } from '../../stores/ui'
import PasswordInput from '../../components/PasswordInput.vue'
import LogoLoader from '../../components/LogoLoader.vue'

const router = useRouter()
const auth = useAuthStore()
const ui = useUiStore()
const form = ref({ name: '', email: '', password: '' })
const loading = ref(false)
const error = ref('')
async function submit() {
	loading.value = true; error.value = ''
	const start = Date.now()
	try {
		const payload = await register(form.value)
		const elapsed = Date.now() - start
		if (elapsed < 1500) await new Promise((r) => setTimeout(r, 1500 - elapsed))
		if (!payload.access_token) { error.value = 'Account created. Check your email to confirm your account, then sign in.'; ui.toast('Check your email to confirm your account.', 'info'); return }
		auth.setSession(payload)
		await auth.refreshProfile().catch(() => {})
		ui.toast('Account created successfully!', 'success'); router.push('/dashboard')
	} catch (cause) { error.value = cause.message; ui.toast(cause.message, 'error') } finally { loading.value = false }
}
</script>

<template><LogoLoader v-if="loading" /><AuthLayout><p class="text-sm font-semibold text-cyan-300">Start learning smarter</p><h1 class="mt-2 text-3xl font-bold text-white">Create your account</h1><p class="mt-3 text-sm text-slate-400">Your personal study workspace is waiting.</p><form class="mt-8 space-y-5" @submit.prevent="submit"><label class="block text-sm font-semibold text-slate-300">Full name<input v-model="form.name" required type="text" autocomplete="name" placeholder="Alex Lee" class="mt-2 w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-white outline-none placeholder:text-slate-600 focus:border-cyan-300/60"></label><label class="block text-sm font-semibold text-slate-300">Email address<input v-model="form.email" required type="email" autocomplete="email" placeholder="you@example.com" class="mt-2 w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-white outline-none placeholder:text-slate-600 focus:border-cyan-300/60"></label><label class="block text-sm font-semibold text-slate-300">Password<PasswordInput v-model="form.password" minlength="8" autocomplete="new-password" placeholder="At least 8 characters" /></label><p v-if="error" class="rounded-lg bg-red-400/10 p-3 text-xs text-red-200">{{ error }}</p><button :disabled="loading" class="w-full rounded-xl bg-indigo-500 py-3.5 font-bold text-white shadow-lg shadow-indigo-500/20 disabled:opacity-50">{{ loading ? 'Creating account...' : 'Create free account' }}</button></form><p class="mt-7 text-center text-sm text-slate-500">Already have an account? <RouterLink to="/login" class="font-bold text-white">Sign in</RouterLink></p></AuthLayout></template>