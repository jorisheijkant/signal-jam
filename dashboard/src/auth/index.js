import supabaseAuth from './providers/supabase.js'
import auth0Auth from './providers/auth0.js'
import clerkAuth from './providers/clerk.js'
import keycloakAuth from './providers/keycloak.js'

const AUTH_PROVIDER = import.meta.env.VITE_AUTH_PROVIDER || 'supabase'

const providers = {
  supabase: supabaseAuth,
  auth0: auth0Auth,
  clerk: clerkAuth,
  keycloak: keycloakAuth,
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
