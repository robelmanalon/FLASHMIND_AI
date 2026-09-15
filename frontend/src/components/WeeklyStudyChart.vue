<script setup>
import { onMounted, onBeforeUnmount, ref } from 'vue'
import { Chart, Filler, LineController, LineElement, PointElement, LinearScale, CategoryScale, Tooltip } from 'chart.js'

Chart.register(Filler, LineController, LineElement, PointElement, LinearScale, CategoryScale, Tooltip)
const props = defineProps({ study: { type: Object, required: true } })
const canvas = ref(null)
let chart
onMounted(() => {
  chart = new Chart(canvas.value, { type: 'line', data: { labels: props.study.labels, datasets: [{ data: props.study.values, borderColor: '#22d3ee', backgroundColor: 'rgba(34, 211, 238, .12)', fill: true, tension: .4, pointRadius: 3, pointBackgroundColor: '#22d3ee', pointBorderColor: '#111522', pointBorderWidth: 2 }] }, options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false }, tooltip: { displayColors: false, backgroundColor: '#171b2d', titleColor: '#fff', bodyColor: '#a5b4fc', padding: 10, callbacks: { label: (context) => `${context.parsed.y} minutes` } } }, scales: { x: { grid: { display: false }, ticks: { color: '#64748b', font: { size: 11 } } }, y: { beginAtZero: true, suggestedMax: 80, grid: { color: 'rgba(148, 163, 184, .08)' }, ticks: { color: '#64748b', font: { size: 11 }, callback: (value) => `${value}m` } } } } })
})
onBeforeUnmount(() => chart?.destroy())
</script>

<template><section class="glass rounded-2xl p-6"><div class="flex items-start justify-between"><div><p class="text-xs font-bold uppercase tracking-[.18em] text-cyan-300">Activity overview</p><h2 class="mt-3 text-xl font-bold text-white">Weekly study chart</h2></div><span class="rounded-lg bg-cyan-400/10 px-2.5 py-1.5 text-xs font-bold text-cyan-300">Minutes</span></div><div class="mt-6 h-56"><canvas ref="canvas"></canvas></div></section></template>
