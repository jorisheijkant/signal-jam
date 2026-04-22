import supabaseDb from './providers/supabase.js'
import postgrestDb from './providers/postgrest.js'

const DB_PROVIDER = import.meta.env.VITE_DB_PROVIDER || 'supabase'

// Posts before this date are excluded from the dashboard and labeling queue
const DASHBOARD_START_DATE = '2026-01-01'

const providers = {
  supabase: supabaseDb,
  postgrest: postgrestDb,
}

const db = providers[DB_PROVIDER]

if (!db) {
  throw new Error(`Unknown database provider: ${DB_PROVIDER}`)
}

export const getPosts = (limit, offset) => db.getPosts(limit, offset, DASHBOARD_START_DATE)
export const getCheckedPosts = (limit, offset) => db.getCheckedPosts(limit, offset, DASHBOARD_START_DATE)
export const getMostActiveAccounts = (limit) => db.getMostActiveAccounts(limit, DASHBOARD_START_DATE)
export const getUnlabeledCount = () => db.getUnlabeledCount(DASHBOARD_START_DATE)
export const getPostCounts = db.getPostCounts
export const getPostsPerDay = db.getPostsPerDay
export const getLastScrapedAt = db.getLastScrapedAt
export const updatePost = db.updatePost
export const updateSiblingReposts = db.updateSiblingReposts
export const deletePost = db.deletePost
export const getSummaries = db.getSummaries
export const getFrames = db.getFrames
export const createFrame = db.createFrame
export const updateFrame = db.updateFrame
export const deleteFrame = db.deleteFrame
export const getActiveFrames = db.getActiveFrames
export const searchPosts = (term, frameId, limit, offset) => db.searchPosts(term, frameId, limit, offset, DASHBOARD_START_DATE)

export default db
