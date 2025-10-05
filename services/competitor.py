# services/competitors.py
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Any

# Lightweight “directory” for demo & bootstrapping.
# You can extend with your industries, or swap with Crunchbase/SerpAPI later.
INDUSTRY_MAP: Dict[str, List[Dict[str, Any]]] = {
    "CRM": [
        {
            "name": "Salesforce",
            "homepage": "https://www.salesforce.com",
            "rss": [
                "https://www.salesforce.com/news/feed/",
            ],
            "github": [],
            "press": ["Salesforce press"],
            "social": ["https://twitter.com/salesforce"],
            "notes": "Enterprise CRM leader; frequent feature releases, acquisitions."
        },
        {
            "name": "HubSpot",
            "homepage": "https://www.hubspot.com",
            "rss": [
                "https://www.hubspot.com/feed",
                "https://productupdates.hubspot.com/rss"
            ],
            "github": [],
            "press": ["HubSpot press"],
            "social": ["https://twitter.com/HubSpot"],
            "notes": "Strong SMB penetration; fast marketing/automation cadence."
        },
        {
            "name": "Zoho CRM",
            "homepage": "https://www.zoho.com/crm/",
            "rss": [
                "https://blogs.zoho.com/feed"
            ],
            "github": [],
            "press": ["Zoho press"],
            "social": ["https://twitter.com/zoho"],
            "notes": "Broad suite; price-competitive with frequent incremental updates."
        },
    ],
    "DevTools": [
        {
            "name": "Vercel",
            "homepage": "https://vercel.com",
            "rss": ["https://vercel.com/changelog/rss.xml"],
            "github": ["https://github.com/vercel/vercel/releases"],
            "press": ["Vercel press"],
            "social": ["https://twitter.com/vercel"],
            "notes": "CI/CD + hosting + DX; frequent framework/runtime releases."
        },
        {
            "name": "Netlify",
            "homepage": "https://www.netlify.com",
            "rss": ["https://www.netlify.com/blog/index.xml"],
            "github": ["https://github.com/netlify"],
            "press": ["Netlify press"],
            "social": ["https://twitter.com/netlify"],
            "notes": "Jamstack originator; strong ecosystem & integrations."
        }
    ]
}

@dataclass
class Competitor:
    name: str
    homepage: str
    rss: List[str] = field(default_factory=list)
    github: List[str] = field(default_factory=list)
    press: List[str] = field(default_factory=list)
    social: List[str] = field(default_factory=list)
    notes: str = ""

def discover_competitors(industry: str) -> List[Competitor]:
    items = INDUSTRY_MAP.get(industry.strip(), [])
    return [Competitor(**i) for i in items]
