export function groupPostsByDay(posts, days) {
  const counts = {}
  for (const post of posts) {
    const day = post.posted_at.slice(0, 10)
    counts[day] = (counts[day] || 0) + 1
  }

  const result = []
  for (let i = days; i >= 0; i--) {
    const d = new Date()
    d.setDate(d.getDate() - i)
    const key = d.toISOString().slice(0, 10)
    result.push({ date: key, count: counts[key] || 0 })
  }

  return result
}

export function groupPostsByAccount(posts, limit) {
  const counts = {}
  for (const post of posts) {
    const id = post.account_id
    if (!counts[id]) {
      counts[id] = { ...post.account, misinfoCount: 0, totalCount: 0 }
    }
    counts[id].totalCount++
    if (post.contains_misinformation) counts[id].misinfoCount++
  }

  return Object.values(counts)
    .sort((a, b) => b.misinfoCount - a.misinfoCount)
    .filter(a => a.misinfoCount > 0)
    .slice(0, limit)
}

export function escapeOrFilterValue(value) {
  return `"${value.replace(/\\/g, '\\\\').replace(/"/g, '\\"')}"`
}

const ARTICLE_TEXT_COLUMNS = ['title', 'summary', 'content']

export function buildArticleTermsFilter(terms) {
  return terms
    .flatMap(term => ARTICLE_TEXT_COLUMNS.map(column => `${column}.ilike.${escapeOrFilterValue(`%${term}%`)}`))
    .join(',')
}
