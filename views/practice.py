"""
Practice page - upload a recording or record with the microphone.
Both ways use the same function: analyze_audio() from utils.py.
"""

import pandas as pd
import streamlit as st

from utils import analyze_audio, show_hero

show_hero(
    "🎤 PresentAI",
    "Practice your speech and get instant feedback on your pace and filler words.",
)


def show_results(results):
    """Display the transcript, the numbers and the feedback."""
    st.subheader("📝 Transcript")
    st.write(results["text"])

    st.subheader("📊 Results")
    col1, col2, col3 = st.columns(3)
    col1.metric("Speaking Pace", f"{results['wpm']} WPM")
    col2.metric("Filler Words", results["filler_total"])
    col3.metric("Duration", f"{round(results['duration'], 1)}s")

    # Pace feedback
    wpm = results["wpm"]
    if wpm < 110:
        st.info("Your pace is a bit slow. Aim for 110-160 WPM for a natural conversational speed.")
    elif wpm > 160:
        st.warning("You're speaking quite fast. Try slowing down slightly for clarity.")
    else:
        st.success("Great pace! You're in the ideal range for clear, engaging speech.")

    # Filler word breakdown
    if results["filler_counts"]:
        st.subheader("🔍 Filler Word Breakdown")
        filler_df = pd.DataFrame(
            list(results["filler_counts"].items()), columns=["Filler Word", "Count"]
        )
        st.bar_chart(filler_df.set_index("Filler Word"))
    else:
        st.success("No filler words detected! 🎉")
        st.balloons()


def run_analysis(audio_bytes, extension):
    """Analyse the audio and show either the results or a clear error."""
    with st.spinner("Transcribing your speech... the first time can take a minute."):
        results, error_message = analyze_audio(audio_bytes, extension)

    if error_message:
        st.error(error_message)
    else:
        show_results(results)


with st.expander("Tips for best results"):
    st.write(
        "- Speak for at least 10-20 seconds, up to 5 minutes.\n"
        "- Record in a quiet place and speak naturally.\n"
        "- Filler words like \"so\" and \"like\" are counted even when they are real words, "
        "so treat the count as a guide, not an exact score.\n"
        "- Your audio is only used for the analysis. It is not saved."
    )

tab_upload, tab_record = st.tabs(["📁 Upload a file", "🎙️ Record with microphone"])

# ----- Option 1: upload a file -----
with tab_upload:
    uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "m4a"])

    if uploaded_file is not None:
        st.audio(uploaded_file)
        if st.button("Analyze uploaded speech", key="analyze_upload"):
            extension = uploaded_file.name.split(".")[-1].lower()
            run_analysis(uploaded_file.getvalue(), extension)

# ----- Option 2: record with the microphone -----
with tab_record:
    if hasattr(st, "audio_input"):
        recorded_audio = st.audio_input("Press the microphone button and start speaking")

        if recorded_audio is not None:
            if st.button("Analyze recorded speech", key="analyze_recording"):
                # st.audio_input always gives us a WAV recording
                run_analysis(recorded_audio.getvalue(), "wav")
    else:
        st.warning("Microphone recording needs a newer version of Streamlit. Please update Streamlit.")
