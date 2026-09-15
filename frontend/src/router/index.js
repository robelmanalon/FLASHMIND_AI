import { createRouter, createWebHistory } from 'vue-router'
import LandingView from '../views/LandingView.vue'
import DashboardView from '../views/DashboardView.vue'
import LoginView from '../views/auth/LoginView.vue'
import RegisterView from '../views/auth/RegisterView.vue'
import ForgotPasswordView from '../views/auth/ForgotPasswordView.vue'
import DecksView from '../views/DecksView.vue'
import DeckEditorView from '../views/DeckEditorView.vue'
import StudyView from '../views/StudyView.vue'
import QuizView from '../views/QuizView.vue'
import GeneratorView from '../views/GeneratorView.vue'
import ProgressView from '../views/ProgressView.vue'
import SettingsView from '../views/SettingsView.vue'
import NotFoundView from '../views/NotFoundView.vue'

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'landing', component: LandingView },
    { path: '/dashboard', name: 'dashboard', component: DashboardView },
    { path: '/login', name: 'login', component: LoginView },
    { path: '/register', name: 'register', component: RegisterView },
    { path: '/forgot-password', name: 'forgot-password', component: ForgotPasswordView },
    { path: '/decks', name: 'decks', component: DecksView },
    { path: '/decks/new', name: 'deck-create', component: DeckEditorView },
    { path: '/decks/:id/edit', name: 'deck-edit', component: DeckEditorView },
    { path: '/study', name: 'study', component: StudyView },
    { path: '/study/:id', name: 'study-deck', component: StudyView },
    { path: '/quiz', name: 'quiz', component: QuizView },
    { path: '/generator', name: 'generator', component: GeneratorView },
    { path: '/progress', name: 'progress', component: ProgressView },
    { path: '/settings', name: 'settings', component: SettingsView },
    { path: '/:pathMatch(.*)*', name: 'not-found', component: NotFoundView },
  ],
})