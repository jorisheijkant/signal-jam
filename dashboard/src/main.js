import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './style.css'

const appTitle = import.meta.env.VITE_APP_TITLE || 'Signal Jam'

router.afterEach((to) => {
  document.title = to.meta.title ? `${to.meta.title} – ${appTitle}` : appTitle
})

createApp(App).use(router).mount('#app')
