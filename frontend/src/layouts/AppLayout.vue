<script setup>
import Sidebar from '../components/Sidebar.vue'
import Navbar from '../components/Navbar.vue'
import BottomNav from '../components/BottomNav.vue'
</script>

<template>
  <div class="mesh-bg min-h-screen text-slate-100">
    <Sidebar />
    <main class="min-h-screen pb-24 lg:pb-0 lg:pl-72"><Navbar /><slot /></main>
    <BottomNav />
  </div>
</template>