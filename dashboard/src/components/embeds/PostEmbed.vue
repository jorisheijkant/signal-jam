<template>
  <TwitterEmbed v-if="platform === 'twitter'" :url="url" />
  <TiktokEmbed v-else-if="platform === 'tiktok'" :url="url" />
  <FacebookEmbed v-else-if="platform === 'facebook'" :url="url" />
</template>

<script setup>
import TwitterEmbed from './TwitterEmbed.vue'
import TiktokEmbed from './TiktokEmbed.vue'
import FacebookEmbed from './FacebookEmbed.vue'

defineProps({
  platform: { type: String, required: true },
  url: { type: String, required: true },
})
</script>
