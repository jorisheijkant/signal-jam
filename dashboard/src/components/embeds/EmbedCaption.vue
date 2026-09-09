<template>
  <p v-if="content" class="text-sm text-gray-700 leading-relaxed whitespace-pre-wrap mt-2">{{ content }}</p>
</template>

<script setup>
defineProps({
  content: {
    type: String,
    default: null
  }
})
</script>
