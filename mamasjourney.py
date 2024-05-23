import yaml
import streamlit as st
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import pandas as pd
from datetime import datetime, timedelta
from github_contents import GithubContents

# Verbindung zu GitHub initialisieren
github = GithubContents(
            st.secrets["github"]["owner"],
            st.secrets["github"]["repo"],
            st.secrets["github"]["token"])

# Load the configuration file
with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Initialize the authenticator
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

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

# Authentication and visualizing the elements
name, authentication_status, username = authenticator.login()
if authentication_status:
    authenticator.logout('Logout', 'main')
    st.write(f'Welcome *{name}*')
    show()
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
