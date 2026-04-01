import { ref } from 'vue'
import { Clerk } from '@clerk/clerk-js'

const publishableKey = import.meta.env.VITE_CLERK_PUBLISHABLE_KEY

let clerk = null
const session = ref(null)

async function init() {
  clerk = new Clerk(publishableKey)
  await clerk.load()

  session.value = clerk.session ?? null

  clerk.addListener(({ session: newSession }) => {
    session.value = newSession ?? null
  })
}

async function signInWithOtp(email) {
  const redirectUrl = import.meta.env.VITE_AUTH_REDIRECT_URL || window.location.origin

  const signIn = await clerk.client.signIn.create({ identifier: email })

  const emailFactor = signIn.supportedFirstFactors.find(
    (ff) => ff.strategy === 'email_link'
  )

  if (!emailFactor) {
    throw new Error('Email link strategy not available. Check your Clerk configuration.')
  }

  await signIn.prepareFirstFactor({
    strategy: 'email_link',
    emailAddressId: emailFactor.emailAddressId,
    redirectUrl,
  })
}

async function signOut() {
  await clerk.signOut()
  session.value = null
}

export default {
  session,
  init,
  signInWithOtp,
  signOut,
}
