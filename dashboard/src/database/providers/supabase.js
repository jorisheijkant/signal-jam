import { createClient } from '@supabase/supabase-js'
import { groupPostsByDay, groupPostsByAccount } from '../utils.js'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabasePublishableKey = import.meta.env.VITE_SUPABASE_PUBLISHABLE_KEY

const client = createClient(supabaseUrl, supabasePublishableKey)

async function getPostsPerDay(days = 20) {
  const since = new Date()
  since.setDate(since.getDate() - days)

  const { data, error } = await client
    .from('posts')
    .select('posted_at')
    .eq('is_relevant', true)
    .gte('posted_at', since.toISOString())
    .order('posted_at', { ascending: true })

  if (error) return { data: null, error }
  return { data: groupPostsByDay(data, days), error: null }
}

async function getPosts(limit = 10, offset = 0, startDate = null) {
  let query = client
    .from('posts')
    .select('*, account:accounts(*)')
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
    .select('*, account:accounts(*)')
    .eq('is_relevant', true)
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
    .select('account_id, contains_misinformation, account:accounts(id, username, platform, account_url)')
    .eq('is_relevant', true)
  if (startDate) query = query.gte('posted_at', startDate)
  const { data, error } = await query

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

async function updateSiblingReposts(post, fields) {
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

  const { data, error } = await client
    .from('posts')
    .select('frame_id, frame:frames(id, name)')
    .not('frame_id', 'is', null)
    .eq('is_relevant', true)
    .eq('is_checked', true)
    .gte('posted_at', since.toISOString())

  if (error) return { data: null, error }

  const counts = {}
  for (const post of data) {
    const id = post.frame_id
    if (!counts[id]) counts[id] = { id, name: post.frame.name, count: 0 }
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

async function searchPosts(term, frameId, limit = 20, offset = 0, startDate = null) {
  let query = client
    .from('posts')
    .select('*, account:accounts(*), frame:frames(id, name)')
    .eq('is_relevant', true)

  if (term) query = query.ilike('content', `%${term}%`)
  if (frameId) query = query.eq('frame_id', frameId)
  if (startDate) query = query.gte('posted_at', startDate)

  const { data, error, count } = await query
    .order('posted_at', { ascending: false })
    .range(offset, offset + limit - 1)

  return { data, error, count }
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
  updateSiblingReposts,
  deletePost,
  getSummaries,
  getFrames,
  createFrame,
  updateFrame,
  deleteFrame,
  getActiveFrames,
  searchPosts,
}
