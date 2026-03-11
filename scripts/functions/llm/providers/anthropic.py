import os
from ..base import LLMProvider


class AnthropicProvider(LLMProvider):
    def __init__(self):
        try:
            import anthropic
        except ImportError:
            raise ImportError("anthropic package not installed. Run: pip install anthropic")

        self.client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        self.model = os.getenv('ANTHROPIC_MODEL', 'claude-sonnet-4-6')

    def complete(self, prompt: str) -> str:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[{'role': 'user', 'content': prompt}],
        )
        return response.content[0].text.strip()
