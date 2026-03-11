<template>
  <main class="flex-grow">
    <div class="flex items-baseline gap-3 mb-6">
      <h2 class="text-2xl font-semibold text-gray-800">Frames</h2>
      <span class="text-sm text-gray-500">{{ frames.length }} frame{{ frames.length !== 1 ? 's' : '' }}</span>
    </div>

    <!-- Add frame form -->
    <form @submit.prevent="addFrame" class="border border-amethyst-200 p-4 md:p-6 mb-6">
      <h3 class="text-sm font-semibold text-gray-700 mb-3">Nieuw frame toevoegen</h3>
      <div class="flex flex-col gap-3">
        <label class="flex flex-col gap-1 text-sm text-gray-700">
          Naam *
          <input
            v-model="newName"
            type="text"
            required
            class="border border-gray-300 rounded-md p-2 text-sm"
            placeholder="Bijv. Klimaatontkenning"
          />
        </label>
        <label class="flex flex-col gap-1 text-sm text-gray-700">
          Beschrijving
          <textarea
            v-model="newDescription"
            rows="2"
            class="border border-gray-300 rounded-md p-2 text-sm"
            placeholder="Optionele beschrijving van het frame..."
          />
        </label>
        <div class="flex items-center gap-3">
          <button
            type="submit"
            :disabled="saving"
            class="px-4 py-2 text-sm border border-amethyst-600 text-amethyst-700 hover:bg-amethyst-100 transition-colors cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {{ saving ? 'Toevoegen...' : 'Toevoegen' }}
          </button>
          <span v-if="saveError" class="text-sm text-red-600">{{ saveError }}</span>
        </div>
      </div>
    </form>

    <!-- Frames list -->
    <div class="space-y-3">
      <div
        v-for="frame in frames"
        :key="frame.id"
        class="border border-amethyst-200 p-4 flex items-start justify-between gap-4"
      >
        <div>
          <div class="font-medium text-gray-800 text-sm">{{ frame.name }}</div>
          <div v-if="frame.description" class="text-sm text-gray-500 mt-1">{{ frame.description }}</div>
        </div>
        <button
          @click="removeFrame(frame)"
          :disabled="frame._deleting"
          class="text-sm text-red-500 hover:text-red-700 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed shrink-0"
        >
          {{ frame._deleting ? 'Verwijderen...' : 'Verwijderen' }}
        </button>
      </div>

      <p v-if="frames.length === 0 && !loading" class="text-sm text-gray-500">
        Nog geen frames aangemaakt.
      </p>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getFrames, createFrame, deleteFrame } from '../database'

const frames = ref([])
const loading = ref(true)
const newName = ref('')
const newDescription = ref('')
const saving = ref(false)
const saveError = ref('')

async function load() {
  loading.value = true
  const { data, error } = await getFrames()
  loading.value = false
  if (error) {
    console.error('Failed to load frames:', error)
    return
  }
  frames.value = data.map(f => ({ ...f, _deleting: false }))
}

async function addFrame() {
  saving.value = true
  saveError.value = ''
  const { data, error } = await createFrame(newName.value.trim(), newDescription.value.trim())
  saving.value = false
  if (error) {
    saveError.value = error.message || 'Fout bij toevoegen'
    return
  }
  frames.value.push({ ...data, _deleting: false })
  frames.value.sort((a, b) => a.name.localeCompare(b.name))
  newName.value = ''
  newDescription.value = ''
}

async function removeFrame(frame) {
  frame._deleting = true
  const { error } = await deleteFrame(frame.id)
  if (error) {
    console.error('Failed to delete frame:', error)
    frame._deleting = false
    return
  }
  frames.value = frames.value.filter(f => f.id !== frame.id)
}

onMounted(load)
</script>
