const PLATFORM_LABELS = {
  twitter: 'X/Twitter',
  tiktok: 'TikTok',
  facebook: 'Facebook',
  instagram: 'Instagram',
}

export function formatPlatformLabel(platform) {
  return PLATFORM_LABELS[platform] || platform
}
