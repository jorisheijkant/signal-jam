import json
from pathlib import Path


def load_json_file(file_path: Path):
    return json.loads(file_path.read_text(encoding='utf-8'))
