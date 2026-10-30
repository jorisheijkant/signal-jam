<template>
  <CollapsibleSection title="Accounts" :subtitle="`${accounts.length} account${accounts.length !== 1 ? 's' : ''}`">
    <p class="text-sm text-gray-500 mb-6">
      De scrapers lezen deze lijst bij elke run. Een account met posts wordt bij verwijderen alleen van de lijst gehaald; zijn posts blijven bewaard.
    </p>

    <form @submit.prevent="addAccount" class="border border-amethyst-200 p-4 md:p-6 mb-6">
      <h3 class="text-sm font-semibold text-gray-700 mb-3">Nieuw account toevoegen</h3>
      <div class="flex flex-col gap-3">
        <label class="flex flex-col gap-1 text-sm text-gray-700">
          Platform *
          <select v-model="newPlatform" class="border border-gray-300 rounded-md p-2 text-sm">
            <option v-for="platform in SCRAPABLE_PLATFORMS" :key="platform" :value="platform">
              {{ formatPlatformLabel(platform) }}
            </option>
          </select>
        </label>
        <label class="flex flex-col gap-1 text-sm text-gray-700">
          Gebruikersnaam of profiel-URL *
          <input
            v-model="newProfile"
            type="text"
            required
            class="border border-gray-300 rounded-md p-2 text-sm"
            placeholder="Bijv. @voorbeeld of https://x.com/voorbeeld"
          />
        </label>
        <label class="flex flex-col gap-1 text-sm text-gray-700">
          Weergavenaam
          <input v-model="newDisplayName" type="text" class="border border-gray-300 rounded-md p-2 text-sm" />
        </label>
        <div class="flex items-center gap-3">
          <button
            type="submit"
            :disabled="isSaving"
            class="px-4 py-2 text-sm border border-amethyst-600 text-amethyst-700 hover:bg-amethyst-100 transition-colors cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {{ isSaving ? 'Toevoegen...' : 'Toevoegen' }}
          </button>
          <span v-if="saveError" class="text-sm text-red-600">{{ saveError }}</span>
        </div>
      </div>
    </form>

    <nav class="flex flex-wrap gap-2 mb-4">
      <button
        v-for="option in platformIndex"
        :key="option.platform ?? 'all'"
        @click="selectedPlatform = option.platform"
        :class="[
          'px-3 py-1 text-sm border cursor-pointer transition-colors',
          option.platform === selectedPlatform
            ? 'border-amethyst-600 bg-amethyst-100 text-amethyst-900'
            : 'border-amethyst-200 text-amethyst-700 hover:bg-amethyst-50',
        ]"
      >
        {{ option.label }} <span class="text-gray-500">{{ option.count }}</span>
      </button>
    </nav>

    <div class="space-y-3">
      <AccountRow
        v-for="account in visibleAccounts"
        :key="account.id"
        :account="account"
        @updated="replaceAccount"
        @removed="removeAccount"
      />
      <p v-if="visibleAccounts.length === 0 && !isLoading" class="text-sm text-gray-500">
        Geen accounts gevonden.
      </p>
    </div>
  </CollapsibleSection>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getWatchedAccounts, addWatchedAccount } from '../database'
import { buildAccountFields } from '../utils/accountForm'
import { SCRAPABLE_PLATFORMS, formatPlatformLabel } from '../utils/platformLabels'
import AccountRow from './AccountRow.vue'
import CollapsibleSection from './CollapsibleSection.vue'

const accounts = ref([])
const isLoading = ref(true)
const newPlatform = ref(SCRAPABLE_PLATFORMS[0])
const newProfile = ref('')
const newDisplayName = ref('')
const isSaving = ref(false)
const saveError = ref('')
const selectedPlatform = ref(null)

const platformIndex = computed(() => [
  { platform: null, label: 'Alle', count: accounts.value.length },
  ...SCRAPABLE_PLATFORMS.map(platform => ({
    platform,
    label: formatPlatformLabel(platform),
    count: accounts.value.filter(account => account.platform === platform).length,
  })),
])

const visibleAccounts = computed(() =>
  selectedPlatform.value
    ? accounts.value.filter(account => account.platform === selectedPlatform.value)
    : accounts.value
)

async function load() {
  const { data, error } = await getWatchedAccounts()
  isLoading.value = false
  if (error) {
    console.error('Failed to load accounts:', error)
    return
  }
  accounts.value = data
}

async function addAccount() {
  isSaving.value = true
  saveError.value = ''
  const fields = buildAccountFields(newPlatform.value, newProfile.value, newDisplayName.value)
  const { data, error } = await addWatchedAccount(fields)
  isSaving.value = false
  if (error) {
    saveError.value = error.message || 'Fout bij toevoegen'
    return
  }
  accounts.value = [...accounts.value.filter(account => account.id !== data.id), data]
  newProfile.value = ''
  newDisplayName.value = ''
}

function replaceAccount(updated) {
  accounts.value = accounts.value.map(account => account.id === updated.id ? updated : account)
}

function removeAccount(removed) {
  accounts.value = accounts.value.filter(account => account.id !== removed.id)
}

onMounted(load)
</script>
