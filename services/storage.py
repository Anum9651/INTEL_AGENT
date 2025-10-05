import json
import os
from typing import List, Dict, Any

STORE_PATH = os.environ.get("INTEL_AGENT_STORE", "intel_data.json")

def _read() -> List[Dict[str, Any]]:
    if not os.path.exists(STORE_PATH):
        return []
    try:
        with open(STORE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except Exception:
        return []

def _write(items: List[Dict[str, Any]]) -> None:
    os.makedirs(os.path.dirname(STORE_PATH) or ".", exist_ok=True)
    with open(STORE_PATH, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

def get_events() -> List[Dict[str, Any]]:
    return _read()

def set_events(items: List[Dict[str, Any]]) -> None:
    """
    Overwrite the store with the provided list, after de-duping by (title, source_url).
    Callers should pass existing + new when they want to append.
    """
    seen = set()
    deduped: List[Dict[str, Any]] = []
    for e in items:
        key = (e.get("title", ""), e.get("source_url", ""))
        if key in seen:
            continue
        seen.add(key)
        deduped.append(e)
    _write(deduped)

def clear_events() -> None:
    _write([])
