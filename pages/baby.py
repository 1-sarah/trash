import yaml
import streamlit as st
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import pandas as pd
from datetime import datetime, timedelta
from github_contents import GithubContents

def show():
    file_suffix = username
    st.header('Baby :ship:')
    st.subheader('Ideen Babyname')
    baby_name_text = st.text_area("Babyname")
    if st.button("Name speichern"):
        new_row = pd.DataFrame({"Datum": [datetime.today()], "Babyname": [baby_name_text]})
        file_name = f"baby_name_{file_suffix}.csv"
        if github.file_exists(file_name):
            mama_babyname_df = github.read_df(file_name)
            mama_babyname_df = pd.concat([mama_babyname_df, new_row], ignore_index=True)
        else:
            mama_babyname_df = new_row.copy()
        github.write_df(file_name, mama_babyname_df, "Speicher Babyname")
    if github.file_exists(f"baby_name_{file_suffix}.csv"):
        mama_babyname_df = github.read_df(f"baby_name_{file_suffix}.csv")
        st.write(mama_babyname_df)
    else:
        st.write("Noch keine Babynamen vorhanden.")
    st.subheader('Entwicklung Baby')
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
    df = pd.DataFrame(fruchtgroessen, columns=["Schwangerschaftswoche", "Fruchtgröße"])
    st.dataframe(df)
