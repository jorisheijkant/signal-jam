<template>
  <div class="facebook-embed">
    <div class="fb-post" :data-href="url" data-width="500" ref="fbRef">
      <a :href="url">Loading Facebook post...</a>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'

const props = defineProps({
  url: {
    type: String,
    required: true
  }
})

const fbRef = ref(null)

const loadFacebookScript = () => {
  if (window.FB) {
    window.FB.XFBML.parse()
    return
  }

  const script = document.createElement('script')
  script.setAttribute('src', 'https://connect.facebook.net/en_US/sdk.js#xfbml=1&version=v18.0')
  script.setAttribute('async', 'true')
  script.setAttribute('defer', 'true')
  script.setAttribute('crossorigin', 'anonymous')
  document.head.appendChild(script)
}

onMounted(() => {
  loadFacebookScript()
})
</script>
