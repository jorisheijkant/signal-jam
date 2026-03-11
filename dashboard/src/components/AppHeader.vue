<template>
  <header class="header p-4 md:p-8 mb-4 md:mb-8 border border-1 border-amethyst-600 flex items-center justify-between">
    <h1 class="text-4xl font-bold">🛰️ Signal Jam</h1>
    <nav class="flex items-center gap-4">
      <router-link to="/" class="text-sm text-amethyst-700 hover:text-amethyst-900">Dashboard</router-link>
      <router-link to="/labelen" class="text-sm text-amethyst-700 hover:text-amethyst-900">
        Labelen<span v-if="unlabeledCount !== null"> ({{ unlabeledCount }})</span>
      </router-link>
      <router-link to="/frames" class="text-sm text-amethyst-700 hover:text-amethyst-900">Frames</router-link>
      <button
        @click="handleSignOut"
        class="px-4 py-2 text-sm border border-amethyst-600 text-amethyst-700 hover:bg-amethyst-100 transition-colors cursor-pointer"
      >
        Log out
      </button>
    </nav>
  </header>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { signOut } from '../auth'
import { getUnlabeledCount } from '../database'

const unlabeledCount = ref(null)

onMounted(async () => {
  const { count } = await getUnlabeledCount()
  unlabeledCount.value = count
})

async function handleSignOut() {
  try {
    await signOut()
  } catch (err) {
    console.error('Sign out failed:', err)
  }
}
</script>
