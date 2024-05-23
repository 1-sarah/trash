import yaml
import streamlit as st
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import pandas as pd
from datetime import datetime, timedelta
from github_contents import GithubContents

# Page Configuration
st.set_page_config(page_title="mamasjourney", page_icon=':ship:', layout="wide",)

# Verbindung zu GitHub initialisieren
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

def main(username):
    st.write(f'Welcome *{username}*')
    
    def load_last_period_date(file_suffix):
        try:
            data = github.read_json(f"last_period_date_{file_suffix}.json")
            last_period_date = pd.to_datetime(data["last_period_date"])
        except:
            last_period_date = None
        return last_period_date

    def save_last_period_date(date, file_suffix):
        github.write_json(f"last_period_date_{file_suffix}.json", {"last_period_date": date.strftime("%Y-%m-%d")}, "Save last period date")

    def calculate_due_date(last_period_date):
        gestation_period = timedelta(days=280)
        due_date = last_period_date + gestation_period
        return due_date


    calendar_weeks_data = {
        'Kalenderwoche': list(range(1, 41)),
        'Ereignis': ['Ultraschall', 'Arztbesuch', 'Ernährungsberatung', 'Geburtsvorbereitungskurs', 'Ruhestunde'] * 8
    } 

    st.title("mamasjourney :ship:")

    file_suffix = username
    last_period_date = load_last_period_date(file_suffix)

    st.header('Mama')
    if last_period_date is not None:
        last_period_date = st.date_input('Letzter Menstruationszyklus', value=last_period_date, format="YYYY/MM/DD")
    else:
        last_period_date = st.date_input('Letzter Menstruationszyklus', format="YYYY/MM/DD")

    if last_period_date:
        due_date = calculate_due_date(last_period_date)
        st.write("Voraussichtlicher Geburtstermin:", due_date)
        st.subheader('Schwangerschafts-Timeline')
        df_calendar_weeks = pd.DataFrame(calendar_weeks_data)
        st.write(df_calendar_weeks)

    st.write('Gewicht')
    weight_date = st.date_input("Datum", value=datetime.today(), max_value=datetime.today(), format="YYYY/MM/DD")
    weight = st.number_input("Gewicht (kg)", min_value=0.0)
    if st.button("Gewicht speichern"):
        new_row = pd.DataFrame({"Datum": [weight_date], "Gewicht (kg)": [weight]})
        file_name = f"weight_{file_suffix}.csv"
        if github.file_exists(file_name):
            weight_df = github.read_df(file_name)
            weight_df = pd.concat([weight_df, new_row], ignore_index=True)
        else:
            weight_df = new_row.copy()
        github.write_df(file_name, weight_df, "Speicher Gewicht")

    st.write('Blutwert')
    blutwerte_text = st.text_area("Blutzuckerwerte")
    if st.button("Blutwert speichern"):
        new_row = pd.DataFrame({"Datum": [weight_date], "Blutzuckerwert (in mg/dL)": [blutwerte_text]})
        file_name = f"blutwert_{file_suffix}.csv"
        if github.file_exists(file_name):
            blutwert_df = github.read_df(file_name)
            blutwert_df = pd.concat([blutwert_df, new_row], ignore_index=True)
        else:
            blutwert_df = new_row.copy()
        github.write_df(file_name, blutwert_df, "Speicher Blutzuckerwert")

    st.subheader('Blutzuckerwert')
    if github.file_exists(f"blutwert_{file_suffix}.csv"):
        blutwert_df = github.read_df(f"blutwert_{file_suffix}.csv")
        st.write(blutwert_df)
    else:
        st.write("Noch keine Blutzuckerwerte vorhanden.")
                
    st.header('Tagebuch')
    tagebuch_text = st.text_area("Tagebuch")
    if st.button("Eintrag speichern"):
        new_row = pd.DataFrame({"Date": [weight_date], "Tagebuch": [tagebuch_text]})
        file_name = f"tagebuch_{file_suffix}.csv"
        if github.file_exists(file_name):
            tagebuch_df = github.read_df(file_name)
            tagebuch_df = pd.concat([tagebuch_df, new_row], ignore_index=True)
        else:
            tagebuch_df = new_row.copy()
        github.write_df(file_name, tagebuch_df, "Speicher Tagebucheintrag")

    st.subheader('Tagebuch')
    if github.file_exists(f"tagebuch_{file_suffix}.csv"):
        tagebuch_df = github.read_df(f"tagebuch_{file_suffix}.csv")
        st.write(tagebuch_df)
    else:
        st.write("Noch keine Tagebucheinträge vorhanden.")

name, authentication_status, username = authenticator.login()

if authentication_status:
    authenticator.logout('Logout', 'main')
    main(username)
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
