# agents/classifier.py
import random

def classify_event(event, demo_mode: bool = False):
    if demo_mode:
        event["impact"] = random.randint(2, 5)
        event["confidence"] = random.randint(60, 95)
    else:
        event["impact"] = 3
        event["confidence"] = 80
    return event
