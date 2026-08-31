<template>
  <div class="instagram-embed">
    <blockquote
      class="instagram-media"
      :data-instgrm-permalink="url"
      data-instgrm-version="14"
      ref="blockquoteRef"
    >
      <a :href="url">Loading Instagram post...</a>
    </blockquote>
    <EmbedCaption :content="content" />
  </div>
</template>

<script setup>
import { onMounted, watch } from 'vue'
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

const loadInstagramScript = () => {
  return new Promise((resolve) => {
    if (window.instgrm) {
      resolve()
      return
    }

    const script = document.createElement('script')
    script.setAttribute('src', 'https://www.instagram.com/embed.js')
    script.setAttribute('async', 'true')
    script.onload = () => resolve()
    document.head.appendChild(script)
  })
}

const processEmbed = async () => {
  await loadInstagramScript()
  window.instgrm?.Embeds?.process()
}

onMounted(() => {
  processEmbed()
})

watch(() => props.url, () => {
  processEmbed()
})
</script>
