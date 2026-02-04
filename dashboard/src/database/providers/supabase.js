import { createClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabasePublishableKey = import.meta.env.VITE_SUPABASE_PUBLISHABLE_KEY

const client = createClient(supabaseUrl, supabasePublishableKey)

async function getPosts() {
  const { data, error } = await client
    .from('posts')
    .select('*, account:accounts(*)')
    .order('posted_at', { ascending: false })

  return { data, error }
}

export default {
  getPosts,
}
