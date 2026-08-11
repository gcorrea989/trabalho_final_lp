import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import plotly.express as px

def grafico_reservas_tipo_quarto(df):

    st.subheader("Quantidade de reservas por tipo de quarto")

    quantidade = (
        df["room_type_reserved"]
        .value_counts()
        .reset_index()
    )

    quantidade.columns = [
        "Tipo de quarto",
        "Quantidade"
    ]

    fig, ax = plt.subplots(figsize=(8, 5))

    sns.barplot(
        data=quantidade,
        x="Tipo de quarto",
        y="Quantidade",
        ax=ax
    )

    ax.set_xlabel("Tipo de quarto")
    ax.set_ylabel("Quantidade de reservas")
    ax.tick_params(axis="x", rotation=30)

    st.pyplot(fig)

def grafico_distribuicao_precos(df):

    st.subheader("Distribuição dos preços das diárias")

    fig = px.histogram(
        df,
        x="avg_price_per_room",
        color="categoria_preco",
        nbins=30,
        labels={
            "avg_price_per_room": "Preço da diária"
        }
    )

    fig.update_layout(
        xaxis_title="Preço da diária (R$)",
        yaxis_title="Quantidade de reservas"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

def grafico_cancelamentos_quarto(df):

    st.subheader("Cancelamentos por tipo de quarto")

    canceladas = (
        df[df["booking_status"] == "Canceled"]
        .groupby("room_type_reserved")
        .size()
        .reset_index(name="Quantidade")
    )

    fig = px.bar(
        canceladas,
        x="room_type_reserved",
        y="Quantidade",
        color="room_type_reserved"
    )

    fig.update_layout(
        xaxis_title="Tipo de quarto",
        yaxis_title="Cancelamentos",
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

def grafico_media_plano(df):

    st.subheader("Média da diária por plano de alimentação")

    medias = (
        df.groupby("type_of_meal_plan")["avg_price_per_room"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        medias,
        x="type_of_meal_plan",
        y="avg_price_per_room",
        color="type_of_meal_plan"
    )

    fig.update_layout(
        xaxis_title="Plano de alimentação",
        yaxis_title="Diária média (R$)",
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

def grafico_canal_reserva(df):

    st.subheader("Reservas por canal")

    canais = (
        df.groupby("market_segment_type")
        .size()
        .reset_index(name="Quantidade")
    )

    fig = px.pie(
        canais,
        names="market_segment_type",
        values="Quantidade"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

def grafico_reservas_mes(df):

    st.subheader("Reservas por mês")

    reservas = (

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

    reservas["MesAno"] = (
        reservas["Periodo"]
        .dt.strftime("%m/%Y")
    )

    fig = px.line(
        reservas,
        x="MesAno",
        y="Reservas",
        color="categoria_preco",
        markers=True
    )

    fig.update_layout(
        xaxis_title="Mês/Ano",
        yaxis_title="Reservas"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

def grafico_cancelamento_familias(df):

    st.subheader(
        "Cancelamentos de reservas com crianças"
    )

    familias = (

        df[
            df["booking_status"] == "Canceled"
        ]

        .groupby(
            [
                "Periodo",
                "no_of_children"
            ]
        )

        .size()

        .reset_index(name="Cancelamentos")

    )

    familias["MesAno"] = (
        familias["Periodo"]
        .dt.strftime("%m/%Y")
    )

    fig = px.line(

        familias,

        x="MesAno",

        y="Cancelamentos",

        color="no_of_children",

        markers=True

    )

    fig.update_layout(

        xaxis_title="Mês/Ano",

        yaxis_title="Quantidade",

        legend_title="Nº de crianças"

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# Graficos adicionais para página de cancelamento
def grafico_taxa_cancelamento_categoria_preco(df):

    st.subheader("Taxa de cancelamento por categoria de preço")

    dados = (
        df.groupby("categoria_preco")
        .agg(
            total_reservas=("booking_status", "size"),
            cancelamentos=("booking_status", lambda x: (x == "Canceled").sum())
        )
        .reset_index()
    )

    dados["taxa_cancelamento"] = (
        dados["cancelamentos"]
        / dados["total_reservas"]
        * 100
    ).round(2)

    fig = px.bar(
        dados,
        x="categoria_preco",
        y="taxa_cancelamento",
        text="taxa_cancelamento",
        color="categoria_preco",
        color_discrete_map={
            "Econômico": "#2E8B57",
            "Intermediário": "#F4A261",
            "Premium": "#E76F51"
        },
        labels={
            "categoria_preco": "Categoria de preço",
            "taxa_cancelamento": "Taxa de cancelamento (%)"
        },
    )

    fig.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside"
    )

    fig.update_layout(
        yaxis_range=[
            0,
            dados["taxa_cancelamento"].max() * 1.15
        ]
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

def grafico_taxa_cancelamento_canal(df):

    st.subheader("Taxa de cancelamento por canal de reserva")

    dados = (
        df.groupby("market_segment_type")
        .agg(
            total_reservas=("booking_status", "size"),
            cancelamentos=("booking_status", lambda x: (x == "Canceled").sum())
        )
        .reset_index()
    )

    dados["taxa_cancelamento"] = (
        dados["cancelamentos"]
        / dados["total_reservas"]
        * 100
    ).round(2)

    dados = dados.sort_values(
        "taxa_cancelamento",
        ascending=False
    )

    fig = px.bar(
        dados,
        x="market_segment_type",
        y="taxa_cancelamento",
        text="taxa_cancelamento",
        labels={
            "market_segment_type": "Canal de reserva",
            "taxa_cancelamento": "Taxa de cancelamento (%)"
        },

    )

    fig.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside"
    )

    fig.update_layout(
        yaxis_range=[
            0,
            dados["taxa_cancelamento"].max() * 1.15
        ]
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

def grafico_cancelamento_antecedencia(df):

    st.subheader("Taxa de cancelamento por antecedência da reserva")

    dados = df.copy()

    dados["faixa_antecedencia"] = pd.cut(
        dados["lead_time"],
        bins=[-1, 7, 30, 60, 90, 180, float("inf")],
        labels=[
            "0-7 dias",
            "Até 30 dias",
            "31–60 dias",
            "61–90 dias",
            "91–180 dias",
            "Mais de 180 dias"
        ]
    )

    resultado = (
        dados.groupby(
            "faixa_antecedencia",
            observed=False
        )
        .agg(
            total_reservas=("booking_status", "size"),
            cancelamentos=(
                "booking_status",
                lambda x: (x == "Canceled").sum()
            )
        )
        .reset_index()
    )

    resultado["taxa_cancelamento"] = (
        resultado["cancelamentos"]
        / resultado["total_reservas"]
        * 100
    )

    fig = px.bar(
        resultado,
        x="faixa_antecedencia",
        y="taxa_cancelamento",
        text="taxa_cancelamento",
        labels={
            "faixa_antecedencia": "Antecedência da reserva",
            "taxa_cancelamento": "Taxa de cancelamento (%)"
        },
    )

    fig.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside"
    )

    fig.update_layout(
        yaxis_title="Taxa de cancelamento (%)",
        xaxis_title="Antecedência da reserva",
        yaxis_range=[
            0,
            resultado["taxa_cancelamento"].max() * 1.15
        ]
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

def grafico_reservas_mes_chegada(df):

    st.subheader("Reservas por mês de chegada")

    reservas = (
        df.groupby("arrival_month")
        .size()
        .reset_index(name="reservas")
    )

    meses = {
        1: "Janeiro",
        2: "Fevereiro",
        3: "Março",
        4: "Abril",
        5: "Maio",
        6: "Junho",
        7: "Julho",
        8: "Agosto",
        9: "Setembro",
        10: "Outubro",
        11: "Novembro",
        12: "Dezembro"
    }

    reservas["mes"] = reservas["arrival_month"].map(meses)

    fig = px.line(
        reservas,
        x="mes",
        y="reservas",
        markers=True,
        labels={
            "mes": "Mês de chegada",
            "reservas": "Quantidade de reservas"
        },
        title="Reservas por mês de chegada"
    )

    fig.update_layout(
        xaxis={
            "categoryorder": "array",
            "categoryarray": list(meses.values())
        }
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )