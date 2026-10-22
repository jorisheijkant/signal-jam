from .base import LLMProvider
from .providers.openai import OpenAIProvider
from .providers.anthropic import AnthropicProvider
from .providers.ollama import OllamaProvider
from .providers.claude_code import ClaudeCodeProvider
from .detect_language_with_llm import detect_language_with_llm, LanguageDetection

PROVIDERS = {
    'openai': OpenAIProvider,
    'anthropic': AnthropicProvider,
    'ollama': OllamaProvider,
    'claude_code': ClaudeCodeProvider,
}

def get_llm_provider(name: str) -> LLMProvider:
    if name not in PROVIDERS:
        raise ValueError(f"Unknown LLM provider '{name}'. Available: {list(PROVIDERS.keys())}")
    return PROVIDERS[name]()
