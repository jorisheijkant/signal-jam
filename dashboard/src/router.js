import { createRouter, createWebHistory } from 'vue-router'
import DashboardPage from './pages/DashboardPage.vue'
import LabelingPage from './pages/LabelingPage.vue'
import FramesPage from './pages/FramesPage.vue'
import SamenvattingenPage from './pages/SamenvattingenPage.vue'
import SearchPage from './pages/SearchPage.vue'
import OverPage from './pages/OverPage.vue'

const routes = [
  { path: '/', component: DashboardPage, meta: { public: true, title: 'Dashboard' } },
  { path: '/labelen', component: LabelingPage, meta: { title: 'Labelen' } },
  { path: '/frames', component: FramesPage, meta: { title: 'Frames' } },
  { path: '/samenvattingen', component: SamenvattingenPage, meta: { public: true, title: 'Samenvattingen' } },
  { path: '/zoeken', component: SearchPage, meta: { public: true, title: 'Zoeken' } },
  { path: '/over', component: OverPage, meta: { public: true, title: 'Over' } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
