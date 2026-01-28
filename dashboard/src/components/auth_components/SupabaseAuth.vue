<script setup>
import { ref } from 'vue'
import { signInWithOtp } from '../../auth'

const loading = ref(false)
const email = ref('')

const handleLogin = async () => {
  try {
    loading.value = true
    await signInWithOtp(email.value)
    alert('Check your email for the login link!')
  } catch (error) {
    if (error instanceof Error) {
      alert(error.message)
    }
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <form @submit.prevent="handleLogin">
    <p class="text-gray-600 mb-4">Sign in via magic link with your email below</p>
    <div class="mb-4">
      <input
        class="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-amethyst-500 focus:border-transparent"
        required
        type="email"
        placeholder="Your email"
        v-model="email"
      />
    </div>
    <div>
      <button
        type="submit"
        class="w-full px-4 py-2 bg-amethyst-600 text-white font-semibold rounded hover:bg-amethyst-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        :disabled="loading"
      >
        {{ loading ? 'Loading...' : 'Send magic link' }}
      </button>
    </div>
  </form>
</template>
