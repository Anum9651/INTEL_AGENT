import os, requests, streamlit as st

MODEL = "llama-3.1-8b-instant"

def _get_key():
    return (st.secrets.get("GROQ_API_KEY") if hasattr(st, "secrets") else None) or os.getenv("GROQ_API_KEY")

def groq_chat(prompt: str, temperature: float = 0.2) -> str:
    key = _get_key()
    if not key:
        raise RuntimeError("Missing GROQ_API_KEY (set in Streamlit secrets or environment).")
    r = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {key}"},
        json={"model": MODEL, "messages":[{"role":"user","content":prompt}], "temperature":temperature},
        timeout=60,
    )
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"].strip()
