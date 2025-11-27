import pandas as pd
import plotly.express as px


def create_pie_chart(
    df, column_name, title=None, color_scheme="Set2", height=500, chart_type="pie"
):
    """
    Crée un diagramme circulaire ou en barres pour une variable donnée (sans split).
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
        total = value_counts.values.sum()
        df_plot = pd.DataFrame(
            {
                "Catégorie": value_counts.index,
                "Nombre": value_counts.values,
                "Pourcentage": (value_counts.values / total * 100).round(1),
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
            hover_data={
                "Pourcentage": True
            },  # Ajouter les pourcentages aux données de survol
        )

        fig.update_traces(
            texttemplate="%{text}",
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>Nombre: %{y}<br>Pourcentage: %{customdata[0]:.1f}%<extra></extra>",
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
    Crée un diagramme pour une variable avec réponses multiples séparées.
    """
    values_list = []
    for value in df[column_name].dropna():
        split_values = [val.strip() for val in str(value).split(separator)]
        values_list.extend(split_values)

    value_counts = pd.Series(values_list).value_counts()

    if title is None:
        title = f"Répartition par {column_name.replace('_', ' ').lower()} (réponses multiples)"

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
            hover_data={"Pourcentage": True},  # Ajout de hover_data
        )

        fig.update_traces(
            texttemplate="%{text}",
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>Nombre: %{y}<br>Pourcentage: %{customdata[0]:.1f}%<extra></extra>",
        )

        fig.update_layout(
            showlegend=False,
            xaxis_title=column_name.replace("_", " "),
            yaxis_title="Nombre de réponses",
            xaxis_tickangle=-45,
            margin=dict(b=100),
            height=height,
        )

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
