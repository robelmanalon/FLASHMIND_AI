import { request } from './api'

const quizQuestions = [
  { id: 1, type: 'multiple-choice', prompt: 'Which organelle is primarily responsible for producing ATP?', options: ['Nucleus', 'Mitochondrion', 'Ribosome', 'Golgi apparatus'], answer: 'Mitochondrion', explanation: 'Mitochondria convert energy from food into ATP, the cell\'s main usable energy source.' },
  { id: 2, type: 'true-false', prompt: 'The cell membrane is selectively permeable.', options: ['True', 'False'], answer: 'True', explanation: 'A selectively permeable membrane allows some substances through while restricting others.' },
  { id: 3, type: 'identification', prompt: 'Identify the jelly-like substance where many cell reactions happen.', answer: 'Cytoplasm', acceptable: ['cytoplasm', 'cytoplasm.'], explanation: 'Cytoplasm fills the cell and surrounds the organelles, providing the environment for many reactions.' },
  { id: 4, type: 'fill-blank', prompt: 'The process by which a cell divides into two identical daughter cells is called ___.', answer: 'Mitosis', acceptable: ['mitosis', 'mitosis.'], explanation: 'Mitosis produces two genetically identical daughter cells for growth and repair.' },
  { id: 5, type: 'multiple-choice', prompt: 'Which structure contains a cell\'s genetic material?', options: ['Cell wall', 'Vacuole', 'Nucleus', 'Cytoplasm'], answer: 'Nucleus', explanation: 'In eukaryotic cells, the nucleus stores DNA and controls gene expression.' },
  { id: 6, type: 'true-false', prompt: 'Ribosomes are surrounded by a double membrane.', options: ['True', 'False'], answer: 'False', explanation: 'Ribosomes are non-membranous structures made of RNA and proteins.' },
]

export function getQuizQuestions() {
  return structuredClone(quizQuestions)
}

export async function getSavedQuizzes() {
  return request('/quiz/saved')
}

export async function getSavedQuiz(id) {
  return request(`/quiz/saved/${id}`)
}

export async function saveQuiz(payload) {
  return request('/quiz/saved', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title: payload.title, questions: payload.questions }),
  })
}

export async function deleteSavedQuiz(id) {
  return request(`/quiz/saved/${id}`, { method: 'DELETE' })
}