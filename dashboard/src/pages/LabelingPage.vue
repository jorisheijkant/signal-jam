<template>
  <main class="flex-grow">
    <div class="flex items-baseline gap-3 mb-6">
      <h2 class="text-2xl font-semibold text-gray-800">Posts labelen</h2>
      <span v-if="unlabeledCount !== null" class="text-sm text-gray-500">{{ unlabeledCount }} nog te labelen</span>
    </div>
    <div class="space-y-6">
      <div
        v-for="post in posts"
        :key="post.id"
        class="border border-amethyst-200 p-4 md:p-6"
      >
        <div class="mb-3">
          <span v-if="post.is_checked" class="inline-block px-2 py-0.5 text-xs font-medium bg-gray-100 text-gray-500 rounded-full">
            Al gelabeld
          </span>
          <span v-else class="inline-block px-2 py-0.5 text-xs font-medium bg-green-100 text-green-700 rounded-full">
            Nog labelen
          </span>
        </div>

        <PostHeader :post="post" />

        <div class="post-embed mb-4">
          <PostEmbed :platform="post.platform" :url="post.url" :content="post.content" />
        </div>

        <AiFactCheckSuggestion :fact-check="post.ai_fact_checks?.[0]" />

        <PostLabelForm :post="post" :frames="frames" @submit="submitPost(post)" />
      </div>

      <button
        v-if="hasMore"
        @click="loadMore"
        class="w-full py-2 text-sm text-gray-600 hover:text-gray-800 border border-gray-300 rounded-md hover:bg-gray-50"
      >
        Meer laden
      </button>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getPosts, updatePost, updateSiblingReposts, deletePost, getUnlabeledCount, getFrames } from '../database'
import { addFormFields } from '../utils/postForm.js'
import PostHeader from '../components/PostHeader.vue'
import PostEmbed from '../components/embeds/PostEmbed.vue'
import PostLabelForm from '../components/PostLabelForm.vue'
import AiFactCheckSuggestion from '../components/AiFactCheckSuggestion.vue'

const PAGE_SIZE = 10
const posts = ref([])
const frames = ref([])
const hasMore = ref(true)
const unlabeledCount = ref(null)

async function loadMore() {
  const { data, error } = await getPosts(PAGE_SIZE, posts.value.length)
  if (error) {
    console.error('Failed to fetch posts:', error)
    return
  }
  posts.value.push(...data.map(addFormFields))
  if (data.length < PAGE_SIZE) hasMore.value = false
}

async function submitPost(post) {
  post._saving = true
  post._saved = false
  post._error = false

  let error

  if (post._form.not_relevant) {
    ;({ error } = await deletePost(post.id))
  } else {
    const fields = {
      is_checked: post._form.is_checked,
      contains_misinformation: post._form.contains_misinformation,
      frame_id: post._form.frame_id,
      notes: post._form.notes,
    }
    ;({ error } = await updatePost(post.id, fields))

    if (!error && (post.parent_post_id || post.post_type === 'original')) {
      await updateSiblingReposts(post, fields)
    }
  }

  post._saving = false
  if (error) {
    post._error = true
  } else if (post._form.not_relevant) {
    posts.value = posts.value.filter(p => p.id !== post.id)
    if (unlabeledCount.value !== null) unlabeledCount.value--
  } else {
    if (post._form.is_checked && !post.is_checked && unlabeledCount.value !== null) {
      unlabeledCount.value--
    }
    post.is_checked = post._form.is_checked
    post._saved = true
    setTimeout(() => { post._saved = false }, 3000)
  }
}

onMounted(async () => {
  const [{ count }, { data: frameData }] = await Promise.all([
    getUnlabeledCount(),
    getFrames(),
  ])
  unlabeledCount.value = count
  frames.value = frameData || []
  loadMore()
})
</script>
