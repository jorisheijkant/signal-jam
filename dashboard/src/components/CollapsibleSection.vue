<template>
  <details open class="group border border-amethyst-200 mb-6">
    <summary class="flex items-baseline gap-3 p-4 cursor-pointer select-none list-none [&::-webkit-details-marker]:hidden">
      <span class="text-gray-400 text-xs transition-transform group-open:rotate-90">▶</span>
      <h2 class="text-xl font-semibold text-gray-800">{{ title }}</h2>
      <span v-if="subtitle" class="text-sm text-gray-500">{{ subtitle }}</span>
    </summary>
    <div class="p-4 pt-0 md:px-6 md:pb-6">
      <slot />
    </div>
  </details>
</template>

<script setup>
defineProps({
  title: { type: String, required: true },
  subtitle: { type: String, default: '' },
})
</script>
