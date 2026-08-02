# fase 2 - Tratamento dos dados
from pathlib import Path
import pandas as pd
from icecream import ic

def carregar_dados(caminho_arquivo) -> pd.DataFrame:
    # Lê e transforma o arquivo em um dataframe
    if not caminho_arquivo.exists():
        raise Exception(f"Arquivo não encontrado: {caminho_arquivo}")

    return pd.read_json(caminho_arquivo)

def calcular_resumo_quartos(dados: pd.DataFrame) -> pd.DataFrame:
    # Calcula a quantidade de reservas 
    # e a média da diária por quarto
    resumo = (
        dados.groupby("room_type_reserved")
        .agg(
            quantidade_reservas=("Booking_ID", "count"),
            valor_medio_diaria=("avg_price_per_room", "mean")
        )
        .reset_index()
    )
    resumo["valor_medio_diaria"] =resumo["valor_medio_diaria"].round(2)

    return resumo

def classificar_preco(valor):
    if valor <= 100 :
        return "Econômico"
    
    if valor <= 200 :
        return "Intermediário"

    return "Premium"

def adicionar_categoria(dados: pd.DataFrame) -> pd.DataFrame:
    # Inclui a coluna de categoria de preços no DF
    dados["categoria_preco"] = (
        dados["avg_price_per_room"].apply(classificar_preco)
    )
    return dados

def adiciona_diferenca_media(dados: pd.DataFrame) -> pd.DataFrame:
    # Adiciona a diferença entre a média e a diária por tipo de quarto
    media_por_quarto = (
        dados.groupby("room_type_reserved")["avg_price_per_room"].transform("mean")
    )
    dados["diferenca_media_quarto"] = (
        dados["avg_price_per_room"] - media_por_quarto
    ).round(2)

    return dados

def tratar_dados(
        caminho_entrada,
        pasta_saida,
        nome_arquivo = "hotel_reservas.json"
) -> tuple[Path, pd.DataFrame]:
    dados = carregar_dados(caminho_entrada)
    resumo_quartos = calcular_resumo_quartos(dados)
    ic(resumo_quartos)
    dados = adicionar_categoria(dados)
    dados = adiciona_diferenca_media(dados)

    pasta_saida.mkdir(parents=True, exist_ok=True)

    caminho_saida = pasta_saida / nome_arquivo

    dados.to_json(
        caminho_saida,
        orient="records",
        indent=4,
        force_ascii=False,
    )

    return caminho_saida, resumo_quartos