import yaml
import streamlit as st
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import pandas as pd
from datetime import datetime, timedelta
from github_contents import GithubContents

# Page Configuration
st.set_page_config(page_title="mamasjourney", page_icon=':ship:', layout="wide")
# Verbindung zu GitHub initialisieren

st.title('mamasjourney :ship:')
st.header('Herzlich Willkommen bei deinem eigenen Schwangerschaftstagebuch')
