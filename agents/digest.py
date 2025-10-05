# agents/digest.py
def build_digest(events):
    top = sorted(events, key=lambda e: e.get("impact", 0), reverse=True)[:5]
    lines = [f"• {e.get('title','')} — impact {e.get('impact','?')}/5" for e in top]
    return "INTEL-AGENT Executive Digest\n\n" + "\n".join(lines)
