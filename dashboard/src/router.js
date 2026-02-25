import { createRouter, createWebHistory } from 'vue-router'
import DashboardPage from './pages/DashboardPage.vue'
import LabelingPage from './pages/LabelingPage.vue'

const routes = [
  { path: '/', component: DashboardPage },
  { path: '/labelen', component: LabelingPage },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
