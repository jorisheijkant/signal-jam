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
import { ref } from 'vue'
import TwitterEmbed from './embeds/TwitterEmbed.vue'
import TiktokEmbed from './embeds/TiktokEmbed.vue'
import FacebookEmbed from './embeds/FacebookEmbed.vue'

const posts = ref([
  {
    id: 1,
    platform: 'twitter',
    url: 'https://x.com/HeroLancelot/status/1991569470331187639'
  },
  {
    id: 2,
    platform: 'twitter',
    url: 'https://x.com/MathildeReali/status/2013167070872035337'
  },
  {
    id: 3,
    platform: 'tiktok',
    url: 'https://www.tiktok.com/@3aztiram3/video/7454603483111558422'
  },
  {
    id: 4,
    platform: 'twitter',
    url: 'https://x.com/PsiloX/status/2000599864892428476'
  }
])
</script>
