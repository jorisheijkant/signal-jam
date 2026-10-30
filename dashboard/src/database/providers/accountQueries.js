const FOREIGN_KEY_VIOLATION = '23503'

function escapeLikePattern(value) {
  return value.replace(/[\\%_]/g, '\\$&')
}

export function createAccountQueries(client) {
  async function getWatchedAccounts() {
    const { data, error } = await client
      .from('accounts')
      .select('*')
      .eq('is_watched', true)
      .order('platform', { ascending: true })
      .order('username', { ascending: true })
    return { data, error }
  }

  async function findAccount(platform, username) {
    const { data, error } = await client
      .from('accounts')
      .select('id')
      .eq('platform', platform)
      .ilike('username', escapeLikePattern(username))
      .maybeSingle()
    return { data, error }
  }

  async function updateAccount(id, fields) {
    const { data, error } = await client
      .from('accounts')
      .update(fields)
      .eq('id', id)
      .select()
      .single()
    return { data, error }
  }

  // The scrapers may already have created the account from its posts, so reuse that row.
  async function addWatchedAccount(fields) {
    const { data: existing, error: findError } = await findAccount(fields.platform, fields.username)
    if (findError) return { data: null, error: findError }
    if (existing) return updateAccount(existing.id, { ...fields, is_watched: true })

    const { data, error } = await client
      .from('accounts')
      .insert({ ...fields, is_watched: true })
      .select()
      .single()
    return { data, error }
  }

  // Accounts with posts cannot be deleted without losing those posts, so they only leave the scrape list.
  async function deleteAccount(id) {
    const { error } = await client.from('accounts').delete().eq('id', id)
    if (error?.code !== FOREIGN_KEY_VIOLATION) return { error, onlyUnwatched: false }

    const { error: unwatchError } = await updateAccount(id, { is_watched: false })
    return { error: unwatchError, onlyUnwatched: !unwatchError }
  }

  return { getWatchedAccounts, addWatchedAccount, updateAccount, deleteAccount }
}
