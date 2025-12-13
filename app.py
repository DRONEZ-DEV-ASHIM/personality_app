# app.py
from flask import Flask, render_template, request, redirect, url_for
import re

app = Flask(__name__)

# very simple personality mapping (toy model)
PERSONALITY_KEYWORDS = {
    "creative": [
        "creative", "imaginative", "inventive",
        "innovative", "artistic", "original", "visionary"
    ],

    "analytical": [
        "logical", "analytical", "data", "think",
        "reason", "problem", "calculate", "analysis"
    ],

    "social": [
        "friendly", "social", "outgoing", "people",
        "team", "talkative", "communication", "network"
    ],

    "reserved": [
        "quiet", "introvert", "reserved", "shy",
        "calm", "private", "silent", "withdrawn"
    ],

    "driven": [
        "ambitious", "driven", "goal", "focused",
        "motivated", "determined", "disciplined", "hardworking"
    ],
}

SENTIMENT_DICT = {
    # very positive
    "excellent": 3, "amazing": 3, "fantastic": 3,
    "awesome": 3, "wonderful": 3, "brilliant": 3,

    # positive
    "great": 2, "good": 1, "happy": 2, "confident": 2,
    "motivated": 2, "optimistic": 2, "satisfied": 1,

    # neutral
    "okay": 0, "neutral": 0, "normal": 0, "average": 0,

    # negative
    "bad": -1, "sad": -2, "tired": -1, "confused": -1,
    "stressed": -2, "worried": -2,

    # very negative
    "terrible": -3, "angry": -3, "frustrated": -3,
    "depressed": -3, "hopeless": -3
}


def extract_personality(text: str):
    text = text.lower()
    scores = {k: 0 for k in PERSONALITY_KEYWORDS}
    words = re.findall(r"\w+", text)
    for p, kws in PERSONALITY_KEYWORDS.items():
        for kw in kws:
            for w in words:
                if kw == w or kw in w:
                    scores[p] += 1
    # pick top 2 personality traits (tie-break deterministic)
    sorted_traits = sorted(scores.items(), key=lambda x: (-x[1], x[0]))
    top = [t for t, s in sorted_traits if s > 0][:2]
    return top or ["balanced"]

def sentiment_score(text: str):
    text = text.lower()
    score = 0
    words = re.findall(r"\w+", text)
    for w in words:
        score += SENTIMENT_DICT.get(w, 0)
    return score

def sentiment_label(score: int):
    if score >= 3:
        return "Very Positive"
    if score >= 1:
        return "Positive"
    if score == 0:
        return "Neutral"
    if score <= -3:
        return "Very Negative"
    return "Negative"

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    text = request.form.get("text", "").strip()
    if not text:
        return redirect(url_for("index"))
    traits = extract_personality(text)
    score = sentiment_score(text)
    label = sentiment_label(score)
    return render_template("result.html", text=text, traits=traits, score=score, label=label)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
