"""
About the Developer page.
Everything in [square brackets] is a placeholder. Replace it with your own text.
"""

import streamlit as st

from utils import show_card, show_hero

show_hero("👤 About the Developer", "The student behind PresentAI.")

st.header("[Student name]")
st.write("**School:** [School name]")

st.header("Short biography")
st.write("[Write 2-3 sentences about yourself here.]")

st.header("Interests")
col1, col2, col3 = st.columns(3)
with col1:
    show_card("Technology", "[Your interest in technology]")
with col2:
    show_card("AI", "[Your interest in AI]")
with col3:
    show_card("Programming", "[Your interest in programming]")

st.header("Why I built PresentAI")
st.write("[Explain in your own words why you chose this project.]")

st.header("Contact")
st.write("[Optional: email, GitHub or LinkedIn link]")
