<template>
  <div class="border border-amethyst-200 p-4">
    <form v-if="isEditing" @submit.prevent="save" class="flex flex-col gap-3">
      <label class="flex flex-col gap-1 text-sm text-gray-700">
        Gebruikersnaam of profiel-URL *
        <input v-model="editProfile" type="text" required class="border border-gray-300 rounded-md p-2 text-sm" />
      </label>
      <label class="flex flex-col gap-1 text-sm text-gray-700">
        Weergavenaam
        <input v-model="editDisplayName" type="text" class="border border-gray-300 rounded-md p-2 text-sm" />
      </label>
      <div class="flex items-center gap-3">
        <button
          type="submit"
          :disabled="isBusy"
          class="px-4 py-2 text-sm border border-amethyst-600 text-amethyst-700 hover:bg-amethyst-100 transition-colors cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {{ isBusy ? 'Opslaan...' : 'Opslaan' }}
        </button>
        <button
          type="button"
          @click="isEditing = false"
          :disabled="isBusy"
          class="px-4 py-2 text-sm text-gray-500 hover:text-gray-700 cursor-pointer disabled:opacity-50"
        >
          Annuleren
        </button>
        <span v-if="errorMessage" class="text-sm text-red-600">{{ errorMessage }}</span>
      </div>
    </form>

    <div v-else class="flex items-start justify-between gap-4">
      <div>
        <a
          :href="account.account_url"
          target="_blank"
          rel="noopener noreferrer"
          class="font-medium text-gray-800 text-sm hover:text-blue-600"
        >
          @{{ account.username }}
        </a>
        <span v-if="account.display_name" class="text-sm text-gray-500 ml-2">{{ account.display_name }}</span>
        <div class="flex items-center gap-2 mt-1">
          <span class="text-xs text-gray-500">{{ formatPlatformLabel(account.platform) }}</span>
          <span v-if="account.is_approved" class="px-2 py-0.5 text-xs font-medium bg-green-100 text-green-700 rounded-full">
            Goedgekeurd
          </span>
        </div>
        <p v-if="errorMessage" class="text-sm text-red-600 mt-1">{{ errorMessage }}</p>
      </div>
      <div class="flex items-center gap-3 shrink-0">
        <button @click="startEdit" class="text-sm text-amethyst-600 hover:text-amethyst-800 cursor-pointer">
          Bewerken
        </button>
        <button
          @click="remove"
          :disabled="isBusy"
          class="text-sm text-red-500 hover:text-red-700 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {{ isBusy ? 'Verwijderen...' : 'Verwijderen' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { updateAccount, deleteAccount } from '../database'
import { buildAccountFields } from '../utils/accountForm'
import { formatPlatformLabel } from '../utils/platformLabels'

const props = defineProps({
  account: { type: Object, required: true },
})

const emit = defineEmits(['updated', 'removed'])

const isEditing = ref(false)
const isBusy = ref(false)
const errorMessage = ref('')
const editProfile = ref('')
const editDisplayName = ref('')

function startEdit() {
  editProfile.value = props.account.username
  editDisplayName.value = props.account.display_name || ''
  errorMessage.value = ''
  isEditing.value = true
}

async function save() {
  isBusy.value = true
  errorMessage.value = ''
  const { platform, ...fields } = buildAccountFields(props.account.platform, editProfile.value, editDisplayName.value)
  const { data, error } = await updateAccount(props.account.id, fields)
  isBusy.value = false
  if (error) {
    errorMessage.value = error.message || 'Fout bij opslaan'
    return
  }
  isEditing.value = false
  emit('updated', data)
}

async function remove() {
  isBusy.value = true
  errorMessage.value = ''
  const { error } = await deleteAccount(props.account.id)
  isBusy.value = false
  if (error) {
    errorMessage.value = error.message || 'Fout bij verwijderen'
    return
  }
  emit('removed', props.account)
}
</script>
