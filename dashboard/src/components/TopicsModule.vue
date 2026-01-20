<template>
  <div class="module topics-module bg-white border border-1 border-amethyst-200 p-4 md:p-8 w-full">
    <h2 class="text-2xl font-semibold text-gray-800 mb-4">Onderwerpen/hashtags</h2>
    <div class="topics-list flex flex-wrap gap-2">
      <div
        v-for="topic in topics"
        :key="topic.id"
        class="topic-pill px-4 py-2 bg-lavender-600 text-white rounded-full text-sm font-medium"
      >
        {{ topic.name }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const topics = ref([
  { id: 1, name: '#Oekraïne' },
  { id: 2, name: '#UkraineWar' },
  { id: 3, name: '#Rusland' },
  { id: 4, name: '#NATO' },
  { id: 5, name: '#Putin' },
  { id: 6, name: '#Zelensky' },
  { id: 8, name: '#FakeNews' },
  { id: 10, name: '#MediaManipulatie' }
])
</script>
