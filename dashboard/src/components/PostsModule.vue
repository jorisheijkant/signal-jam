<template>
  <div class="module posts-module bg-white border border-1 border-amethyst-200 p-4 md:p-8 w-full">
    <h2 class="text-2xl font-semibold text-gray-800 mb-4">Relevante posts</h2>
    <div class="posts-feed overflow-y-auto max-h-[800px] space-y-4">
      <div
        v-for="post in posts"
        :key="post.id"
        class="post-embed"
        :class="post.contains_misinformation ? 'border-l-4 border-amethyst-500 pl-3' : ''"
      >
        <div class="flex items-center gap-2 mb-2 flex-wrap">
          <span class="text-sm font-medium text-gray-800">
            {{ post.account?.display_name || post.account?.username || 'Onbekend' }}
          </span>
          <span class="text-xs text-gray-400">
            @{{ post.account?.username }}
          </span>
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
            v-if="post.contains_misinformation"
            class="inline-block px-2 py-0.5 text-xs font-medium bg-amethyst-600 text-white rounded-full"
          >
            Bevat misinformatie
          </span>
        </div>
        <TwitterEmbed v-if="post.platform === 'twitter'" :url="post.url" />
        <TiktokEmbed v-else-if="post.platform === 'tiktok'" :url="post.url" />
        <FacebookEmbed v-else-if="post.platform === 'facebook'" :url="post.url" />
      </div>
      <button
        v-if="hasMore"
        @click="loadMore"
        class="w-full py-2 text-sm text-gray-600 hover:text-gray-800 border border-gray-300 rounded-md hover:bg-gray-50"
      >
        Meer laden
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getCheckedPosts } from '../database'
import TwitterEmbed from './embeds/TwitterEmbed.vue'
import TiktokEmbed from './embeds/TiktokEmbed.vue'
import FacebookEmbed from './embeds/FacebookEmbed.vue'

const PAGE_SIZE = 10
const posts = ref([])
const hasMore = ref(true)

function formatDate(ts) {
  if (!ts) return ''
  const d = new Date(ts)
  return d.toLocaleString('nl-NL', { day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' })
}

async function loadMore() {
  const { data, error } = await getCheckedPosts(PAGE_SIZE, posts.value.length)
  if (error) {
    console.error('Failed to fetch posts:', error)
    return
  }
  posts.value.push(...data)
  if (data.length < PAGE_SIZE) {
    hasMore.value = false
  }
}

onMounted(loadMore)
</script>
