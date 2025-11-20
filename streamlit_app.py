import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


def create_pie_chart(
    df, column_name, title=None, color_scheme="Set2", height=500, chart_type="pie"
):
    """
    Crée un diagramme circulaire ou en barres pour une variable donnée (sans split).

    Parameters:
    -----------
    df : pandas.DataFrame
        Le dataframe contenant les données
    column_name : str
        Le nom de la colonne à analyser
    title : str, optional
        Le titre du graphique (par défaut: "Répartition par {column_name}")
    color_scheme : str, optional
        La palette de couleurs Plotly (par défaut: "Set2")
    height : int, optional
        La hauteur du graphique en pixels (par défaut: 500)
    chart_type : str, optional
        Type de graphique: 'pie' ou 'bar' (par défaut: 'pie')

    Returns:
    --------
    plotly.graph_objects.Figure
        Le graphique Plotly créé
    """

    value_counts = df[column_name].value_counts()

    if title is None:
        title = f"Répartition par {column_name.replace('_', ' ').lower()}"

    if chart_type == "pie":
        fig = px.pie(
            values=value_counts.values,
            names=value_counts.index,
            title=title,
            labels={"names": column_name.replace("_", " "), "values": "Nombre"},
            color_discrete_sequence=getattr(px.colors.qualitative, color_scheme),
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent+label",
            hovertemplate="<b>%{label}</b><br>Nombre: %{value}<br>Pourcentage: %{percent}<extra></extra>",
        )

        fig.update_layout(
            showlegend=True,
            legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1.02),
            margin=dict(r=250),
            height=height,
        )

    else:  # bar chart
        # Créer un dataframe pour le graphique
        df_plot = pd.DataFrame(
            {
                "Catégorie": value_counts.index,
                "Nombre": value_counts.values,
                "Pourcentage": (value_counts.values / value_counts.sum() * 100).round(
                    1
                ),
            }
        )

        fig = px.bar(
            df_plot,
            x="Catégorie",
            y="Nombre",
            title=title,
            text="Nombre",
            color="Catégorie",
            color_discrete_sequence=getattr(px.colors.qualitative, color_scheme),
        )

        fig.update_traces(
            texttemplate="%{text}",
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>Nombre: %{y}<br>Pourcentage: %{customdata:.1f}%<extra></extra>",
            customdata=df_plot["Pourcentage"],
        )

        fig.update_layout(
            showlegend=False,
            xaxis_title=column_name.replace("_", " "),
            yaxis_title="Nombre de réponses",
            xaxis_tickangle=-45,
            margin=dict(b=100),
            height=height,
        )

    return fig


def create_pie_chart_split(
    df,
    column_name,
    title=None,
    color_scheme="Set2",
    height=500,
    separator=",",
    chart_type="pie",
):
    """
    Crée un diagramme circulaire ou en barres pour une variable avec réponses multiples séparées.

    Parameters:
    -----------
    df : pandas.DataFrame
        Le dataframe contenant les données
    column_name : str
        Le nom de la colonne à analyser
    title : str, optional
        Le titre du graphique (par défaut: "Répartition par {column_name}")
    color_scheme : str, optional
        La palette de couleurs Plotly (par défaut: "Set2")
    height : int, optional
        La hauteur du graphique en pixels (par défaut: 500)
    separator : str, optional
        Le séparateur utilisé pour les réponses multiples (par défaut: ',')
    chart_type : str, optional
        Type de graphique: 'pie' ou 'bar' (par défaut: 'pie')

    Returns:
    --------
    plotly.graph_objects.Figure
        Le graphique Plotly créé
    """

    # Séparer les valeurs multiples et compter toutes les occurrences
    values_list = []
    for value in df[column_name].dropna():
        # Séparer par le séparateur et nettoyer les espaces
        split_values = [val.strip() for val in str(value).split(separator)]
        values_list.extend(split_values)

    # Compter les occurrences
    value_counts = pd.Series(values_list).value_counts()

    # Titre par défaut si non spécifié
    if title is None:
        title = f"Répartition par {column_name.replace('_', ' ').lower()} (réponses multiples)"

    # Créer le graphique selon le type choisi
    if chart_type == "pie":
        fig = px.pie(
            values=value_counts.values,
            names=value_counts.index,
            title=title,
            labels={"names": column_name.replace("_", " "), "values": "Nombre"},
            color_discrete_sequence=getattr(px.colors.qualitative, color_scheme),
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent+label",
            hovertemplate="<b>%{label}</b><br>Nombre: %{value}<br>Pourcentage: %{percent}<extra></extra>",
        )

        fig.update_layout(
            showlegend=True,
            legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1.02),
            margin=dict(r=250),
            height=height,
        )

    else:  # bar chart
        # Créer un dataframe pour le graphique
        df_plot = pd.DataFrame(
            {
                "Catégorie": value_counts.index,
                "Nombre": value_counts.values,
                "Pourcentage": (value_counts.values / len(values_list) * 100).round(1),
            }
        )

        fig = px.bar(
            df_plot,
            x="Catégorie",
            y="Nombre",
            title=title,
            text="Nombre",
            color="Catégorie",
            color_discrete_sequence=getattr(px.colors.qualitative, color_scheme),
        )

        fig.update_traces(
            texttemplate="%{text}",
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>Nombre: %{y}<br>Pourcentage: %{customdata:.1f}%<extra></extra>",
            customdata=df_plot["Pourcentage"],
        )

        fig.update_layout(
            showlegend=False,
            xaxis_title=column_name.replace("_", " "),
            yaxis_title="Nombre de réponses",
            xaxis_tickangle=-45,
            margin=dict(b=100),
            height=height,
        )

    # Ajouter une annotation pour le nombre total de réponses
    fig.add_annotation(
        text=f"Total: {len(values_list)} réponses (multiples possibles)",
        xref="paper",
        yref="paper",
        x=0,
        y=-0.15,
        showarrow=False,
        font=dict(size=12, color="gray"),
    )

    return fig


# import numpy as np
st.set_page_config(
    page_title="MotivIA - Analyse des questionnaires", page_icon="📊", layout="wide"
)

st.title("Analyse des questionnaires MotivIA")
st.subheader("Données de l'Académie d'Orléans-Tours.")

df_prof = pd.read_csv("Data/profs.csv", index_col=0)

# Sidebar - Filtres
st.sidebar.header("🔍 Filtres")

# Charger les données originales (avant filtrage)
df_original = pd.read_csv("Data/profs.csv", index_col=0)
df_prof = df_original.copy()

# Filtre par type d'établissement avec multiselect
if "Type_etab" in df_prof.columns:
    st.sidebar.subheader("Type d'établissement")

    # Obtenir tous les types uniques
    all_types = sorted(df_prof["Type_etab"].dropna().unique().tolist())

    # Options de sélection rapide
    col1, col2 = st.sidebar.columns(2)
    with col1:
        select_all_lycees = st.checkbox("Tous lycées", value=False)
        select_all_types = st.checkbox("Tous les établissements", value=False)
    with col2:
        select_all_colleges = st.checkbox("Tous collèges", value=False)

    # Définir les types selon les sélections
    lycee_types = [
        "LYCEE POLYVALENT",
        "LYCEE GENERAL",
        "LYCEE PROFESSIONNEL",
        "LYCEE GENERAL ET TECHNOLOGIQUE",
        "LPO LYCEE DES METIERS",
        "LP LYCEE DES METIERS",
    ]

    college_types = [
        "COLLEGE",
        "SECTION ENSEIGNT PROFESSIONNEL",  # Si c'est lié aux collèges
    ]

    # Déterminer les types par défaut
    default_types = all_types  # Par défaut, tous sont sélectionnés

    if select_all_lycees and select_all_colleges:
        # Si les deux sont cochés, sélectionner lycées + collèges
        default_types = [t for t in lycee_types + college_types if t in all_types]
    elif select_all_lycees:
        # Seulement les lycées
        default_types = [t for t in lycee_types if t in all_types]
    elif select_all_colleges:
        # Seulement les collèges
        default_types = [t for t in college_types if t in all_types]
    elif select_all_types:
        default_types = all_types

    # Cases à cocher pour chaque type
    selected_types = st.sidebar.multiselect(
        "Sélectionner les types:",
        options=all_types,
        default=default_types,
        help="Sélectionnez un ou plusieurs types d'établissement",
    )

    # Appliquer le filtre si des types sont sélectionnés
    if selected_types:
        df_prof = df_prof[df_prof["Type_etab"].isin(selected_types)]
    else:
        st.sidebar.warning("⚠️ Aucun type sélectionné")
        df_prof = df_prof.iloc[0:0]  # DataFrame vide

# Filtre par département avec multiselect
if "Departement" in df_prof.columns:
    st.sidebar.subheader("Département")

    # Obtenir les départements disponibles après le filtrage par type
    available_depts = sorted(df_prof["Departement"].dropna().unique().tolist())

    # Option pour tout sélectionner/désélectionner
    select_all_depts = st.sidebar.checkbox(
        "Sélectionner tous les départements", value=True
    )

    if select_all_depts:
        default_depts = available_depts
    else:
        default_depts = []

    # Cases à cocher pour chaque département
    selected_depts = st.sidebar.multiselect(
        "Sélectionner les départements:",
        options=available_depts,
        default=default_depts,
        help="Sélectionnez un ou plusieurs départements",
    )

    # Appliquer le filtre si des départements sont sélectionnés
    if selected_depts:
        df_prof = df_prof[df_prof["Departement"].isin(selected_depts)]
    else:
        st.sidebar.warning("⚠️ Aucun département sélectionné")
        df_prof = df_prof.iloc[0:0]  # DataFrame vide

# Afficher le nombre de résultats après filtrage
st.sidebar.markdown("---")
col1, col2 = st.sidebar.columns(2)
with col1:
    st.metric("Total filtré", len(df_prof))
with col2:
    st.metric("Total initial", len(df_original))

if len(df_prof) == 0:
    st.warning("Aucune donnée ne correspond aux filtres sélectionnés")

# with st.expander("Données 'brutes'"):
#     st.dataframe(df_prof)

tab1, tab2, tab3 = st.tabs(
    ["Données de contexte", "Commentaires écrits", "Commentaires oraux"]
)

with tab1:
    st.header("Données de contexte")

    st.metric(label="Nombre de réponses", value=len(df_prof))

    with st.expander("Carte"):
        st.map(
            df_prof,
            latitude="latitude",
            longitude="longitude",
        )

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

    col1, col2 = st.columns(2)

    with col1:
        # Répartition par matières
        # Compter les occurrences de chaque discipline
        discipline_counts = df_prof["Discipline"].value_counts()

        # Version 1 : Diagramme circulaire simple avec px.pie
        fig = px.pie(
            values=discipline_counts.values,
            names=discipline_counts.index,
            title="Répartition des enseignants par discipline",
            labels={"names": "Discipline", "values": "Nombre"},
        )

        fig.update_traces(
            hovertemplate="<b>%{label}</b><br>Nombre: %{value}<br>Pourcentage: %{percent}<extra></extra>",
        )

        fig.update_layout(
            showlegend=True,
            legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1.02),
            margin=dict(r=200),  # Marge à droite pour la légende
            height=500,
        )

        st.plotly_chart(fig, use_container_width=True)
    with col2:
        # Temps enseignement

        temps_counts = df_prof["Temps_enseignement"].value_counts()

        # Diagramme circulaire
        fig = px.pie(
            values=temps_counts.values,
            names=temps_counts.index,
            title="Répartition par temps d'enseignement",
            labels={"names": "Temps d'enseignement", "values": "Nombre"},
            color_discrete_sequence=px.colors.qualitative.Set2,
        )

        # Personnaliser l'affichage
        fig.update_traces(
            textposition="inside",
            textinfo="percent+label",
            hovertemplate="<b>%{label}</b><br>Nombre: %{value}<br>Pourcentage: %{percent}<extra></extra>",
        )

        fig.update_layout(
            showlegend=True,
            legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1.02),
            margin=dict(r=200),
            height=500,
        )

        st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        # Fréquence d'évaluation
        # Séparer les valeurs multiples et compter toutes les occurrences
        freq_eval_list = []
        for value in df_prof["Freq_eval"].dropna():
            # Séparer par virgule et nettoyer les espaces
            frequencies = [freq.strip() for freq in str(value).split(",")]
            freq_eval_list.extend(frequencies)

        # Compter les occurrences
        freq_eval_counts = pd.Series(freq_eval_list).value_counts()

        # Diagramme circulaire
        fig = px.pie(
            values=freq_eval_counts.values,
            names=freq_eval_counts.index,
            title="Fréquence d'évaluation des enseignants (réponses multiples comptées)",
            labels={"names": "Fréquence d'évaluation", "values": "Nombre"},
            color_discrete_sequence=px.colors.qualitative.Pastel,
        )

        # Personnaliser l'affichage
        fig.update_traces(
            textposition="inside",
            textinfo="percent+label",
            hovertemplate="<b>%{label}</b><br>Nombre: %{value}<br>Pourcentage: %{percent}<extra></extra>",
        )

        fig.update_layout(
            showlegend=True,
            legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1.02),
            margin=dict(r=250),
            height=500,
        )

        st.plotly_chart(fig, use_container_width=True)

        # Optionnel : afficher le nombre total de réponses
        st.caption(
            f"Note : Total de {len(freq_eval_list)} réponses (certains enseignants ont sélectionné plusieurs fréquences)"
        )

    with col2:
        fig1 = create_pie_chart(
            df_prof,
            "grille",
            "Usage d'une grille, des descripteurs ou des critères d'évaluation prédéfinis ",
        )
        st.plotly_chart(fig1, use_container_width=True)

    fig1 = create_pie_chart_split(
        df_prof,
        "Preoccupation_IA",
        "Principales préoccupations concernant l'usage de l'IA pour les commentaires ?",
        color_scheme="Pastel",
        chart_type="bar",
    )
    st.plotly_chart(fig1, use_container_width=True)

    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            fig1 = create_pie_chart(
                df_prof,
                "Freq_comm_ecrit",
                "Fréquence des commentaires écrits ",
            )
            st.plotly_chart(fig1, use_container_width=True)
        with col2:
            fig1 = create_pie_chart_split(
                df_prof,
                "Difficultes_comm_ecrit",
                "Difficulités lors des commentaires écrits ",
                chart_type="bar",
            )
            st.plotly_chart(fig1, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            fig1 = create_pie_chart(
                df_prof,
                "Trace_comm_ecrit",
                "Gardez-vous une trace de vos commentaires écrits ? ",
            )
            st.plotly_chart(fig1, use_container_width=True)
        with col2:
            fig1 = create_pie_chart(
                df_prof,
                "Lecture_comm_ecrit",
                "Lecture des commentaires par les élèves ",
            )
            st.plotly_chart(fig1, use_container_width=True)

    with tab3:

        #
        #

        col1, col2 = st.columns(2)
        with col1:
            fig1 = create_pie_chart(
                df_prof,
                "Freq_comm_oral",
                "Fréquence des commentaires à l'oral",
            )
            st.plotly_chart(fig1, use_container_width=True)
        with col2:
            fig1 = create_pie_chart_split(
                df_prof,
                "Moment_comm_oral",
                "A quel moments sont faits les commentaires à l'oral",
                chart_type="bar",
            )
            st.plotly_chart(fig1, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            fig1 = create_pie_chart_split(
                df_prof,
                "Objectif_comm_oral",
                "Objectif du commentaire oral",
            )
            st.plotly_chart(fig1, use_container_width=True)
        with col2:
            fig1 = create_pie_chart_split(
                df_prof,
                "Comprehension_comm_oral",
                "Compréhension du commentaire oral",
            )
            st.plotly_chart(fig1, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            fig1 = create_pie_chart_split(
                df_prof,
                "Questions_comm_oral",
                "Les élèves peuvent-ils facilement vous poser des questions sur vos commentaires ?",
                chart_type="bar",
            )
            st.plotly_chart(fig1, use_container_width=True)
        with col2:
            fig1 = create_pie_chart_split(
                df_prof,
                "Eleve_mal_a_l_aise",
                "Des élèves ont-ils déjà été mal à l'aise lorsque vous donniez un commentaire oral ?",
            )
            st.plotly_chart(fig1, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            fig1 = create_pie_chart_split(
                df_prof,
                "Avantages_comm_oral",
                "Avantages des commentaires oraux.",
            )
            st.plotly_chart(fig1, use_container_width=True)
        with col2:
            fig1 = create_pie_chart_split(
                df_prof,
                "Inconveniants_oral",
                "Inconvénients des commentaires oraux.",
            )
            st.plotly_chart(fig1, use_container_width=True)
