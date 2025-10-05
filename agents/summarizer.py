# agents/summarizer.py
def summarize_event(event):
    text = event.get("raw", "")
    event["summary"] = (
        text[:200] + "..." if len(text) > 200 else text
    )
    return event
