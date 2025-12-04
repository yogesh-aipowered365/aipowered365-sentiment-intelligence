
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from functools import lru_cache
from typing import Dict, Any, List

MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment-latest"


@lru_cache(maxsize=1)
def get_sentiment_pipeline():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
    return pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)


def analyze_sentiment(text: str) -> Dict[str, Any]:
    if not text or not str(text).strip():
        return {"label": "NEUTRAL", "score": 0.0, "explanation": "Please enter some text to analyze."}
    pipe = get_sentiment_pipeline()
    r = pipe(str(text))[0]
    label = r["label"].upper()
    score = float(r["score"])
    explanation = (
        "This looks mostly positive. Great choice of words and tone!"
        if label == "POSITIVE" else
        "This sounds negative. The model detects frustration or sadness."
        if label == "NEGATIVE" else
        "The tone seems neutral or balanced."
    )
    return {"label": label, "score": round(score, 4), "explanation": explanation}


def analyze_sentiments_bulk(texts: List[str]) -> List[Dict[str, Any]]:
    """Batch inference: returns a list of dicts for the given list of texts."""
    pipe = get_sentiment_pipeline()
    # Ensure strings and handle blanks
    safe_texts = [str(t) if (t is not None and str(t).strip())
                  else "" for t in texts]
    results = pipe(safe_texts)
    out = []
    for r in results:
        label = r["label"].upper() if isinstance(r, dict) else "NEUTRAL"
        score = float(r.get("score", 0.0)) if isinstance(r, dict) else 0.0
        explanation = (
            "This looks mostly positive. Great choice of words and tone!"
            if label == "POSITIVE" else
            "This sounds negative. The model detects frustration or sadness."
            if label == "NEGATIVE" else
            "The tone seems neutral or balanced."
        )
        out.append({"label": label, "score": round(
            score, 4), "explanation": explanation})
    return out
