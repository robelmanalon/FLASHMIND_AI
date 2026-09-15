import { defineStore } from 'pinia'
import { deleteSavedQuiz, getQuizQuestions, getSavedQuizzes, saveQuiz } from '../services/quizApi'

export const useQuizStore = defineStore('quiz', {
  state: () => ({ questions: [], currentIndex: 0, answers: {}, timeLeft: 30, status: 'idle', loading: false, history: [], savedQuizzes: [], currentQuizTitle: '' }),
  getters: {
    currentQuestion: (state) => state.questions[state.currentIndex],
    answeredCount: (state) => Object.keys(state.answers).length,
    score: (state) => state.questions.reduce((total, question) => total + (state.answers[question.id]?.correct ? 1 : 0), 0),
    percentage() { return this.questions.length ? Math.round((this.score / this.questions.length) * 100) : 0 },
  },
  actions: {
    async startQuiz() {
      this.loading = true
      const questions = await getQuizQuestions()
      this.setQuestions(questions)
      this.loading = false
    },
    setQuestions(questions, title = '') {
      this.questions = questions || []
      this.currentQuizTitle = title
      this.currentIndex = 0
      this.answers = {}
      this.timeLeft = 30
      this.status = 'active'
    },
    async loadSavedQuizzes() {
      this.savedQuizzes = await getSavedQuizzes()
    },
    async saveQuiz(title, questions) {
      const quiz = await saveQuiz({ title, questions: questions || this.questions })
      this.savedQuizzes.unshift(quiz)
      return quiz
    },
    async openSavedQuiz(id) {
      const quizzes = await getSavedQuizzes()
      const quiz = quizzes.find((item) => String(item.id) === String(id))
      if (!quiz) throw new Error('Quiz not found')
      this.setQuestions(quiz.questions, quiz.title)
    },
    async deleteSavedQuiz(id) {
      await deleteSavedQuiz(id)
      await this.loadSavedQuizzes()
    },
    recordAnswer(value) {
      const question = this.currentQuestion
      if (!question || this.answers[question.id]) return
      const normalized = String(value ?? '').trim().toLowerCase()
      const accepted = [question.answer, ...(question.acceptable || [])].map((answer) => String(answer).trim().toLowerCase())
      this.answers[question.id] = { value, correct: accepted.includes(normalized), explanation: question.explanation }
    },
    nextQuestion() {
      if (this.currentIndex < this.questions.length - 1) { this.currentIndex += 1; this.timeLeft = 30 }
      else this.finishQuiz()
    },
    resetTimer() { this.timeLeft = 30 },
    finishQuiz() {
      this.status = 'results'
      this.history.unshift({ id: Date.now(), score: this.score, total: this.questions.length, percentage: this.percentage, date: new Date().toLocaleDateString() })
    },
    retryQuiz() { this.setQuestions(this.questions, this.currentQuizTitle) },
    resetQuiz() { this.questions = []; this.currentQuizTitle = ''; this.currentIndex = 0; this.answers = {}; this.timeLeft = 30; this.status = 'idle' },
  },
})