from pathlib import Path
import pandas as pd
import streamlit as st

from graficos import grafico_canal_reserva, grafico_cancelamento_familias, grafico_distribuicao_precos, grafico_media_plano, grafico_reservas_mes, grafico_reservas_tipo_quarto, grafico_cancelamentos_quarto


BASE = Path(__file__).resolve().parent

ARQUIVO = (
    BASE
    / "dados_separados"
    / "07_dados_tratados"
    / "hotel_reservas.json"
)


# =========================================================
# Função para carregar a base de dados
# =========================================================

@st.cache_data
def carregar_base(arquivo):

    return pd.read_json(arquivo)

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
# Sidebar e Métricas
# ==========================================

def aplicar_filtros(df):

    st.sidebar.header("Filtros")

    anos = sorted(df["arrival_year"].unique())

    anos_selecionados = st.sidebar.multiselect(
        "Ano",
        options=anos,
        default=anos
    )

    quartos = sorted(df["room_type_reserved"].unique())

    quartos_selecionados = st.sidebar.multiselect(
        "Tipo de quarto",
        options=quartos,
        default=quartos
    )

    planos = sorted(df["type_of_meal_plan"].unique())

    planos_selecionados = st.sidebar.multiselect(
        "Plano de alimentação",
        options=planos,
        default=planos
    )

    canais = sorted(df["market_segment_type"].unique())

    canais_selecionados = st.sidebar.multiselect(
        "Canal de reserva",
        options=canais,
        default=canais
    )

    categorias = sorted(df["categoria_preco"].unique())

    categorias_selecionadas = st.sidebar.multiselect(
        "Categoria de preço",
        options=categorias,
        default=categorias
    )


    df_filtrado = df[
        (df["arrival_year"].isin(anos_selecionados))
        &
        (df["room_type_reserved"].isin(quartos_selecionados))
        &
        (df["type_of_meal_plan"].isin(planos_selecionados))
        &
        (df["market_segment_type"].isin(canais_selecionados))
        &
        (df["categoria_preco"].isin(categorias_selecionadas))
    ]

    return df_filtrado

def exibir_metricas(df):

    total_reservas = len(df)

    total_cancelamentos = len(
        df[
            df["booking_status"] == "Canceled"
        ]
    )

    diaria_media = df["avg_price_per_room"].mean()

    taxa_cancelamento = (
        (total_cancelamentos / total_reservas) * 100
        if total_reservas > 0
        else 0
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Reservas",
            value=f"{total_reservas:,}".replace(",", ".")
        )

    with col2:
        st.metric(
            label="Cancelamentos",
            value=f"{total_cancelamentos:,}".replace(",", ".")
        )

    with col3:
        st.metric(
            label="Diária média",
            value=f"R$ {diaria_media:.2f}"
        )

    with col4:
        st.metric(
            label="Taxa de cancelamento",
            value=f"{taxa_cancelamento:.1f}%"
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

    df = carregar_base(ARQUIVO)

    df = preparar_dados(df)

    df = aplicar_filtros(df)

    exibir_metricas(df)    

    col1, col2 = st.columns(2)

    with col1:
        grafico_reservas_tipo_quarto(df)

    with col2:
        grafico_distribuicao_precos(df)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        grafico_cancelamentos_quarto(df)

    with col2:
        grafico_media_plano(df)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        grafico_canal_reserva(df)

    with col2:
        grafico_reservas_mes(df)