# Crisis detection with simple keyword rules.
CRISIS_KEYWORDS = {
    "suicide", "kill myself", "end it all", "hurt myself", "self harm", "self-harm",
    "cannot go on", "die", "no reason to live", "jump", "poison", "cut myself"
}

def is_crisis(text: str) -> bool:
    t = text.lower()
    return any(k in t for k in CRISIS_KEYWORDS)