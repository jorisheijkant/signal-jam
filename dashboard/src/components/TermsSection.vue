<template>
  <CollapsibleSection :title="title" :subtitle="`${terms.length} term${terms.length !== 1 ? 'en' : ''}`">
    <p class="text-sm text-gray-500 mb-6">{{ description }}</p>
    <p v-if="errorMessage" class="text-sm text-red-600 mb-3">{{ errorMessage }}</p>
    <div class="space-y-3">
      <TermList
        v-for="platform in SCRAPABLE_PLATFORMS"
        :key="platform"
        :platform="platform"
        :terms="termsForPlatform(platform)"
        @add="term => add(platform, term)"
        @remove="remove"
      />
    </div>
  </CollapsibleSection>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getTerms, addTerm, deleteTerm } from '../database'
import { SCRAPABLE_PLATFORMS } from '../utils/platformLabels'
import CollapsibleSection from './CollapsibleSection.vue'
import TermList from './TermList.vue'

const props = defineProps({
  kind: { type: String, required: true },
  title: { type: String, required: true },
  description: { type: String, required: true },
})

const terms = ref([])
const errorMessage = ref('')

function termsForPlatform(platform) {
  return terms.value.filter(term => term.platform === platform)
}

async function load() {
  const { data, error } = await getTerms(props.kind)
  if (error) {
    console.error('Failed to load terms:', error)
    return
  }
  terms.value = data
}

async function add(platform, term) {
  errorMessage.value = ''
  const { data, error } = await addTerm({ platform, kind: props.kind, term })
  if (error) {
    errorMessage.value = error.code === '23505' ? `"${term}" staat al in de lijst` : error.message || 'Fout bij toevoegen'
    return
  }
  terms.value = [...terms.value, data]
}

async function remove(term) {
  errorMessage.value = ''
  const { error } = await deleteTerm(term.id)
  if (error) {
    errorMessage.value = error.message || 'Fout bij verwijderen'
    return
  }
  terms.value = terms.value.filter(existing => existing.id !== term.id)
}

onMounted(load)
</script>
