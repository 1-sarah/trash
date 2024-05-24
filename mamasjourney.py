import yaml
import streamlit as st
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import pandas as pd
from datetime import datetime, timedelta
from github_contents import GithubContents
import toml

# Define the content for config.toml
config_data = {
    'params': {
        'customCSS': ["custom.css"]
    }
}

with open('config.toml', 'w') as config_file:
    toml.dump(config_data, config_file)

# Define the content for custom.css
css_content = """
body {
    background-color: #E6E6FA; /* Pastel violet */
    font-family: 'Comic Sans MS', cursive, sans-serif; /* Example of a soft font */
    color: #333333; /* Optional: a soft text color */
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Comic Sans MS', cursive, sans-serif;
}

p {
    font-family: 'Comic Sans MS', cursive, sans-serif;
}
"""

# Write the custom.css file
with open('custom.css', 'w') as css_file:
    css_file.write(css_content)

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
