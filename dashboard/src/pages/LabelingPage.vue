<template>
  <main class="flex-grow">
    <div class="max-w-3xl mx-auto mb-8">
      <h2 class="text-2xl font-semibold text-gray-800 mb-2">Posts labelen</h2>
      <p class="text-sm">Een account wordt toegevoegd aan de database zodra drie van zijn posts als desinformatie zijn bevestigd. Hieronder staan de accounts die we volgen en nog niet genoeg bevestigde posts hebben, gevolgd door losse posts van andere accounts die via zoektermen binnenkwamen.</p>
    </div>

    <section class="max-w-3xl mx-auto mb-12">
      <h3 class="text-lg font-semibold text-gray-800 mb-4">
        Gevolgde accounts
        <span class="text-sm font-normal text-gray-500">{{ accounts.length }} te beoordelen</span>
      </h3>
      <div class="space-y-6">
        <AccountReviewCard
          v-for="account in accounts"
          :key="account.account_id"
          :account="account"
          :frames="frames"
        />
        <p v-if="accounts.length === 0" class="text-sm text-gray-400">Geen accounts om te beoordelen.</p>
      </div>
    </section>

    <section class="max-w-3xl mx-auto">
      <h3 class="text-lg font-semibold text-gray-800 mb-4">
        Posts van andere accounts
        <span v-if="otherPostsCount !== null" class="text-sm font-normal text-gray-500">{{ otherPostsCount }} te beoordelen</span>
      </h3>
      <div class="space-y-6">
        <ReviewPostCard
          v-for="post in otherPosts"
          :key="post.id"
          :post="post"
          :frames="frames"
          @reviewed="removeOtherPost(post)"
        />
        <button
          v-if="hasMoreOtherPosts"
          @click="loadMoreOtherPosts"
          class="w-full py-2 text-sm text-gray-600 hover:text-gray-800 border border-gray-300 hover:bg-gray-50"
        >
          Meer laden
        </button>
        <p v-if="otherPosts.length === 0" class="text-sm text-gray-400">Geen posts om te beoordelen.</p>
      </div>
    </section>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getAccountReviewQueue, getUnreviewedPostsFromOtherAccounts, getFrames } from '../database'
import AccountReviewCard from '../components/AccountReviewCard.vue'
import ReviewPostCard from '../components/ReviewPostCard.vue'

const PAGE_SIZE = 10

const frames = ref([])
const accounts = ref([])
const otherPosts = ref([])
const otherPostsCount = ref(null)
const hasMoreOtherPosts = ref(true)

async function loadAccounts() {
  const { data, error } = await getAccountReviewQueue()
  if (error) {
    console.error('Failed to fetch accounts to review:', error)
    return
  }
  accounts.value = data
}

async function loadMoreOtherPosts() {
  const { data, error, count } = await getUnreviewedPostsFromOtherAccounts(PAGE_SIZE, otherPosts.value.length)
  if (error) {
    console.error('Failed to fetch posts:', error)
    return
  }
  otherPosts.value.push(...data)
  otherPostsCount.value = count
  if (data.length < PAGE_SIZE) hasMoreOtherPosts.value = false
}

function removeOtherPost(post) {
  otherPosts.value = otherPosts.value.filter(candidate => candidate.id !== post.id)
  otherPostsCount.value--
}

onMounted(async () => {
  const { data: frameData } = await getFrames()
  frames.value = frameData || []
  loadAccounts()
  loadMoreOtherPosts()
})
</script>
