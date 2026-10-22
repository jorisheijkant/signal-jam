import asyncio
import os
from ..base import LLMProvider


class ClaudeCodeProvider(LLMProvider):
    """Runs prompts through the local Claude Code CLI, so they use the logged-in subscription."""

    def __init__(self):
        try:
            import claude_agent_sdk
        except ImportError:
            raise ImportError("claude-agent-sdk package not installed. Run: pip install claude-agent-sdk")

        self.sdk = claude_agent_sdk
        self.model = os.getenv('CLAUDE_CODE_MODEL')

    def complete(self, prompt: str) -> str:
        return asyncio.run(self._query(prompt)).strip()

    async def _query(self, prompt: str) -> str:
        options = self.sdk.ClaudeAgentOptions(
            model=self.model,
            allowed_tools=[],
            max_turns=1,
        )
        result_text = ''
        async for message in self.sdk.query(prompt=prompt, options=options):
            if isinstance(message, self.sdk.ResultMessage):
                result_text = message.result or ''
        return result_text
