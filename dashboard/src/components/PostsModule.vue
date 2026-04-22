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
        <PostHeader :post="post" />
        <PostEmbed :platform="post.platform" :url="post.url" />
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
import PostHeader from './PostHeader.vue'
import PostEmbed from './embeds/PostEmbed.vue'

const PAGE_SIZE = 10
const posts = ref([])
const hasMore = ref(true)

async function loadMore() {
  const { data, error } = await getCheckedPosts(PAGE_SIZE, posts.value.length)
  if (error) {
    console.error('Failed to fetch posts:', error)
    return
  }
  posts.value.push(...data)
  if (data.length < PAGE_SIZE) hasMore.value = false
}

onMounted(loadMore)
</script>
