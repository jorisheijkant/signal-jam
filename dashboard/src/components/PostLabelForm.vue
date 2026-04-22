<template>
  <div class="flex flex-col gap-3">
    <label class="flex items-center gap-2 text-sm text-red-600">
      <input type="checkbox" v-model="post._form.not_relevant" class="accent-red-600" />
      Is niet relevant
    </label>

    <label class="flex items-center gap-2 text-sm text-gray-700">
      <input type="checkbox" v-model="post._form.contains_misinformation" class="accent-amethyst-600" />
      Bevat misinformatie
    </label>

    <label class="flex items-center gap-2 text-sm text-gray-700">
      <input type="checkbox" v-model="post._form.is_checked" class="accent-amethyst-600" />
      Gecheckt
    </label>

    <label class="flex flex-col gap-1 text-sm text-gray-700">
      Frame
      <select v-model="post._form.frame_id" class="border border-gray-300 rounded-md p-2 text-sm">
        <option :value="null">— Geen frame —</option>
        <option v-for="frame in frames" :key="frame.id" :value="frame.id">{{ frame.name }}</option>
      </select>
    </label>

    <label class="flex flex-col gap-1 text-sm text-gray-700">
      Notities
      <textarea
        v-model="post._form.notes"
        rows="2"
        class="border border-gray-300 rounded-md p-2 text-sm"
        placeholder="Voeg notities toe..."
      />
    </label>

    <div class="flex items-center gap-3">
      <button
        @click="$emit('submit')"
        :disabled="post._saving"
        class="px-4 py-2 text-sm border border-amethyst-600 text-amethyst-700 hover:bg-amethyst-100 transition-colors cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {{ post._saving ? 'Opslaan...' : 'Opslaan' }}
      </button>
      <span v-if="post._saved" class="text-sm text-green-600">Opgeslagen!</span>
      <span v-if="post._error" class="text-sm text-red-600">Fout bij opslaan</span>
    </div>
  </div>
</template>

<script setup>
defineProps({
  post: { type: Object, required: true },
  frames: { type: Array, required: true },
})

defineEmits(['submit'])
</script>
