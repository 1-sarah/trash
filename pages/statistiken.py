import yaml
import streamlit as st
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import pandas as pd
from github_contents import GithubContents

# Initialize GithubContents object
github = GithubContents(
    st.secrets["github"]["owner"],
    st.secrets["github"]["repo"],
    st.secrets["github"]["token"]
)

# Read DataFrame and column names from GitHub
def read_df(csv):
    if github.file_exists(csv):
        df = github.read_df(csv)
        xaxis = df.columns[0]
        yaxis = df.columns[1]
        return df, xaxis, yaxis
    else:
        st.error(f"File {csv} does not exist.")
        return None, None, None

# Function to plot the graph
def plot_graph(csv, title, y_label):
    df, xaxis, yaxis = read_df(csv)
    if df is not None and xaxis is not None and yaxis is not None:
        st.write(f"### {title}:")
        st.write(f"X-Achse: {xaxis}, Y-Achse: {yaxis}")
        st.line_chart(df.set_index(xaxis)[yaxis], color='#77ddaa', height=0, width=0)  # Plot the line chart
    else:
        st.error("Error in loading DataFrame or column names.")

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

# Authentication and visualizing the charts
name, authentication_status, username = authenticator.login()
if authentication_status:
    authenticator.logout('Logout', 'main')
    st.write(f'Welcome *{name}*')
    st.header('Statistiken :ship:')
    plot_graph(f'weights_{username}.csv', 'Gewichtsverlauf', 'kg')
    plot_graph(f'blutwert_{username}.csv', 'Blutzuckerwerte Verlauf', 'mg/dL')
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
