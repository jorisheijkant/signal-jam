<template>
  <div class="tiktok-embed">
    <blockquote class="tiktok-embed" cite="" :data-video-id="videoId" ref="tiktokRef">
      <a :href="url">Tiktok laden...</a>
    </blockquote>
    <EmbedCaption :content="content" />
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue'
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

const tiktokRef = ref(null)

const videoId = computed(() => {
  const match = props.url.match(/\/video\/(\d+)/)
  return match ? match[1] : ''
})

const loadTiktokScript = () => {
  if (window.tiktokEmbed) {
    return
  }

  const script = document.createElement('script')
  script.setAttribute('src', 'https://www.tiktok.com/embed.js')
  script.setAttribute('async', 'true')
  document.head.appendChild(script)
}

onMounted(() => {
  loadTiktokScript()
})
</script>
