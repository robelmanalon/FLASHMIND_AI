<template>
  <div class="loader-wrapper">
    <div class="tech-ring"></div>

    <div class="cyber-box">
      <div class="grid-bg"></div>
      <div class="corner top-left"></div>
      <div class="corner top-right"></div>
      <div class="corner bottom-left"></div>
      <div class="corner bottom-right"></div>
      <svg class="lightning-icon" viewBox="0 0 24 24">
        <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z" />
      </svg>
      <div class="laser-beam"></div>
    </div>

    <div class="hud-text">[LOADING...]</div>
  </div>
</template>

<style scoped>
.loader-wrapper {
  position: fixed;
  inset: 0;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 30px;
  background-color: #05070f;
  font-family: 'Consolas', 'Courier New', monospace;
}
@media (prefers-reduced-motion: reduce) {
  .loader-wrapper *, .loader-wrapper *::before, .loader-wrapper *::after {
    animation-duration: 0.8s !important;
    animation-iteration-count: infinite !important;
  }
}

/* Outer Rotating Tech Ring */
.tech-ring {
  position: absolute;
  width: 140px;
  height: 140px;
  border: 2px dashed rgba(0, 243, 255, 0.4);
  border-radius: 50%;
  animation: rotateRing 8s linear infinite;
}

/* Main Square Container */
.cyber-box {
  position: relative;
  width: 100px;
  height: 100px;
  background: rgba(10, 15, 30, 0.85);
  border: 2px solid #00f3ff;
  border-radius: 16px;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  box-shadow:
    0 0 15px rgba(0, 243, 255, 0.3),
    inset 0 0 15px rgba(0, 243, 255, 0.2);
  animation: boxGlitch 4s infinite;
}

/* Holographic Grid Background */
.grid-bg {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(0, 243, 255, 0.1) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 243, 255, 0.1) 1px, transparent 1px);
  background-size: 8px 8px;
}

/* Lightning Icon with Neon Glow */
.lightning-icon {
  width: 48px;
  height: 48px;
  fill: #00f3ff;
  z-index: 3;
  filter: drop-shadow(0 0 8px #00f3ff);
  animation: iconPulse 1.5s ease-in-out infinite alternate;
}

/* Scanning Laser Beam */
.laser-beam {
  position: absolute;
  left: 0;
  width: 100%;
  height: 6px;
  background: #fff;
  box-shadow:
    0 0 10px #fff,
    0 0 20px #00f3ff,
    0 0 30px #ff0055;
  z-index: 4;
  animation: scanLaser 1.4s cubic-bezier(0.4, 0, 0.2, 1) infinite;
}

/* Neon Corner Accents */
.corner {
  position: absolute;
  width: 8px;
  height: 8px;
  border-color: #ff0055;
  border-style: solid;
  z-index: 5;
}
.top-left { top: 4px; left: 4px; border-width: 2px 0 0 2px; }
.top-right { top: 4px; right: 4px; border-width: 2px 2px 0 0; }
.bottom-left { bottom: 4px; left: 4px; border-width: 0 0 2px 2px; }
.bottom-right { bottom: 4px; right: 4px; border-width: 0 2px 2px 0; }

/* Futuristic HUD Text */
.hud-text {
  color: #00f3ff;
  font-size: 12px;
  letter-spacing: 4px;
  text-shadow: 0 0 8px #00f3ff;
}

/* ================= ANIMATIONS ================= */

@keyframes scanLaser {
  0% { top: -10%; }
  50% { top: 100%; }
  100% { top: -10%; }
}

@keyframes rotateRing {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes iconPulse {
  0% {
    transform: scale(0.95);
    filter: drop-shadow(0 0 5px #00f3ff);
  }
  100% {
    transform: scale(1.05);
    filter: drop-shadow(0 0 15px #00f3ff) drop-shadow(0 0 25px #ff0055);
  }
}

@keyframes boxGlitch {
  0%, 92%, 100% {
    transform: translate(0, 0);
    border-color: #00f3ff;
  }
  93% {
    transform: translate(-2px, 1px);
    border-color: #ff0055;
  }
  95% {
    transform: translate(2px, -1px);
  }
}
</style>