# agents/discover.py
from __future__ import annotations
from typing import List, Dict, Any
from services.competitors import discover_competitors, Competitor

def discover(company: str, industry: str) -> List[Dict[str, Any]]:
    """Return normalized competitor list for the chosen industry."""
    comps: List[Competitor] = discover_competitors(industry)
    payload: List[Dict[str, Any]] = []
    for c in comps:
        payload.append({
            "company": company,
            "competitor": c.name,
            "industry": industry,
            "sources": {
                "homepage": c.homepage,
                "rss": c.rss,
                "github": c.github,
                "press": c.press,
                "social": c.social,
            },
            "notes": c.notes,
            # baseline threat until we compute:
            "threat_score": 2,       # 1..5
            "threat_level": "Moderate",
        })
    return payload
