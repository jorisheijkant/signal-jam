export function createTermQueries(client) {
  async function getTerms(kind) {
    const { data, error } = await client
      .from('scrape_terms')
      .select('*')
      .eq('kind', kind)
      .order('id', { ascending: true })
    return { data, error }
  }

  async function addTerm(fields) {
    const { data, error } = await client
      .from('scrape_terms')
      .insert(fields)
      .select()
      .single()
    return { data, error }
  }

  async function deleteTerm(id) {
    const { error } = await client.from('scrape_terms').delete().eq('id', id)
    return { error }
  }

  return { getTerms, addTerm, deleteTerm }
}
