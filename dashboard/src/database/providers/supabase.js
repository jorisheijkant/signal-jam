import { createClient } from '@supabase/supabase-js'
import { groupPostsByDay, groupPostsByAccount, buildArticleTermsFilter } from '../utils.js'
import { fetchAllRows } from './fetchAllRows.js'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabasePublishableKey = import.meta.env.VITE_SUPABASE_PUBLISHABLE_KEY

const client = createClient(supabaseUrl, supabasePublishableKey)

async function getPostsPerDay(days = 20) {
  const since = new Date()
  since.setDate(since.getDate() - days)

  const buildQuery = () => client
    .from('posts')
    .select('posted_at')
    .eq('is_relevant', true)
    .gte('posted_at', since.toISOString())
    .order('posted_at', { ascending: true })

  const { data, error } = await fetchAllRows(buildQuery)
  if (error) return { data: null, error }
  return { data: groupPostsByDay(data, days), error: null }
}

async function getPosts(limit = 10, offset = 0, startDate = null) {
  let query = client
    .from('posts')
    .select('*, account:accounts(*), ai_fact_checks(likely_disinformation, reasoning, provider, checked_at, ai_fact_check_sources(title, link)), reposted_by:post_reposts(reposted_at, account:accounts(id, username, display_name, account_url))')
    .eq('is_relevant', true)
  if (startDate) query = query.gte('posted_at', startDate)
  const { data, error } = await query
    .order('is_checked', { ascending: true })
    .order('posted_at', { ascending: false })
    .range(offset, offset + limit - 1)

  return { data, error }
}

async function getCheckedPosts(limit = 10, offset = 0, startDate = null) {
  let query = client
    .from('posts')
    .select('*, account:accounts(*), reposted_by:post_reposts(reposted_at, account:accounts(id, username, display_name, account_url))')
    .eq('is_relevant', true)
  if (startDate) query = query.gte('posted_at', startDate)
  const { data, error } = await query
    .eq('is_checked', true)
    .order('posted_at', { ascending: false })
    .range(offset, offset + limit - 1)

  return { data, error }
}

async function getMostActiveAccounts(limit = 6, startDate = null) {
  const buildQuery = () => {
    let query = client
      .from('posts')
      .select('account_id, contains_misinformation, account:accounts(id, username, platform, account_url)')
      .eq('is_relevant', true)
    if (startDate) query = query.gte('posted_at', startDate)
    return query
  }

  const { data, error } = await fetchAllRows(buildQuery)
  if (error) return { data: null, error }
  return { data: groupPostsByAccount(data, limit), error: null }
}

async function getPostCounts() {
  const [{ count: total, error: e1 }, { count: misinfo, error: e2 }] = await Promise.all([
    client.from('posts').select('*', { count: 'exact', head: true }).eq('is_relevant', true),
    client.from('posts').select('*', { count: 'exact', head: true }).eq('is_relevant', true).eq('contains_misinformation', true),
  ])
  return { total, misinfo, error: e1 || e2 }
}

async function getLastScrapedAt() {
  const { data, error } = await client
    .from('posts')
    .select('scraped_at')
    .order('scraped_at', { ascending: false })
    .limit(1)
    .single()
  return { data, error }
}

async function getUnlabeledCount(startDate = null) {
  let query = client
    .from('posts')
    .select('*', { count: 'exact', head: true })
    .eq('is_relevant', true)
  if (startDate) query = query.gte('posted_at', startDate)
  const { count, error } = await query.eq('is_checked', false)
  return { count, error }
}

async function updatePost(id, fields) {
  const { data, error } = await client
    .from('posts')
    .update(fields)
    .eq('id', id)
    .select()
  return { data, error }
}

async function deletePost(id) {
  const { error } = await client
    .from('posts')
    .update({ is_relevant: false, is_checked: true })
    .eq('id', id)
  return { error }
}

async function getSummaries() {
  const { data, error } = await client
    .from('summaries')
    .select('*')
    .order('week_start', { ascending: false })
  return { data, error }
}

async function getFrames() {
  const { data, error } = await client
    .from('frames')
    .select('*')
    .order('name', { ascending: true })
  return { data, error }
}

async function getActiveFrames(days = 30) {
  const since = new Date()
  since.setDate(since.getDate() - days)

  const buildQuery = () => client
    .from('posts')
    .select('frame_id, frame:frames(id, name, description)')
    .not('frame_id', 'is', null)
    .eq('is_relevant', true)
    .eq('is_checked', true)
    .gte('posted_at', since.toISOString())

  const { data, error } = await fetchAllRows(buildQuery)
  if (error) return { data: null, error }

  const counts = {}
  for (const post of data) {
    const id = post.frame_id
    if (!counts[id]) counts[id] = { id, name: post.frame.name, description: post.frame.description, count: 0 }
    counts[id].count++
  }

  return { data: Object.values(counts).sort((a, b) => b.count - a.count), error: null }
}

async function createFrame(name, description = '') {
  const { data, error } = await client
    .from('frames')
    .insert({ name, description })
    .select()
    .single()
  return { data, error }
}

async function updateFrame(id, fields) {
  const { data, error } = await client
    .from('frames')
    .update(fields)
    .eq('id', id)
    .select()
    .single()
  return { data, error }
}

async function deleteFrame(id) {
  const { error } = await client
    .from('frames')
    .delete()
    .eq('id', id)
  return { error }
}

function escapeOrFilterValue(value) {
  return `"${value.replace(/\\/g, '\\\\').replace(/"/g, '\\"')}"`
}

async function getAccountIdsMatchingUsername(term) {
  const { data, error } = await client
    .from('accounts')
    .select('id')
    .ilike('username', `%${term}%`)
  if (error || !data) return []
  return data.map(account => account.id)
}

async function getPostIdsRepostedByAccounts(accountIds) {
  if (accountIds.length === 0) return []
  const { data, error } = await client
    .from('post_reposts')
    .select('post_id')
    .in('account_id', accountIds)
  if (error || !data) return []
  return [...new Set(data.map(row => row.post_id))]
}

async function buildTermFilter(term) {
  const orFilters = [`content.ilike.${escapeOrFilterValue(`%${term}%`)}`]

  const matchingAccountIds = await getAccountIdsMatchingUsername(term)
  if (matchingAccountIds.length === 0) return orFilters.join(',')

  orFilters.push(`account_id.in.(${matchingAccountIds.join(',')})`)

  const repostedPostIds = await getPostIdsRepostedByAccounts(matchingAccountIds)
  if (repostedPostIds.length > 0) {
    orFilters.push(`id.in.(${repostedPostIds.join(',')})`)
  }

  return orFilters.join(',')
}

async function searchPosts({ term, frameId, platform, startDate, endDate, containsMisinformation, isChecked }, limit = 20, offset = 0) {
  let query = client
    .from('posts')
    .select('*, account:accounts(*), frame:frames(id, name), reposted_by:post_reposts(reposted_at, account:accounts(id, username, display_name, account_url))')
    .eq('is_relevant', true)

  if (term) query = query.or(await buildTermFilter(term))
  if (frameId) query = query.eq('frame_id', frameId)
  if (platform) query = query.eq('platform', platform)
  if (containsMisinformation) query = query.eq('contains_misinformation', true)
  if (isChecked) query = query.eq('is_checked', true)
  if (startDate) query = query.gte('posted_at', startDate)
  if (endDate) query = query.lte('posted_at', `${endDate}T23:59:59`)

  const { data, error, count } = await query
    .order('posted_at', { ascending: false })
    .range(offset, offset + limit - 1)

  return { data, error, count }
}

async function searchArticles({ term, relatedTerms, startDate, endDate }, limit = 20, offset = 0) {
  let query = client
    .from('articles')
    .select('url, title, source, language, summary, content, published_at')

  if (term) query = query.or(buildArticleTermsFilter([term]))
  if (relatedTerms) query = query.or(buildArticleTermsFilter(relatedTerms))
  if (startDate) query = query.gte('published_at', startDate)
  if (endDate) query = query.lte('published_at', `${endDate}T23:59:59`)

  const { data, error } = await query
    .order('published_at', { ascending: false })
    .range(offset, offset + limit - 1)

  return { data, error }
}

export default {
  getPostCounts,
  getPosts,
  getCheckedPosts,
  getPostsPerDay,
  getMostActiveAccounts,
  getUnlabeledCount,
  getLastScrapedAt,
  updatePost,
  deletePost,
  getSummaries,
  getFrames,
  createFrame,
  updateFrame,
  deleteFrame,
  getActiveFrames,
  searchPosts,
  searchArticles,
}
