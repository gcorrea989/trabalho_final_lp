from pathlib import Path

from extracao import consolidar_dados
from tratamento import tratar_dados

PROJETO_DIR = Path(__file__).resolve().parent
DADOS_DIR = PROJETO_DIR / "dados_separados"
CONSOLIDADOS_DIR = DADOS_DIR / "06_dados_consolidados"
TRATADOS_DIR = DADOS_DIR / "07_dados_tratados"

def main():
    # Pipeline de extração e tratamento dos dados
    try:
        # Etapa 01
        arquivo_saida, quantidade = consolidar_dados(
            pasta_dados = DADOS_DIR,
            pasta_saida = CONSOLIDADOS_DIR,
            nome_arquivo="dados_consolidados.json"
        )

        print("Consolidação de dados concluída")
        print(f"Quantidade de reservas processadas: {quantidade}")
        print(f"Arquivo gerado: {arquivo_saida}")

        # Etapa 02
        arquivo_tratado, resumo_quartos = tratar_dados(
            caminho_entrada=arquivo_saida,
            pasta_saida=TRATADOS_DIR
        )

        print(f" 1 - Resumo por tipo de quarto:\n")
        print(resumo_quartos.to_string(index=False))

    except Exception as e:
        print(f"Ocorreram erros: {e}")

if __name__ == "__main__":
    main()