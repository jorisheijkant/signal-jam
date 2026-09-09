import os

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    HookMatcher,
    ResultMessage,
    ServerToolUseBlock,
    TextBlock,
    ToolUseBlock,
    query,
)
from dotenv import load_dotenv

from .trim_euvsdisinfo_output import trim_euvsdisinfo_output

full_prompt = """You will see a social media post in Dutch. Use the EUvsDisinfo MCP to check whether EUvsDisinfo has done a fact check on this (the site has fact checks in English). Search for specific events and information first, but if that does not give results, feel free to take a bit of a broader view and look for fact checks about the main topic of the post. You can also use the web search tool to find more information on the topic.

Write the "reasoning" field in Dutch, regardless of the language of your sources."""

FACT_CHECK_RESULT_SCHEMA = {
    "type": "object",
    "properties": {
        "likely_disinformation": {
            "type": "boolean",
            "description": "Whether the post is likely disinformation.",
        },
        "reasoning": {
            "type": "string",
            "maxLength": 400,
            "description": "Concise explanation for the verdict, written in Dutch.",
        },
        "sources": {
            "type": "array",
            "minItems": 3,
            "maxItems": 3,
            "items": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "link": {"type": "string"},
                },
                "required": ["title", "link"],
            },
            "description": "Three sources found that support the reasoning.",
        },
    },
    "required": ["likely_disinformation", "reasoning", "sources"],
}

load_dotenv()
EUVSDISINFO_MCP_BASE_URL = os.getenv("EUVSDISINFO_MCP_URL")
EUVSDISINFO_API_KEY = os.getenv("EUVSDISINFO_API_KEY")
# ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

MODEL = "claude-sonnet-5"


async def fact_check_with_claude(claim=""):
    """Fact-check a claim with Claude and return the structured verdict, or None if none was produced."""

    euvsdisinfo_mcp_url = f"{EUVSDISINFO_MCP_BASE_URL}?key={EUVSDISINFO_API_KEY}"

    options = ClaudeAgentOptions(
        model=MODEL,
        system_prompt=full_prompt,
        mcp_servers={
            "euvsdisinfo": {"type": "http", "url": euvsdisinfo_mcp_url}
        },
        allowed_tools=[
            "WebSearch",
            "mcp__euvsdisinfo__search",
            "mcp__euvsdisinfo__articles",
            "mcp__euvsdisinfo__cases",
            "mcp__euvsdisinfo__narratives",
        ],
        disallowed_tools=[
        "Bash", "Read", "Write", "Edit", "Glob", "Grep",
        "NotebookEdit", "WebFetch", "TodoWrite", "Task",
        "BashOutput", "KillShell", "Skill", "SlashCommand",
        "ExitPlanMode",
        ],
        hooks={
            "PostToolUse": [HookMatcher(hooks=[trim_euvsdisinfo_output])],
        },
        max_turns=6,
        output_format={"type": "json_schema", "schema": FACT_CHECK_RESULT_SCHEMA},
    )

    fact_check_result = None

    async for message in query(prompt=f"Fact-check this statement: '{claim}'", options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, (ToolUseBlock, ServerToolUseBlock)):
                    print(f"--> Calling Tool: {block.name} with {block.input}")
                elif isinstance(block, TextBlock):
                    print(block.text, end="", flush=True)
        elif isinstance(message, ResultMessage):
            fact_check_result = message.structured_output
            if message.usage:
                print(f" Usage of tokens: {message.usage}")

    return fact_check_result

