import os

from functions.llm import get_llm_provider

DEFAULT_OLLAMA_TRANSLATION_MODEL = 'gemma4:latest'


def build_translation_llm():
    """The LLM for translating articles, configured through TRANSLATION_PROVIDER and TRANSLATION_MODEL in .env.

    Returns None when it cannot be set up (for example a missing package), so scraping can go on untranslated."""
    provider_name = os.getenv('TRANSLATION_PROVIDER', 'ollama')
    model = os.getenv('TRANSLATION_MODEL') or (DEFAULT_OLLAMA_TRANSLATION_MODEL if provider_name == 'ollama' else None)
    try:
        llm = get_llm_provider(provider_name, model)
    except Exception as error:
        print(f"[translation disabled] could not set up {provider_name} — {error}")
        return None
    print(f"Translating with {provider_name} ({model})")
    return llm
