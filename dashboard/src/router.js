import { createRouter, createWebHistory } from 'vue-router'
import DashboardPage from './pages/DashboardPage.vue'
import LabelingPage from './pages/LabelingPage.vue'
import FramesPage from './pages/FramesPage.vue'
import SamenvattingenPage from './pages/SamenvattingenPage.vue'
import SearchPage from './pages/SearchPage.vue'

const routes = [
  { path: '/', component: DashboardPage, meta: { public: true } },
  { path: '/labelen', component: LabelingPage },
  { path: '/frames', component: FramesPage },
  { path: '/samenvattingen', component: SamenvattingenPage },
  { path: '/zoeken', component: SearchPage, meta: { public: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
