import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# import numpy as np
st.set_page_config(
    page_title="MotivIA - Analyse des questionnaires", page_icon="📊", layout="wide"
)

st.title("Analyse des questionnaires MotivIA")
st.subheader("Données de l'Académie d'Orléans-Tours.")

df_prof = pd.read_csv("Data/profs.csv", index_col=0)

# Sidebar - Filtres
st.sidebar.header("🔍 Filtres")
# Filtre par type d'établissement
if "Type_etab" in df_prof.columns:
    types_etab = ["Tous", "Tous lycées"] + sorted(
        df_prof["Type_etab"].dropna().unique().tolist()
    )
    type_selected = st.sidebar.selectbox("Type d'établissement", types_etab)
    if type_selected == "Tous lycées":
        df_prof = df_prof[
            df_prof["Type_etab"].isin(
                [
                    "LYCEE POLYVALENT",
                    "LYCEE GENERAL",
                    "LYCEE PROFESSIONNEL",
                    "LYCEE GENERAL ET TECHNOLOGIQUE",
                    "LPO LYCEE DES METIERS",
                    "LP LYCEE DES METIERS",
                ]
            )
        ]
    elif type_selected != "Tous":
        df_prof = df_prof[df_prof["Type_etab"] == type_selected]

# Filtre par département
if "Departement" in df_prof.columns:
    depts = ["Tous"] + sorted(df_prof["Departement"].dropna().unique().tolist())
    dept_selected = st.sidebar.selectbox("Département", depts)

    if dept_selected != "Tous":
        df_prof = df_prof[df_prof["Departement"] == dept_selected]


with st.expander("Données 'brutes'"):
    st.dataframe(df_prof)

tab1, tab2, tab3 = st.tabs(["Données de contexte", "tab2", "tab3"])

with tab1:
    st.header("Données de contexte")
    # Agréger les données
    df_pivot = (
        df_prof.groupby(["Type_etab", "Departement"]).size().reset_index(name="count")
    )
    df_pivot = df_pivot.pivot(
        index="Type_etab", columns="Departement", values="count"
    ).fillna(0)

    # Créer le graphique empilé
    fig = go.Figure()

    # Ajouter une trace pour chaque département
    for dept in df_pivot.columns:
        fig.add_trace(
            go.Bar(
                name=dept,
                x=df_pivot.index,
                y=df_pivot[dept],
                text=df_pivot[dept].astype(int),
                textposition="inside",
            )
        )

    # Mise en page
    fig.update_layout(
        barmode="stack",
        title="Répartition par type d'établissement et département",
        xaxis_title="Type d'établissement",
        yaxis_title="Nombre",
        xaxis_tickangle=-45,
        showlegend=True,
        legend=dict(
            title="Départements",
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02,
        ),
        margin=dict(b=100),
    )

    st.plotly_chart(fig, use_container_width=True)
