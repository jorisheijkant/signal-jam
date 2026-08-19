import json
import re
from abc import ABC, abstractmethod

JSON_CODE_FENCE_PATTERN = re.compile(r"^```(?:json)?\s*|\s*```$", re.IGNORECASE | re.MULTILINE)


class LLMProvider(ABC):
    @abstractmethod
    def complete(self, prompt: str) -> str:
        """Send a prompt and return the response text."""
        pass

    def complete_structured(self, prompt: str, schema: dict) -> dict:
        """Send a prompt expecting a JSON response matching schema, return it as a dict.

        Providers with native schema-enforced output should override this. The
        default falls back to asking for JSON in the prompt and stripping any
        markdown code fence the model wraps the response in.
        """
        full_prompt = (
            f"{prompt}\n\n"
            "Respond with a single JSON object only, no other text, matching this schema:\n"
            f"{json.dumps(schema)}"
        )
        response = self.complete(full_prompt)
        cleaned = JSON_CODE_FENCE_PATTERN.sub("", response).strip()
        return json.loads(cleaned)
