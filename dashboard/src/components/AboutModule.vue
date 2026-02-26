<template>
  <div class="module about-module bg-white border border-1 border-amethyst-200 p-4 md:p-8 w-full">
    <h2 class="text-2xl font-semibold text-gray-800 mb-4">Over dit dashboard</h2>
    <p class="text-gray-600 mb-6">In dit dashboard houden we de verspreiding van desinformatie rond de oorlog in Oekraine in de gaten.</p>
    <p class="text-gray-600 mb-6">Ondersteunde platforms</p>
    <ul class="text-gray-600 mb-6 list-disc list-inside">
      <li v-for="platform in supportedPlatforms" :key="platform">{{platform}}</li>
    </ul>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const supportedPlatforms = ref(["X/Twitter", "Facebook (in aanbouw)", "TikTok (in aanbouw)"])
</script>
