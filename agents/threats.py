# agents/threat.py
from __future__ import annotations
from typing import Dict, Any

def score_threat(comp: Dict[str, Any], recent_events: int = 0) -> Dict[str, Any]:
    """
    Heuristic threat: active feeds + recent events bump score.
    1 Low • 2 Moderate • 3 Elevated • 4 High • 5 Critical
    """
    base = 1
    src = comp.get("sources", {})
    richness = len(src.get("rss", [])) + len(src.get("github", [])) + len(src.get("social", []))
    if richness >= 3:
        base += 1
    if "press" in src and src["press"]:
        base += 1
    # Activity factor:
    if recent_events >= 3:
        base += 1
    if recent_events >= 6:
        base += 1

    base = max(1, min(base, 5))
    levels = {1: "Low", 2: "Moderate", 3: "Elevated", 4: "High", 5: "Critical"}
    comp["threat_score"] = base
    comp["threat_level"] = levels[base]
    return comp
