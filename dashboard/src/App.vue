<template>
  <div v-if="session" class="dashboard-container min-h-screen bg-white p-4 md:p-8 max-w-[1800px] mx-auto flex flex-col">
    <AppHeader />
    <main class="module-container flex-grow grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 md:gap-6">
      <div class="module-column flex flex-col gap-3 md:gap-6">
        <LastModifiedModule />
        <AboutModule />
        <DailyActivityModule />
      </div>
      <div class="module-column flex flex-col gap-3 md:gap-6">
        <PostsModule />
      </div>
      <div class="module-column flex flex-col gap-3 md:gap-6">
        <TopicsModule />
        <MostActiveAccountsModule />
      </div>
    </main>
    <footer class="footer p-4 md:p-8 mb-4 md:mb-8 mt-4 md:mt-8 border border-1 border-amethyst-200">
      <p class="copyright text-mb-4 text-gray-300 text-right">© Signal Jam/Joris Heijkant, 2026</p>
    </footer>
  </div>

  <!-- Implement when ready and Supabase is properly set up -->
  <AuthModule v-else />
</template>

<script setup>
import { onMounted } from 'vue'

import { session, init as initAuth } from './auth'

import AppHeader from './components/AppHeader.vue'
import AuthModule from './components/AuthModule.vue'
import AboutModule from './components/AboutModule.vue'
import LastModifiedModule from './components/LastModifiedModule.vue'
import PostsModule from './components/PostsModule.vue'
import TopicsModule from './components/TopicsModule.vue'
import MostActiveAccountsModule from './components/MostActiveAccountsModule.vue'
import DailyActivityModule from './components/DailyActivityModule.vue'

onMounted(() => {
  initAuth()
})

</script>
