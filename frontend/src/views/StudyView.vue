<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AppLayout from '../layouts/AppLayout.vue'
import FlashCard from '../components/FlashCard.vue'
import LoadingSpinner from '../components/LoadingSpinner.vue'
import { useDeckStore } from '../stores/decks'
import { recordStudyReview } from '../services/api'

const route = useRoute()
const router = useRouter()
const store = useDeckStore()
const currentIndex = ref(0)
const cardRef = ref(null)
const shuffled = ref(false)
const cards = ref([])
const currentCard = computed(() => cards.value[currentIndex.value])
const progress = computed(() => cards.value.length ? ((currentIndex.value + 1) / cards.value.length) * 100 : 0)

onMounted(async () => {
  await store.loadDecks()
  if (!store.decks.length) return
  const wanted = route.params.id
  const match = store.decks.find((deck) => String(deck.id) === String(wanted))
  const deck = match || store.decks[0]
  await store.loadDeck(deck.id)
  cards.value = [...(store.current?.cards || [])]
})
function next() { if (currentIndex.value < cards.value.length - 1) currentIndex.value += 1 }
function previous() { if (currentIndex.value > 0) currentIndex.value -= 1 }
function updateCard(card) { cards.value[currentIndex.value] = card }
function shuffle() { cards.value = [...cards.value].sort(() => Math.random() - .5); currentIndex.value = 0; shuffled.value = true }
async function rate(rating) {
  try { await recordStudyReview(currentCard.value.id, rating) } catch { /* Allow the mock study flow when the API is offline. */ }
  next()
}
function onKeydown(event) { if (['INPUT', 'TEXTAREA'].includes(event.target.tagName)) return; if (event.key === ' ') { event.preventDefault(); cardRef.value?.flip() } if (event.key === 'ArrowRight') next(); if (event.key === 'ArrowLeft') previous(); if (['1', '2', '3', '4'].includes(event.key)) rate(['again', 'hard', 'good', 'easy'][Number(event.key) - 1]) }
onMounted(() => window.addEventListener('keydown', onKeydown))
onBeforeUnmount(() => window.removeEventListener('keydown', onKeydown))
</script>

<template>
  <AppLayout><div class="mx-auto max-w-5xl px-5 py-6 sm:px-8"><header class="flex items-center justify-between gap-4"><div><button class="text-sm font-semibold text-cyan-300" @click="router.push('/decks')">← Exit session</button><h1 class="mt-3 text-2xl font-bold text-white sm:text-3xl">{{ store.current?.title || 'Study session' }}</h1></div><button class="rounded-xl border border-white/10 px-4 py-2.5 text-sm font-bold text-slate-300 hover:bg-white/5" :class="{ 'text-cyan-300': shuffled }" @click="shuffle">⇄ Shuffle</button></header><div v-if="store.loading || !currentCard" class="flex min-h-[55vh] items-center justify-center"><LoadingSpinner /></div><template v-else><div class="mx-auto mt-8 max-w-3xl"><div class="mb-3 flex items-center justify-between text-xs font-bold text-slate-500"><span>Card {{ currentIndex + 1 }} of {{ cards.length }}</span><span>{{ Math.round(progress) }}% complete</span></div><div class="h-1.5 rounded-full bg-white/10"><div class="h-full rounded-full bg-gradient-to-r from-indigo-400 to-cyan-300 transition-all" :style="{ width: `${progress}%` }"></div></div></div><div class="mt-8 flex justify-center"><FlashCard ref="cardRef" :card="currentCard" :index="currentIndex" @update:card="updateCard" /></div><div class="mx-auto mt-7 flex max-w-3xl items-center justify-between gap-3"><button class="rounded-xl border border-white/10 px-4 py-3 text-sm font-bold text-slate-400 disabled:opacity-30" :disabled="currentIndex === 0" @click="previous">← Previous</button><div class="hidden items-center gap-2 text-[11px] text-slate-600 sm:flex"><kbd>Space</kbd> flip <kbd>←</kbd><kbd>→</kbd> navigate</div><button class="rounded-xl border border-white/10 px-4 py-3 text-sm font-bold text-slate-400 disabled:opacity-30" :disabled="currentIndex === cards.length - 1" @click="next">Next →</button></div><div class="mx-auto mt-8 grid max-w-3xl grid-cols-4 gap-2 sm:gap-3"><button v-for="(label, index) in ['Again', 'Hard', 'Good', 'Easy']" :key="label" class="rounded-xl border px-2 py-3 text-xs font-bold transition sm:text-sm" :class="index === 0 ? 'border-red-400/20 bg-red-400/5 text-red-300 hover:bg-red-400/10' : index === 1 ? 'border-orange-400/20 bg-orange-400/5 text-orange-300 hover:bg-orange-400/10' : index === 2 ? 'border-cyan-400/20 bg-cyan-400/5 text-cyan-300 hover:bg-cyan-400/10' : 'border-indigo-400/20 bg-indigo-400/5 text-indigo-300 hover:bg-indigo-400/10'" @click="rate(['again', 'hard', 'good', 'easy'][index])">{{ label }} <span class="hidden opacity-50 sm:inline">{{ index + 1 }}</span></button></div></template></div></AppLayout>
</template>