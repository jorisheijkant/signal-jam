import supabaseDb from './providers/supabase.js'

// Configure which database provider to use
const DB_PROVIDER = import.meta.env.VITE_DB_PROVIDER || 'supabase'

const providers = {
  supabase: supabaseDb,
}

const db = providers[DB_PROVIDER]

if (!db) {
  throw new Error(`Unknown database provider: ${DB_PROVIDER}`)
}

export const getPosts = db.getPosts
export const getPostsPerDay = db.getPostsPerDay
export const getMostActiveAccounts = db.getMostActiveAccounts

export default db
