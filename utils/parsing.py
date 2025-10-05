import feedparser, requests

def fetch_rss(url: str, company: str):
    feed = feedparser.parse(url)
    out = []
    for e in feed.entries[:12]:
        out.append({
            "company": company,
            "source_url": e.get("link"),
            "source_type": "rss",
            "title": e.get("title",""),
            "raw": (e.get("summary") or e.get("description") or "")[:1500],
            "published_at": e.get("published") or e.get("updated") or ""
        })
    return out

def fetch_github_releases(repo_url: str, company: str):
    parts = repo_url.rstrip("/").split("/")
    if len(parts) < 2: return []
    owner, repo = parts[-2], parts[-1]
    try:
        rel = requests.get(f"https://api.github.com/repos/{owner}/{repo}/releases", timeout=30).json()[:8]
    except Exception:
        rel = []
    out = []
    for r in rel:
        out.append({
            "company": company,
            "source_url": r.get("html_url"),
            "source_type": "github",
            "title": r.get("name") or f"Release {r.get('tag_name')}",
            "raw": (r.get("body") or "")[:1500],
            "published_at": r.get("published_at") or ""
        })
    return out
