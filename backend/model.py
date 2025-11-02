# Lightweight, explainable mood analysis for a student project.
# No external models; uses simple keyword scoring.
from typing import Literal

POSITIVE_WORDS = {
    "grateful", "hope", "okay", "good", "better", "improve", "calm", "relax", "peace",
    "managed", "coping", "progress", "smile", "joy", "happy"
}
NEGATIVE_WORDS = {
    "sad", "down", "anxious", "panic", "tired", "angry", "hopeless", "worthless",
    "stress", "stressed", "overwhelmed", "depressed", "cry", "alone", "scared", "fear",
    "fail", "failure"
}

def analyze_mood(text: str) -> Literal["positive", "neutral", "negative"]:
    t = text.lower()
    pos = sum(1 for w in POSITIVE_WORDS if w in t)
    neg = sum(1 for w in NEGATIVE_WORDS if w in t)

    if neg > pos and neg > 0:
        return "negative"
    if pos > neg and pos > 0:
        return "positive"
    return "neutral"