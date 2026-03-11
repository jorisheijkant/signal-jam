import { createClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabasePublishableKey = import.meta.env.VITE_SUPABASE_PUBLISHABLE_KEY

const client = createClient(supabaseUrl, supabasePublishableKey)

async function getPostsPerDay(days = 20) {
  const since = new Date()
  since.setDate(since.getDate() - days)

  const { data, error } = await client
    .from('posts')
    .select('posted_at')
    .gte('posted_at', since.toISOString())
    .order('posted_at', { ascending: true })

  if (error) return { data: null, error }

  const counts = {}
  for (const post of data) {
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

  return { data: result, error: null }
}

async function getPosts(limit = 10, offset = 0, startDate = null) {
  let query = client
    .from('posts')
    .select('*, account:accounts(*)')
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
    .select('*, account:accounts(*)')
  if (startDate) query = query.gte('posted_at', startDate)
  const { data, error } = await query
    .eq('is_checked', true)
    .order('posted_at', { ascending: false })
    .range(offset, offset + limit - 1)

  return { data, error }
}

async function getMostActiveAccounts(limit = 6, startDate = null) {
  let query = client
    .from('posts')
    .select('account_id, account:accounts(id, username, platform, account_url)')
  if (startDate) query = query.gte('posted_at', startDate)
  const { data, error } = await query

  if (error) return { data: null, error }

  const counts = {}
  for (const post of data) {
    const id = post.account_id
    if (!counts[id]) {
      counts[id] = { ...post.account, postCount: 0 }
    }
    counts[id].postCount++
  }

  const result = Object.values(counts)
    .sort((a, b) => b.postCount - a.postCount)
    .slice(0, limit)

  return { data: result, error: null }
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
  if (startDate) query = query.gte('posted_at', startDate)
  const { count, error } = await query
    .eq('is_checked', false)
  return { count, error }
}

async function updatePost(id, fields) {
  console.log('[DB] updatePost →', { id, fields })
  const response = await client
    .from('posts')
    .update(fields)
    .eq('id', id)
    .select()

  console.log('[DB] updatePost ←', {
    status: response.status,
    statusText: response.statusText,
    data: response.data,
    error: response.error,
  })

  if (!response.error && (!response.data || response.data.length === 0)) {
    console.warn('[DB] updatePost: no rows updated — check RLS policies or if post id exists:', id)
  }

  return { data: response.data, error: response.error }
}

async function updateSiblingReposts(post, fields) {
  // Determine the root post id: if this post is itself a repost, use its parent;
  // if it's the original, use its own id.
  const rootId = post.parent_post_id ?? post.id

  const { data, error } = await client
    .from('posts')
    .update(fields)
    .eq('parent_post_id', rootId)
    .neq('id', post.id)
    .select('id')

  return { data, error }
}

async function deletePost(id) {
  console.log('[DB] deletePost →', { id })
  const response = await client
    .from('posts')
    .delete()
    .eq('id', id)

  console.log('[DB] deletePost ←', {
    status: response.status,
    statusText: response.statusText,
    error: response.error,
  })

  return { error: response.error }
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

  const { data, error } = await client
    .from('posts')
    .select('frame_id, frame:frames(id, name)')
    .not('frame_id', 'is', null)
    .eq('is_checked', true)
    .gte('posted_at', since.toISOString())

  if (error) return { data: null, error }

  const counts = {}
  for (const post of data) {
    const id = post.frame_id
    if (!counts[id]) {
      counts[id] = { id, name: post.frame.name, count: 0 }
    }
    counts[id].count++
  }

  const result = Object.values(counts).sort((a, b) => b.count - a.count)
  return { data: result, error: null }
}

async function createFrame(name, description = '') {
  const { data, error } = await client
    .from('frames')
    .insert({ name, description })
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

export default {
  getPosts,
  getCheckedPosts,
  getPostsPerDay,
  getMostActiveAccounts,
  getUnlabeledCount,
  getLastScrapedAt,
  updatePost,
  updateSiblingReposts,
  deletePost,
  getSummaries,
  getFrames,
  createFrame,
  deleteFrame,
  getActiveFrames,
}
