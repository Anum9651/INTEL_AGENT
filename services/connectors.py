# services/connectors.py
from __future__ import annotations
from typing import List, Dict, Any
import datetime as dt

# Keep it minimal: RSS via feedparser is the safest universal source
# Add to requirements.txt: feedparser
import feedparser

def fetch_rss_feed(url: str, limit: int = 8) -> List[Dict[str, Any]]:
    d = feedparser.parse(url)
    items: List[Dict[str, Any]] = []
    for e in d.entries[:limit]:
        items.append({
            "title": e.get("title", "(no title)"),
            "summary": e.get("summary", "")[:500],
            "link": e.get("link"),
            "published": str(e.get("published", "")),
            "source_type": "rss",
        })
    return items

def gather_sources(sources: Dict[str, Any], demo_mode: bool = False) -> List[Dict[str, Any]]:
    """
    Aggregate recent items from the competitor's sources.
    For now: RSS support (works everywhere). You can extend with
    GitHub releases, Product Hunt, NewsAPI, etc.
    """
    results: List[Dict[str, Any]] = []
    if demo_mode:
        # seed a couple of fake-but-realistic entries
        now = dt.datetime.utcnow().isoformat()
        results.extend([
            {
                "title": "Launch: Workflow Automation v2",
                "summary": "New automation builder with conditional branches and webhook steps.",
                "link": sources.get("homepage"),
                "published": now,
                "source_type": "press",
            },
            {
                "title": "Pricing Update",
                "summary": "Introduced startup plan with usage-based billing and fair overages.",
                "link": sources.get("homepage"),
                "published": now,
                "source_type": "site",
            },
        ])
        return results

    # Real RSS pulls
    for u in sources.get("rss", []):
        try:
            results.extend(fetch_rss_feed(u))
        except Exception:
            pass

    # (Optional) GitHub & others can be added here when you wire keys
    return results
