<template>
  <main class="flex-grow">
    <div class="flex items-baseline gap-3 mb-6">
      <h2 class="text-2xl font-semibold text-gray-800">Zoeken</h2>
    </div>

    <form @submit.prevent="runSearch" class="flex flex-wrap gap-3 mb-6">
      <input
        v-model="term"
        type="text"
        placeholder="Zoekterm..."
        class="border border-gray-300 px-3 py-2 text-sm flex-grow min-w-48"
      />
      <select
        v-model="selectedFrameId"
        class="border border-gray-300 px-3 py-2 text-sm"
      >
        <option :value="null">Alle frames</option>
        <option v-for="frame in frames" :key="frame.id" :value="frame.id">
          {{ frame.name }}
        </option>
      </select>
      <select
        v-model="selectedPlatform"
        class="border border-gray-300 px-3 py-2 text-sm"
      >
        <option :value="null">Alle platformen</option>
        <option v-for="platform in PLATFORMS" :key="platform.value" :value="platform.value">
          {{ platform.label }}
        </option>
      </select>
      <input
        v-model="startDate"
        type="date"
        class="border border-gray-300 px-3 py-2 text-sm"
      />
      <input
        v-model="endDate"
        type="date"
        class="border border-gray-300 px-3 py-2 text-sm"
      />
      <button
        type="submit"
        class="px-4 py-2 text-sm border border-amethyst-600 text-amethyst-700 hover:bg-amethyst-100 transition-colors cursor-pointer"
      >
        Zoeken
      </button>
    </form>

    <div v-if="searched" class="mb-4 text-sm text-gray-500">
      <span v-if="posts.length === 0">Geen resultaten gevonden.</span>
      <span v-else>{{ posts.length }} resultaten{{ hasMore ? '+' : '' }}</span>
    </div>

    <div class="space-y-6">
      <div
        v-for="post in posts"
        :key="post.id"
        class="border border-amethyst-200 p-4 md:p-6 max-w-lg"
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

        <PostLabelForm v-if="session" :post="post" :frames="frames" @submit="submitPost(post)" />
      </div>

      <button
        v-if="hasMore && searched"
        @click="loadMore"
        :disabled="loading"
        class="w-full py-2 text-sm text-gray-600 hover:text-gray-800 border border-gray-300 hover:bg-gray-50 disabled:opacity-50"
      >
        {{ loading ? 'Laden...' : 'Meer laden' }}
      </button>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { searchPosts, getFrames, updatePost, updateSiblingReposts, deletePost } from '../database'
import { session } from '../auth'
import { addFormFields } from '../utils/postForm.js'
import PostHeader from '../components/PostHeader.vue'
import PostEmbed from '../components/embeds/PostEmbed.vue'
import PostLabelForm from '../components/PostLabelForm.vue'

const PAGE_SIZE = 20
const PLATFORMS = [
  { value: 'twitter', label: 'Twitter' },
  { value: 'tiktok', label: 'TikTok' },
  { value: 'facebook', label: 'Facebook' },
  { value: 'instagram', label: 'Instagram' },
]
const route = useRoute()
const router = useRouter()

const term = ref('')
const selectedFrameId = ref(null)
const selectedPlatform = ref(null)
const startDate = ref('')
const endDate = ref('')
const frames = ref([])
const posts = ref([])
const hasMore = ref(false)
const searched = ref(false)
const loading = ref(false)

function buildQuery() {
  const query = {}
  if (term.value) query.term = term.value
  if (selectedFrameId.value != null) query.frameId = String(selectedFrameId.value)
  if (selectedPlatform.value) query.platform = selectedPlatform.value
  if (startDate.value) query.startDate = startDate.value
  if (endDate.value) query.endDate = endDate.value
  return query
}

async function runSearch() {
  router.replace({ query: buildQuery() })

  posts.value = []
  hasMore.value = false
  searched.value = false
  loading.value = true

  const { data, error } = await searchPosts(
    term.value || null,
    selectedFrameId.value,
    PAGE_SIZE,
    0,
    startDate.value || null,
    endDate.value || null,
    selectedPlatform.value || null
  )
  loading.value = false
  if (error) {
    console.error('Search failed:', error)
    return
  }
  posts.value = (data || []).map(addFormFields)
  hasMore.value = (data?.length ?? 0) === PAGE_SIZE
  searched.value = true
}

async function loadMore() {
  loading.value = true
  const { data, error } = await searchPosts(
    term.value || null,
    selectedFrameId.value,
    PAGE_SIZE,
    posts.value.length,
    startDate.value || null,
    endDate.value || null,
    selectedPlatform.value || null
  )
  loading.value = false
  if (error) {
    console.error('Load more failed:', error)
    return
  }
  posts.value.push(...(data || []).map(addFormFields))
  hasMore.value = (data?.length ?? 0) === PAGE_SIZE
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
  } else {
    post.is_checked = post._form.is_checked
    post._saved = true
    setTimeout(() => { post._saved = false }, 3000)
  }
}

onMounted(async () => {
  const { data } = await getFrames()
  frames.value = data || []

  if (route.query.term) term.value = route.query.term
  if (route.query.frameId) selectedFrameId.value = parseInt(route.query.frameId)
  if (route.query.platform) selectedPlatform.value = route.query.platform
  if (route.query.startDate) startDate.value = route.query.startDate
  if (route.query.endDate) endDate.value = route.query.endDate

  const hasParams = route.query.term || route.query.frameId || route.query.platform || route.query.startDate || route.query.endDate
  if (hasParams) await runSearch()
})
</script>
