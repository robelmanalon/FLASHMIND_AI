<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue'

const props = defineProps({
  message: { type: String, default: 'Processing...' },
  subMessages: { type: Array, default: () => ['ANALYZING_INPUT...', 'SEARCHING KNOWLEDGE...', 'PROCESSING INFORMATION...', 'PREPARING RESULT...'] },
})

const subIndex = ref(0)
const status = ref(props.subMessages[0] || 'INITIALIZING...')
let timer

onMounted(() => {
  if (props.subMessages.length) {
    timer = setInterval(() => {
      subIndex.value = (subIndex.value + 1) % props.subMessages.length
      status.value = props.subMessages[subIndex.value]
    }, 1800)
  }
})
onBeforeUnmount(() => clearInterval(timer))
</script>

<template>
  <div class="fixed inset-0 z-[90] flex flex-col items-center justify-center bg-[#02040a]/80 p-6 backdrop-blur-sm" role="status" aria-live="polite">
    <div class="core-stage">
      <div class="reactor-glow"></div>
      <div class="ring-outer"></div>
      <div class="ring-inner"></div>
      <div class="node-box">
        <svg class="neural-net" viewBox="0 0 100 100">
          <line x1="15" y1="15" x2="85" y2="85" class="net-line" />
          <line x1="85" y1="15" x2="15" y2="85" class="net-line" />
          <circle cx="15" cy="15" r="3" fill="#ff007f" />
          <circle cx="85" cy="15" r="3" fill="#00f3ff" />
          <circle cx="15" cy="85" r="3" fill="#00f3ff" />
          <circle cx="85" cy="85" r="3" fill="#ff007f" />
        </svg>
        <svg class="ai-brain-core" viewBox="0 0 24 24">
          <path d="M12 2a10 10 0 0 1 10 10c0 5.523-4.477 10-10 10S2 17.523 2 12A10 10 0 0 1 12 2zm0 3a7 7 0 0 0-7 7c0 2.38 1.19 4.48 3 5.74V15a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1v2.74c1.81-1.26 3-3.36 3-5.74a7 7 0 0 0-7-7z" />
        </svg>
        <div class="laser-scan"></div>
      </div>
    </div>
    <div class="hud-console mt-8">
      <span class="prompt-symbol">&gt;</span>
      <span class="status-text">{{ status }}</span>
    </div>
    <p class="mt-4 text-sm text-slate-400">{{ message }}</p>
  </div>
</template>

<style scoped>
.core-stage {
  position: relative;
  width: 140px;
  height: 140px;
  display: flex;
  justify-content: center;
  align-items: center;
}
.reactor-glow {
  position: absolute;
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: radial-gradient(circle, #00f3ff 0%, #8b5cf6 50%, transparent 70%);
  filter: blur(25px);
  opacity: 0.5;
  animation: reactorPulse 2s ease-in-out infinite alternate;
}
.ring-outer {
  position: absolute;
  inset: 0;
  border: 1.5px dashed rgba(0, 243, 255, 0.4);
  border-radius: 50%;
  animation: spinClockwise 10s linear infinite;
}
.ring-inner {
  position: absolute;
  inset: 12px;
  border: 2px solid transparent;
  border-top-color: #ff007f;
  border-bottom-color: #00f3ff;
  border-radius: 50%;
  animation: spinCounter 4s cubic-bezier(0.68, -0.55, 0.265, 1.55) infinite;
}
.node-box {
  position: relative;
  width: 80px;
  height: 80px;
  background: rgba(10, 15, 30, 0.75);
  border: 1px solid rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow:
    0 0 30px rgba(0, 243, 255, 0.25),
    inset 0 0 15px rgba(139, 92, 246, 0.3);
  animation: floatNode 3s ease-in-out infinite alternate;
}
.neural-net {
  position: absolute;
  width: 100%;
  height: 100%;
  z-index: 2;
}
.net-line {
  stroke: #00f3ff;
  stroke-width: 1.5;
  stroke-dasharray: 4 2;
  opacity: 0.6;
  animation: dashMove 1s linear infinite;
}
.ai-brain-core {
  width: 36px;
  height: 36px;
  fill: #ffffff;
  z-index: 3;
  filter: drop-shadow(0 0 10px #00f3ff) drop-shadow(0 0 20px #ff007f);
  animation: coreGlow 1.5s ease-in-out infinite alternate;
}
.laser-scan {
  position: absolute;
  left: 0;
  width: 100%;
  height: 4px;
  background: #ffffff;
  box-shadow:
    0 0 10px #00f3ff,
    0 0 20px #ff007f;
  z-index: 4;
  animation: scanVertical 1.6s ease-in-out infinite;
}
.hud-console {
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(0, 243, 255, 0.2);
  padding: 10px 18px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 10px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
}
.prompt-symbol {
  color: #ff007f;
  font-weight: bold;
  font-family: 'Fira Code', 'Courier New', monospace;
}
.status-text {
  color: #00f3ff;
  font-size: 12px;
  letter-spacing: 2px;
  font-family: 'Fira Code', 'Courier New', monospace;
  min-width: 220px;
}

@keyframes scanVertical {
  0% { top: 0%; opacity: 0; }
  15% { opacity: 1; }
  85% { opacity: 1; }
  100% { top: 100%; opacity: 0; }
}
@keyframes spinClockwise { 100% { transform: rotate(360deg); } }
@keyframes spinCounter { 100% { transform: rotate(-360deg); } }
@keyframes floatNode { 0% { transform: translateY(-5px); } 100% { transform: translateY(5px); } }
@keyframes reactorPulse { 0% { transform: scale(0.8); opacity: 0.3; } 100% { transform: scale(1.2); opacity: 0.7; } }
@keyframes dashMove { 100% { stroke-dashoffset: -12; } }
@keyframes coreGlow { 0% { transform: scale(0.9); } 100% { transform: scale(1.1); } }

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.8s !important;
    animation-iteration-count: infinite !important;
  }
}
</style>