import os
try:
    import streamlit as st  # type: ignore
except Exception:
    st = None  # type: ignore

def get_groq_key() -> str | None:
    key = None
    try:
        if st is not None:
            key = (st.secrets.get("GROQ_API_KEY")  # type: ignore[attr-defined]
                   if hasattr(st, "secrets") else None)
    except Exception:
        key = None
    return key or os.getenv("GROQ_API_KEY")

def has_groq_key() -> bool:
    return bool(get_groq_key())
