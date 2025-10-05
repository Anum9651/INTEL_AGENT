# agents/fetcher.py
import datetime as dt

def fetch_sources(company: str, rss_url: str = "", gh_repo: str = "", demo_mode: bool = False):
    now_iso = dt.datetime.utcnow().isoformat() + "Z"
    if demo_mode:
        return [
            {"title": "HubSpot launches predictive AI engine", "source_type": "rss", "source_url": rss_url,
             "competitor": "HubSpot", "raw": "HubSpot introduces new AI model for lead scoring.", "published_at": now_iso},
            {"title": "Salesforce expands GPT integration", "source_type": "github", "source_url": gh_repo,
             "competitor": "Salesforce", "raw": "Commit: added EinsteinGPT 2.0 prototype.", "published_at": now_iso},
        ]
    return []
