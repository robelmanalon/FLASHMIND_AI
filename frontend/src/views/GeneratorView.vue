<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import AppLayout from '../layouts/AppLayout.vue'
import LoadingSpinner from '../components/LoadingSpinner.vue'
import LoadingOverlay from '../components/LoadingOverlay.vue'
import { generateStudyMaterials } from '../services/api'
import { useUiStore } from '../stores/ui'
import { useDeckStore } from '../stores/decks'
import { useQuizStore } from '../stores/quiz'

const router = useRouter()
const ui = useUiStore()
const deckStore = useDeckStore()
const quizStore = useQuizStore()
const fileInput = ref(null)
const selectedFile = ref(null)
const result = ref(null)
const loading = ref(false)
const error = ref('')
const saving = ref(false)
const flashcardCount = ref(10)
const quizCount = ref(10)
const outputType = ref('flashcards')
const choices = [['flashcards', 'Flashcards', '▤'], ['quiz', 'Quiz', '✓'], ['deck', 'Deck', '▦']]
const loadingSteps = {
  flashcards: ['NEURAL_NET_INIT()', 'ANALYZING_INPUT...', 'EXTRACTING KEY TERMS...', 'CRAFTING QUESTIONS...', 'POLISHING FLASHCARDS...'],
  quiz: ['NEURAL_NET_INIT()', 'ANALYZING_INPUT...', 'SPOTTING QUESTION-WORTHY FACTS...', 'WRITING OPTIONS...', 'ADDING ANSWER KEYS...'],
  deck: ['NEURAL_NET_INIT()', 'ANALYZING_INPUT...', 'ORGANIZING TOPICS...', 'BUILDING FLASHCARDS...', 'ASSEMBLING QUIZ...'],
}

function chooseFile(event) {
  const file = event.target.files?.[0]
  if (file) { selectedFile.value = file; result.value = null; error.value = '' }
}
function onDrop(event) {
  const file = event.dataTransfer.files?.[0]
  if (file) { selectedFile.value = file; result.value = null; error.value = '' }
}
async function generate() {
  if (!selectedFile.value) return
  loading.value = true
  error.value = ''
  try { result.value = await generateStudyMaterials(selectedFile.value, { flashcardCount: flashcardCount.value, quizCount: quizCount.value }) } catch (cause) { error.value = cause.message } finally { loading.value = false }
}
async function saveGenerated() {
  if (!result.value || saving.value) return
  saving.value = true
  try {
    const generated = result.value.result
    const baseTitle = (result.value.filename || 'Study notes').replace(/\.[^.]+$/, '')
    if (outputType.value === 'quiz') {
      const questions = (generated.quiz_questions || []).map((question, index) => ({
        id: index + 1,
        type: question.type,
        prompt: question.question,
        options: question.options && question.options.length ? question.options : null,
        answer: question.answer,
        acceptable: [question.answer],
        explanation: question.explanation,
      }))
      await quizStore.saveQuiz(`${baseTitle} quiz`, questions)
      ui.toast('Quiz saved to your quiz folders', 'success')
      router.push('/quiz')
      return
    }
    const cards = (generated.flashcards || []).map((card, index) => ({
      id: Date.now() + index,
      question: card.question,
      answer: card.answer,
      hint: card.explanation || null,
      bookmarked: false,
      favorite: false,
    }))
    const subject = baseTitle.toLowerCase().includes('bio') ? 'Biology' : baseTitle.toLowerCase().includes('spani') ? 'Languages' : baseTitle.toLowerCase().includes('design') ? 'Design' : 'General'
    await deckStore.save({
      id: null,
      title: outputType.value === 'deck' ? baseTitle : `${baseTitle} flashcards`,
      subject,
      description: `AI-generated from ${result.value.filename}`,
      cards,
    })
    ui.toast(`${cards.length} flashcards saved to your decks`, 'success')
    router.push('/decks')
  } catch (cause) {
    ui.toast(cause.message || 'Failed to save', 'error')
  } finally {
    saving.value = false
  }
}
function formatSize(bytes) { return `${(bytes / 1024).toFixed(1)} KB` }
</script>

<template>
  <AppLayout>
    <LoadingOverlay v-if="loading" message="FlashMind AI is generating" :sub-messages="loadingSteps[outputType]" />
    <div class="mx-auto max-w-6xl px-5 py-8 sm:px-8">
      <header><p class="text-sm font-medium text-cyan-300">AI-powered study tools</p><h1 class="mt-2 text-3xl font-bold text-white sm:text-4xl">Generate study materials</h1><p class="mt-2 max-w-2xl text-slate-400">Upload your notes and choose what FlashMind should create.</p></header>
      <section class="mt-9 grid gap-6 xl:grid-cols-[.85fr_1.4fr] xl:items-start">
        <div class="space-y-5">
          <div class="glass rounded-3xl p-6">
            <div class="flex items-center justify-between"><div><h2 class="font-bold text-white">1. Upload your notes</h2><p class="mt-1 text-xs text-slate-500">PDF, DOCX, or TXT up to 15 MB</p></div><span class="text-2xl text-cyan-300">↑</span></div>
            <button class="mt-6 flex w-full flex-col items-center justify-center rounded-2xl border border-dashed border-cyan-300/30 bg-cyan-300/5 px-5 py-10 text-center transition hover:bg-cyan-300/10" @click="fileInput?.click()" @dragover.prevent @drop.prevent="onDrop"><span class="grid h-12 w-12 place-items-center rounded-xl bg-cyan-300/10 text-2xl text-cyan-300">＋</span><span class="mt-4 text-sm font-bold text-slate-200">Drop a document here</span><span class="mt-1 text-xs text-slate-500">or click to browse files</span></button>
            <input ref="fileInput" type="file" accept=".pdf,.docx,.txt,application/pdf,text/plain,application/vnd.openxmlformats-officedocument.wordprocessingml.document" class="hidden" @change="chooseFile">
            <div v-if="selectedFile" class="mt-4 flex items-center justify-between rounded-xl bg-white/5 px-4 py-3"><div class="min-w-0"><p class="truncate text-sm font-semibold text-white">{{ selectedFile.name }}</p><p class="text-xs text-slate-500">{{ formatSize(selectedFile.size) }}</p></div><button class="text-xs font-bold text-slate-500 hover:text-white" @click="selectedFile = null">Remove</button></div>
          </div>
          <div class="glass rounded-2xl p-6"><h2 class="font-bold text-white">2. What do you want to create?</h2><div class="mt-5 grid grid-cols-3 gap-2"><button v-for="choice in choices" :key="choice[0]" type="button" class="rounded-xl border px-2 py-3 text-xs font-bold transition sm:px-3 sm:text-sm" :class="outputType === choice[0] ? 'border-cyan-300/50 bg-cyan-300/10 text-cyan-200' : 'border-white/10 text-slate-400 hover:bg-white/5'" @click="outputType = choice[0]"><span class="mr-1">{{ choice[2] }}</span>{{ choice[1] }}</button></div><div class="mt-5 grid grid-cols-2 gap-3"><label class="text-xs font-semibold text-slate-400">Flashcards<input v-model.number="flashcardCount" type="number" min="1" max="50" class="mt-2 w-full rounded-xl border border-white/10 bg-white/5 px-3 py-2.5 text-white outline-none"></label><label class="text-xs font-semibold text-slate-400">Quiz questions<input v-model.number="quizCount" type="number" min="1" max="50" class="mt-2 w-full rounded-xl border border-white/10 bg-white/5 px-3 py-2.5 text-white outline-none"></label></div><button :disabled="!selectedFile || loading" class="mt-5 flex w-full items-center justify-center gap-3 rounded-xl bg-indigo-500 py-3.5 text-sm font-bold text-white shadow-lg shadow-indigo-500/20 disabled:cursor-not-allowed disabled:opacity-40" @click="generate"><LoadingSpinner v-if="loading" />{{ loading ? 'Generating with Gemini...' : `Generate ${outputType}` }}</button><p v-if="error" class="mt-3 rounded-xl bg-red-400/10 p-3 text-xs leading-5 text-red-200">{{ error }}</p></div>
        </div>
        <div class="glass min-h-[500px] rounded-3xl p-6 sm:p-8">
          <div v-if="!result" class="flex min-h-[430px] flex-col items-center justify-center text-center"><span class="grid h-16 w-16 place-items-center rounded-2xl bg-indigo-400/10 text-3xl text-indigo-300">✦</span><h2 class="mt-6 text-xl font-bold text-white">Your preview will appear here</h2><p class="mt-2 max-w-sm text-sm leading-6 text-slate-500">Review generated content before saving it to your workspace.</p></div>
          <div v-else><div class="flex flex-col justify-between gap-4 sm:flex-row sm:items-start"><div><p class="text-xs font-bold uppercase tracking-[.18em] text-cyan-300">Preview · {{ outputType }}</p><h2 class="mt-2 text-2xl font-bold text-white">Generated from {{ result.filename }}</h2><p class="mt-1 text-xs text-slate-500">{{ result.characters_extracted.toLocaleString() }} characters · {{ result.chunks_processed }} chunk{{ result.chunks_processed === 1 ? '' : 's' }}</p></div><button class="rounded-xl bg-cyan-400 px-4 py-2.5 text-sm font-bold text-slate-950 disabled:cursor-not-allowed disabled:opacity-60" :disabled="saving" @click="saveGenerated">{{ saving ? 'Saving...' : `Save ${outputType}` }}</button></div>
            <div v-if="outputType === 'flashcards' || outputType === 'deck'" class="mt-8 space-y-3"><h3 class="font-bold text-white">Flashcards ({{ result.result.flashcards.length }})</h3><article v-for="(card, index) in result.result.flashcards" :key="index" class="rounded-xl border border-white/10 bg-white/[.03] p-4"><p class="text-sm font-semibold text-white">{{ index + 1 }}. {{ card.question }}</p><p class="mt-2 text-sm leading-6 text-slate-400">{{ card.answer }}</p></article></div>
<div v-if="outputType === 'quiz' || outputType === 'deck'" class="mt-8 space-y-3"><h3 class="font-bold text-white">Quiz questions ({{ result.result.quiz_questions.length }})</h3><article v-for="(question, index) in result.result.quiz_questions" :key="index" class="rounded-xl border border-white/10 bg-white/[.03] p-4"><div class="flex items-start justify-between gap-3"><p class="text-sm font-semibold text-white">{{ index + 1 }}. {{ question.question }}</p><span class="rounded-md bg-indigo-400/10 px-2 py-1 text-[10px] font-bold uppercase text-indigo-200">{{ question.type }}</span></div><p v-if="question.options.length" class="mt-3 text-xs text-slate-500">{{ question.options.join(' · ') }}</p><p class="mt-2 text-xs text-cyan-300">Answer: {{ question.answer }}</p></article></div>
          </div>
        </div>
      </section>
    </div>
  </AppLayout>
</template>
