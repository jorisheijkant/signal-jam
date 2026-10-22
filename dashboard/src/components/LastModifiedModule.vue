<template>
  <div class="module last-modified bg-white border border-1 border-amethyst-200 p-4 md:p-8 w-full">
    <h2 class="text-2xl font-semibold text-gray-800 mb-4">Laatst bijgewerkt</h2>
    <p class="text-gray-600 mb-4">{{ lastModified }}</p>
    <div class="flex flex-col gap-1 text-sm text-gray-600">
      <p>Aantal posts in database: <span class="font-medium text-gray-800">{{ totalCount }}</span></p>
      <p>Versie: {{ appVersion }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getLastScrapedAt, getPostCounts } from '../database'

const lastModified = ref('Laden...')
const totalCount = ref('—')

const appVersion = __APP_VERSION__

onMounted(async () => {
  const [{ data, error }, counts] = await Promise.all([
    getLastScrapedAt(),
    getPostCounts(),
  ])

  if (error || !data) {
    lastModified.value = 'Onbekend'
  } else {
    lastModified.value = new Date(data.scraped_at).toLocaleString('nl-NL', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  if (!counts.error) {
    totalCount.value = counts.total ?? '—'
  }
})
</script>
