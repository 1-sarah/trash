import yaml
import streamlit as st
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import bcrypt
from github_contents import GithubContents

# Load secrets
github = GithubContents(
    st.secrets["github"]["owner"],
    st.secrets["github"]["repo"],
    st.secrets["github"]["token"]
)

# Load configuration
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
        # Load existing credentials from YAML
        with open('./config.yaml', 'r') as file:
            config = yaml.load(file, Loader=SafeLoader)

        # Check if username already exists
        if new_username in config['credentials']['usernames']:
            st.error("Username already exists. Please choose a different one.")
        else:
            # Hash the password
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            # Add new user to YAML file with hashed password
            config['credentials']['usernames'][new_username] = {
                'email': '',  # You can add email field if needed
                'name': '',   # You can add name field if needed
                'password': hashed_password
            }
            with open('./config.yaml', 'w') as file:
                yaml.dump(config, file)
            st.success("Registration successful. You can now login.")

# Toggle between login and registration
if 'login_page' not in st.session_state:
    st.session_state.login_page = 'login'  # Default to login page

# Add a toggle widget for switching between login and registration
st.sidebar.title("Authentication")
toggle = st.sidebar.radio("Choose an option", ('Login', 'Register'))

if toggle == 'Login':
    st.session_state.login_page = 'login'
elif toggle == 'Register':
    st.session_state.login_page = 'register'

if st.session_state.login_page == 'login':
    name, authentication_status, username = authenticator.login()
    
    if authentication_status:
        st.session_state.logged_in = True
        st.session_state.username = username
        st.write(f"Welcome, {username}!")
        # You can add a redirect or further actions here
    elif authentication_status == False:
        st.error('Username/password is incorrect')
    elif authentication_status == None:
        st.warning('Please enter your username and password')

elif st.session_state.login_page == 'register':
    registration()
