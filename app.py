from flask import Flask, render_template, request, redirect, url_for
import re

app = Flask(__name__)

# ---------------- PERSONALITY KEYWORDS (WEIGHTED) ---------------- #

PERSONALITY_KEYWORDS = {
    "creative": {
        "creative": 1, "imaginative": 1, "inventive": 1,
        "innovative": 2, "artistic": 2, "visionary": 3
    },
    "analytical": {
        "logical": 1, "analytical": 2, "data": 1,
        "think": 1, "reason": 2, "analysis": 3
    },
    "social": {
        "friendly": 1, "social": 1, "outgoing": 2,
        "people": 1, "team": 2, "communication": 3
    },
    "reserved": {
        "quiet": 1, "introvert": 2, "reserved": 1,
        "shy": 1, "calm": 2, "private": 2
    },
    "driven": {
        "ambitious": 2, "driven": 2, "goal": 1,
        "focused": 2, "motivated": 3, "disciplined": 3
    }
}

# ---------------- SENTIMENT WORDS ---------------- #

SENTIMENT_DICT = {
    "excellent": 3, "amazing": 3, "fantastic": 3,
    "awesome": 3, "brilliant": 3, "love": 3,
    "great": 2, "good": 1, "happy": 2,
    "confident": 2, "motivated": 2, "success": 2,
    "okay": 0, "neutral": 0,
    "bad": -1, "sad": -2, "stressed": -2,
    "tired": -1, "confused": -1,
    "terrible": -3, "angry": -3,
    "frustrated": -3, "depressed": -3, "hate": -3
}

# ---------------- LOGIC FUNCTIONS ---------------- #

def extract_personality(text):
    words = re.findall(r"\w+", text.lower())
    scores = {trait: 0 for trait in PERSONALITY_KEYWORDS}

    for trait, keywords in PERSONALITY_KEYWORDS.items():
        for word in words:
            if word in keywords:
                scores[trait] += keywords[word]

    sorted_traits = sorted(scores.items(), key=lambda x: (-x[1], x[0]))
    top = [t for t, s in sorted_traits if s > 0][:2]
    return top if top else ["balanced"]


def sentiment_score(text):
    words = re.findall(r"\w+", text.lower())
    return sum(SENTIMENT_DICT.get(w, 0) for w in words)


def sentiment_label(score):
    if score >= 3:
        return "Very Positive"
    if score >= 1:
        return "Positive"
    if score == 0:
        return "Neutral"
    if score <= -3:
        return "Very Negative"
    return "Negative"

# ---------------- ROUTES ---------------- #

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    name = request.form.get("name", "User")
    gender = request.form.get("gender", "Not specified")
    text = request.form.get("text", "").strip()

    if not text:
        return redirect(url_for("index"))

    traits = extract_personality(text)
    score = sentiment_score(text)
    label = sentiment_label(score)

    return render_template(
        "result.html",
        name=name,
        gender=gender,
        text=text,
        traits=traits,
        score=score,
        label=label
    )

# ---------------- RUN ---------------- #

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
