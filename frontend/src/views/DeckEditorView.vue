<script setup>
import { computed, onMounted, reactive } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AppLayout from '../layouts/AppLayout.vue'
import LoadingSpinner from '../components/LoadingSpinner.vue'
import { useDeckStore } from '../stores/decks'

const route = useRoute()
const router = useRouter()
const store = useDeckStore()
const isEdit = computed(() => Boolean(route.params.id))
const form = reactive({ id: null, title: '', subject: 'General', description: '', cards: [] })

onMounted(async () => {
  if (isEdit.value) {
    await store.loadDeck(route.params.id)
    if (store.current) Object.assign(form, store.current, { cards: store.current.cards.map((card) => ({ ...card })) })
  } else addCard()
})
function addCard() { form.cards.push({ id: Date.now() + form.cards.length, question: '', answer: '', bookmarked: false, favorite: false }) }
function removeCard(index) { if (form.cards.length > 1) form.cards.splice(index, 1) }
async function save() { if (!form.title.trim()) return; await store.save({ ...form, cards: form.cards.filter((card) => card.question.trim() && card.answer.trim()) }); router.push('/decks') }
</script>

<template>
  <AppLayout><div class="mx-auto max-w-4xl px-5 py-8 sm:px-8"><header class="flex items-end justify-between gap-4"><div><RouterLink to="/decks" class="text-sm font-semibold text-cyan-300">← Back to decks</RouterLink><h1 class="mt-3 text-3xl font-bold text-white">{{ isEdit ? 'Edit deck' : 'Create a deck' }}</h1><p class="mt-2 text-slate-400">Build a small, focused set of cards for your next session.</p></div></header><div v-if="store.loading" class="flex min-h-64 items-center justify-center"><LoadingSpinner /></div><form v-else class="mt-8 space-y-6" @submit.prevent="save"><section class="glass rounded-2xl p-6"><h2 class="text-lg font-bold text-white">Deck details</h2><div class="mt-5 grid gap-5 sm:grid-cols-2"><label class="text-sm font-semibold text-slate-300 sm:col-span-2">Deck name<input v-model="form.title" required placeholder="e.g. Organic chemistry" class="mt-2 w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-white outline-none placeholder:text-slate-600 focus:border-cyan-300/60"></label><label class="text-sm font-semibold text-slate-300">Subject<select v-model="form.subject" class="mt-2 w-full rounded-xl border border-white/10 bg-[#151a2c] px-4 py-3 text-white outline-none focus:border-cyan-300/60"><option>General</option><option>Biology</option><option>Languages</option><option>Design</option><option>History</option></select></label><label class="text-sm font-semibold text-slate-300">Description<input v-model="form.description" placeholder="What will you learn?" class="mt-2 w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-white outline-none placeholder:text-slate-600 focus:border-cyan-300/60"></label></div></section><section class="space-y-4"><div class="flex items-center justify-between"><h2 class="text-lg font-bold text-white">Flashcards <span class="text-sm font-normal text-slate-500">({{ form.cards.length }})</span></h2><button type="button" class="rounded-xl border border-cyan-300/20 px-4 py-2 text-sm font-bold text-cyan-300 hover:bg-cyan-300/10" @click="addCard">+ Add card</button></div><article v-for="(card, index) in form.cards" :key="card.id" class="glass rounded-2xl p-5"><div class="mb-4 flex items-center justify-between"><span class="text-xs font-bold uppercase tracking-[.18em] text-slate-500">Card {{ index + 1 }}</span><button type="button" class="text-xs font-semibold text-red-300 disabled:text-slate-600" :disabled="form.cards.length === 1" @click="removeCard(index)">Remove</button></div><div class="grid gap-4 sm:grid-cols-2"><textarea v-model="card.question" required rows="4" placeholder="Question or prompt" class="resize-none rounded-xl border border-white/10 bg-white/5 p-4 text-sm text-white outline-none placeholder:text-slate-600 focus:border-cyan-300/60"></textarea><textarea v-model="card.answer" required rows="4" placeholder="Answer or explanation" class="resize-none rounded-xl border border-white/10 bg-white/5 p-4 text-sm text-white outline-none placeholder:text-slate-600 focus:border-cyan-300/60"></textarea></div></article></section><div class="flex justify-end gap-3"><RouterLink to="/decks" class="rounded-xl border border-white/10 px-5 py-3 text-sm font-bold text-slate-300">Cancel</RouterLink><button :disabled="store.saving" class="rounded-xl bg-indigo-500 px-6 py-3 text-sm font-bold text-white disabled:opacity-50">{{ store.saving ? 'Saving...' : 'Save deck' }}</button></div></form></div></AppLayout>
</template>