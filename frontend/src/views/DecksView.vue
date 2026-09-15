<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import AppLayout from '../layouts/AppLayout.vue'
import LoadingSpinner from '../components/LoadingSpinner.vue'
import { useDeckStore } from '../stores/decks'
import ConfirmDialog from '../components/ConfirmDialog.vue'
import { useUiStore } from '../stores/ui'

const router = useRouter()
const store = useDeckStore()
const ui = useUiStore()
const deckPendingDelete = ref(null)
onMounted(() => store.loadDecks())

async function remove() {
  if (!deckPendingDelete.value) return
  await store.remove(deckPendingDelete.value.id)
  ui.toast('Deck deleted successfully', 'success')
  deckPendingDelete.value = null
}
</script>

<template>
  <AppLayout>
    <div class="mx-auto max-w-7xl px-5 py-8 sm:px-8">
      <header class="flex flex-col justify-between gap-5 sm:flex-row sm:items-end"><div><p class="text-sm font-medium text-cyan-300">Your library</p><h1 class="mt-2 text-3xl font-bold text-white sm:text-4xl">My decks</h1><p class="mt-2 text-slate-400">Keep every subject in one focused study space.</p></div><button class="rounded-xl bg-indigo-500 px-5 py-3 text-sm font-bold text-white shadow-lg shadow-indigo-500/20" @click="router.push('/decks/new')">+ Create deck</button></header>
      <div v-if="store.loading" class="flex min-h-72 items-center justify-center"><LoadingSpinner /></div>
      <div v-else class="mt-10 grid gap-5 md:grid-cols-2 xl:grid-cols-3">
        <article v-for="deck in store.decks" :key="deck.id" class="glass overflow-hidden rounded-2xl"><div :class="`h-2 bg-gradient-to-r ${deck.color}`"></div><div class="p-6"><div class="flex items-start justify-between"><div><span class="rounded-lg bg-white/5 px-2.5 py-1 text-[11px] font-bold uppercase tracking-wider text-slate-400">{{ deck.subject }}</span><h2 class="mt-4 text-xl font-bold text-white">{{ deck.title }}</h2></div><button class="text-slate-500 hover:text-white" aria-label="Deck options">•••</button></div><p class="mt-3 min-h-12 text-sm leading-6 text-slate-400">{{ deck.description }}</p><div class="mt-7 flex justify-between text-xs text-slate-500"><span>{{ deck.cards.length }} cards</span><span>Updated {{ deck.updated }}</span></div><div class="mt-3 h-1.5 rounded-full bg-white/10"><div class="h-full rounded-full bg-gradient-to-r from-indigo-400 to-cyan-300" :style="{ width: `${deck.progress}%` }"></div></div><div class="mt-6 flex gap-2"><button class="flex-1 rounded-xl bg-indigo-500/15 px-3 py-2.5 text-sm font-bold text-indigo-200 hover:bg-indigo-500/25" @click="router.push(`/study/${deck.id}`)">Study deck</button><button class="rounded-xl border border-white/10 px-3 py-2.5 text-sm font-bold text-slate-300 hover:bg-white/5" @click="router.push(`/decks/${deck.id}/edit`)">Edit</button><button class="rounded-xl border border-white/10 px-3 py-2.5 text-sm font-bold text-slate-500 hover:border-red-400/30 hover:text-red-300" @click="deckPendingDelete = deck">Delete</button></div></div></article>
      </div>
      <div v-if="!store.loading && !store.decks.length" class="glass mt-8 rounded-2xl p-12 text-center text-slate-400">No decks yet. Create your first study deck.</div>
    </div><ConfirmDialog v-if="deckPendingDelete" title="Delete deck?" :message="`This will remove ${deckPendingDelete.title} and its study progress.`" confirm-label="Delete deck" @cancel="deckPendingDelete = null" @confirm="remove" />
  </AppLayout>
</template>