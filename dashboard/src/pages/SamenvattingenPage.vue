<template>
  <main class="flex-grow">
    <div class="flex flex-col gap-2 mb-6">
      <h2 class="text-2xl font-semibold text-gray-800">Samenvattingen</h2>
      <p class="text-sm text-red-400">Onderstaande samenvattingen zijn gegenereerd door kunstmatige intelligentie. Check altijd het originele materiaal voordat je hier te heftige conclusies aan verbindt.</p>
    </div>

    <div v-if="loading" class="text-sm text-gray-400">Laden...</div>

    <div v-else-if="summaries.length === 0" class="text-sm text-gray-400">
      Nog geen samenvattingen beschikbaar.
    </div>

    <div v-else class="space-y-6">
      <div
        v-for="summary in summaries"
        :key="summary.id"
        class="border border-amethyst-200 p-4 md:p-6"
      >
        <div class="flex items-baseline justify-between gap-4 mb-3">
          <h3 class="font-semibold text-gray-800">
            {{ formatWeek(summary.week_start, summary.week_end) }}
          </h3>
          <span class="text-xs text-gray-400 shrink-0">
            {{ summary.llm_provider }} · {{ formatDate(summary.generated_at) }}
          </span>
        </div>

        <p class="text-sm text-gray-700 leading-relaxed whitespace-pre-wrap">{{ summary.content }}</p>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getSummaries } from '../database'

const summaries = ref([])
const loading = ref(true)

function formatWeek(weekStart, weekEnd) {
  const fmt = d => new Date(d).toLocaleDateString('nl-NL', { day: 'numeric', month: 'long', year: 'numeric' })
  return `${fmt(weekStart)} – ${fmt(weekEnd)}`
}

function formatDate(ts) {
  if (!ts) return ''
  return new Date(ts).toLocaleDateString('nl-NL', { day: 'numeric', month: 'short', year: 'numeric' })
}

onMounted(async () => {
  const { data, error } = await getSummaries()
  loading.value = false
  if (error) {
    console.error('Failed to load summaries:', error)
    return
  }
  summaries.value = data
})
</script>
