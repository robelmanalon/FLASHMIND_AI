<script setup>
import { computed, ref } from 'vue'
import AppLayout from '../layouts/AppLayout.vue'
import { useAuthStore } from '../stores/auth'
import { useUiStore } from '../stores/ui'
import { updateProfile, getApiUrl, setApiUrl } from '../services/api'

const auth = useAuthStore()
const ui = useUiStore()

const editName = ref(auth.user?.name || '')
const editAvatar = ref(auth.user?.avatar_url || '')
const saving = ref(false)
const saved = ref(false)
const fileInput = ref(null)
const serverUrl = ref(getApiUrl())

const initials = computed(() => (auth.user?.name || 'Guest').split(' ').map((part) => part[0]).join('').slice(0, 2).toUpperCase())
const memberSince = computed(() => {
	if (!auth.user?.created_at) return '—'
	return new Date(auth.user.created_at).toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric' })
})

function onFileChange(e) {
	const file = e.target.files?.[0]
	if (!file) return
	if (file.size > 2 * 1024 * 1024) {
		ui.toast('Image must be under 2 MB', 'error')
		return
	}
	const reader = new FileReader()
	reader.onload = () => { editAvatar.value = reader.result }
	reader.readAsDataURL(file)
}

function removeAvatar() {
	editAvatar.value = ''
	if (fileInput.value) fileInput.value.value = ''
}

async function saveProfile() {
	if (!editName.value.trim()) {
		ui.toast('Name cannot be empty', 'error')
		return
	}
	saving.value = true
	saved.value = false
	try {
		const data = await updateProfile({ name: editName.value.trim(), avatar_url: editAvatar.value || null })
		auth.updateUserData({ name: data.name, avatar_url: data.avatar_url })
		saved.value = true
		ui.toast('Profile updated successfully', 'success')
		setTimeout(() => { saved.value = false }, 2000)
	} catch (err) {
		ui.toast(err.message || 'Failed to update profile', 'error')
	} finally {
		saving.value = false
	}
}

function signOut() {
	auth.logout()
	window.location.href = '/login'
}

function saveServerUrl() {
	const url = serverUrl.value.trim().replace(/\/+$/, '')
	if (!url) {
		ui.toast('Server URL cannot be empty', 'error')
		return
	}
	const cached = localStorage.getItem('flashmind-api-url')
	if (cached === url) {
		ui.toast('Server URL already saved', 'info')
		return
	}
	localStorage.setItem('flashmind-api-url', url)
	if (url === import.meta.env.VITE_API_URL) {
		localStorage.removeItem('flashmind-api-url')
	}
	ui.toast('Server URL saved. Reopen the app to apply.', 'success')
}

function resetServerUrl() {
	localStorage.removeItem('flashmind-api-url')
	serverUrl.value = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'
	ui.toast('Server URL reset to default', 'success')
}
</script>

<template>
	<AppLayout>
		<div class="mx-auto max-w-3xl px-5 py-8 sm:px-8">
			<header class="flex items-end justify-between gap-4"><div><p class="text-sm font-medium text-cyan-300">Account</p><h1 class="mt-2 text-3xl font-bold tracking-tight text-white">Settings</h1><p class="mt-2 text-slate-400">Manage your profile and preferences.</p></div></header>

			<section class="mt-9 rounded-3xl bg-gradient-to-br from-indigo-500 to-purple-600 p-7 shadow-2xl shadow-indigo-950/30"><div class="flex items-center gap-5"><span v-if="!editAvatar" class="grid h-16 w-16 place-items-center rounded-2xl bg-white/15 text-xl font-bold text-white">{{ initials }}</span><img v-else :src="editAvatar" alt="Profile picture" class="h-16 w-16 rounded-2xl object-cover ring-2 ring-white/20" /><div><p class="text-xl font-bold text-white">{{ auth.user?.name || 'Guest' }}</p><p class="mt-1 text-sm text-indigo-100">{{ auth.user?.email || 'Sign in to manage your account' }}</p><p class="mt-1 text-xs text-indigo-200/80">Member since {{ memberSince }}</p></div></div></section>

			<section class="mt-6 rounded-3xl border border-white/10 bg-white/5 p-7">
				<h2 class="text-lg font-bold text-white">Edit Profile</h2>
				<p class="mt-1 text-sm text-slate-400">Update your name and profile picture.</p>

				<div class="mt-6 flex items-center gap-5">
					<div class="relative group">
						<button v-if="!editAvatar" class="grid h-20 w-20 place-items-center rounded-2xl bg-gradient-to-br from-indigo-400 to-cyan-300 text-2xl font-bold text-slate-950 transition hover:opacity-80" @click="fileInput?.click()">{{ initials }}</button>
						<button v-else class="relative block" @click="fileInput?.click()">
							<img :src="editAvatar" alt="Profile picture" class="h-20 w-20 rounded-2xl object-cover ring-2 ring-white/20 transition hover:ring-cyan-300/50" />
							<span class="absolute inset-0 grid place-items-center rounded-2xl bg-black/50 text-xs font-bold text-white opacity-0 transition group-hover:opacity-100">Change</span>
						</button>
						<button v-if="editAvatar" class="absolute -right-2 -top-2 grid h-6 w-6 place-items-center rounded-full bg-red-500 text-xs text-white shadow-lg transition hover:bg-red-400" aria-label="Remove profile picture" @click="removeAvatar">✕</button>
						<input ref="fileInput" type="file" accept="image/*" class="hidden" @change="onFileChange" />
					</div>
					<div>
						<p class="text-sm font-semibold text-white">Profile Picture</p>
						<p class="mt-1 text-xs text-slate-400">JPG, PNG or GIF. Max 2 MB.</p>
						<button class="mt-2 text-xs font-semibold text-cyan-300 transition hover:text-cyan-200" @click="fileInput?.click()">Upload image</button>
					</div>
				</div>

				<div class="mt-6">
					<label for="settings-name" class="block text-sm font-semibold text-slate-300">Display Name</label>
					<input id="settings-name" v-model="editName" type="text" maxlength="80" class="mt-2 w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-white placeholder-slate-500 outline-none transition focus:border-cyan-400/50 focus:ring-2 focus:ring-cyan-400/20" placeholder="Your name" />
				</div>

				<div class="mt-6">
					<label class="block text-sm font-semibold text-slate-300">Email</label>
					<input :value="auth.user?.email" type="email" disabled class="mt-2 w-full cursor-not-allowed rounded-xl border border-white/5 bg-white/[0.02] px-4 py-3 text-sm text-slate-500" />
					<p class="mt-1.5 text-xs text-slate-500">Email cannot be changed from here.</p>
				</div>

				<div class="mt-7 flex items-center gap-3">
					<button class="rounded-xl bg-indigo-500 px-6 py-2.5 text-sm font-bold text-white shadow-lg shadow-indigo-500/20 transition hover:bg-indigo-400 disabled:cursor-not-allowed disabled:opacity-50" :disabled="saving" @click="saveProfile">{{ saving ? 'Saving...' : 'Save changes' }}</button>
					<span v-if="saved" class="text-sm font-semibold text-emerald-400">✓ Saved</span>
				</div>
			</section>

			<section class="mt-6 rounded-3xl border border-white/10 bg-white/5 p-7">
				<h2 class="text-lg font-bold text-white">Server Connection</h2>
				<p class="mt-1 text-sm text-slate-400">Backend API address. Set this to your computer's LAN IP (e.g. http://192.168.10.5:8000) when using the app on a phone.</p>
				<div class="mt-5 flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
					<input v-model="serverUrl" type="text" placeholder="http://192.168.x.x:8000" class="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-white placeholder-slate-500 outline-none transition focus:border-cyan-400/50 focus:ring-2 focus:ring-cyan-400/20 sm:max-w-md" />
					<div class="flex shrink-0 gap-2">
						<button class="rounded-xl bg-indigo-500 px-5 py-2.5 text-sm font-bold text-white shadow-lg shadow-indigo-500/20 transition hover:bg-indigo-400" @click="saveServerUrl">Save URL</button>
						<button class="rounded-xl border border-white/10 bg-white/5 px-5 py-2.5 text-sm font-semibold text-slate-300 transition hover:bg-white/10" @click="resetServerUrl">Reset</button>
					</div>
				</div>
			</section>

			<section class="mt-6 rounded-3xl border border-white/10 bg-white/5 p-7"><div class="flex items-center justify-between"><div><h2 class="text-lg font-bold text-white">Appearance</h2><p class="mt-1 text-sm text-slate-400">Switch between light and dark mode.</p></div><button class="flex items-center gap-2 rounded-xl border border-white/10 bg-white/5 px-4 py-2.5 text-sm font-semibold text-slate-300 transition hover:bg-white/10" @click="ui.toggleTheme"><span aria-hidden="true">{{ ui.theme === 'dark' ? '☼' : '☾' }}</span>{{ ui.theme === 'dark' ? 'Dark mode' : 'Light mode' }}</button></div></section>

			<section class="mt-6 rounded-3xl border border-white/10 bg-white/5 p-7"><div class="flex items-center justify-between"><div><h2 class="text-lg font-bold text-white">Signed in as</h2><p class="mt-1 text-sm text-slate-400">{{ auth.user?.email || 'No active session' }}</p></div><button class="rounded-xl bg-indigo-500 px-5 py-2.5 text-sm font-bold text-white shadow-lg shadow-indigo-500/20 transition hover:bg-indigo-400" @click="signOut">Sign out</button></div></section>
		</div>
	</AppLayout>
</template>
