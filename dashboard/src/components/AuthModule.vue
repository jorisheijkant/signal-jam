<template>
  <div class="module auth-module bg-white border border-1 border-amethyst-600 p-4 md:p-8 w-full max-w-md">
    <h1 class="text-2xl font-bold text-gray-800 mb-2">🛰️ Signal Jam</h1>
    <h2 class="text-xl font-semibold text-gray-600 mb-6">Inloggen</h2>
    <SupabaseAuth v-if="authProvider === 'supabase'" />
    <Auth0Auth v-else-if="authProvider === 'auth0'" />
    <ClerkAuth v-else-if="authProvider === 'clerk'" />
    <KeycloakAuth v-else-if="authProvider === 'keycloak'" />
  </div>
</template>

<script setup>
import SupabaseAuth from "./auth_components/SupabaseAuth.vue";
import Auth0Auth from "./auth_components/Auth0Auth.vue";
import ClerkAuth from "./auth_components/ClerkAuth.vue";
import KeycloakAuth from "./auth_components/KeycloakAuth.vue";

const authProvider = import.meta.env.VITE_AUTH_PROVIDER || "supabase";
</script>
