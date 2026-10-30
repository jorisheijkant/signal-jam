<template>
  <main class="flex-grow">
    <h2 class="text-2xl font-semibold text-gray-800 mb-6">Instellingen</h2>

    <AccountsSection />
    <FramesSection />
    <TermsSection
      kind="search"
      title="Zoektermen"
      description="Termen waarop de scrapers per platform zoeken. Ze worden ongewijzigd in de zoek-URL gebruikt, dus %22rt.com%22 zoekt op de exacte zin."
    />
    <TermsSection
      kind="filter"
      title="Filtertermen"
      description="Een post van een account telt mee voor het thema zodra hij minstens één van deze woorden bevat (hoofdletterongevoelig). Zonder filtertermen telt elke post mee."
    />
  </main>
</template>

<script setup>
import AccountsSection from '../components/AccountsSection.vue'
import FramesSection from '../components/FramesSection.vue'
import TermsSection from '../components/TermsSection.vue'
</script>
