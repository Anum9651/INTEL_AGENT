# services/scores.py
from __future__ import annotations
from typing import Dict, Any, List

def summarize_activity(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Simple counters by source type."""
    by_type = {}
    for e in events:
        t = e.get("source_type", "other")
        by_type[t] = by_type.get(t, 0) + 1
    total = len(events)
    return {"total": total, "by_type": by_type}
