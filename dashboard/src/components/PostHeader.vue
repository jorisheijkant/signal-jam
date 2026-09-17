<template>
  <div class="flex items-center gap-2 mb-3 flex-wrap">
    <span class="text-sm font-medium text-gray-800">
      {{ post.account?.display_name || post.account?.username || 'Onbekend' }}
    </span>
    <span class="text-xs text-gray-400">@{{ post.account?.username }}</span>
    <span class="text-xs text-gray-400">·</span>
    <span class="text-xs text-gray-400">{{ formatDate(post.posted_at) }}</span>
    <span v-if="post.post_type === 'repost'" class="inline-flex items-center gap-1 px-1.5 py-0.5 text-xs font-medium bg-gray-100 text-gray-500 rounded">
      ↻ repost
    </span>
    <span v-else-if="post.post_type === 'quote'" class="inline-flex items-center gap-1 px-1.5 py-0.5 text-xs font-medium bg-gray-100 text-gray-500 rounded">
      ❝ quote
    </span>
    <span v-else-if="post.post_type === 'reply'" class="inline-flex items-center gap-1 px-1.5 py-0.5 text-xs font-medium bg-gray-100 text-gray-500 rounded">
      ↩ reply
    </span>
    <span
      v-if="post.reposted_by?.length"
      class="inline-flex items-center gap-1 px-1.5 py-0.5 text-xs font-medium bg-gray-100 text-gray-500 rounded"
      :title="repostedByLabel"
    >
      ↻ {{ post.reposted_by.length }}
    </span>
    <span
      v-if="post.contains_misinformation"
      class="inline-block px-2 py-0.5 text-xs font-medium bg-amethyst-600 text-white rounded-full"
    >
      Bevat desinformatie
    </span>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  post: { type: Object, required: true },
})

const repostedByLabel = computed(() =>
  (props.post.reposted_by || [])
    .map(repost => `@${repost.account?.username || 'onbekend'}`)
    .join(', ')
)

function formatDate(ts) {
  if (!ts) return ''
  return new Date(ts).toLocaleString('nl-NL', { day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' })
}
</script>
