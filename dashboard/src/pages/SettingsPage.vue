<template>
  <main class="flex-grow">
    <h2 class="text-2xl font-semibold text-gray-800 mb-6">Instellingen</h2>

    <AccountsSection />
    <FramesSection />
    <TermsSection
      kind="search"
      title="Zoektermen"
      description="Naast de posts van bovenstaande accounts zoeken we ook los naar bepaalde termen op elk platform. Deze kun je hier toevoegen."
    />
    <TermsSection
      kind="filter"
      title="Filtertermen"
      description="Niet elke post van de binnengehaalde accounts gaat over het thema. Zodra een post minstens één van deze woorden bevat valt hij onder het hoofdthema van het dashboard."
    />
  </main>
</template>

<script setup>
import AccountsSection from '../components/AccountsSection.vue'
import FramesSection from '../components/FramesSection.vue'
import TermsSection from '../components/TermsSection.vue'
</script>
