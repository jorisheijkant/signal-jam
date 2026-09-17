const LLM_PROVIDER_LABELS = {
  anthropic: 'Anthropic',
  openai: 'OpenAI',
  ollama: 'Ollama',
}

export function formatLlmProviderLabel(provider) {
  if (!provider) return ''
  return LLM_PROVIDER_LABELS[provider] || (provider.charAt(0).toUpperCase() + provider.slice(1))
}
