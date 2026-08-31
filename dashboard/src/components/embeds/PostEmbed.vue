<template>
  <TwitterEmbed v-if="platform === 'twitter'" :url="url" />
  <TiktokEmbed v-else-if="platform === 'tiktok'" :url="url" :content="content" />
  <FacebookEmbed v-else-if="platform === 'facebook'" :url="url" />
  <InstagramEmbed v-else-if="platform === 'instagram'" :url="url" :content="content" />
</template>

<script setup>
import TwitterEmbed from './TwitterEmbed.vue'
import TiktokEmbed from './TiktokEmbed.vue'
import FacebookEmbed from './FacebookEmbed.vue'
import InstagramEmbed from './InstagramEmbed.vue'

defineProps({
  platform: { type: String, required: true },
  url: { type: String, required: true },
  content: { type: String, default: null },
})
</script>
