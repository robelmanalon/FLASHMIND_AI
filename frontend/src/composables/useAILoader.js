import { computed, onBeforeUnmount, ref } from 'vue'

const messages = [
  'AI is reading your document...',
  'Extracting important concepts...',
  'Creating smart flashcards...',
  'Generating quiz questions...',
  'Almost done preparing your study deck...',
]

export function useAILoader() {
  const visible = ref(false)
  const progress = ref(0)
  const message = ref(messages[0])
  let progressTimer
  let messageTimer

  function clearTimers() {
    window.clearInterval(progressTimer)
    window.clearInterval(messageTimer)
  }

  function start() {
    clearTimers()
    visible.value = true
    progress.value = 0
    message.value = messages[0]
    let step = 0
    let messageIndex = 0

    progressTimer = window.setInterval(() => {
      const steps = [12, 28, 41, 56, 73, 88, 95]
      if (step < steps.length) progress.value = steps[step++]
    }, 900)
    messageTimer = window.setInterval(() => {
      messageIndex = (messageIndex + 1) % messages.length
      message.value = messages[messageIndex]
    }, 2000)
  }

  async function finish() {
    clearTimers()
    progress.value = 100
    message.value = 'Your study materials are ready.'
    await new Promise((resolve) => window.setTimeout(resolve, 650))
    visible.value = false
  }

  function stop() {
    clearTimers()
    visible.value = false
  }

  onBeforeUnmount(clearTimers)

  return { visible, progress, message, messages, start, finish, stop, isComplete: computed(() => progress.value >= 100) }
}
