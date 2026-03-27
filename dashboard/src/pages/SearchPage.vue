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

        <div class="flex items-center gap-2 mb-3 flex-wrap">
          <span class="text-sm font-medium text-gray-800">
            {{ post.account?.display_name || post.account?.username || 'Onbekend' }}
          </span>
          <span class="text-xs text-gray-400">@{{ post.account?.username }}</span>
          <span class="text-xs text-gray-400">·</span>
          <span class="text-xs text-gray-400">{{ formatDate(post.posted_at) }}</span>
          <span v-if="post.post_type === 'repost'" class="inline-flex items-center gap-1 px-1.5 py-0.5 text-xs font-medium bg-gray-100 text-gray-500 rounded">
            ↻ repost
          </span>
          <span v-else-if="post.post_type === 'quote'" class="inline-flex items-center gap-1 px-1.5 py-0.5 text-xs font-medium bg-gray-100 text-gray-500 rounded">
            ❝ quote
          </span>
          <span v-else-if="post.post_type === 'reply'" class="inline-flex items-center gap-1 px-1.5 py-0.5 text-xs font-medium bg-gray-100 text-gray-500 rounded">
            ↩ reply
          </span>
        </div>

        <div class="post-embed mb-4">
          <TwitterEmbed v-if="post.platform === 'twitter'" :url="post.url" />
          <TiktokEmbed v-else-if="post.platform === 'tiktok'" :url="post.url" />
          <FacebookEmbed v-else-if="post.platform === 'facebook'" :url="post.url" />
        </div>

        <div v-if="session" class="flex flex-col gap-3">
          <label class="flex items-center gap-2 text-sm text-red-600">
            <input
              type="checkbox"
              v-model="post._form.not_relevant"
              class="accent-red-600"
            />
            Is niet relevant
          </label>

          <label class="flex items-center gap-2 text-sm text-gray-700">
            <input
              type="checkbox"
              v-model="post._form.contains_misinformation"
              class="accent-amethyst-600"
            />
            Bevat misinformatie
          </label>

          <label class="flex items-center gap-2 text-sm text-gray-700">
            <input
              type="checkbox"
              v-model="post._form.is_checked"
              class="accent-amethyst-600"
            />
            Gecheckt
          </label>

          <label class="flex flex-col gap-1 text-sm text-gray-700">
            Frame
            <select
              v-model="post._form.frame_id"
              class="border border-gray-300 rounded-md p-2 text-sm"
            >
              <option :value="null">— Geen frame —</option>
              <option v-for="frame in frames" :key="frame.id" :value="frame.id">
                {{ frame.name }}
              </option>
            </select>
          </label>

          <label class="flex flex-col gap-1 text-sm text-gray-700">
            Notities
            <textarea
              v-model="post._form.notes"
              rows="2"
              class="border border-gray-300 rounded-md p-2 text-sm"
              placeholder="Voeg notities toe..."
            />
          </label>

          <div class="flex items-center gap-3">
            <button
              @click="submitPost(post)"
              :disabled="post._saving"
              class="px-4 py-2 text-sm border border-amethyst-600 text-amethyst-700 hover:bg-amethyst-100 transition-colors cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {{ post._saving ? 'Opslaan...' : 'Opslaan' }}
            </button>
            <span v-if="post._saved" class="text-sm text-green-600">Opgeslagen!</span>
            <span v-if="post._error" class="text-sm text-red-600">Fout bij opslaan</span>
          </div>
        </div>
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
import { searchPosts, getFrames, updatePost, updateSiblingReposts, deletePost } from '../database'
import { session } from '../auth'
import TwitterEmbed from '../components/embeds/TwitterEmbed.vue'
import TiktokEmbed from '../components/embeds/TiktokEmbed.vue'
import FacebookEmbed from '../components/embeds/FacebookEmbed.vue'

function formatDate(ts) {
  if (!ts) return ''
  const d = new Date(ts)
  return d.toLocaleString('nl-NL', { day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' })
}

function addFormFields(post) {
  post._form = {
    not_relevant: false,
    is_checked: post.is_checked || false,
    contains_misinformation: post.contains_misinformation || false,
    frame_id: post.frame_id || null,
    notes: post.notes || '',
  }
  post._saving = false
  post._saved = false
  post._error = false
  return post
}

const PAGE_SIZE = 20
const term = ref('')
const selectedFrameId = ref(null)
const frames = ref([])
const posts = ref([])
const hasMore = ref(false)
const searched = ref(false)
const loading = ref(false)

async function runSearch() {
  posts.value = []
  hasMore.value = false
  searched.value = false
  loading.value = true

  const { data, error } = await searchPosts(term.value || null, selectedFrameId.value, PAGE_SIZE, 0)
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
  const { data, error } = await searchPosts(term.value || null, selectedFrameId.value, PAGE_SIZE, posts.value.length)
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
      const { error: siblingError } = await updateSiblingReposts(post, fields)
      if (siblingError) console.warn('Failed to update sibling reposts:', siblingError)
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
})
</script>
