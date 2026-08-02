from pathlib import Path

import pandas as pd

import streamlit as st

import matplotlib.pyplot as plt
import seaborn as sns

import plotly.express as px

BASE = Path(__file__).resolve().parent

ARQUIVO = (
    BASE
    / "dados_separados"
    / "07_dados_tratados"
    / "hotel_reservas.json"
)


# ==========================================================
# Função para carregar a base de dados
# =========================================================

@st.cache_data
def carregar_base():

    return pd.read_json(ARQUIVO)

def preparar_dados(df):

    df["data_chegada"] = pd.to_datetime(
        dict(
            year=df["arrival_year"],
            month=df["arrival_month"],
            day=df["arrival_date"]
        ),
        errors="coerce"
    )

    df = df.sort_values("data_chegada")

    df["Periodo"] = df["data_chegada"].dt.to_period("M")

    df["MesAno"] = df["Periodo"].dt.strftime("%m/%Y")

    return df

# ==========================================
# GRÁFICO RESERVAS - Seaborn
# ==========================================

def grafico_reservas(df):

    dados = (

        df

        .groupby(
            [
                "Periodo",
                "categoria_preco"
            ]
        )

        .size()

        .reset_index(name="Reservas")

    )

    dados["MesAno"] = (
        dados["Periodo"]
        .dt
        .strftime("%m/%Y")
    )

    fig, ax = plt.subplots(
        figsize=(14,6)
    )

    sns.lineplot(

        data=dados,

        x="MesAno",

        y="Reservas",

        hue="categoria_preco",

        marker="o",

        linewidth=2,

        ax=ax

    )

    ax.set_title(
        "Reservas por categoria de preço"
    )

    ax.set_xlabel("Mês/Ano")

    ax.set_ylabel("Quantidade")

    plt.xticks(rotation=45)

    plt.tight_layout()

    st.pyplot(fig)


# ==========================================
# GRÁFICO CANCELAMENTOS - Plotly
# ==========================================

def grafico_cancelamentos(df):

    canceladas = df[
        df["booking_status"] == "Canceled"
    ]

    dados = (

        canceladas

        .groupby(
            [
                "Periodo",
                "categoria_preco"
            ]
        )

        .size()

        .reset_index(name="Cancelamentos")

    )

    dados["MesAno"] = (
        dados["Periodo"]
        .dt
        .strftime("%m/%Y")
    )

    fig = px.line(

        dados,

        x="MesAno",

        y="Cancelamentos",

        color="categoria_preco",

        markers=True,

        title="Cancelamentos por categoria de preço"

    )

    fig.update_layout(

        xaxis_title="Mês/Ano",

        yaxis_title="Quantidade",

        legend_title="Categoria"

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ==========================================
# MAIN
# ==========================================

def main():

    st.set_page_config(

        page_title="Hotel Reservations",

        page_icon="🏨",

        layout="wide"

    )

    st.title("Dashboard - Hotel Reservations")

    st.markdown(
        "Análise das reservas utilizando Streamlit, Seaborn e Plotly."
    )

    df = carregar_base()

    df = preparar_dados(df)

    st.divider()

    st.subheader(
        "Reservas por categoria de preço"
    )

    grafico_reservas(df)

    st.divider()

    st.subheader(
        "Cancelamentos por categoria de preço"
    )

    grafico_cancelamentos(df)