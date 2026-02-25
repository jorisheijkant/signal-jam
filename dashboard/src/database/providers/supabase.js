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

async function getPosts(limit = 10, offset = 0) {
  const { data, error } = await client
    .from('posts')
    .select('*, account:accounts(*)')
    .order('posted_at', { ascending: false })
    .range(offset, offset + limit - 1)

  return { data, error }
}

async function getCheckedPosts(limit = 10, offset = 0) {
  const { data, error } = await client
    .from('posts')
    .select('*, account:accounts(*)')
    .eq('is_checked', true)
    .order('posted_at', { ascending: false })
    .range(offset, offset + limit - 1)

  return { data, error }
}

async function getMostActiveAccounts(limit = 6) {
  const { data, error } = await client
    .from('posts')
    .select('account_id, account:accounts(id, username, platform, account_url)')

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
    .delete()
    .eq('id', id)

  return { error }
}

export default {
  getPosts,
  getCheckedPosts,
  getPostsPerDay,
  getMostActiveAccounts,
  updatePost,
  deletePost,
}
