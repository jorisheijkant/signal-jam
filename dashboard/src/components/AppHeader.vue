<template>
  <header class="header p-4 md:p-8 mb-4 md:mb-8 border border-1 border-amethyst-600 flex items-center justify-between">
    <h1 class="text-4xl font-bold">🛰️ Signal Jam</h1>
    <button
      @click="handleSignOut"
      class="px-4 py-2 text-sm border border-amethyst-600 text-amethyst-700 hover:bg-amethyst-100 transition-colors cursor-pointer"
    >
      Log out
    </button>
  </header>
</template>

<script setup>
import { signOut } from '../auth'

async function handleSignOut() {
  try {
    await signOut()
  } catch (err) {
    console.error('Sign out failed:', err)
  }
}
</script>
