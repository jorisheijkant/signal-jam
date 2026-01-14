<template>
  <div class="min-h-screen bg-gray-100 p-8">
    <header class="bg-gradient-to-r from-purple-500 to-purple-700 text-white rounded-lg p-8 mb-8">
      <h1 class="text-4xl font-bold">Signal Jam dashboard</h1>
    </header>
    <main class="flex justify-center">
      <div class="bg-white rounded-lg shadow-lg p-8 max-w-md w-full">
        <h2 class="text-2xl font-semibold text-gray-800 mb-4">Welcome to your Vue Dashboard</h2>
        <p class="text-gray-600 mb-6">In dit dashboard houden we de verspreiding van desinformatie rond de oorlog in Oekraine in de gaten.</p>
        <p class="text-grey-800 mb-6">Ondersteunde platforms</p>
        <ul class="text-gray-600 mb-6">
          <li v-for="platform in supportedPlatforms">{{platform}}</li>
        </ul>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const supportedPlatforms = ref(["X/Twitter"])

</script>
