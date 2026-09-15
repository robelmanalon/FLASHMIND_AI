<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import AppLayout from '../layouts/AppLayout.vue'
import LoadingSpinner from '../components/LoadingSpinner.vue'
import QuizQuestionCard from '../components/QuizQuestionCard.vue'
import ConfirmDialog from '../components/ConfirmDialog.vue'
import { useQuizStore } from '../stores/quiz'
import { useUiStore } from '../stores/ui'

const quiz = useQuizStore()
const ui = useUiStore()
const selected = ref('')
const quizPendingDelete = ref(null)
let timer
const question = computed(() => quiz.currentQuestion)
const answered = computed(() => question.value && quiz.answers[question.value.id])
const progress = computed(() => quiz.questions.length ? ((quiz.currentIndex + (answered.value ? 1 : 0)) / quiz.questions.length) * 100 : 0)
const typeLabels = { 'multiple-choice': 'Multiple choice', 'true-false': 'True or false', identification: 'Identification', 'fill-blank': 'Fill in the blank' }
const pageTitle = computed(() => quiz.currentQuizTitle || 'AI quiz')

function begin() { quiz.startQuiz() }
function select(value) { if (!answered.value) selected.value = value }
function submit() { if (!answered.value) quiz.recordAnswer(selected.value) }
function next() { quiz.nextQuestion(); selected.value = '' }
function tick() { if (quiz.status !== 'active' || answered.value) return; if (quiz.timeLeft > 0) quiz.timeLeft -= 1; else { quiz.recordAnswer(''); next() } }
function startTimer() { clearInterval(timer); timer = setInterval(tick, 1000) }
watch(() => quiz.status, (status) => { if (status === 'active') startTimer(); else clearInterval(timer) })
watch(() => quiz.currentIndex, () => { selected.value = ''; quiz.resetTimer() })
onMounted(async () => { await quiz.loadSavedQuizzes() })
onBeforeUnmount(() => clearInterval(timer))
async function openSaved(id) {
  try { await quiz.openSavedQuiz(id) } catch (error) { ui.toast(error.message, 'error') }
}
async function removeSaved() {
  if (!quizPendingDelete.value) return
  await quiz.deleteSavedQuiz(quizPendingDelete.value.id)
  ui.toast('Quiz folder deleted', 'success')
  quizPendingDelete.value = null
}
</script>

<template>
  <AppLayout><div class="mx-auto max-w-4xl px-5 py-8 sm:px-8"><header class="flex items-end justify-between gap-4"><div><p class="text-sm font-medium text-cyan-300">Knowledge check</p><h1 class="mt-2 text-3xl font-bold text-white sm:text-4xl">{{ pageTitle }}</h1><p v-if="quiz.status === 'idle'" class="mt-2 text-slate-400">Choose a saved quiz folder to review, or start a practice quiz.</p><p v-else class="mt-2 text-slate-400">A focused review to test what you know.</p></div><div v-if="quiz.status === 'active'" class="flex items-center gap-2 rounded-xl border px-4 py-2.5 text-sm font-bold" :class="quiz.timeLeft <= 8 ? 'border-red-400/30 text-red-300' : 'border-white/10 text-slate-300'"><span>◷</span> 00:{{ String(quiz.timeLeft).padStart(2, '0') }}</div></header>

    <div v-if="quiz.loading" class="flex min-h-96 items-center justify-center"><LoadingSpinner /></div>

    <section v-else-if="quiz.status === 'active' && question" class="mt-9"><div class="mb-4 flex items-center justify-between text-xs font-bold text-slate-500"><span>Question {{ quiz.currentIndex + 1 }} of {{ quiz.questions.length }} <span class="ml-2 text-slate-700">•</span> <span class="ml-2">{{ typeLabels[question.type] }}</span></span><span>{{ Math.round(progress) }}% complete</span></div><div class="h-1.5 rounded-full bg-white/10"><div class="h-full rounded-full bg-gradient-to-r from-indigo-400 to-cyan-300 transition-all duration-500" :style="{ width: `${progress}%` }"></div></div><div class="mt-6"><QuizQuestionCard :question="question" :selected="selected" :locked="Boolean(answered)" @select="select" /><div v-if="answered" class="mt-4 rounded-2xl border border-indigo-400/20 bg-indigo-400/5 p-5"><p class="text-xs font-bold uppercase tracking-[.18em] text-indigo-300">Explanation</p><p class="mt-2 text-sm leading-6 text-slate-300">{{ question.explanation }}</p><p class="mt-3 text-xs font-semibold" :class="answered.correct ? 'text-emerald-300' : 'text-red-300'">{{ answered.correct ? 'Correct answer' : `Correct answer: ${question.answer}` }}</p></div></div><div class="mt-6 flex justify-end"><button v-if="!answered" :disabled="!selected" class="rounded-xl bg-indigo-500 px-6 py-3 text-sm font-bold text-white shadow-lg shadow-indigo-500/20 disabled:cursor-not-allowed disabled:opacity-40" @click="submit">Check answer</button><button v-else class="rounded-xl bg-cyan-400 px-6 py-3 text-sm font-bold text-slate-950" @click="next">{{ quiz.currentIndex === quiz.questions.length - 1 ? 'See results' : 'Next question →' }}</button></div></section>

    <section v-else-if="quiz.status === 'results'" class="mt-9"><div class="glass rounded-3xl p-8 text-center sm:p-12"><span class="mx-auto grid h-16 w-16 place-items-center rounded-2xl bg-cyan-400/10 text-3xl text-cyan-300">✦</span><p class="mt-6 text-sm font-bold uppercase tracking-[.2em] text-cyan-300">Quiz complete</p><h2 class="mt-3 text-4xl font-bold text-white">{{ quiz.percentage }}%</h2><p class="mt-2 text-slate-400">You answered {{ quiz.score }} of {{ quiz.questions.length }} correctly.</p><div class="mx-auto mt-8 grid max-w-sm grid-cols-2 gap-3 text-left"><div class="rounded-xl bg-white/5 p-4"><p class="text-xs text-slate-500">Score</p><p class="mt-1 text-xl font-bold text-white">{{ quiz.score }} / {{ quiz.questions.length }}</p></div><div class="rounded-xl bg-white/5 p-4"><p class="text-xs text-slate-500">Attempts saved</p><p class="mt-1 text-xl font-bold text-white">{{ quiz.history.length }}</p></div></div><div class="mt-8 flex justify-center gap-3"><button class="rounded-xl border border-white/10 px-5 py-3 text-sm font-bold text-slate-300" @click="quiz.retryQuiz()">Retry quiz</button><button class="rounded-xl border border-white/10 px-5 py-3 text-sm font-bold text-slate-300" @click="quiz.resetQuiz()">Back to folders</button><RouterLink to="/dashboard" class="rounded-xl bg-indigo-500 px-5 py-3 text-sm font-bold text-white">Back to dashboard</RouterLink></div></div><section class="mt-6"><h2 class="text-lg font-bold text-white">Review answers</h2><div class="mt-3 space-y-3"><article v-for="(item, index) in quiz.questions" :key="item.id" class="glass rounded-2xl p-4"><div class="flex items-start gap-3"><span class="grid h-7 w-7 shrink-0 place-items-center rounded-lg text-xs font-bold" :class="quiz.answers[item.id]?.correct ? 'bg-emerald-400/10 text-emerald-300' : 'bg-red-400/10 text-red-300'">{{ quiz.answers[item.id]?.correct ? '✓' : '×' }}</span><div><p class="text-sm font-semibold text-slate-200">{{ index + 1 }}. {{ item.prompt }}</p><p class="mt-2 text-xs text-slate-500">Your answer: <span class="text-slate-300">{{ quiz.answers[item.id]?.value || 'No answer' }}</span><span v-if="!quiz.answers[item.id]?.correct" class="ml-2 text-cyan-300">Correct: {{ item.answer }}</span></p><p class="mt-2 text-xs leading-5 text-slate-500">{{ item.explanation }}</p></div></div></article></div></section><div class="mt-6"><h2 class="text-lg font-bold text-white">Score history</h2><div class="mt-3 space-y-2"><div v-for="attempt in quiz.history" :key="attempt.id" class="glass flex items-center justify-between rounded-xl px-4 py-3 text-sm"><span class="text-slate-400">{{ attempt.date }}</span><span class="font-bold text-cyan-300">{{ attempt.score }}/{{ attempt.total }} · {{ attempt.percentage }}%</span></div></div></div></section>

    <section v-else class="mt-9">
      <div class="flex flex-col justify-between gap-4 sm:flex-row sm:items-center"><div><h2 class="text-lg font-bold text-white">Quiz folders</h2><p class="mt-1 text-sm text-slate-400">{{ quiz.savedQuizzes.length }} saved quiz{{ quiz.savedQuizzes.length === 1 ? '' : 'zes' }} — each stays in its own folder.</p></div><button class="rounded-xl border border-white/10 px-4 py-2.5 text-sm font-bold text-slate-300 hover:bg-white/5" @click="begin">+ Start practice quiz</button></div>
      <div v-if="quiz.savedQuizzes.length" class="mt-5 grid gap-4 sm:grid-cols-2">
        <article v-for="item in quiz.savedQuizzes" :key="item.id" class="glass rounded-2xl p-5">
          <div class="flex items-start justify-between gap-3"><div class="min-w-0"><span class="rounded-lg bg-cyan-400/10 px-2.5 py-1 text-[11px] font-bold uppercase tracking-wider text-cyan-300">Quiz</span><h3 class="mt-3 truncate text-lg font-bold text-white">{{ item.title }}</h3></div><span class="text-xl text-cyan-300">✓</span></div>
          <p class="mt-3 text-sm text-slate-500">{{ item.questions.length }} questions · saved {{ item.createdAt }}</p>
          <div class="mt-5 flex gap-2"><button class="flex-1 rounded-xl bg-indigo-500/15 px-3 py-2.5 text-sm font-bold text-indigo-200 hover:bg-indigo-500/25" @click="openSaved(item.id)">Take quiz →</button><button class="rounded-xl border border-white/10 px-3 py-2.5 text-sm font-bold text-slate-500 hover:border-red-400/30 hover:text-red-300" @click="quizPendingDelete = item">Delete</button></div>
        </article>
      </div>
      <div v-else class="glass mt-5 rounded-2xl p-12 text-center"><p class="text-2xl text-slate-500">✓</p><h3 class="mt-4 text-lg font-bold text-white">No saved quizzes yet</h3><p class="mx-auto mt-2 max-w-sm text-sm leading-6 text-slate-400">Save a generated quiz from the AI Generator and it will appear here in its own folder.</p></div>
    </section>
  </div><ConfirmDialog v-if="quizPendingDelete" title="Delete quiz folder?" :message="`This will remove ${quizPendingDelete.title} and its saved questions.`" confirm-label="Delete quiz" @cancel="quizPendingDelete = null" @confirm="removeSaved" /></AppLayout>
</template>