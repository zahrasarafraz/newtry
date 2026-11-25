"""
app.py - the entry point of PresentAI.

Run it with:  streamlit run app.py

This file does three jobs:
  1. sets up the page (title, icon),
  2. adds the shared styling,
  3. creates the navigation menu and runs the page the user chose.
The pages themselves live in the views/ folder.
"""

import streamlit as st

from utils import load_css

# Must be the first Streamlit command
st.set_page_config(page_title="PresentAI", page_icon="🎤")

load_css()

# The pages of the app (title, icon and the file that contains each page)
practice_page = st.Page("views/practice.py", title="Practice", icon="🎤", default=True)
info_page = st.Page("views/project_info.py", title="Project Information", icon="📘")
about_page = st.Page("views/about_developer.py", title="About the Developer", icon="👤")

# The menu in the sidebar
navigation = st.navigation([practice_page, info_page, about_page])

st.sidebar.caption("PresentAI - a student project for practising speeches.")

# Run the page the user clicked
navigation.run()
