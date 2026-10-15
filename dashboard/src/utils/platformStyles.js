// Full class names are spelled out so Tailwind can find them.
const PLATFORM_STYLES = {
  twitter: { badgeClass: 'bg-sky-100 text-sky-700', dotClass: 'bg-sky-500' },
  tiktok: { badgeClass: 'bg-pink-100 text-pink-700', dotClass: 'bg-pink-500' },
  facebook: { badgeClass: 'bg-blue-100 text-blue-700', dotClass: 'bg-blue-500' },
  instagram: { badgeClass: 'bg-orange-100 text-orange-700', dotClass: 'bg-orange-500' },
}

const FALLBACK_STYLE = { badgeClass: 'bg-gray-100 text-gray-600', dotClass: 'bg-gray-400' }

export const PLATFORM_NAMES = Object.keys(PLATFORM_STYLES)

export function getPlatformStyle(platform) {
  return PLATFORM_STYLES[platform] || FALLBACK_STYLE
}
