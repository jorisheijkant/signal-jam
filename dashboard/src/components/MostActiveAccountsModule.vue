<template>
  <div class="module most-active-accounts-module bg-white border border-1 border-amethyst-200 p-4 md:p-8 w-full">
    <h2 class="text-2xl font-semibold text-gray-800 mb-4">Meest actieve accounts</h2>
    <div class="accounts-list space-y-3">
      <div
        v-for="account in accounts"
        :key="account.id"
        class="account-item flex items-center justify-between border-b border-gray-200 pb-3 last:border-b-0"
      >
        <div class="account-info flex-1">
          <a
            :href="account.link"
            target="_blank"
            rel="noopener noreferrer"
            class="font-medium text-gray-800 hover:text-blue-600"
          >
            {{ account.username }}
          </a>
          <p class="text-sm text-gray-500">{{ account.platform }}</p>
        </div>
        <div class="account-activity text-right">
          <span class="text-sm font-semibold text-gray-600">{{ account.postCount }} posts</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const accounts = ref([
  {
    id: 1,
    username: '@nieuws_alternative',
    platform: 'X/Twitter',
    link: 'https://twitter.com/nieuws_alternative',
    postCount: 247
  },
  {
    id: 2,
    username: '@waarheid_nu',
    platform: 'X/Twitter',
    link: 'https://twitter.com/waarheid_nu',
    postCount: 189
  },
  {
    id: 3,
    username: '@media_kritiek',
    platform: 'X/Twitter',
    link: 'https://twitter.com/media_kritiek',
    postCount: 156
  },
  {
    id: 4,
    username: '@realfacts2024',
    platform: 'TikTok',
    link: 'https://www.tiktok.com/@realfacts2024',
    postCount: 134
  },
  {
    id: 5,
    username: '@onafhankelijk_nieuws',
    platform: 'Facebook',
    link: 'https://www.facebook.com/onafhankelijk.nieuws',
    postCount: 112
  },
  {
    id: 6,
    username: '@vrije_media_nl',
    platform: 'X/Twitter',
    link: 'https://twitter.com/vrije_media_nl',
    postCount: 98
  }
])
</script>
