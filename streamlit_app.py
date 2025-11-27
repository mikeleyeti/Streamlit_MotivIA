import streamlit as st

st.set_page_config(
    page_title="MotivIA - Analyse des questionnaires", page_icon="📊", layout="wide"
)

st.title("📊 Analyse des questionnaires MotivIA")
st.subheader("Académie d'Orléans-Tours")

st.markdown(
    """
## Bienvenue sur l'application d'analyse MotivIA

Cette application permet d'analyser les données des questionnaires collectés auprès des professeurs et des élèves.

### 📍 Navigation

Utilisez le menu latéral pour accéder aux différentes sections :

- **📊 Données Professeurs** : Analyse des réponses des enseignants
- **📚 Données Élèves** : Analyse des réponses des élèves

### 📈 Fonctionnalités

- Filtrage dynamique des données
- Visualisations interactives
- Export des résultats
- Analyse comparative

---

### 🎯 Objectifs de l'étude

Cette étude vise à comprendre les pratiques d'évaluation et de feedback dans l'académie, 
en particulier l'usage des commentaires écrits et oraux, ainsi que les perspectives sur l'utilisation de l'IA.
"""
)

# Métriques globales si vous avez les deux datasets
col1, col2, col3 = st.columns(3)

try:
    import pandas as pd

    df_prof = pd.read_csv("Data/profs.csv", index_col=0)
    df_eleves = pd.read_csv("Data/eleves.csv", index_col=0)

    with col1:
        st.metric("Total Professeurs", len(df_prof))
    with col2:
        st.metric("Total Élèves", len(df_eleves))
    with col3:
        st.metric("Établissements", df_prof["UAI"].nunique())
except:
    st.info("Chargez les données pour voir les statistiques globales")
