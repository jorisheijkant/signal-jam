<template>
  <div v-if="session" class="dashboard-container min-h-screen bg-white p-4 md:p-8 max-w-[1800px] mx-auto flex flex-col">
    <AppHeader />
    <router-view />
    <footer class="footer p-4 md:p-8 mb-4 md:mb-8 mt-4 md:mt-8 border border-1 border-amethyst-200">
      <p class="copyright text-mb-4 text-gray-300 text-right">&copy; Signal Jam/Joris Heijkant, 2026</p>
    </footer>
  </div>

  <AuthModule v-else />
</template>

<script setup>
import { onMounted } from 'vue'

import { session, init as initAuth } from './auth'

import AppHeader from './components/AppHeader.vue'
import AuthModule from './components/AuthModule.vue'

onMounted(() => {
  initAuth()
})
</script>
