import { ref } from 'vue'
import { createAuth0Client } from '@auth0/auth0-spa-js'

const domain = import.meta.env.VITE_AUTH0_DOMAIN
const clientId = import.meta.env.VITE_AUTH0_CLIENT_ID

let client = null
const session = ref(null)

async function init() {
  client = await createAuth0Client({
    domain,
    clientId,
    authorizationParams: {
      redirect_uri: import.meta.env.VITE_AUTH_REDIRECT_URL || window.location.origin,
    },
  })

  // Handle redirect callback after Auth0 redirects back
  if (window.location.search.includes('code=') && window.location.search.includes('state=')) {
    await client.handleRedirectCallback()
    window.history.replaceState({}, document.title, window.location.pathname)
  }

  const isAuthenticated = await client.isAuthenticated()
  if (isAuthenticated) {
    const user = await client.getUser()
    session.value = { user }
  }
}

async function signInWithOtp(email) {
  await client.loginWithRedirect({
    authorizationParams: {
      login_hint: email,
    },
  })
}

async function signOut() {
  await client.logout({
    logoutParams: {
      returnTo: import.meta.env.VITE_AUTH_REDIRECT_URL || window.location.origin,
    },
  })
  session.value = null
}

export default {
  session,
  init,
  signInWithOtp,
  signOut,
}
