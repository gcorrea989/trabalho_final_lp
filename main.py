from pathlib import Path

from extracao import consolidar_dados

PROJETO_DIR = Path(__file__).resolve().parent
DADOS_DIR = PROJETO_DIR / "dados_separados"
SAIDA_DIR = DADOS_DIR / "06_dados_consolidados"

def main():
    # Pipeline de extração e tratamento dos dados
    try:
        arquivo_saida, quantidade = consolidar_dados(
            pasta_dados = DADOS_DIR,
            pasta_saida = SAIDA_DIR,
        )

        print("Consolidação de dados concluída")
        print(f"Quantidade de reservas processadas: {quantidade}")
        print(f"Arquivo gerado: {arquivo_saida}")

    
    except Exception as e:
        print(f"Ocorreram erros: {e}")

if __name__ == "__main__":
    main()