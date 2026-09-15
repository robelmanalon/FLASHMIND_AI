<script setup>
import AppLayout from '../layouts/AppLayout.vue'
import { useFlashcardStore } from '../stores/flashcards'
import StatCard from '../components/StatCard.vue'
import RecentDecksWidget from '../components/RecentDecksWidget.vue'
import ContinueStudyingWidget from '../components/ContinueStudyingWidget.vue'
import TodaysProgressWidget from '../components/TodaysProgressWidget.vue'
import WeeklyStudyChart from '../components/WeeklyStudyChart.vue'
import RecentActivityWidget from '../components/RecentActivityWidget.vue'
import SkeletonBlock from '../components/SkeletonBlock.vue'
import { onMounted } from 'vue'
import { computed } from 'vue'
import { useAuthStore } from '../stores/auth'

const store = useFlashcardStore()
const auth = useAuthStore()
const firstName = computed(() => auth.user?.name?.split(' ')[0] || 'learner')
const greeting = computed(() => auth.user ? (auth.user.lastActiveAt ? 'Welcome back' : 'Good morning') : 'Welcome')
onMounted(() => store.loadDashboard())
</script>

<template>
  <AppLayout>
    <div class="mx-auto max-w-7xl px-5 py-8 sm:px-8">
      <header class="flex items-end justify-between gap-4"><div><p class="welcome-sub text-sm font-medium text-cyan-300">Monday, September 7</p><h1 class="welcome-heading mt-2 text-3xl font-bold tracking-tight text-white sm:text-4xl">{{ greeting }}, {{ firstName }}.</h1><p class="welcome-sub mt-2 text-slate-400">Your next breakthrough is one focused session away.</p></div><button class="hidden rounded-xl bg-indigo-500 px-5 py-3 text-sm font-bold text-white shadow-lg shadow-indigo-500/20 sm:block">+ Create deck</button></header>
      <section class="mt-9 grid gap-5 xl:grid-cols-[1.5fr_1fr]"><div class="relative overflow-hidden rounded-3xl bg-gradient-to-br from-indigo-500 to-purple-600 p-7 shadow-2xl shadow-indigo-950/30"><div class="relative z-10"><p class="text-sm font-bold uppercase tracking-wider text-indigo-100">Your next session</p><h2 class="mt-5 max-w-md text-3xl font-bold leading-tight text-white">Review 12 cards to keep your 7 day streak alive.</h2><button class="mt-7 rounded-xl bg-white px-5 py-3 text-sm font-bold text-indigo-700">Start studying <span aria-hidden="true">→</span></button></div><div class="absolute -right-12 -top-20 h-64 w-64 rounded-full border-[32px] border-white/10"></div></div><div class="glass rounded-3xl p-7"><p class="text-sm font-bold uppercase tracking-wider text-slate-400">Weekly focus</p><div class="mt-6 flex items-center gap-6"><div class="grid h-28 w-28 place-items-center rounded-full" style="background: conic-gradient(#22d3ee 74%, #273047 0)"><div class="grid h-20 w-20 place-items-center rounded-full bg-[#111522] text-xl font-bold">74%</div></div><div><p class="text-lg font-bold text-white">Almost there</p><p class="mt-1 text-sm leading-6 text-slate-400">Complete 2 more sessions to hit your weekly goal.</p></div></div></div></section>
      <div v-if="store.loading" class="mt-8 grid gap-4 sm:grid-cols-2 xl:grid-cols-4" aria-label="Loading dashboard"><div v-for="item in 4" :key="item" class="glass rounded-2xl p-5"><SkeletonBlock class-name="h-4 w-24" /><SkeletonBlock class-name="mt-5 h-8 w-28" /><SkeletonBlock class-name="mt-3 h-3 w-36" /></div></div>
      <template v-else-if="store.data">
        <section class="mt-8 grid gap-4 sm:grid-cols-2 xl:grid-cols-4"><StatCard v-for="stat in store.data.stats" :key="stat.label" v-bind="stat" /></section>
        <section class="mt-10 grid gap-5 xl:grid-cols-[1.35fr_1fr]"><ContinueStudyingWidget :session="store.data.continueStudying" /><TodaysProgressWidget :progress="store.data.todayProgress" /></section>
        <section class="mt-5 grid gap-5 xl:grid-cols-[1.35fr_1fr]"><WeeklyStudyChart :study="store.data.weeklyStudy" /><RecentActivityWidget :activity="store.data.activity" /></section>
        <section class="mt-10"><div class="flex items-center justify-between"><h2 class="text-xl font-bold text-white">Recent decks</h2><a href="/decks" class="text-sm font-bold text-cyan-300">View all →</a></div><div class="mt-5 grid gap-4 md:grid-cols-3"><RecentDecksWidget v-for="deck in store.data.recentDecks" :key="deck.id" :deck="deck" /></div></section>
      </template>
    </div>
  </AppLayout>
</template>

<style scoped>
/* Fade-in subtitle */
.welcome-sub {
  opacity: 0;
  animation: welcome-fade-up 0.8s ease forwards 0.2s;
}

/* Main heading: fade-in + glow */
.welcome-heading {
  position: relative;
  display: inline-block;
  opacity: 0;
  animation:
    welcome-fade-up 0.8s ease forwards 0.5s,
    welcome-glow 3s ease-in-out infinite alternate 1.3s;
}

/* Shine sweep layer */
.welcome-heading::after {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent 0%, #00f3ff 50%, transparent 100%);
  background-size: 200% 100%;
  background-position: -200% 0;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: welcome-shine 3s ease-in-out infinite 1.5s;
  pointer-events: none;
}

@media (prefers-reduced-motion: reduce) {
  .welcome-sub, .welcome-heading {
    animation-duration: 0.6s !important;
    animation-iteration-count: 1 !important;
  }
  .welcome-heading::after { animation: none; }
}

@keyframes welcome-fade-up {
  from { opacity: 0; transform: translateY(16px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes welcome-glow {
  0% { text-shadow: 0 0 10px rgba(0, 243, 255, 0.2); }
  100% { text-shadow: 0 0 20px rgba(0, 243, 255, 0.6), 0 0 30px rgba(168, 85, 247, 0.4); }
}

@keyframes welcome-shine {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}
</style>