const EXCERPT_LENGTH = 300

export function formatArticleDate(timestamp) {
  return new Date(timestamp).toLocaleDateString('nl-NL', { day: 'numeric', month: 'short', year: 'numeric' })
}

export function getArticleExcerpt(article) {
  const text = article.summary || article.content || ''
  const plainText = text.replace(/<[^>]*>/g, '').trim()
  if (plainText.length <= EXCERPT_LENGTH) return plainText
  return `${plainText.slice(0, EXCERPT_LENGTH).trimEnd()}…`
}
