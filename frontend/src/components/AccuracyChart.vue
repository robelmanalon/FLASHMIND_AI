<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue'
import { CategoryScale, Chart, Filler, LineController, LineElement, LinearScale, PointElement, Tooltip } from 'chart.js'

Chart.register(Filler, LineController, LineElement, PointElement, LinearScale, CategoryScale, Tooltip)
const props = defineProps({ accuracy: { type: Object, required: true } })
const canvas = ref(null)
let chart
onMounted(() => {
  chart = new Chart(canvas.value, { type: 'line', data: { labels: props.accuracy.labels, datasets: [{ data: props.accuracy.values, borderColor: '#a78bfa', backgroundColor: 'rgba(167, 139, 250, .13)', fill: true, tension: .4, pointRadius: 3, pointBackgroundColor: '#a78bfa', pointBorderColor: '#111522', pointBorderWidth: 2 }] }, options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false }, tooltip: { displayColors: false, backgroundColor: '#171b2d', callbacks: { label: (context) => `${context.parsed.y}% accuracy` } } }, scales: { x: { grid: { display: false }, ticks: { color: '#64748b' } }, y: { min: 60, max: 100, grid: { color: 'rgba(148, 163, 184, .08)' }, ticks: { color: '#64748b', callback: (value) => `${value}%` } } } } })
})
onBeforeUnmount(() => chart?.destroy())
</script>

<template><section class="glass rounded-2xl p-6"><div class="flex items-start justify-between"><div><p class="text-xs font-bold uppercase tracking-[.18em] text-purple-300">Performance</p><h2 class="mt-3 text-xl font-bold text-white">Accuracy over time</h2></div><span class="rounded-lg bg-purple-400/10 px-2.5 py-1.5 text-xs font-bold text-purple-300">This week</span></div><div class="mt-6 h-56"><canvas ref="canvas"></canvas></div></section></template>