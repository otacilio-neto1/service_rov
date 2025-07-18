import os
import shutil

def mover_service_csv():
    # Caminho de origem (onde está o arquivo gerado)
    origem = os.path.join("archives", "service.parquet")

    # Caminho de destino (na rede)
    destino = r'\\repositoriodadosexcel.file.core.windows.net\servidor-rota\service_rov\service.parquet'

    try:
        if os.path.exists(origem):
            # shutil.move() move o arquivo (remove da origem)
            # Se quiser apenas copiar, use shutil.copy2()
            shutil.move(origem, destino)
            print(f"Arquivo movido com sucesso para: {destino}")
        else:
            print(f"Arquivo de origem não encontrado: {origem}")
    except Exception as e:
        print(f"Erro ao mover arquivo: {e}")

if __name__ == "__main__":
    mover_service_csv()
