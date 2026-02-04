<template>
  <div class="module posts-module bg-white border border-1 border-amethyst-200 p-4 md:p-8 w-full">
    <h2 class="text-2xl font-semibold text-gray-800 mb-4">Relevante posts</h2>
    <div class="posts-feed overflow-y-auto max-h-[800px] space-y-4">
      <div v-for="post in posts" :key="post.id" class="post-embed">
        <TwitterEmbed v-if="post.platform === 'twitter'" :url="post.url" />
        <TiktokEmbed v-else-if="post.platform === 'tiktok'" :url="post.url" />
        <FacebookEmbed v-else-if="post.platform === 'facebook'" :url="post.url" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getPosts } from '../database'
import TwitterEmbed from './embeds/TwitterEmbed.vue'
import TiktokEmbed from './embeds/TiktokEmbed.vue'
import FacebookEmbed from './embeds/FacebookEmbed.vue'

const posts = ref([])

onMounted(async () => {
  const { data, error } = await getPosts()
  if (error) {
    console.error('Failed to fetch posts:', error)
    return
  }
  posts.value = data
})
</script>
