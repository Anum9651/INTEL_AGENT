# agents/recommender.py
import random

def generate_recommendation(event, demo_mode=False):
    suggestions = [
        "Highlight this feature gap in next product sprint.",
        "Investigate competitor marketing campaign reach.",
        "Alert sales team to adjust value proposition.",
        "Monitor customer sentiment shift post-launch.",
    ]
    event["so_what"] = random.choice(suggestions)
    return event
