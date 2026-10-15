<template>
  <slot v-if="isUnlocked" />
  <main v-else class="flex-grow">
    <form @submit.prevent="submitPassword" class="max-w-sm mx-auto flex flex-col gap-3">
      <h2 class="text-2xl font-semibold text-gray-800">Artikelen</h2>
      <p class="text-sm">Deze pagina is beveiligd. Vul het wachtwoord in om verder te gaan.</p>
      <input
        v-model="enteredPassword"
        type="password"
        placeholder="Wachtwoord"
        autocomplete="off"
        class="border border-gray-300 px-3 py-2 text-sm"
      />
      <p v-if="hasWrongPassword" class="text-sm text-red-400">Onjuist wachtwoord.</p>
      <button
        type="submit"
        class="px-4 py-2 text-sm border border-amethyst-600 text-amethyst-700 hover:bg-amethyst-100 transition-colors cursor-pointer"
      >
        Openen
      </button>
    </form>
  </main>
</template>

<script setup>
import { ref } from 'vue'
import { isArticlesUnlocked, tryUnlockArticles } from '../utils/passwordGate.js'

const isUnlocked = ref(isArticlesUnlocked())
const enteredPassword = ref('')
const hasWrongPassword = ref(false)

function submitPassword() {
  isUnlocked.value = tryUnlockArticles(enteredPassword.value)
  hasWrongPassword.value = !isUnlocked.value
}
</script>
