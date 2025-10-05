
POSITIVE_WORDS = {"growth", "beat", "gain", "strong", "up", "positive", "profit"}
NEGATIVE_WORDS = {"loss", "miss", "down", "decline", "negative", "weak", "drop"}

def simple_sentiment(text: str) -> str:
    """Rule-based bull/bear/neutral classifier."""
    text = (text or "").lower()
    pos = sum(w in text for w in POSITIVE_WORDS)
    neg = sum(w in text for w in NEGATIVE_WORDS)
    if pos > neg:
        return "bull"
    elif neg > pos:
        return "bear"
    else:
        return "neutral"

def route_document_rule(title: str, content: str):
    """Route a document to earnings, macro, or news specialist."""
    text = ((title or "") + " " + (content or "")).lower()
    if any(k in text for k in ["eps", "guidance", "revenue", "earnings"]):
        return "earnings", "matched: earnings keyword"
    elif any(k in text for k in ["inflation", "rates", "pmi", "jobless", "cpi"]):
        return "macro", "matched: macro keyword"
    else:
        return "news", "default: general news"
