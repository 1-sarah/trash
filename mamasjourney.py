import streamlit as st
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import pandas as pd
from datetime import datetime, timedelta
from github_contents import GithubContents

# Page Configuration
st.set_page_config(page_title="mamasjourney", page_icon=':ship:', layout="wide")

# Import pages
from pages import mama, baby, statistiken, links

# Create a dictionary mapping page names to functions
pages = {
    "Mama": mama,
    "Baby": baby,
    "Statistiken": statistiken,
    "Weiterführende Links": links
}

# Add a selectbox in the sidebar for page navigation
st.sidebar.title("Navigation")
page_selection = st.sidebar.selectbox("Select a page", options=list(pages.keys()))

# Call the selected page function
selected_page = pages[page_selection]
selected_page.show()
