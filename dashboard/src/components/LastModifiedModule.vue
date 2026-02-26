<template>
  <div class="module last-modified bg-white border border-1 border-amethyst-200 p-4 md:p-8 w-full">
    <h2 class="text-2xl font-semibold text-gray-800 mb-4">Laatst bijgewerkt</h2>
    <p class="text-gray-600">{{ lastModified }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getLastScrapedAt } from '../database'

const lastModified = ref('Laden...')

onMounted(async () => {
  const { data, error } = await getLastScrapedAt()
  if (error || !data) {
    lastModified.value = 'Onbekend'
    return
  }
  lastModified.value = new Date(data.scraped_at).toLocaleString('nl-NL', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
})
</script>
