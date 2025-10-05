# services/ai.py
from typing import List, Dict, Any, Optional
import os

try:
    import streamlit as st  # type: ignore
except Exception:
    st = None  # type: ignore


def _get_secret(name: str) -> Optional[str]:
    val = None
    try:
        if st is not None and hasattr(st, "secrets"):
            val = st.secrets.get(name)  # type: ignore[attr-defined]
    except Exception:
        val = None
    return val or os.getenv(name)


def _use_groq():
    """
    Return a 'client' with .chat.completions.create(...), or (None, reason).
    Honors:
      - GROQ_API_KEY (required)
      - GROQ_MODEL (optional, defaults to a safe list with retry)
      - FORCE_LOCAL_AI=true  -> disable Groq entirely
    """
    if (_get_secret("FORCE_LOCAL_AI") or "").strip().lower() in ("1", "true", "yes"):
        return None, "Forced local mode"

    key = _get_secret("GROQ_API_KEY")
    if not key:
        return None, "Missing GROQ_API_KEY"

    # First try official SDK; if missing, use tiny HTTP shim.
    try:
        from groq import Groq  # type: ignore
        return Groq(api_key=key), None
    except Exception:
        pass

    # HTTP shim (no groq package needed)
    try:
        import requests  # noqa: F401
    except Exception as http_err:
        return None, f"requests not installed: {http_err}"

    class _GroqHTTPClient:
        def __init__(self, api_key: str):
            self.api_key = api_key

        class _Chat:
            def __init__(self, outer: "._GroqHTTPClient"):
                self.outer = outer

            class _Completions:
                def __init__(self, outer_chat: "._GroqHTTPClient._Chat"):
                    self.outer_chat = outer_chat

                def create(self, model: str, messages: list, temperature: float = 0.2):
                    import requests
                    url = "https://api.groq.com/openai/v1/chat/completions"
                    headers = {
                        "Authorization": f"Bearer {self.outer_chat.outer.api_key}",
                        "Content-Type": "application/json",
                    }
                    payload = {
                        "model": model,
                        "messages": messages,
                        "temperature": temperature,
                    }
                    resp = requests.post(url, headers=headers, json=payload, timeout=30)
                    resp.raise_for_status()
                    data = resp.json()

                    class _Msg:
                        def __init__(self, content: str):
                            self.content = content

                    class _Choice:
                        def __init__(self, content: str):
                            self.message = _Msg(content)

                    class _Resp:
                        def __init__(self, content: str):
                            self.choices = [_Choice(content)]

                    return _Resp(data["choices"][0]["message"]["content"])

            @property
            def completions(self):
                return _GroqHTTPClient._Chat._Completions(self)

        @property
        def chat(self):
            return _GroqHTTPClient._Chat(self)

    return _GroqHTTPClient(key), None


def _groq_chat(client, messages: list[str | Dict[str, str]]) -> str:
    """
    Try one or more models. You can change default via env/secret:
      GROQ_MODEL="llama3-8b-8192"
    Fallback order is conservative for reliability.
    """
    preferred = _get_secret("GROQ_MODEL") or "llama3-8b-8192"
    candidates = [preferred, "llama3-70b-8192"]

    last_err = None
    for model in candidates:
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.2,
            )
            return resp.choices[0].message.content.strip()
        except Exception as e:
            last_err = e
    raise RuntimeError(str(last_err) if last_err else "Unknown Groq error")


def _top_competitors(events: List[Dict[str, Any]], n: int = 3) -> list[str]:
    from collections import Counter
    cnt = Counter([e.get("competitor", "Unknown") for e in events])
    return [name for name, _ in cnt.most_common(n)]


def generate_digest(company: str, industry: str, events: List[Dict[str, Any]], demo_mode: bool) -> Dict[str, Any]:
    client, err = _use_groq()

    # Normalize facts
    bullet_facts = [
        f"- {e.get('competitor','?')}: {e.get('title','(no title)')} (impact {e.get('impact',3)})"
        for e in events[:80]
    ]
    prompt = (
        f"You are a competitive intelligence analyst for {company} in {industry}.\n"
        f"Write a tight 120-160 word executive summary, 3 key threats, 3 opportunities, "
        f"and 5 recommended actions based strictly on these signals:\n"
        f"{chr(10).join(bullet_facts)}\n"
        "Format as plain text without markdown tables."
    )

    if client:
        try:
            text = _groq_chat(client, [{"role": "user", "content": prompt}])
            return {
                "summary": text,
                "threats": [{"title": "See summary", "severity": "High", "description": "See executive summary"}],
                "opportunities": [{"title": "See summary", "description": "See executive summary"}],
                "actions": [l for l in text.split("\n") if l.strip().startswith(("1","2","3","4","5"))][:5],
            }
        except Exception:
            # swallow and go local
            err = "Remote AI disabled"

    # Local heuristic (quiet, clean output for demo)
    top = _top_competitors(events, 3)
    total = len(events)
    return {
        "summary": (
            f"{company} in {industry}: {total} signals captured."
            + (f" Most active: {', '.join(top)}." if top else "")
        ),
        "threats": [
            {"title": "Feature parity closing", "severity": "High",
             "category": "Product", "competitor": (top[0] if top else "Unknown"),
             "description": "Rapid ship cadence suggests parity risk.", "impact": "Loss of differentiation."}
        ],
        "opportunities": [
            {"title": "Own the AI narrative", "timeframe": "Q1–Q2", "effort": "Medium",
             "description": "Bundle ML/automation into a named initiative.",
             "rationale": "Competitors announce AI often; consistent messaging can win attention."}
        ],
        "actions": [
            "Ship a monthly ‘What’s new’ post + RSS.",
            "Diff competitors’ release notes for alerts.",
            "Brief sales on top 3 talking points.",
            "Publish two teardown posts this quarter.",
            "Test pricing/packaging on top plan.",
        ],
    }


def chat_query(prompt: str, company: str, industry: str,
               events: List[Dict[str, Any]], demo_mode: bool) -> str:
    client, err = _use_groq()
    context = "\n".join(
        f"- {e.get('competitor','?')}: {e.get('title','(no title)')} (impact {e.get('impact',3)})"
        for e in events[:80]
    )

    if client:
        try:
            return _groq_chat(
                client,
                [
                    {"role": "system", "content": f"You help {company} in {industry} with competitive intelligence."},
                    {"role": "user", "content": f"{prompt}\n\nContext:\n{context}"},
                ],
            )
        except Exception:
            pass  # clean fallback below

    # Clean local fallback (no scary error preface)
    highs = [e for e in events if e.get("impact", 0) >= 4] or events[:3]
    lines = [f"• {e.get('title','(no title)')} — {e.get('competitor','?')} (impact {e.get('impact',3)})"
             for e in highs[:5]]
    guidance = [
        "Track release notes/RSS weekly for these competitors.",
        "Compare feature gaps and pricing.",
        "Prepare counter-messaging if any threatens your core ICP.",
    ]
    return "Here are the top signals I’m considering:\n" + "  \n".join(lines) + \
           "\n\nSuggested next steps:\n" + "\n".join([f"{i+1}. {g}" for i, g in enumerate(guidance)])
