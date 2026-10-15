<template>
  <PasswordGate>
  <main class="flex-grow">
    <div class="max-w-3xl mx-auto flex flex-col gap-2 mb-6">
      <h2 class="text-2xl font-semibold text-gray-800">Artikelen</h2>
      <p class="text-sm">Artikelen van Russische staatsmedia (zoals RT en TASS) en Nederlandstalige propagandasites als Pravda. De meeste artikelen zijn in het Engels/Russisch, de stukken van Pravda verschijnen wel in (erg krom) Nederlands.</p>
      <p class="text-sm text-red-400">Let op: dit is informatie van Russische propagandakanalen. Neem deze niet zomaar voor waar aan en probeer deze niet verder te verspreiden. Veel van de sites zul je vanwege Nederlandse blokkades niet kunnen bezoeken.       </p>
    </div>

    <form @submit.prevent="submitSearch" class="max-w-3xl mx-auto flex flex-wrap gap-3 mb-6">
      <input
        v-model="term"
        type="text"
        placeholder="Zoekterm..."
        class="border border-gray-300 px-3 py-2 text-sm flex-grow min-w-48"
      />
      <input v-model="startDate" type="date" class="border border-gray-300 px-3 py-2 text-sm" />
      <input v-model="endDate" type="date" class="border border-gray-300 px-3 py-2 text-sm" />
      <button
        type="submit"
        class="px-4 py-2 text-sm border border-amethyst-600 text-amethyst-700 hover:bg-amethyst-100 transition-colors cursor-pointer"
      >
        Zoeken
      </button>
      <label class="flex items-center gap-2 w-full text-sm text-gray-600 cursor-pointer">
        <input v-model="onlyAboutNetherlands" type="checkbox" @change="runSearch" />
        Alleen artikelen over Nederland
      </label>
    </form>

    <ul class="max-w-3xl mx-auto flex flex-wrap gap-x-4 gap-y-1 mb-6 text-xs text-gray-600" aria-label="Legenda">
      <li v-for="source in ARTICLE_SOURCE_NAMES" :key="source" class="flex items-center gap-1.5">
        <span class="inline-block w-2.5 h-2.5 rounded-full" :class="getArticleSourceStyle(source).dotClass"></span>
        {{ source }}
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
    <div v-else-if="articles.length === 0" class="max-w-3xl mx-auto text-sm text-gray-400">Geen artikelen gevonden.</div>

    <div v-else class="max-w-3xl mx-auto space-y-4">
      <article
        v-for="article in articles"
        :key="article.url"
        class="border border-amethyst-200 p-4 md:p-6"
      >
        <div class="flex items-baseline justify-between gap-4 mb-2 text-xs text-gray-400">
          <span
            class="inline-block px-2 py-0.5 text-xs font-medium rounded-full"
            :class="getArticleSourceStyle(article.source).badgeClass"
          >
            {{ article.source }}
          </span>
          <span>{{ formatArticleDate(article.published_at) }}</span>
        </div>
        <a
          :href="article.url"
          target="_blank"
          rel="noopener noreferrer"
          class="font-medium text-gray-800 hover:text-blue-600"
        >
          {{ article.title }}
        </a>
        <p v-if="getArticleExcerpt(article)" class="text-sm text-gray-600 leading-relaxed mt-2">
          {{ getArticleExcerpt(article) }}
        </p>
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
  </PasswordGate>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { searchArticles } from '../database'
import PasswordGate from '../components/PasswordGate.vue'
import { NETHERLANDS_SEARCH_TERMS } from '../utils/netherlandsSearchTerms.js'
import { ARTICLE_SOURCE_NAMES, getArticleSourceStyle } from '../utils/articleSources.js'
import { formatArticleDate, getArticleExcerpt } from '../utils/articles.js'

const PAGE_SIZE = 20

const term = ref('')
const onlyAboutNetherlands = ref(true)
const startDate = ref('')
const endDate = ref('')
const articles = ref([])
const hasMore = ref(false)
const loading = ref(false)
const isSearching = ref(false)

async function fetchPage(offset) {
  loading.value = true
  const { data, error } = await searchArticles(
    {
      term: term.value || null,
      relatedTerms: onlyAboutNetherlands.value ? NETHERLANDS_SEARCH_TERMS : null,
      startDate: startDate.value || null,
      endDate: endDate.value || null,
    },
    PAGE_SIZE,
    offset
  )
  loading.value = false
  if (error) {
    console.error('Failed to load articles:', error)
    return []
  }
  hasMore.value = data.length === PAGE_SIZE
  return data
}

async function submitSearch() {
  if (term.value) onlyAboutNetherlands.value = false
  await runSearch()
}

async function runSearch() {
  articles.value = []
  isSearching.value = true
  const firstPage = await fetchPage(0)
  articles.value = firstPage
  isSearching.value = false
}

async function loadMore() {
  articles.value.push(...await fetchPage(articles.value.length))
}

onMounted(runSearch)
</script>
