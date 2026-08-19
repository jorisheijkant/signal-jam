import os
import urllib.request
import json
from ..base import LLMProvider


class OllamaProvider(LLMProvider):
    def __init__(self):
        self.base_url = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
        self.model = os.getenv('OLLAMA_MODEL', 'llama3')

    def complete(self, prompt: str) -> str:
        return self._generate(prompt)['response'].strip()

    def complete_structured(self, prompt: str, schema: dict) -> dict:
        response = self._generate(prompt, format=schema)['response']
        return json.loads(response)

    def _generate(self, prompt: str, format: dict = None) -> dict:
        body = {
            'model': self.model,
            'prompt': prompt,
            'stream': False,
        }
        if format is not None:
            body['format'] = format

        req = urllib.request.Request(
            f'{self.base_url}/api/generate',
            data=json.dumps(body).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
        )

        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode('utf-8'))
