import { ref } from 'vue'
import Keycloak from 'keycloak-js'

const session = ref(null)
let keycloak = null

async function init() {
  keycloak = new Keycloak({
    url: import.meta.env.VITE_KEYCLOAK_URL,
    realm: import.meta.env.VITE_KEYCLOAK_REALM,
    clientId: import.meta.env.VITE_KEYCLOAK_CLIENT_ID,
  })

  const authenticated = await keycloak.init({
    onLoad: 'check-sso',
    silentCheckSsoRedirectUri: window.location.origin + '/silent-check-sso.html',
    pkceMethod: 'S256',
  })

  if (authenticated) {
    session.value = { user: keycloak.tokenParsed }
  }

  // Refresh the token before it expires so the session stays alive
  keycloak.onTokenExpired = async () => {
    try {
      await keycloak.updateToken(30)
      session.value = { user: keycloak.tokenParsed }
    } catch {
      session.value = null
    }
  }
}

async function signInWithOtp(email) {
  keycloak.login({
    loginHint: email,
    redirectUri: import.meta.env.VITE_AUTH_REDIRECT_URL || window.location.origin,
  })
}

async function signOut() {
  await keycloak.logout({
    redirectUri: import.meta.env.VITE_AUTH_REDIRECT_URL || window.location.origin,
  })
  session.value = null
}

export default {
  session,
  init,
  signInWithOtp,
  signOut,
}
