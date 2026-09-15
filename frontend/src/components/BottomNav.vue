<script setup>
import { useRoute } from 'vue-router'

const route = useRoute()
const menu = [
  ['Dashboard', '/dashboard', 'M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z'],
  ['Deck', '/decks', 'M4 6H2v14c0 1.1.9 2 2 2h14v-2H4V6zm16-4H8c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm-1 9H9V9h10v2zm-4 4H9v-2h6v2zm4-8H9V5h10v2z'],
  ['AI', '/generator', 'M13 2L3 14h9l-1 8 10-12h-9l1-8z'],
  ['Quiz', '/quiz', 'M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z'],
  ['Study', '/study', 'M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm.5-13H11v6l5.25 3.15.75-1.23-4.5-2.67z'],
  ['Progress', '/progress', 'M16 6l2.29 2.29-4.88 4.88-4-4L2 16.59 3.41 18l6-6 4 4 6.3-6.29L22 12V6z'],
  ['Settings', '/settings', 'M19.14 12.94c.04-.3.06-.61.06-.94 0-.32-.02-.64-.07-.94l2.03-1.58c.18-.14.23-.41.12-.61l-1.92-3.32c-.12-.22-.37-.29-.59-.22l-2.39.96c-.5-.38-1.03-.7-1.62-.94l-.36-2.54c-.04-.24-.24-.41-.48-.41h-3.84c-.24 0-.43.17-.47.41l-.36 2.54c-.59.24-1.13.57-1.62.94l-2.39-.96c-.22-.08-.47 0-.59.22L2.74 8.87c-.12.21-.08.47.12.61l2.03 1.58c-.05.3-.07.62-.07.94s.02.64.07.94l-2.03 1.58c-.18.14-.23.41-.12.61l1.92 3.32c.12.22.37.29.59.22l2.39-.96c.5.38 1.03.7 1.62.94l.36 2.54c.05.24.24.41.48.41h3.84c.24 0 .44-.17.47-.41l.36-2.54c.59-.24 1.13-.56 1.62-.94l2.39.96c.22.08.47 0 .59-.22l1.92-3.32c.12-.22.07-.47-.12-.61l-2.01-1.58zM12 15.6c-1.98 0-3.6-1.62-3.6-3.6s1.62-3.6 3.6-3.6 3.6 1.62 3.6 3.6-1.62 3.6-3.6 3.6z'],
]
const isActive = (path) => path === '/' ? route.path === '/' : route.path.startsWith(path)
</script>

<template>
  <nav class="fixed inset-x-0 bottom-0 z-40 flex justify-center pb-4 lg:hidden" aria-label="Primary navigation">
    <div class="flex items-center gap-2 border border-white/10 bg-slate-900/75 px-3 py-2 backdrop-blur-xl" style="border-radius: 28px; box-shadow: 0 20px 40px rgba(0,0,0,0.6), inset 0 1px 0 rgba(255,255,255,0.15);">
      <RouterLink
        v-for="item in menu" :key="item[1]" :to="item[1]"
        class="relative flex h-14 w-14 flex-col items-center justify-center rounded-[18px] text-slate-500 outline-none transition-colors duration-300"
        :class="{ 'active text-white': isActive(item[1]) }"
      >
        <div class="active-bg"></div>
        <svg class="relative z-[3] h-5 w-5 fill-current transition-all duration-300" viewBox="0 0 24 24"><path :d="item[2]"/></svg>
        <span class="relative z-[3] mt-1 text-[10px] font-semibold tracking-wide">{{ item[0] }}</span>
      </RouterLink>
    </div>
  </nav>
</template>

<style scoped>
.active .active-bg {
  position: absolute;
  inset: 0;
  border-radius: 18px;
  background: linear-gradient(135deg, rgba(129, 140, 248, 0.2), rgba(0, 243, 255, 0.15));
  border: 1px solid rgba(0, 243, 255, 0.4);
  box-shadow: 0 0 15px rgba(0, 243, 255, 0.2);
}
.active svg {
  transform: translateY(-2px) scale(1.1);
  color: #00f3ff;
  filter: drop-shadow(0 0 6px #00f3ff);
}
.active .active-bg + svg + span {
  color: #00f3ff;
  opacity: 1;
}
</style>