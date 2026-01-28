import supabaseAuth from './providers/supabase.js'

// Configure which auth provider to use
const AUTH_PROVIDER = import.meta.env.VITE_AUTH_PROVIDER || 'supabase'

const providers = {
  supabase: supabaseAuth,
}

const auth = providers[AUTH_PROVIDER]

if (!auth) {
  throw new Error(`Unknown auth provider: ${AUTH_PROVIDER}`)
}

export const session = auth.session
export const init = auth.init
export const signInWithOtp = auth.signInWithOtp
export const signOut = auth.signOut

export default auth
