import { createRouter, createWebHistory } from 'vue-router'
import DashboardPage from './pages/DashboardPage.vue'
import LabelingPage from './pages/LabelingPage.vue'
import FramesPage from './pages/FramesPage.vue'

const routes = [
  { path: '/', component: DashboardPage },
  { path: '/labelen', component: LabelingPage },
  { path: '/frames', component: FramesPage },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
