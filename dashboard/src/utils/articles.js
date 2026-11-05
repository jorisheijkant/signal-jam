const EXCERPT_LENGTH = 300

export function formatArticleDate(timestamp) {
  return new Date(timestamp).toLocaleDateString('nl-NL', { day: 'numeric', month: 'short', year: 'numeric' })
}

export function isArticleTranslated(article) {
  return Boolean(article.title_en)
}

export function getArticleTitle(article) {
  return article.title_en || article.title
}

function toPlainText(text) {
  return text.replace(/<[^>]*>/g, '').trim()
}

export function getArticleExcerpt(article) {
  // A translated content is only the start of the article, so it always ends on an ellipsis
  if (article.content_en) return `${toPlainText(article.content_en).slice(0, EXCERPT_LENGTH).trimEnd()}…`

  const plainText = toPlainText(article.summary || article.content || '')
  if (plainText.length <= EXCERPT_LENGTH) return plainText
  return `${plainText.slice(0, EXCERPT_LENGTH).trimEnd()}…`
}
