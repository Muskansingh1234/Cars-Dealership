"""Tiny, dependency-free lexicon sentiment analyser (the 'sentiment analysis microservice')."""
import re

POSITIVE = {
    "amazing", "awesome", "best", "brilliant", "clean", "comfortable", "courteous", "easy",
    "enjoyed", "excellent", "fair", "fantastic", "fast", "friendly", "good", "great", "happy",
    "helpful", "honest", "impressed", "love", "loved", "outstanding", "perfect", "pleasant",
    "professional", "quick", "recommend", "recommended", "satisfied", "smooth", "superb",
    "thank", "thanks", "wonderful", "knowledgeable", "transparent", "welcoming",
}
NEGATIVE = {
    "avoid", "awful", "bad", "broken", "delay", "delayed", "disappointed", "disappointing",
    "dirty", "dishonest", "expensive", "frustrating", "hate", "hated", "horrible", "lied",
    "mediocre", "nightmare", "overpriced", "poor", "problem", "problems", "pushy", "rude",
    "scam", "slow", "terrible", "unhelpful", "unprofessional", "useless", "waste", "worst",
}
NEGATORS = {"not", "no", "never", "hardly", "barely", "cannot"}


def analyze(text):
    """Return (label, score). label is 'positive', 'negative' or 'neutral'."""
    tokens = re.findall(r"[a-z']+", (text or "").lower())
    score = 0
    for i, tok in enumerate(tokens):
        value = 1 if tok in POSITIVE else -1 if tok in NEGATIVE else 0
        if not value:
            continue
        window = tokens[max(0, i - 2): i]
        if any(w in NEGATORS or w.endswith("n't") for w in window):
            value = -value
        score += value
    label = "positive" if score > 0 else "negative" if score < 0 else "neutral"
    return label, score
