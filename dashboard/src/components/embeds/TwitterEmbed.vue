<template>
  <div class="twitter-embed">
    <div ref="containerRef"></div>
    <EmbedCaption :content="content" />
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'
import EmbedCaption from './EmbedCaption.vue'

const props = defineProps({
  url: {
    type: String,
    required: true
  },
  content: {
    type: String,
    default: null
  }
})

const containerRef = ref(null)

const loadTwitterScript = () => {
  return new Promise((resolve) => {
    if (window.twttr) {
      resolve()
      return
    }

    const script = document.createElement('script')
    script.setAttribute('src', 'https://platform.twitter.com/widgets.js')
    script.setAttribute('async', 'true')
    script.setAttribute('charset', 'utf-8')
    script.onload = () => resolve()
    document.head.appendChild(script)
  })
}

const createEmbed = async () => {
  if (!containerRef.value) return

  await loadTwitterScript()

  // Clear container
  containerRef.value.innerHTML = ''

  if (window.twttr && window.twttr.widgets) {
    try {
      await window.twttr.widgets.createTweet(
        getTweetId(props.url),
        containerRef.value,
        {
          theme: 'light',
          conversation: 'none'
        }
      )
    } catch (error) {
      console.error('Error embedding tweet:', error)
      containerRef.value.innerHTML = `<p class="text-gray-500 text-sm">Could not load tweet: <a href="${props.url}" target="_blank" class="text-blue-600 hover:underline">${props.url}</a></p>`
    }
  }
}

const getTweetId = (url) => {
  // Extract tweet ID from URL (works for both twitter.com and x.com)
  const match = url.match(/status\/(\d+)/)
  return match ? match[1] : null
}

onMounted(() => {
  createEmbed()
})

watch(() => props.url, () => {
  createEmbed()
})
</script>
