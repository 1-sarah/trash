import yaml
import streamlit as st
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import pandas as pd
from datetime import datetime, timedelta
from github_contents import GithubContents

st.set_page_config(page_title='mamasjourney', page_icon=':ship:', layout='wide', initial_sidebar_state= 'auto')

github = GithubContents(
            st.secrets["github"]["owner"],
            st.secrets["github"]["repo"],
            st.secrets["github"]["token"])

with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Authenticator
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

def registration():
    st.header("Registration")
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")

    if st.button("Register"):
        # Check if username already exists
        if new_username in config['credentials']:
            st.error("Username already exists. Please choose a different one.")
        else:
            # Add new user to YAML file
            config['credentials'][new_username] = new_password
            with open('./config.yaml', 'w') as file:
                yaml.dump(config, file)
            st.success("Registration successful. You can now login.")

from pages import 👩‍🍼_Mama,🚼_Baby,📈_Statistiken,🔗_Links
page_names_to_funcs = {
    "1_👩‍🍼_Mama": mama,
    "2_🚼_Baby": baby,
    "3_📈_Statistiken": statistiken,
    "4_🔗_Links": links
}   
def main(username):
    st.sidebar.success('')
    page_name = st.sidebar.selectbox("Wählen Sie eine Seite", page_names_to_funcs.keys())
    page_names_to_funcs[page_name]()
         

name, authentication_status, username = authenticator.login()

if authentication_status:
    authenticator.logout('Logout', 'main')
    main(username)
elif authentication_status == False:
    st.error('Username/password is incorrect')
    registration()  
elif authentication_status == None:
    st.warning('Please enter your username and password')
    registration()
