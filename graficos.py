import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
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