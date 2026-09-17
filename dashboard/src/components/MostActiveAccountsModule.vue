<template>
  <div class="module most-active-accounts-module bg-white border border-1 border-amethyst-200 p-4 md:p-8 w-full">
    <h2 class="text-2xl font-semibold text-gray-800 mb-4">Meest actieve accounts</h2>
    <p class="text-sm text-gray-400 mb-4">Aantal posts met misinformatie (en totaal aantal posts in de database).</p>
    <div class="accounts-list space-y-3">
      <div
        v-for="account in accounts"
        :key="account.id"
        class="account-item flex items-center justify-between border-b border-gray-200 pb-3 last:border-b-0"
      >
        <div class="account-info flex-1">
          <a
            :href="account.account_url"
            target="_blank"
            rel="noopener noreferrer"
            class="font-medium text-gray-800 hover:text-blue-600"
          >
            @{{ account.username }}
          </a>
          <p class="text-sm text-gray-500">{{ formatPlatformLabel(account.platform) }}</p>
        </div>
        <div class="account-activity text-right">
          <span class="text-sm font-semibold text-gray-600">{{ account.misinfoCount }} <span class="text-gray-400">({{ account.totalCount }})</span></span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getMostActiveAccounts } from '../database'
import { formatPlatformLabel } from '../utils/platformLabels.js'

const accounts = ref([])

onMounted(async () => {
  const { data, error } = await getMostActiveAccounts()
  if (error) {
    console.error('Failed to fetch most active accounts:', error)
    return
  }
  accounts.value = data
})
</script>
