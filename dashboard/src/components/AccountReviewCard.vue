<template>
  <section class="border border-amethyst-200 p-4 md:p-6">
    <header class="flex flex-wrap items-baseline justify-between gap-2 mb-4">
      <div>
        <a
          :href="account.account_url"
          target="_blank"
          rel="noopener noreferrer"
          class="font-medium text-gray-800 hover:text-blue-600"
        >
          @{{ account.username }}
        </a>
        <p class="text-sm text-gray-500">{{ formatPlatformLabel(account.platform) }}</p>
      </div>
      <span v-if="isApproved" class="px-2 py-0.5 text-xs font-medium bg-green-100 text-green-700 rounded-full">
        Goedgekeurd
      </span>
      <span v-else class="text-sm font-semibold text-gray-600">
        {{ confirmedCount }} van {{ POSTS_NEEDED_FOR_APPROVAL }} bevestigd
      </span>
    </header>

    <div v-if="!isApproved" class="space-y-4">
      <ReviewPostCard
        v-for="post in posts"
        :key="post.id"
        :post="post"
        :frames="frames"
        @reviewed="handleReviewed(post, $event)"
      />
      <p v-if="posts.length === 0" class="text-sm text-gray-400">Alle posts van dit account zijn beoordeeld.</p>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getUnreviewedPostsForAccount } from '../database'
import { formatPlatformLabel } from '../utils/platformLabels.js'
import { POSTS_NEEDED_FOR_APPROVAL } from '../utils/accountApproval.js'
import { REVIEW_VERDICTS } from '../utils/reviewPost.js'
import ReviewPostCard from './ReviewPostCard.vue'

const props = defineProps({
  account: { type: Object, required: true },
  frames: { type: Array, required: true },
})

const posts = ref([])
const confirmedCount = ref(props.account.confirmed_count)
const isApproved = computed(() => confirmedCount.value >= POSTS_NEEDED_FOR_APPROVAL)

function handleReviewed(post, verdict) {
  posts.value = posts.value.filter(candidate => candidate.id !== post.id)
  if (verdict === REVIEW_VERDICTS.MISINFORMATION) confirmedCount.value++
}

onMounted(async () => {
  const { data, error } = await getUnreviewedPostsForAccount(props.account.account_id)
  if (error) {
    console.error('Failed to fetch posts for account:', error)
    return
  }
  posts.value = data
})
</script>
