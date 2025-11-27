import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import create_pie_chart, create_pie_chart_split

st.set_page_config(page_title="Données élèves - MotivIA", page_icon="📊", layout="wide")

st.title("📊 Analyse des données élèves")
st.subheader("Questionnaire élèves - Académie d'Orléans-Tours")

# Charger les données
df_original = pd.read_csv(
    "Data/eleves.csv",
)
df_eleves = df_original.copy()


st.sidebar.header("🔍 Filtres Élèves")
# Filtre par type d'établissement avec multiselect
if "Classe" in df_eleves.columns:
    st.sidebar.subheader("Classe")

    # Obtenir toutes les classes uniques et les trier
    all_classes = sorted(df_eleves["Classe"].dropna().unique().tolist())

    # Options de sélection rapide
    col1, col2 = st.sidebar.columns(2)
    with col1:
        select_all_classes = st.checkbox("Tout sélectionner", value=True)
    with col2:
        select_none = st.checkbox("Tout désélectionner", value=False)

    # Logique de sélection rapide
    if select_none:
        default_classes = []
    elif select_all_classes:
        default_classes = all_classes
    else:
        default_classes = []

    # Multiselect pour les classes
    selected_classes = st.sidebar.pills(
        "Sélectionner les classes:",
        options=all_classes,
        default=default_classes,
        help="Sélectionnez une ou plusieurs classes",
        selection_mode="multi",
    )

    # Appliquer le filtre
    if selected_classes:
        df_eleves = df_eleves[df_eleves["Classe"].isin(selected_classes)]
    else:
        st.sidebar.warning("⚠️ Aucune classe sélectionnée")
        df_eleves = df_eleves.iloc[0:0]  # DataFrame vide

# Filtre par ages (si la colonne existe)
if "Age" in df_eleves.columns:
    st.sidebar.subheader("Age")

    # Obtenir les ages disponibles après le filtrage par classe
    available_ages = sorted(df_eleves["Age"].dropna().unique().tolist())

    if len(df_eleves) > 0:
        start_age, end_age = st.sidebar.select_slider(
            "Sélectionner les ages:",
            options=available_ages,
            value=(min(available_ages), max(available_ages)),
        )

        if start_age and end_age:
            df_eleves = df_eleves[
                (df_eleves["Age"] <= end_age) & (df_eleves["Age"] >= start_age)
            ]
        elif not start_age or end_age:
            st.sidebar.warning("⚠️ Aucun ages sélectionné")
            df_eleves = df_eleves.iloc[0:0]


# Afficher le nombre de résultats après filtrage
st.sidebar.markdown("---")
col1, col2 = st.sidebar.columns(2)
with col1:
    st.metric("Total filtré", len(df_eleves))
with col2:
    st.metric("Total initial", len(df_original))

if len(df_eleves) == 0:
    st.warning("Aucune donnée ne correspond aux filtres sélectionnés")


# Onglets pour les analyses élèves
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "Vue d'ensemble",
        "Commentaires écrits",
        "Commentaires oraux",
        "Comparaison écrit / oral",
        "Motivation, habitudes de travail",
    ]
)

with tab1:
    st.header("Vue d'ensemble")

    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Nombre d'élèves", len(df_eleves))
    with col2:
        if "Classe" in df_eleves.columns:
            st.metric("Classes représentées", df_eleves["Classe"].nunique())
    with col3:
        if "Niveau" in df_eleves.columns:
            st.metric("Niveaux représentés", df_eleves["Niveau"].nunique())
    with col4:
        if "Etablissement" in df_eleves.columns:
            st.metric("Établissements", df_eleves["Etablissement"].nunique())

    # Visualisation de la répartition par classe

    if "Classe" in df_eleves.columns:
        bar1 = st.toggle("Diagramme en barre", value=True, key=1)
        fig_classe = create_pie_chart(
            df_eleves,
            "Classe",
            "Répartition par classe",
            chart_type="bar" if bar1 else "pie",
        )
        st.plotly_chart(fig_classe, use_container_width=True)

with tab2:
    st.header("Commentaires écrits")
    col1, col2 = st.columns(2)
    with col1:
        bar_Freq_comm_ecrit = st.toggle(
            "Diagramme en barre",
            value=True,
        )
        fig_Freq_comm_ecrit = create_pie_chart(
            df_eleves,
            "Freq_comm_ecrit",
            "Est-ce que tes enseignants écrivent des commentaires (ou appréciations) sur tes copies ou devoirs ?",
            chart_type="bar" if bar_Freq_comm_ecrit else "pie",
        )
        st.plotly_chart(fig_Freq_comm_ecrit, use_container_width=True)
    with col2:
        bar_Lecture_comm_ecrit = st.toggle(
            "Diagramme en barre", value=False, key="Lecture_comm_ecrit"
        )
        fig_Lecture_comm_ecrit = create_pie_chart(
            df_eleves,
            "Lecture_comm_ecrit",
            "Est-ce que tu lis toujours les commentaires écrits des enseignants ?",
            chart_type="bar" if bar_Lecture_comm_ecrit else "pie",
        )
        st.plotly_chart(fig_Lecture_comm_ecrit, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        bar_Objectif_commentaire = st.toggle(
            "Diagramme en barre",
            value=False,
            key="Que cherches-tu en priorité dans une appréciation ? ",
        )
        fig_Objectif_commentaire = create_pie_chart(
            df_eleves,
            "Objectif_commentaire",
            "Que cherches-tu en priorité dans une appréciation ?",
            chart_type="bar" if bar_Objectif_commentaire else "pie",
        )
        st.plotly_chart(fig_Objectif_commentaire, use_container_width=True)
    with col2:
        bar_Impact_comm_ecrit = st.toggle(
            "Diagramme en barre", value=True, key="Impact_comm_ecrit"
        )
        fig_Impact_comm_ecrit = create_pie_chart(
            df_eleves,
            "Impact_comm_ecrit",
            "Est-ce que les commentaires écrits t’aident à progresser ?",
            chart_type="bar" if bar_Impact_comm_ecrit else "pie",
        )
        st.plotly_chart(fig_Impact_comm_ecrit, use_container_width=True)

    bar_Comp_comm_ecrit = st.toggle(
        "Diagramme en barre", value=True, key="Comp_comm_ecrit"
    )
    fig_Comp_comm_ecrit = create_pie_chart_split(
        df_eleves,
        "Comp_comm_ecrit",
        "Quand tu ne comprends pas un commentaire écrit, que fais-tu ?",
        chart_type="bar" if bar_Comp_comm_ecrit else "pie",
    )
    st.plotly_chart(fig_Comp_comm_ecrit, use_container_width=True)

with tab3:
    st.header("Les commentaires oraux.")
    col1, col2 = st.columns(2)
    with col1:
        bar_Freq_comm_oral = st.toggle(
            "Diagramme en barre", value=False, key="Freq_comm_oral"
        )
        fig_Freq_comm_oral = create_pie_chart(
            df_eleves,
            "Freq_comm_oral",
            "Est-ce que tes enseignants te font des commentaires à l'oral sur ton travail ?",
            chart_type="bar" if bar_Freq_comm_oral else "pie",
        )
        st.plotly_chart(fig_Freq_comm_oral, use_container_width=True)

    with col2:
        bar_Moment_comm_oral = st.toggle(
            "Diagramme en barre", value=True, key="Moment_comm_oral"
        )
        fig_Moment_comm_oral = create_pie_chart_split(
            df_eleves,
            "Moment_comm_oral",
            "Quand tes enseignants te font-ils des commentaires oraux sur ton travail ? (Réponses multiples)",
            chart_type="bar" if bar_Moment_comm_oral else "pie",
        )
        st.plotly_chart(fig_Moment_comm_oral, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        bar_Prof_comm_oral_prive = st.toggle(
            "Diagramme en barre", value=False, key="Prof_comm_oral_prive"
        )
        fig_comm_oral_prive = create_pie_chart(
            df_eleves,
            "Prof_comm_oral_prive",
            "Préfères-tu recevoir des commentaires en privé ou devant la classe ?",
            chart_type="bar" if bar_Prof_comm_oral_prive else "pie",
        )
        st.plotly_chart(fig_comm_oral_prive, use_container_width=True)

    with col2:
        bar_Gene_comm_oral = st.toggle(
            "Diagramme en barre", value=True, key="Gene_comm_oral"
        )
        fig_Gene_comm_oral = create_pie_chart(
            df_eleves,
            "Gene_comm_oral",
            "As-tu déjà été mal à l'aise lors de commentaires oraux devant la classe ?",
            chart_type="bar" if bar_Gene_comm_oral else "pie",
        )
        st.plotly_chart(fig_Gene_comm_oral, use_container_width=True)

    bar_Raison_gene_comm_oral = st.toggle(
        "Diagramme en barre", value=True, key="Raison_gene_comm_oral"
    )
    fig_Raison_gene_comm_oral = create_pie_chart_split(
        df_eleves,
        "Raison_gene_comm_oral",
        "Si tu as été mal à l'aise, pourquoi ? (Réponses multiples)",
        chart_type="bar" if bar_Raison_gene_comm_oral else "pie",
    )
    st.plotly_chart(fig_Raison_gene_comm_oral, use_container_width=True)

    liste_gene_autre = [
        "J'aime pas que cela est dit a voit haute",
        "remarques des autres camarades (suite à un 21/20)",
        "c'est un commentaire positif, mais ça me gêne d'avoir eu un compliment, seulement moi ou un petit groupe",
        "",
    ]
    st.write("'Si tu as été mal à l'aise, pourquoi ?' Autres réponses :")
    st.write(liste_gene_autre)

    bar_Impact_comm_oral = st.toggle(
        "Diagramme en barre", value=False, key="Impact_comm_oral"
    )
    fig_Impact_comm_oral = create_pie_chart_split(
        df_eleves,
        "Impact_comm_oral",
        "Est-ce que ces commentaires oraux t’aident à progresser ?",
        chart_type="bar" if bar_Impact_comm_oral else "pie",
    )
    st.plotly_chart(fig_Impact_comm_oral, use_container_width=True)

with tab4:
    st.header("Comparaison écrit / oral")
    col1, col2 = st.columns(2)
    with col1:
        bar2 = st.toggle("Diagramme en barre", value=False, key=2)
        fig_pref_ecrit_oral = create_pie_chart(
            df_eleves,
            "Pref_ecrit_oral",
            "Préfères-tu les commentaires oraux ou écrits ?",
            chart_type="bar" if bar2 else "pie",
        )
        st.plotly_chart(fig_pref_ecrit_oral, use_container_width=True)

    liste_autre = [
        "Les oraux m'angoisse",
        "Parce que c’est pareil",
        "je ne sais pas",
        "Car c'est clair ",
        "je trouve ça mieux ",
        "Car mes camarades ne peuvent pas voir ",
        "Je n’ai pas vraiment d’explications à donner, je préfère juste. ",
        "J’aime le fait que les professeurs prennent le temps de rédiger une appréciation : ils ont l’air plus impliqués dans la réussite des élèves ",
        "Cela dépend des commentaires ",
        "car c'est plus personnel",
    ]
    st.write(
        "'Préfères-tu les commentaires oraux ou écrits ? Pourquoi ?' : 10 groupes de réponses"
    )
    st.write(liste_autre)

    with col2:
        # bar2 = st.toggle("Diagramme en barre", value=True, key=2)
        fig_Pref_freq_oral = create_pie_chart(
            df_eleves,
            "Pref_freq_oral",
            "Est-ce que tu aimerais que tes enseignants te parlent plus souvent de ton travail à l’oral ?",
            # chart_type="bar" if bar2 else "pie",
        )
        st.plotly_chart(fig_Pref_freq_oral, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        bar3 = st.toggle(
            "Diagramme en barre",
            value=False,
        )
        fig_Besoin_comm_oral = create_pie_chart_split(
            df_eleves,
            "Besoin_comm_oral",
            "Qu’est-ce que tu aimerais entendre dans les commentaires oraux ? (réponses multiples)",
            chart_type="bar" if bar3 else "pie",
        )
        st.plotly_chart(fig_Besoin_comm_oral, use_container_width=True)

with tab5:
    st.subheader("Ressenti et motivation")
    col1, col2 = st.columns(2)
    with col1:
        bar_Motiv_comm = st.toggle("Diagramme en barre", value=False, key="Motiv_comm")
        fig_Motiv_comm = create_pie_chart_split(
            df_eleves,
            "Motiv_comm",
            "Comment les commentaires jouent-ils sur ta motivation à préparer au mieux la prochaine évaluation ?",
            chart_type="bar" if bar_Motiv_comm else "pie",
        )
        st.plotly_chart(fig_Motiv_comm, use_container_width=True)
    with col2:
        bar_Peur = st.toggle("Diagramme en barre", value=False, key="Peur")
        fig_Peur = create_pie_chart_split(
            df_eleves,
            "Peur",
            "As-tu déjà eu peur de poser une question sur un commentaire que tu ne comprenais pas ?",
            chart_type="bar" if bar_Peur else "pie",
        )
        st.plotly_chart(fig_Peur, use_container_width=True)

    st.write(
        "Comment les commentaires jouent-ils sur ta motivation à préparer au mieux la prochaine évaluation ? Pourquoi ?' : 3 groupes de réponses."
    )
    liste_motiv_text = [
        "car j'ai envie d'avoir un meilleur commentaire a chaque fois",
        "Cela me pousse à réussir",
        "Ne sais pas quoi repondre",
    ]
    st.write(liste_motiv_text)

    st.subheader("Méthodes de travail")
    bar_Methodes_travail = st.toggle(
        "Diagramme en barre", value=False, key="Methodes_travail"
    )
    fig_Methodes_travail = create_pie_chart_split(
        df_eleves,
        "Methodes_travail",
        "Que fais-tu en général pour préparer une évaluation ? (Réponses multiples)",
        chart_type="bar" if bar_Methodes_travail else "pie",
    )
    st.plotly_chart(fig_Methodes_travail, use_container_width=True)

    st.write("Quelques réponses au commentaire libre :")
    liste_comm_libre = [
        "ils sont gentils, et essaye vraiment de m'aider pour ma part",
        "Ils faut réussir à être moins sec quand certains parlent ",
        "respecter et avoir une facon de parler aux eleves cela ne les concernent pas tous ",
        "Motivé au lieu de rabaisser ",
    ]
    st.write(liste_comm_libre)
