import { ref } from 'vue'
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabasePublishableKey = import.meta.env.VITE_SUPABASE_PUBLISHABLE_KEY

const client = createClient(supabaseUrl, supabasePublishableKey)

const session = ref(null)

async function init() {
  const { data } = await client.auth.getSession()
  session.value = data.session

  client.auth.onAuthStateChange((_, newSession) => {
    session.value = newSession
  })
}

async function signInWithOtp(email) {
  const { error } = await client.auth.signInWithOtp({
    email,
    options: {
      emailRedirectTo: import.meta.env.VITE_AUTH_REDIRECT_URL,
    },
  })
  if (error) throw error
}

async function signOut() {
  const { error } = await client.auth.signOut()
  if (error) throw error
  session.value = null
}

export default {
  session,
  init,
  signInWithOtp,
  signOut,
}
