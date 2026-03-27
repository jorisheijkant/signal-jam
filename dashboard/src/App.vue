<template>
  <div v-if="session || route.meta.public" class="dashboard-container min-h-screen bg-white p-4 md:p-8 max-w-[1800px] mx-auto flex flex-col">
    <AppHeader />
    <router-view />
    <footer class="footer p-4 md:p-8 mb-4 md:mb-8 mt-4 md:mt-8 border border-1 border-amethyst-200">
      <p class="copyright text-mb-4 text-gray-300 text-right">&copy; Signal Jam/Joris Heijkant, 2026</p>
    </footer>
  </div>

  <div v-else class="min-h-screen bg-gray-50 flex items-center justify-center p-4">
    <AuthModule />
  </div>

  <div
    v-if="showAuthModal && !session"
    class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4"
    @click.self="showAuthModal = false"
  >
    <div class="relative">
      <button
        @click="showAuthModal = false"
        class="absolute -top-3 -right-3 w-7 h-7 bg-white border border-gray-300 text-gray-500 hover:text-gray-800 text-sm flex items-center justify-center z-10"
      >
        ✕
      </button>
      <AuthModule />
    </div>
  </div>
</template>

<script setup>
import { onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'

import { session, init as initAuth } from './auth'
import { showAuthModal } from './authModal'

import AppHeader from './components/AppHeader.vue'
import AuthModule from './components/AuthModule.vue'

const route = useRoute()

// Close modal once user logs in
watch(session, (val) => {
  if (val) showAuthModal.value = false
})

onMounted(() => {
  initAuth()
})
</script>
