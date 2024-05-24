import yaml
import streamlit as st
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import pandas as pd
from datetime import datetime
from github_contents import GithubContents

# Verbindung zu GitHub initialisieren
github = GithubContents(
    st.secrets["github"]["owner"],
    st.secrets["github"]["repo"],
    st.secrets["github"]["token"])

# Liste der Fruchtgrössen
fruchtgroessen = [
    ("4 Wochen", "Mohnsamen"),
    ("5 Wochen", "Sesamsamen"),
    ("6 Wochen", "Linsenkorn"),
    ("7 Wochen", "Blaubeere"),
    ("8 Wochen", "Kidneybohne"),
    ("9 Wochen", "Traube"),
    ("10 Wochen", "Kirsche"),
    ("11 Wochen", "Erdbeere"),
    ("12 Wochen", "Limette"),
    ("13 Wochen", "Erbsenschote"),
    ("14 Wochen", "Zitrone"),
    ("15 Wochen", "Apfel"),
    ("16 Wochen", "Avocado"),
    ("17 Wochen", "Rübe"),
    ("18 Wochen", "Paprika"),
    ("19 Wochen", "Mango"),
    ("20 Wochen", "Banane"),
    ("21 Wochen", "Karotte"),
    ("22 Wochen", "Papaya"),
    ("23 Wochen", "Grapefruit"),
    ("24 Wochen", "Maiskolben"),
    ("25 Wochen", "Aubergine"),
    ("26 Wochen", "Zucchini"),
    ("27 Wochen", "Blumenkohl"),
    ("28 Wochen", "Aubergine"),
    ("29 Wochen", "Butternusskürbis"),
    ("30 Wochen", "Kohlkopf"),
    ("31 Wochen", "Kokosnuss"),
    ("32 Wochen", "Jicama (Yam Bean)"),
    ("33 Wochen", "Ananas"),
    ("34 Wochen", "Melone"),
    ("35 Wochen", "Honigmelone"),
    ("36 Wochen", "Romanesco"),
    ("37 Wochen", "Lauch"),
    ("38 Wochen", "Rhabarber"),
    ("39 Wochen", "Wassermelone"),
    ("40 Wochen", "Kürbis"),
]

# Main definieren mit allen gewünschten Funktionen
def baby_main(username):
    file_suffix = username
    st.header('Baby :ship:')
    st.subheader('Ideen Babyname')
    babyname_date = st.date_input("Datum", value=datetime.today(), max_value=datetime.today(), format="YYYY/MM/DD")
    babyname_text = st.text_area("Babyname")
    if st.button("Name speichern"):
        new_row = pd.DataFrame({"Datum": [babyname_date], "Babyname": [babyname_text]})
        file_name = f"babyname_{file_suffix}.csv"
        if github.file_exists(file_name):
            babyname_df = github.read_df(file_name)
            babyname_df = pd.concat([babyname_df, new_row], ignore_index=True)
        else:
            babyname_df = new_row.copy()
        github.write_df(file_name, babyname_df, "Speicher Babyname")
    if github.file_exists(f"babyname_{file_suffix}.csv"):
        babyname_df = github.read_df(f"babyname_{file_suffix}.csv")
        st.write(babyname_df)
    else:
        st.write("Noch keine Babynamen vorhanden.")
    st.subheader('Entwicklung Baby')
    df = pd.DataFrame(fruchtgroessen, columns=["Schwangerschaftswoche", "Fruchtgröße"])
    st.dataframe(df)

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

# Authentication and visualizing the elements
name, authentication_status, username = authenticator.login()
if authentication_status:
    authenticator.logout('Logout', 'main')
    st.write(f'Welcome *{name}*')
    baby_main(username)
elif authentication_status == False:
    st.error('Username/password is incorrect')
    st.write("Please log in first to access this page.")
    if st.button("Go to Main Page"):
        st.session_state.login_page = 'login'
        st.experimental_rerun()
elif authentication_status == None:
    st.warning('Please enter your username and password')
    st.write("Please log in first to access this page.")
    if st.button("Go to Main Page"):
        st.session_state.login_page = 'login'
        st.experimental_rerun()
