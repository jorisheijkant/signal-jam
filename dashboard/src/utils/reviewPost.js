import { updatePost, deletePost } from '../database'

export const REVIEW_VERDICTS = {
  MISINFORMATION: 'misinformation',
  NOT_MISINFORMATION: 'notMisinformation',
  NOT_RELEVANT: 'notRelevant',
}

export function reviewPost(post, verdict, { frameId, notes }) {
  if (verdict === REVIEW_VERDICTS.NOT_RELEVANT) return deletePost(post.id)

  return updatePost(post.id, {
    is_checked: true,
    contains_misinformation: verdict === REVIEW_VERDICTS.MISINFORMATION,
    frame_id: frameId,
    notes,
  })
}
