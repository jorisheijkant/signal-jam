import os

MAX_EUVSDISINFO_OUTPUT_CHARS = int(os.getenv("MAX_EUVSDISINFO_OUTPUT_CHARS", "1500"))


async def trim_euvsdisinfo_output(input_data, tool_use_id, context):
    tool_name = input_data.get("tool_name", "")
    if not tool_name.startswith("mcp__euvsdisinfo__"):
        return {}

    tool_response = input_data.get("tool_response")
    text = tool_response if isinstance(tool_response, str) else str(tool_response)

    if len(text) <= MAX_EUVSDISINFO_OUTPUT_CHARS:
        return {}

    trimmed = text[:MAX_EUVSDISINFO_OUTPUT_CHARS] + "\n\n[...truncated, article was longer...]"

    return {
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "updatedToolOutput": trimmed,
        }
    }
