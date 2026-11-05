from pathlib import Path

from functions.utils.split_text_into_chunks import split_text_into_chunks
from .base import LLMProvider

PROMPT_PATH = Path(__file__).parents[2] / 'prompts' / 'translate_to_english.txt'
MAX_CHUNK_LENGTH = 3000


def translate_to_english(llm: LLMProvider, text: str) -> str:
    """Translate text into English. Long texts are translated in chunks so they fit a small local model."""
    prompt_template = PROMPT_PATH.read_text(encoding='utf-8')
    chunks = split_text_into_chunks(text, MAX_CHUNK_LENGTH)
    translated_chunks = [llm.complete(prompt_template.format(text=chunk)) for chunk in chunks]
    return '\n'.join(translated_chunks)
