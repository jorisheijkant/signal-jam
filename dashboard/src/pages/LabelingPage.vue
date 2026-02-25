<template>
  <main class="flex-grow">
    <h2 class="text-2xl font-semibold text-gray-800 mb-6">Posts labelen</h2>
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

        <div class="post-embed mb-4">
          <TwitterEmbed v-if="post.platform === 'twitter'" :url="post.url" />
          <TiktokEmbed v-else-if="post.platform === 'tiktok'" :url="post.url" />
          <FacebookEmbed v-else-if="post.platform === 'facebook'" :url="post.url" />
        </div>

        <div class="flex flex-col gap-3">
          <label class="flex items-center gap-2 text-sm text-red-600">
            <input
              type="checkbox"
              v-model="post._form.not_relevant"
              class="accent-red-600"
            />
            Is niet relevant (wordt verwijderd)
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
import { getPosts, updatePost, deletePost } from '../database'
import TwitterEmbed from '../components/embeds/TwitterEmbed.vue'
import TiktokEmbed from '../components/embeds/TiktokEmbed.vue'
import FacebookEmbed from '../components/embeds/FacebookEmbed.vue'

const PAGE_SIZE = 10
const posts = ref([])
const hasMore = ref(true)

function addFormFields(post) {
  post._form = {
    not_relevant: false,
    is_checked: post.is_checked || false,
    contains_misinformation: post.contains_misinformation || false,
    notes: post.notes || '',
  }
  post._saving = false
  post._saved = false
  post._error = false
  return post
}

async function loadMore() {
  const { data, error } = await getPosts(PAGE_SIZE, posts.value.length)
  if (error) {
    console.error('Failed to fetch posts:', error)
    return
  }
  posts.value.push(...data.map(addFormFields))
  if (data.length < PAGE_SIZE) {
    hasMore.value = false
  }
}

async function submitPost(post) {
  console.log('[Labeling] submitPost called for post id:', post.id, '| not_relevant:', post._form.not_relevant)
  post._saving = true
  post._saved = false
  post._error = false

  let error

  if (post._form.not_relevant) {
    console.log('[Labeling] Action: delete post', post.id)
    ;({ error } = await deletePost(post.id))
  } else {
    const fields = {
      is_checked: post._form.is_checked,
      contains_misinformation: post._form.contains_misinformation,
      notes: post._form.notes,
    }
    console.log('[Labeling] Action: update post', post.id, 'with', fields)
    ;({ error } = await updatePost(post.id, fields))
  }

  post._saving = false
  if (error) {
    console.error('[Labeling] Operation failed for post', post.id, '→ error:', error)
    post._error = true
  } else if (post._form.not_relevant) {
    console.log('[Labeling] Delete succeeded, removing post from list:', post.id)
    posts.value = posts.value.filter(p => p.id !== post.id)
  } else {
    console.log('[Labeling] Update succeeded for post:', post.id)
    post.is_checked = post._form.is_checked
    post._saved = true
    setTimeout(() => { post._saved = false }, 3000)
  }
}

onMounted(loadMore)
</script>
