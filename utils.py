"""
utils.py - the helper functions for PresentAI.

This file holds the "engine" of the app: transcribing speech, counting
filler words and calculating the speaking pace. The pages in the
views/ folder only call these functions and show the results.
"""

import os
import re
import tempfile

import streamlit as st
from faster_whisper import WhisperModel
from faster_whisper.audio import decode_audio  # used to read an audio file safely

# ---------- SETTINGS ----------
FILLER_WORDS = [
    "um", "umm", "uh", "uhh", "uhm", "hmm", "erm",
    "like", "you know", "so", "actually", "basically", "literally", "i mean",
]

# A hint for Whisper: sample text that contains fillers, so it is more likely to keep them
FILLER_PROMPT = "Umm, so, uh, I was, like, thinking... you know, hmm, let me start."

# Limits that keep the free cloud server from being overloaded
MAX_FILE_MB = 25        # biggest file we accept
MIN_SECONDS = 1         # shorter recordings are treated as empty
MAX_SECONDS = 300       # 5 minutes


# ---------- LOOK AND FEEL ----------
def load_css():
    """Add a little extra styling on top of the Streamlit theme."""
    st.markdown(
        """
        <style>
        .block-container { padding-top: 2rem; max-width: 900px; }
        .hero {
            background: linear-gradient(135deg, #3B5BDB, #5C7CFA);
            padding: 1.6rem 2rem;
            border-radius: 16px;
            margin-bottom: 1.5rem;
        }
        .hero h1 { color: white; margin: 0; padding: 0; font-size: 2rem; }
        .hero p { color: #E7ECFF; margin: 0.4rem 0 0 0; font-size: 1.05rem; }
        .card {
            background: #F1F4FB;
            border-left: 5px solid #3B5BDB;
            padding: 1rem 1.2rem;
            border-radius: 10px;
            margin-bottom: 1rem;
        }
        .card h4 { margin: 0 0 0.3rem 0; }
        .card p { margin: 0; }
        [data-testid="stMetric"] {
            background: #F1F4FB;
            padding: 0.8rem 1rem;
            border-radius: 12px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def show_hero(title, subtitle):
    """Show the big coloured banner at the top of a page."""
    st.markdown(
        f'<div class="hero"><h1>{title}</h1><p>{subtitle}</p></div>',
        unsafe_allow_html=True,
    )


def show_card(title, text):
    """Show a small highlighted box with a title and a short text."""
    st.markdown(
        f'<div class="card"><h4>{title}</h4><p>{text}</p></div>',
        unsafe_allow_html=True,
    )


# ---------- LOAD WHISPER MODEL (cached so it only loads once) ----------
@st.cache_resource
def load_model():
    return WhisperModel("base", device="cpu", compute_type="int8")


# ---------- ANALYSIS FUNCTIONS ----------
def transcribe_audio(audio_path):
    model = load_model()
    segments, info = model.transcribe(audio_path, initial_prompt=FILLER_PROMPT)
    full_text = ""
    duration = 0
    for segment in segments:
        full_text += segment.text + " "
        duration = segment.end  # last segment's end time = total duration
    text = full_text.strip()

    # On silence, Whisper can repeat our hint back. Treat that as "no speech".
    letters_only = re.sub(r"[^a-z ]", "", text.lower())
    hint_letters = re.sub(r"[^a-z ]", "", FILLER_PROMPT.lower())
    if letters_only == hint_letters:
        text = ""

    return text, duration


def count_filler_words(text):
    text_lower = text.lower()
    counts = {}
    total = 0
    for filler in FILLER_WORDS:
        # word-boundary match so "like" doesn't match inside "likely"
        pattern = r"\b" + re.escape(filler) + r"\b"
        matches = re.findall(pattern, text_lower)
        if matches:
            counts[filler] = len(matches)
            total += len(matches)
    return counts, total


def calculate_wpm(text, duration_seconds):
    word_count = len(text.split())
    if duration_seconds <= 0:
        return 0, word_count
    minutes = duration_seconds / 60
    wpm = word_count / minutes
    return round(wpm, 1), word_count


# ---------- AUDIO HELPERS (used by both upload and microphone) ----------
def save_temp_audio(audio_bytes, extension):
    """Save audio bytes to a temporary file and return its path.
    Every call gets its own unique file name, so two users never clash."""
    with tempfile.NamedTemporaryFile(delete=False, suffix="." + extension) as temp_file:
        temp_file.write(audio_bytes)
        return temp_file.name


def get_audio_duration(audio_path):
    """Read the audio file and return its real length in seconds.
    This raises an error if the file is not valid audio."""
    samples = decode_audio(audio_path, sampling_rate=16000)
    return len(samples) / 16000


def analyze_audio(audio_bytes, extension):
    """THE ONE PIPELINE: both the uploaded file and the microphone
    recording come here.

    Returns two things: (results, error_message).
    - If everything works: results is a dictionary, error_message is None.
    - If something is wrong: results is None and error_message explains why.
    """
    # 1. Basic checks before we do any heavy work
    if len(audio_bytes) == 0:
        return None, "The recording is empty. Please record again or choose another file."
    if len(audio_bytes) > MAX_FILE_MB * 1024 * 1024:
        return None, f"This file is too large. Please use a file under {MAX_FILE_MB} MB."

    temp_path = save_temp_audio(audio_bytes, extension)

    try:
        # 2. Make sure it is real audio and check the length
        try:
            length = get_audio_duration(temp_path)
        except Exception:
            return None, "We could not read this audio file. Please try a different mp3, wav or m4a file."

        if length < MIN_SECONDS:
            return None, "The recording is too short. Please speak for at least a few seconds."
        if length > MAX_SECONDS:
            return None, f"This recording is longer than {MAX_SECONDS // 60} minutes. Please use a shorter one."

        # 3. Transcribe, then measure
        text, duration = transcribe_audio(temp_path)
        if not text:
            return None, "We could not hear any speech in this recording. Please try again."

        wpm, word_count = calculate_wpm(text, duration)
        filler_counts, filler_total = count_filler_words(text)

        results = {
            "text": text,
            "duration": duration,
            "wpm": wpm,
            "word_count": word_count,
            "filler_counts": filler_counts,
            "filler_total": filler_total,
        }
        return results, None

    except Exception as error:
        return None, f"Something went wrong while analysing the speech: {error}"

    finally:
        # 4. Always delete the temporary file, even if there was an error
        if os.path.exists(temp_path):
            os.remove(temp_path)
