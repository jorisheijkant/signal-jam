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
      counts[id] = { ...post.account, totalCount: 0 }
    }
    counts[id].totalCount++
  }

  return Object.values(counts)
    .sort((a, b) => b.totalCount - a.totalCount)
    .slice(0, limit)
}

export function filterUnreviewedThemePosts(query) {
  return query
    .eq('is_relevant', true)
    .eq('relevant_for_signal_jam_theme', true)
    .eq('is_checked', false)
    .neq('post_type', 'repost')
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
