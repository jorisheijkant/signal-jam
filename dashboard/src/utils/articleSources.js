// Full class names are spelled out so Tailwind can find them. Add a line here when scraping a new outlet.
const ARTICLE_SOURCE_STYLES = {
  'Russia Today': { badgeClass: 'bg-red-100 text-red-700', dotClass: 'bg-red-500' },
  'Tass': { badgeClass: 'bg-blue-100 text-blue-700', dotClass: 'bg-blue-500' },
  'Lenta RU': { badgeClass: 'bg-amber-100 text-amber-700', dotClass: 'bg-amber-500' },
  'Gazeta': { badgeClass: 'bg-emerald-100 text-emerald-700', dotClass: 'bg-emerald-500' },
  'Pravda NL': { badgeClass: 'bg-violet-100 text-violet-700', dotClass: 'bg-violet-500' },
}

const FALLBACK_STYLE = { badgeClass: 'bg-gray-100 text-gray-600', dotClass: 'bg-gray-400' }

export const ARTICLE_SOURCE_NAMES = Object.keys(ARTICLE_SOURCE_STYLES)

export function getArticleSourceStyle(source) {
  return ARTICLE_SOURCE_STYLES[source] || FALLBACK_STYLE
}
