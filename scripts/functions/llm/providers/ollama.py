import os
import urllib.request
import json
from ..base import LLMProvider


class OllamaProvider(LLMProvider):
    def __init__(self):
        self.base_url = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
        self.model = os.getenv('OLLAMA_MODEL', 'llama3')

    def complete(self, prompt: str) -> str:
        payload = json.dumps({
            'model': self.model,
            'prompt': prompt,
            'stream': False,
        }).encode('utf-8')

        req = urllib.request.Request(
            f'{self.base_url}/api/generate',
            data=payload,
            headers={'Content-Type': 'application/json'},
        )

        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode('utf-8'))

        return result['response'].strip()
