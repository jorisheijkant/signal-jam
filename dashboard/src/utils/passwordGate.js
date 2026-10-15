// Not secure: the password ships with the frontend. It only keeps casual visitors out.
const ARTICLES_PASSWORD = 'kipkyiv'
const UNLOCKED_STORAGE_KEY = 'articlesUnlocked'

export function isArticlesUnlocked() {
  try {
    return localStorage.getItem(UNLOCKED_STORAGE_KEY) === 'true'
  } catch {
    return false
  }
}

export function tryUnlockArticles(enteredPassword) {
  const isCorrect = enteredPassword === ARTICLES_PASSWORD
  if (isCorrect) rememberUnlock()
  return isCorrect
}

function rememberUnlock() {
  try {
    localStorage.setItem(UNLOCKED_STORAGE_KEY, 'true')
  } catch {
    // Storage unavailable: the visitor just has to enter the password again next time
  }
}
