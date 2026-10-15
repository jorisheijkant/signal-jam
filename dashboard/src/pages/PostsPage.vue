<template>
  <main class="flex-grow">
    <div class="max-w-3xl mx-auto flex flex-col gap-2 mb-6">
      <h2 class="text-2xl font-semibold text-gray-800">Posts</h2>
      <p class="text-sm">Posts van sociale media over Nederland waarvan we vermoeden dat ze onderdeel zijn van pro-Russische beïnvloeding. Standaard zie je alleen de posts waarvan we hebben vastgesteld dat ze desinformatie bevatten. Zoek je op een term, dan zoek je door alle posts.</p>
    </div>

    <form @submit.prevent="submitSearch" class="max-w-3xl mx-auto flex flex-wrap gap-3 mb-6">
      <input
        v-model="term"
        type="text"
        placeholder="Zoekterm..."
        class="border border-gray-300 px-3 py-2 text-sm flex-grow min-w-48"
      />
      <select v-model="selectedFrameId" class="border border-gray-300 px-3 py-2 text-sm">
        <option :value="null">Alle frames</option>
        <option v-for="frame in frames" :key="frame.id" :value="frame.id">
          {{ frame.name }}
        </option>
      </select>
      <select v-model="selectedPlatform" class="border border-gray-300 px-3 py-2 text-sm">
        <option :value="null">Alle platformen</option>
        <option v-for="platform in PLATFORM_NAMES" :key="platform" :value="platform">
          {{ formatPlatformLabel(platform) }}
        </option>
      </select>
      <input v-model="startDate" type="date" class="border border-gray-300 px-3 py-2 text-sm" />
      <input v-model="endDate" type="date" class="border border-gray-300 px-3 py-2 text-sm" />
      <button
        type="submit"
        class="px-4 py-2 text-sm border border-amethyst-600 text-amethyst-700 hover:bg-amethyst-100 transition-colors cursor-pointer"
      >
        Zoeken
      </button>
      <label class="flex items-center gap-2 w-full text-sm text-gray-600 cursor-pointer">
        <input v-model="onlyMisinformation" type="checkbox" @change="runSearch" />
        Alleen posts met desinformatie
      </label>
    </form>

    <ul class="max-w-3xl mx-auto flex flex-wrap gap-x-4 gap-y-1 mb-6 text-xs text-gray-600" aria-label="Legenda">
      <li v-for="platform in PLATFORM_NAMES" :key="platform" class="flex items-center gap-1.5">
        <span class="inline-block w-2.5 h-2.5 rounded-full" :class="getPlatformStyle(platform).dotClass"></span>
        {{ formatPlatformLabel(platform) }}
      </li>
    </ul>

    <div v-if="isSearching" class="max-w-3xl mx-auto space-y-4" role="status" aria-label="Laden">
      <div v-for="placeholder in 3" :key="placeholder" class="border border-amethyst-200 p-4 md:p-6 animate-pulse">
        <div class="h-4 w-24 rounded-full bg-amethyst-200 mb-3"></div>
        <div class="h-4 w-3/4 rounded bg-amethyst-200 mb-3"></div>
        <div class="h-3 w-full rounded bg-amethyst-100 mb-2"></div>
        <div class="h-3 w-5/6 rounded bg-amethyst-100"></div>
      </div>
    </div>
    <div v-else-if="posts.length === 0" class="max-w-3xl mx-auto text-sm text-gray-400">Geen posts gevonden.</div>

    <div v-else class="max-w-3xl mx-auto space-y-4">
      <article
        v-for="post in posts"
        :key="post.id"
        class="border border-amethyst-200 p-4 md:p-6"
      >
        <div class="flex items-center gap-2 mb-3">
          <span
            class="inline-block px-2 py-0.5 text-xs font-medium rounded-full"
            :class="getPlatformStyle(post.platform).badgeClass"
          >
            {{ formatPlatformLabel(post.platform) }}
          </span>
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
      </article>

      <button
        v-if="hasMore"
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
import { searchPosts, getFrames, updatePost, deletePost } from '../database'
import { session } from '../auth'
import { addFormFields } from '../utils/postForm.js'
import { formatPlatformLabel } from '../utils/platformLabels.js'
import { PLATFORM_NAMES, getPlatformStyle } from '../utils/platformStyles.js'
import PostHeader from '../components/PostHeader.vue'
import PostEmbed from '../components/embeds/PostEmbed.vue'
import PostLabelForm from '../components/PostLabelForm.vue'

const PAGE_SIZE = 20
const route = useRoute()
const router = useRouter()

const term = ref('')
const onlyMisinformation = ref(true)
const selectedFrameId = ref(null)
const selectedPlatform = ref(null)
const startDate = ref('')
const endDate = ref('')
const frames = ref([])
const posts = ref([])
const hasMore = ref(false)
const loading = ref(false)
const isSearching = ref(false)

function buildQuery() {
  const query = {}
  if (term.value) query.term = term.value
  if (selectedFrameId.value != null) query.frameId = String(selectedFrameId.value)
  if (selectedPlatform.value) query.platform = selectedPlatform.value
  if (startDate.value) query.startDate = startDate.value
  if (endDate.value) query.endDate = endDate.value
  return query
}

async function fetchPage(offset) {
  loading.value = true
  const { data, error } = await searchPosts(
    {
      term: term.value || null,
      frameId: selectedFrameId.value,
      platform: selectedPlatform.value || null,
      startDate: startDate.value || null,
      endDate: endDate.value || null,
      containsMisinformation: onlyMisinformation.value,
    },
    PAGE_SIZE,
    offset
  )
  loading.value = false
  if (error) {
    console.error('Failed to load posts:', error)
    return []
  }
  hasMore.value = data.length === PAGE_SIZE
  return data.map(addFormFields)
}

async function submitSearch() {
  if (term.value) onlyMisinformation.value = false
  await runSearch()
}

async function runSearch() {
  router.replace({ query: buildQuery() })
  posts.value = []
  isSearching.value = true
  const firstPage = await fetchPage(0)
  posts.value = firstPage
  isSearching.value = false
}

async function loadMore() {
  posts.value.push(...await fetchPage(posts.value.length))
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

function applyQueryParams() {
  const { term: queryTerm, frameId, platform, startDate: queryStart, endDate: queryEnd } = route.query
  if (queryTerm) term.value = queryTerm
  if (frameId) selectedFrameId.value = parseInt(frameId)
  if (platform) selectedPlatform.value = platform
  if (queryStart) startDate.value = queryStart
  if (queryEnd) endDate.value = queryEnd

  const hasSearchParams = Object.keys(route.query).length > 0
  if (hasSearchParams) onlyMisinformation.value = false
}

onMounted(async () => {
  const { data } = await getFrames()
  frames.value = data || []
  applyQueryParams()
  await runSearch()
})
</script>
