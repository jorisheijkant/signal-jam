const PAGE_SIZE = 1000

// PostgREST caps unbounded selects at PAGE_SIZE rows, so any query whose result
// can grow past that needs to be paged through explicitly or it silently truncates.
export async function fetchAllRows(buildQuery) {
  const rows = []
  let offset = 0

  while (true) {
    const { data, error } = await buildQuery().range(offset, offset + PAGE_SIZE - 1)
    if (error) return { data: null, error }

    rows.push(...data)
    if (data.length < PAGE_SIZE) break
    offset += PAGE_SIZE
  }

  return { data: rows, error: null }
}
