def split_text_into_chunks(text: str, max_chunk_length: int) -> list[str]:
    """Split text on line breaks into chunks of at most max_chunk_length characters.

    A single line longer than the limit becomes its own chunk, it is never cut in half."""
    chunks = []
    current_lines = []
    current_length = 0

    for line in text.split('\n'):
        if current_lines and current_length + len(line) > max_chunk_length:
            chunks.append('\n'.join(current_lines))
            current_lines = []
            current_length = 0
        current_lines.append(line)
        current_length += len(line) + 1

    chunks.append('\n'.join(current_lines))
    return chunks
