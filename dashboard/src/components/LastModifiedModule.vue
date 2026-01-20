<template>
  <div class="module last-modified bg-white border border-1 border-amethyst-200 p-4 md:p-8 w-full">
    <h2 class="text-2xl font-semibold text-gray-800 mb-4">Laatst bijgewerkt</h2>
    <p class="text-gray-600">{{ lastModified }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const lastModified = ref(new Date().toLocaleString('nl-NL', {
  year: 'numeric',
  month: 'long',
  day: 'numeric',
  hour: '2-digit',
  minute: '2-digit'
}))
</script>
