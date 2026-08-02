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


