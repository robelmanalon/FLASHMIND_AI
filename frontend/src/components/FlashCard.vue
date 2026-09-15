<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
  card: { type: Object, required: true },
  index: { type: Number, default: 0 },
})
const emit = defineEmits(['update:card'])
const flipped = ref(false)
const isBookmarked = computed(() => props.card.bookmarked)
const isFavorite = computed(() => props.card.favorite)

function toggle(key) {
  emit('update:card', { ...props.card, [key]: !props.card[key] })
}

defineExpose({ flip: () => { flipped.value = !flipped.value } })
</script>

<template>
  <div class="group relative h-[min(52vh,430px)] min-h-[290px] w-full max-w-3xl cursor-pointer [perspective:1400px]" @click="flipped = !flipped">
    <div class="relative h-full w-full transition-transform duration-700 [transform-style:preserve-3d]" :class="{ '[transform:rotateY(180deg)]': flipped }">
      <section class="absolute inset-0 flex flex-col items-center justify-center rounded-[2rem] border border-white/10 bg-gradient-to-br from-[#202742] via-[#171b30] to-[#101423] p-8 text-center shadow-2xl shadow-black/30 [backface-visibility:hidden] sm:p-14"><span class="absolute left-7 top-7 text-xs font-bold uppercase tracking-[.2em] text-cyan-300">Question {{ index + 1 }}</span><span class="absolute right-7 top-7 text-xs text-slate-500">Click to flip</span><h2 class="max-w-2xl text-2xl font-bold leading-relaxed text-white sm:text-4xl">{{ card.question }}</h2><p class="absolute bottom-8 text-xs text-slate-500">Think of your answer, then reveal it</p></section>
      <section class="absolute inset-0 flex rotate-y-180 flex-col items-center justify-center rounded-[2rem] border border-cyan-300/20 bg-gradient-to-br from-cyan-950/80 via-[#151d32] to-indigo-950/80 p-8 text-center shadow-2xl shadow-cyan-950/20 [backface-visibility:hidden] sm:p-14"><span class="absolute left-7 top-7 text-xs font-bold uppercase tracking-[.2em] text-cyan-300">Answer</span><h2 class="max-w-2xl text-xl font-medium leading-relaxed text-slate-100 sm:text-3xl">{{ card.answer }}</h2><p class="absolute bottom-8 text-xs text-slate-500">Click to see the question</p></section>
    </div>
    <div class="absolute bottom-5 right-5 z-10 flex gap-2" @click.stop><button class="grid h-9 w-9 place-items-center rounded-lg bg-black/20 text-lg transition hover:bg-white/10" :class="isBookmarked ? 'text-cyan-300' : 'text-slate-500'" aria-label="Bookmark card" @click="toggle('bookmarked')">⌑</button><button class="grid h-9 w-9 place-items-center rounded-lg bg-black/20 text-lg transition hover:bg-white/10" :class="isFavorite ? 'text-pink-300' : 'text-slate-500'" aria-label="Favorite card" @click="toggle('favorite')">♥</button></div>
  </div>
</template>

<style scoped>
.rotate-y-180 { transform: rotateY(180deg); }
</style>