import re
import logging
from functools import wraps
from flask import redirect, session

from google import genai  # google-genai

logger = logging.getLogger(__name__)

client = genai.Client()

ALLOWED_EMOTIONS = ["happy", "sad", "angry", "calm", "anxious", "hopeful", "bored"]


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def _normalize_output(text: str) -> str:
    t = (text or "").strip().lower()
    t = re.sub(r"[^a-z\s\.\!\?,-]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def analyze_emotion(user_text: str) -> str:
    """Return one of the allowed emotions. Defaults to 'calm'."""
    try:
        if not user_text or not user_text.strip():
            return "calm"

        text = user_text.strip()
        if len(text) > 800:
            text = text[:800]

        prompt = (
            "Determine the main emotion of the following text.\n"
            f"Choose one from: {ALLOWED_EMOTIONS}.\n"
            "Return only one English word, no explanation.\n"
            "If the text is in Chinese, translate it first before analyzing.\n\n"
            f"Text:\n{text}\n"
        )

        resp = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        raw = getattr(resp, "text", "") or ""
        out = _normalize_output(raw)

        for e in ALLOWED_EMOTIONS:
            if re.search(rf"\b{re.escape(e)}\b", out):
                return e

        # Fallback if model outputs Chinese
        zh_emotions = {
            "sad": ["难过", "悲伤", "伤心", "沮丧"],
            "happy": ["开心", "快乐", "高兴"],
            "angry": ["生气", "愤怒", "恼火"],
            "calm": ["平静", "放松"],
            "anxious": ["焦虑", "担心", "紧张"],
            "hopeful": ["希望", "期待", "有盼头"],
            "bored": ["无聊", "没意思", "乏味"],
        }
        for emo, kws in zh_emotions.items():
            if any(k in raw for k in kws):
                return emo

        return "calm"

    except Exception as e:
        logger.exception("Gemini analyze_emotion failed: %s", str(e))
        return "calm"
