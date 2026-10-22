<template>
  <div class="border border-amethyst-200 p-4 md:p-6 max-w-lg">
    <PostHeader :post="post" />

    <div class="post-embed mb-4">
      <PostEmbed :platform="post.platform" :url="post.url" :content="post.content" />
    </div>

    <div class="flex flex-col gap-3 max-w-md mb-4">
      <label class="flex flex-col gap-1 text-sm text-gray-700">
        Frame
        <select v-model="frameId" class="border border-gray-300 rounded-md p-2 text-sm">
          <option :value="null">— Geen frame —</option>
          <option v-for="frame in frames" :key="frame.id" :value="frame.id">{{ frame.name }}</option>
        </select>
      </label>

      <label class="flex flex-col gap-1 text-sm text-gray-700">
        Motivatie
        <textarea
          v-model="notes"
          rows="2"
          class="border border-gray-300 rounded-md p-2 text-sm"
          placeholder="Waarom wel of geen desinformatie?"
        />
      </label>
    </div>

    <div class="flex flex-wrap items-center gap-3">
      <button
        v-for="action in ACTIONS"
        :key="action.verdict"
        @click="review(action.verdict)"
        :disabled="isSaving"
        class="px-4 py-2 text-sm border transition-colors cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
        :class="action.classes"
      >
        {{ action.label }}
      </button>
      <span v-if="hasError" class="text-sm text-red-600">Fout bij opslaan</span>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { reviewPost, REVIEW_VERDICTS } from '../utils/reviewPost.js'
import PostHeader from './PostHeader.vue'
import PostEmbed from './embeds/PostEmbed.vue'

const ACTIONS = [
  {
    verdict: REVIEW_VERDICTS.MISINFORMATION,
    label: 'Bevat desinformatie',
    classes: 'border-amethyst-600 text-amethyst-700 hover:bg-amethyst-100',
  },
  {
    verdict: REVIEW_VERDICTS.NOT_MISINFORMATION,
    label: 'Geen desinformatie',
    classes: 'border-gray-300 text-gray-700 hover:bg-gray-50',
  },
  {
    verdict: REVIEW_VERDICTS.NOT_RELEVANT,
    label: 'Is niet relevant',
    classes: 'border-red-300 text-red-600 hover:bg-red-50',
  },
]

const props = defineProps({
  post: { type: Object, required: true },
  frames: { type: Array, required: true },
})

const emit = defineEmits(['reviewed'])

const frameId = ref(props.post.frame_id ?? null)
const notes = ref(props.post.notes ?? '')
const isSaving = ref(false)
const hasError = ref(false)

async function review(verdict) {
  isSaving.value = true
  hasError.value = false
  const { error } = await reviewPost(props.post, verdict, { frameId: frameId.value, notes: notes.value })
  isSaving.value = false

  if (error) {
    hasError.value = true
    return
  }
  emit('reviewed', verdict)
}
</script>
