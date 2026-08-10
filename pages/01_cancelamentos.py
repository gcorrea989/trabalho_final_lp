from pathlib import Path
import pandas as pd
import streamlit as st
from graficos import ( 
    grafico_taxa_cancelamento_categoria_preco, grafico_taxa_cancelamento_canal,
    grafico_cancelamento_antecedencia, grafico_reservas_mes_chegada
    )

from visualizacao import ARQUIVO, carregar_base, aplicar_filtros



st.set_page_config(

    page_title="Cancelamentos",

    layout="wide"

)

# Dados

df = carregar_base(ARQUIVO)
df = aplicar_filtros(df)

# =============================
# Página
# =============================

st.title("Análise de Cancelamentos")

st.markdown(
    """
        Esta página apresenta análises específicas sobre o comportamento
        dos cancelamentos das reservas.
    """
)

st.divider()
col1, col2 = st.columns(2)

with col1:
    grafico_taxa_cancelamento_categoria_preco(df)

with col2:
    grafico_taxa_cancelamento_canal(df)

st.divider()

col3, col4 = st.columns(2)

with col3:
    grafico_cancelamento_antecedencia(df)
with col4:
    grafico_reservas_mes_chegada(df)