from dataclasses import dataclass
from typing import Optional

from .base import LLMProvider

LANGUAGE_DETECTION_PROMPT = (
    "Identify the primary language of the following social media post. "
    "Note if it contains multiple languages or heavy slang/emoji use.\n\n"
    "Post text:\n\"{post_text}\""
)

LANGUAGE_DETECTION_SCHEMA = {
    "type": "object",
    "properties": {
        "language_name": {"type": "string", "description": "The full language name"},
        "iso_639_1": {"type": "string", "description": "Two-letter ISO 639-1 code, e.g. 'en', 'es', 'fr', 'ja'"},
        "confidence": {"type": "number", "description": "Score between 0.0 and 1.0"},
        "is_multilingual": {"type": "boolean"},
        "notes": {"type": ["string", "null"]},
    },
    "required": ["language_name", "iso_639_1", "confidence", "is_multilingual"],
}


@dataclass
class LanguageDetection:
    language_name: str
    iso_639_1: str
    confidence: float
    is_multilingual: bool
    notes: Optional[str] = None


def detect_language_with_llm(llm: LLMProvider, post_text: str) -> LanguageDetection:
    prompt = LANGUAGE_DETECTION_PROMPT.format(post_text=post_text)
    data = llm.complete_structured(prompt, LANGUAGE_DETECTION_SCHEMA)
    return LanguageDetection(**data)
