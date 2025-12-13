from flask import Flask, render_template, request, redirect, url_for
import re

app = Flask(__name__)

# --------------------------------------------------
# PERSONALITY KEYWORDS WITH WEIGHTS (POINTS)
# --------------------------------------------------

PERSONALITY_KEYWORDS = {
    "creative": {
        "creative": 1,
        "imaginative": 1,
        "inventive": 1,
        "innovative": 2,
        "artistic": 2,
        "visionary": 3
    },

    "analytical": {
        "logical": 1,
        "analytical": 2,
        "data": 1,
        "think": 1,
        "reason": 2,
        "analysis": 3
    },

    "social": {
        "friendly": 1,
        "social": 1,
        "outgoing": 2,
        "people": 1,
        "team": 2,
        "communication": 3
    },

    "reserved": {
        "quiet": 1,
        "introvert": 2,
        "reserved": 1,
        "shy": 1,
        "calm": 2,
        "private": 2
    },

    "driven": {
        "ambitious": 2,
        "driven": 2,
        "goal": 1,
        "focused": 2,
        "motivated": 3,
        "disciplined": 3
    }
}

# --------------------------------------------------
# SENTIMENT DICTIONARY WITH POINTS
# --------------------------------------------------

SENTIMENT_DICT = {
    # very positive
    "excellent": 3, "amazing": 3, "fantastic": 3,
    "awesome": 3, "brilliant": 3, "love": 3,

    # positive
    "great": 2, "good": 1, "happy": 2,
    "confident": 2, "motivated": 2,
    "optimistic": 2, "success": 2,

    # neutral
    "okay": 0, "neutral": 0, "normal": 0,

    # negative
    "bad": -1, "sad": -2, "tired": -1,
    "confused": -1, "stressed": -2,
    "failure": -2,

    # very negative
    "terrible": -3, "angry": -3,
    "frustrated": -3, "depressed": -3,
    "hate": -3
}

# --------------------------------------------------
# LOGIC FUNCTIONS
# --------------------------------------------------

def extract_personality(text: str):
    text = text.lower()
    words = re.findall(r"\w+", text)

    scores = {trait: 0 for trait in PERSONALITY_KEYWORDS}

    for trait, keywords in PERSONALITY_KEYWORDS.items():
        for word in words:
            if word in keywords:
                scores[trait] += keywords[word]

    # sort by score (desc), then name (asc) for stability
    sorted_traits = sorted(scores.items(), key=lambda x: (-x[1], x[0]))

    top_traits = [trait for trait, score in sorted_traits if score > 0][:2]

    return top_traits if top_traits else ["balanced"]


def sentiment_score(text: str):
    text = text.lower()
    words = re.findall(r"\w+", text)

    score = 0
    for word in words:
        score += SENTIMENT_DICT.get(word, 0)

    return score


def sentiment_label(score: int):
    if score >= 3:
        return "Very Positive"
    elif score >= 1:
        return "Positive"
    elif score == 0:
        return "Neutral"
    elif score <= -3:
        return "Very Negative"
    else:
        return "Negative"

# --------------------------------------------------
# ROUTES
# --------------------------------------------------

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

    return render_template(
        "result.html",
        text=text,
        traits=traits,
        score=score,
        label=label
    )

# --------------------------------------------------
# MAIN
# --------------------------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
