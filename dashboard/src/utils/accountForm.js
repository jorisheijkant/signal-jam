const PROFILE_URL_BUILDERS = {
  twitter: (username) => `https://x.com/${username}`,
  tiktok: (username) => `https://www.tiktok.com/@${username}`,
  instagram: (username) => `https://www.instagram.com/${username}/`,
}

export function parseUsername(input) {
  const trimmed = input.trim()
  const isProfileUrl = trimmed.includes('/') || trimmed.includes('.')
  const path = isProfileUrl ? new URL(trimmed.includes('://') ? trimmed : `https://${trimmed}`).pathname : trimmed
  return path.split('/').filter(Boolean)[0]?.replace(/^@/, '') ?? ''
}

export function buildProfileUrl(platform, username) {
  return PROFILE_URL_BUILDERS[platform](username)
}

export function buildAccountFields(platform, input, displayName) {
  const username = parseUsername(input)
  return {
    platform,
    username,
    account_url: buildProfileUrl(platform, username),
    display_name: displayName.trim() || null,
  }
}
