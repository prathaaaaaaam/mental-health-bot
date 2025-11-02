from datetime import datetime

CRISIS_RESOURCES = [
    "If you are in immediate danger, please contact local emergency services now.",
    "India: Aasra 24x7 Helpline: 91-22-27546669",
    "Global directory (IFRC): https://www.ifrc.org/national-societies-directory"
]

def crisis_reply() -> str:
    msg = (
        "I'm really sorry you're going through this. Your life matters and you deserve support. "
        "I can't provide emergency help, but here are immediate options:\n- "
        + "\n- ".join(CRISIS_RESOURCES) +
        "\nIf you can, consider reaching a trusted person nearby right now."
    )
    return msg

TEMPLATES = {
    "positive": [
        "I'm glad you shared that. It sounds like there are small wins in your day. "
        "Would you like a short exercise (e.g., 4-7-8 breathing or a quick gratitude note)?",
    ],
    "neutral": [
        "Thanks for opening up. I'm here with you. "
        "Would grounding help? Try '5-4-3-2-1' (name 5 things you see, 4 feel, 3 hear, 2 smell, 1 taste)."
    ],
    "negative": [
        "That sounds heavy, and it’s understandable to feel this way. "
        "We can try a tiny step: write one worry on paper, then list one action that reduces it by 1%. "
        "I'm listening if you want to share more."
    ]
}

DISCLAIMER = (
    "\n\nNote: I'm not a substitute for professional care. If you feel unsafe, please contact local help."
)

def empathetic_reply(mood: str, user_text: str) -> str:
    choices = TEMPLATES.get(mood, TEMPLATES["neutral"])
    # Simple variation: pick by current minute to avoid extra deps
    idx = datetime.utcnow().minute % len(choices)
    return choices[idx] + DISCLAIMER