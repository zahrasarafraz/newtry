"""Project Information page."""

import streamlit as st

from utils import show_card, show_hero

show_hero("📘 Project Information", "What PresentAI is and how it works.")

st.header("What is PresentAI?")
st.write(
    "PresentAI is a web app that helps people practise speaking. You upload a recording or "
    "record your voice, and the app turns your speech into text and tells you how fast you "
    "spoke and how many filler words (like \"um\" and \"uh\") you used."
)

st.header("The problem")
st.write(
    "Many students feel nervous when they present, and it is hard to notice your own habits "
    "while you are speaking. Most people do not have someone to listen and give feedback "
    "every time they practise."
)

st.header("Why is speech practice useful?")
col1, col2 = st.columns(2)
with col1:
    show_card("Builds confidence", "The more you practise, the calmer you feel on the day.")
    show_card("Improves clarity", "A steady pace helps the audience follow your ideas.")
with col2:
    show_card("Shows your habits", "Hearing and seeing your fillers helps you notice them.")
    show_card("Private and instant", "You can practise alone and get feedback straight away.")

st.header("How it works")
st.markdown(
    "1. **Record or upload** your practice speech (mp3, wav or m4a).\n"
    "2. **Speech-to-text:** the faster-whisper model writes down what you said.\n"
    "3. **Analysis:** the app counts the words, the filler words and your words per minute (WPM).\n"
    "4. **Feedback:** you see your transcript, your numbers and a short tip about your pace."
)

st.header("Main features")
st.markdown(
    "- Upload an audio file or record with your microphone\n"
    "- Transcript of your speech\n"
    "- Speaking pace in words per minute, with feedback\n"
    "- Filler word count and a chart of which fillers you used\n"
    "- Your audio is not saved"
)

st.header("Technologies used")
st.markdown(
    "- **Python** - the programming language\n"
    "- **Streamlit** - builds the web pages\n"
    "- **faster-whisper** - converts speech to text\n"
    "- **pandas** - organises the filler word data for the chart\n"
    "- **GitHub and Streamlit Community Cloud** - to share the app online"
)

st.header("Limits of this version")
st.write(
    "Speech-to-text is not perfect, and the filler word count can differ slightly between "
    "attempts. Words like \"so\" and \"like\" are counted even when they are used normally."
)

st.header("Possible future improvements")
st.markdown(
    "- An AI coach that writes personal tips after each speech\n"
    "- Feedback on volume, intonation and energy\n"
    "- Saving progress over time for each user\n"
    "- Analysing video, such as body language"
)
