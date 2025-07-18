import os

def removerarq():
    # Caminho da pasta onde ficam os arquivos baixados
    pasta_archives = os.path.join("archives")

    # Caminho do arquivo na rede (corrigido para usar barra invertida dupla)
    arquivo_rede = r'\\repositoriodadosexcel.file.core.windows.net\servidor-rota\service_rov\service.parquet'

    # Remover todos os arquivos da pasta archives
    try:
        if os.path.exists(pasta_archives):
            for nome_arquivo in os.listdir(pasta_archives):
                caminho_completo = os.path.join(pasta_archives, nome_arquivo)
                if os.path.isfile(caminho_completo):
                    os.remove(caminho_completo)
                    print(f"Arquivo removido da pasta archives: {caminho_completo}")
            print("Todos os arquivos foram removidos da pasta 'archives'.")
        else:
            print(f"Pasta não encontrada: {pasta_archives}")
    except Exception as e:
        print(f"Erro ao remover arquivos da pasta 'archives': {e}")

    # Remover arquivo da rede
    try:
        if os.path.exists(arquivo_rede):
            os.remove(arquivo_rede)
            print(f"Arquivo removido da rede: {arquivo_rede}")
        else:
            print(f"Arquivo na rede não encontrado, nada a remover: {arquivo_rede}")
    except Exception as e:
        print(f"Erro ao remover o arquivo da rede: {e}")

if __name__ == "__main__":
    removerarq()
