<template>
  <div
    v-if="factCheck"
    class="mb-4 p-3 border text-sm max-w-md"
    :class="factCheck.likely_disinformation ? 'border-red-200 bg-red-50' : 'border-gray-200 bg-gray-50'"
  >
    <span
      class="inline-block px-2 py-0.5 text-xs font-medium rounded-full"
      :class="factCheck.likely_disinformation ? 'bg-red-100 text-red-700' : 'bg-gray-100 text-gray-600'"
    >
      AI: {{ factCheck.likely_disinformation ? 'Waarschijnlijk desinformatie' : 'Waarschijnlijk geen desinformatie' }}
    </span>

    <p class="mt-2 text-gray-700">{{ factCheck.reasoning }}</p>

    <table v-if="sources.length" class="mt-2 w-full">
      <tbody>
        <tr v-for="source in sources" :key="source.link" class="border-t border-red-100 first:border-t-0">
          <td class="py-1 pr-2">
            <a :href="source.link" target="_blank" rel="noopener noreferrer" class="text-amethyst-700 hover:underline">
              {{ source.title }}
            </a>
          </td>
        </tr>
      </tbody>
    </table>
  </div>

  <div v-else class="mb-4 p-3 border border-gray-200 bg-gray-50 text-sm text-gray-500 max-w-md">
    Nog niet door AI gecheckt
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  factCheck: { type: Object, default: null },
})

const sources = computed(() => props.factCheck?.ai_fact_check_sources ?? [])
</script>
