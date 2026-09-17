<template>
  <main class="flex-grow">
    <div class="max-w-3xl mx-auto flex flex-col gap-2 mb-6">
      <h2 class="text-2xl font-semibold text-gray-800">Samenvattingen</h2>
      <p class="text-sm">Onderstaand vind je de samenvattingen van waar de pro-Russische posts op sociale media mee aankwamen, per week. Ook hebben we samenvattingen gemaakt van de berichtgeving over Nederland via Russische staatsmedia (zoals RT, Tass en RIA) en bekende Russische desinformatienetwerken als Pravda. Zo hopen we wat meer inzicht te kunnen bieden in de narratieven die de Russische propagandamachine probeert uit te rollen.</p> 

      <p class="text-sm text-red-400">Onderstaande samenvattingen zijn gegenereerd door kunstmatige intelligentie. Check altijd het originele materiaal voordat je hier te heftige conclusies aan verbindt.</p>
    </div>

    <div v-if="loading" class="text-sm text-gray-400">Laden...</div>

    <div v-else-if="summaries.length === 0" class="text-sm text-gray-400">
      Nog geen samenvattingen beschikbaar.
    </div>

    <div v-else class="max-w-3xl mx-auto space-y-10">
      <div v-for="yearGroup in groupedSummaries" :key="yearGroup.year">
        <div class="sticky top-0 z-20 h-12 flex items-center bg-white border-b border-amethyst-100">
          <h3 class="text-xl font-bold text-gray-800">{{ yearGroup.year }}</h3>
        </div>

        <div class="space-y-8 mt-4">
          <div v-for="monthGroup in yearGroup.months" :key="monthGroup.month">
            <div class="sticky top-12 z-10 h-9 flex items-center bg-white border-b border-amethyst-50">
              <h4 class="text-sm font-semibold uppercase tracking-wide text-gray-500">{{ monthGroup.label }}</h4>
            </div>

            <div class="space-y-6 mt-3">
              <div
                v-for="summary in monthGroup.summaries"
                :key="summary.id"
                class="border border-amethyst-200 p-4 md:p-6"
              >
                <div class="flex items-baseline justify-between gap-4 mb-4 pb-3 border-b border-amethyst-100">
                  <div>
                    <h5 class="font-semibold text-gray-800">Week {{ getIsoWeekNumber(summary.week_start) }}</h5>
                    <p class="text-xs text-gray-400 mt-0.5">{{ formatWeek(summary.week_start, summary.week_end) }}</p>
                  </div>
                  <span class="text-xs text-gray-400 shrink-0">
                    {{ formatLlmProviderLabel(summary.llm_provider) }} · Samenvatting gemaakt op: {{ formatDate(summary.generated_at) }}
                  </span>
                </div>

                <div class="space-y-5">
                  <section>
                    <h6 class="text-sm font-semibold text-gray-600 mb-2">Narratieven op sociale media</h6>
                    <p class="text-sm text-gray-700 leading-relaxed whitespace-pre-wrap">{{ summary.content }}</p>
                  </section>

                  <section>
                    <h6 class="text-sm font-semibold text-gray-600 mb-2">Narratieven op Russische propagandakanalen</h6>
                    <p v-if="summary.propaganda_channels_content" class="text-sm text-gray-700 leading-relaxed whitespace-pre-wrap">{{ summary.propaganda_channels_content }}</p>
                    <p v-else class="text-sm text-gray-400 italic">Nog niet beschikbaar.</p>
                  </section>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getSummaries } from '../database'
import { formatLlmProviderLabel } from '../utils/llmProviderLabels.js'

const summaries = ref([])
const loading = ref(true)

const groupedSummaries = computed(() => {
  const years = new Map()

  for (const summary of summaries.value) {
    const date = new Date(summary.week_start)
    const year = date.getUTCFullYear()
    const month = date.getUTCMonth()

    if (!years.has(year)) years.set(year, new Map())
    const months = years.get(year)
    if (!months.has(month)) months.set(month, [])
    months.get(month).push(summary)
  }

  return [...years.entries()].map(([year, months]) => ({
    year,
    months: [...months.entries()].map(([month, monthSummaries]) => ({
      month,
      label: formatMonthLabel(month),
      summaries: monthSummaries,
    })),
  }))
})

function formatMonthLabel(monthIndex) {
  const label = new Date(Date.UTC(2000, monthIndex, 1)).toLocaleDateString('nl-NL', { month: 'long', timeZone: 'UTC' })
  return label.charAt(0).toUpperCase() + label.slice(1)
}

function formatWeek(weekStart, weekEnd) {
  const fmt = d => new Date(d).toLocaleDateString('nl-NL', { day: 'numeric', month: 'long', year: 'numeric' })
  return `${fmt(weekStart)} – ${fmt(weekEnd)}`
}

function getIsoWeekNumber(dateStr) {
  const date = new Date(dateStr)
  const target = new Date(date.valueOf())
  const dayNumber = (date.getUTCDay() + 6) % 7
  target.setUTCDate(target.getUTCDate() - dayNumber + 3)
  const firstThursday = target.valueOf()
  target.setUTCMonth(0, 1)
  if (target.getUTCDay() !== 4) {
    target.setUTCMonth(0, 1 + ((4 - target.getUTCDay()) + 7) % 7)
  }
  return 1 + Math.ceil((firstThursday - target) / 604800000)
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
