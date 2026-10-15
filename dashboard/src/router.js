import { createRouter, createWebHistory } from 'vue-router'
import DashboardPage from './pages/DashboardPage.vue'
import LabelingPage from './pages/LabelingPage.vue'
import FramesPage from './pages/FramesPage.vue'
import SamenvattingenPage from './pages/SamenvattingenPage.vue'
import PostsPage from './pages/PostsPage.vue'
import ArticlesPage from './pages/ArticlesPage.vue'
import OverPage from './pages/OverPage.vue'

const routes = [
  { path: '/', component: DashboardPage, meta: { public: true, title: 'Dashboard' } },
  { path: '/labelen', component: LabelingPage, meta: { title: 'Labelen' } },
  { path: '/frames', component: FramesPage, meta: { title: 'Frames' } },
  { path: '/samenvattingen', component: SamenvattingenPage, meta: { public: true, title: 'Samenvattingen' } },
  { path: '/posts', component: PostsPage, meta: { public: true, title: 'Posts' } },
  { path: '/zoeken', redirect: to => ({ path: '/posts', query: to.query }) },
  { path: '/artikelen', component: ArticlesPage, meta: { public: true, title: 'Artikelen' } },
  { path: '/over', component: OverPage, meta: { public: true, title: 'Over' } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
