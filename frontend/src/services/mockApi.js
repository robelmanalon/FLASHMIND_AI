import { request } from './api'

export function getDashboardData() {
  return request('/dashboard')
}

export function getProgressData() {
  return request('/progress')
}