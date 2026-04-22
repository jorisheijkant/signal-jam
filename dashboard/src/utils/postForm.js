export function addFormFields(post) {
  post._form = {
    not_relevant: false,
    is_checked: post.is_checked || false,
    contains_misinformation: post.contains_misinformation || false,
    frame_id: post.frame_id || null,
    notes: post.notes || '',
  }
  post._saving = false
  post._saved = false
  post._error = false
  return post
}
