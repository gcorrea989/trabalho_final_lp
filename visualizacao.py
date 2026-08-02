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
