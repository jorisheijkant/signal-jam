<template>
  <div class="border border-amethyst-200 p-4">
    <h3 class="text-sm font-semibold text-gray-700 mb-3">{{ formatPlatformLabel(platform) }}</h3>

    <ul class="flex flex-wrap gap-2 mb-3">
      <li
        v-for="term in terms"
        :key="term.id"
        class="flex items-center gap-2 pl-3 pr-2 py-1 text-sm bg-amethyst-50 border border-amethyst-200"
      >
        <span class="break-all">{{ term.term }}</span>
        <button
          @click="$emit('remove', term)"
          class="text-gray-400 hover:text-red-600 cursor-pointer"
          :aria-label="`Verwijder ${term.term}`"
        >
          ×
        </button>
      </li>
      <li v-if="terms.length === 0" class="text-sm text-gray-500">Nog geen termen.</li>
    </ul>

    <form @submit.prevent="submit" class="flex gap-2">
      <input
        v-model="newTerm"
        type="text"
        required
        class="flex-grow border border-gray-300 rounded-md p-2 text-sm"
        placeholder="Nieuwe term"
      />
      <button
        type="submit"
        class="px-4 py-2 text-sm border border-amethyst-600 text-amethyst-700 hover:bg-amethyst-100 transition-colors cursor-pointer"
      >
        Toevoegen
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { formatPlatformLabel } from '../utils/platformLabels'

defineProps({
  platform: { type: String, required: true },
  terms: { type: Array, required: true },
})

const emit = defineEmits(['add', 'remove'])

const newTerm = ref('')

function submit() {
  const term = newTerm.value.trim()
  if (!term) return
  emit('add', term)
  newTerm.value = ''
}
</script>
