<template>
  <main class="module-container flex-grow grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 md:gap-6">
    <div class="module-column flex flex-col gap-3 md:gap-6">
      <LastModifiedModule />
      <AboutModule />
      <DailyActivityModule />
    </div>
    <div class="module-column flex flex-col gap-3 md:gap-6">
      <PostsModule />
    </div>
    <div class="module-column flex flex-col gap-3 md:gap-6">
      <TopicsModule />
      <MostActiveAccountsModule />
    </div>
  </main>
</template>

<script setup>
import AboutModule from '../components/AboutModule.vue'
import LastModifiedModule from '../components/LastModifiedModule.vue'
import PostsModule from '../components/PostsModule.vue'
import TopicsModule from '../components/TopicsModule.vue'
import MostActiveAccountsModule from '../components/MostActiveAccountsModule.vue'
import DailyActivityModule from '../components/DailyActivityModule.vue'
</script>
