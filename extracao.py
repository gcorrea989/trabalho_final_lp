"""
Fase 1 - Extração e consolidação dos dados
Os dados serão salvos em um novo diretório - dados_consolidados
""" 

from pathlib import Path
import pandas as pd
from icecream import ic

FORMATOS = {".json", ".txt"}

def localizar_arquivos(pasta_dados: Path):
    # lista arquivos das subpastas
    arquivos = []

    for caminho in pasta_dados.rglob("*"):
        if caminho.is_file() and caminho.suffix.lower() in FORMATOS:
            pastas_ignoradas = {"06_dados_consolidados", "07_dados_tratados"}
            if not pastas_ignoradas.intersection(caminho.parts):
                arquivos.append(caminho)

    return sorted(arquivos)


def ler_arquivos(caminho: Path) -> pd.DataFrame:
    # lê de acordo com o formato do arquivo
    extensao = caminho.suffix.lower()

    if extensao == ".json":
        return pd.read_json(caminho)

    if extensao == ".txt":
        return pd.read_csv(caminho, sep="|")

    raise ValueError(f"Formato não suportado para o arquivo: {caminho}")


def consolidar_dados(pasta_dados: Path, pasta_saida: Path, nome_arquivo="hotel_reservas.json"):
    # lê todos os arquivos e une os dados por ID. No final, salva um json na pasta destino

    arquivos = localizar_arquivos(pasta_dados)

    if not arquivos:
        return f"Nenhum arquivo JSOn ou TXT encontrado na pasta {pasta_dados}"

    tabelas = []

    for arquivo in arquivos:
        tabela = ler_arquivos(arquivo)

        if "Booking_ID" not in tabela.columns:
            raise ValueError(f"O arfquivo {arquivo.name} não possui coluna de ID")

        tabelas.append(tabela)

    # Unir os arquivos em uma úinica tabela
    dados_empilhados = pd.concat(
        tabelas, ignore_index=True, sort=False
    )

    # Agrupar pro ID
    dados_consolidados = (
        dados_empilhados.groupby("Booking_ID", as_index=False, sort=True)
        .first()
        .convert_dtypes()
    )
    ic(dados_consolidados.tail(4))

    pasta_saida.mkdir(parents=True, exist_ok=True)

    caminho_saida = pasta_saida / nome_arquivo

    # Salva o json na pasta de destino
    dados_consolidados.to_json(
        caminho_saida,
        orient="records",
        indent=4,
        force_ascii=False
    )

    return caminho_saida, len(dados_consolidados)