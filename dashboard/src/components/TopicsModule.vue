<template>
  <div class="module topics-module bg-white border border-1 border-amethyst-200 p-4 md:p-8 w-full">
    <h2 class="text-2xl font-semibold text-gray-800 mb-4">Onderwerpen</h2>
    <p class="text-sm text-gray-400 mb-4">De frames die de laatste maand het meest actief zijn.</p>
    <ul v-if="frames.length" class="space-y-2">
      <li
        v-for="(frame, index) in frames"
        :key="frame.id"
        class="border-b border-gray-100 pb-2 last:border-b-0"
      >
        <button
          v-if="frame.description"
          type="button"
          @click="toggleExpand(frame)"
          class="flex items-center justify-between w-full text-left cursor-pointer"
        >
          <div class="flex items-center gap-2">
            <svg
              class="w-3 h-3 shrink-0 text-amethyst-500 transition-transform"
              :class="{ 'rotate-90': frame._expanded }"
              viewBox="0 0 8 8"
              fill="currentColor"
            >
              <path d="M0 0l8 4-8 4z" />
            </svg>
            <span class="text-xs font-bold text-amethyst-400 w-4 text-right">{{ index + 1 }}</span>
            <span class="text-sm font-medium text-gray-800">{{ frame.name }}</span>
          </div>
          <span class="text-sm font-semibold text-amethyst-700 bg-amethyst-50 px-2 py-0.5 rounded-full">{{ frame.count }}</span>
        </button>
        <div v-else class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="text-xs font-bold text-amethyst-400 w-4 text-right">{{ index + 1 }}</span>
            <span class="text-sm font-medium text-gray-800">{{ frame.name }}</span>
          </div>
          <span class="text-sm font-semibold text-amethyst-700 bg-amethyst-50 px-2 py-0.5 rounded-full">{{ frame.count }}</span>
        </div>
        <p v-if="frame._expanded" class="text-sm text-gray-500 mt-1 pl-9">{{ frame.description }}</p>
      </li>
    </ul>
    <p v-else class="text-sm text-gray-400">Geen actieve frames in de laatste maand.</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getActiveFrames } from '../database'

const frames = ref([])

onMounted(async () => {
  const { data, error } = await getActiveFrames(30)
  if (error) {
    console.error('Failed to load active frames:', error)
    return
  }
  frames.value = data.map(frame => ({ ...frame, _expanded: false }))
})

function toggleExpand(frame) {
  frame._expanded = !frame._expanded
}
</script>
