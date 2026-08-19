import json
import random
from pathlib import Path


def pick_rotating_sample(items, sample_size, state_path, state_key):
    if not items:
        return []

    state_path = Path(state_path)
    state = _load_state(state_path)
    queue = [item for item in state.get(state_key, []) if item in items]

    selected = []
    while len(selected) < min(sample_size, len(items)):
        if not queue:
            queue = _shuffled(items)
        candidate = queue.pop(0)
        if candidate not in selected:
            selected.append(candidate)

    state[state_key] = queue
    _save_state(state_path, state)

    return selected


def _shuffled(items):
    shuffled_items = list(items)
    random.shuffle(shuffled_items)
    return shuffled_items


def _load_state(state_path):
    if not state_path.exists():
        return {}
    with open(state_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def _save_state(state_path, state):
    state_path.parent.mkdir(parents=True, exist_ok=True)
    with open(state_path, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
