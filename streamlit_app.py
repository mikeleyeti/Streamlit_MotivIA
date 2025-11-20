import streamlit as st
import pandas as pd

# import numpy as np

st.title("Analyse des questionnaires MotivIA")
st.subheader("Données de l'Académie d'Orléans-Tours.")

df_prof = pd.read_csv("Data/profs.csv", index_col=0)
st.dataframe(df_prof)
