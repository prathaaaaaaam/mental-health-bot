from backend.model import analyze_mood
from backend.safety import is_crisis

def test_analyze_mood():
    assert analyze_mood("I feel sad and stressed") == "negative"
    assert analyze_mood("I feel hopeful and calm") == "positive"
    assert analyze_mood("today was a day") == "neutral"

def test_is_crisis():
    assert is_crisis("I want to kill myself") is True
    assert is_crisis("I'm stressed") is False