import yaml
import streamlit as st
from yaml.loader import SafeLoader
from multiapp import Multiapp
import streamlit_authenticator as stauth
import pandas as pd
from datetime import datetime, timedelta
from github_contents import GithubContents
from apps import mama, baby

# Page Configuration
st.set_page_config(page_title="mamasjourney", page_icon=':ship:', layout="wide")

st.title('mamasjourney :ship:')
st.subheader('Herzlich Willkommen bei deinem eigenen Schwangerschaftstagebuch')
# Multiapp
app = Multiapp()
app.add_app('👩‍🍼Mama', mama.app)
app.add_app('🚼Baby', baby.app)
app.run()


