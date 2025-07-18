import time
import os
from dotenv import load_dotenv
from bot.extract import extrair_dados
from bot.mover import mover_service_csv
from bot.remove import removerarq
# from services.email_service import enviar_email  # opcional futuramente

# Setup
load_dotenv()                  # Carrega variáveis do .env

def main():
    try:
        removerarq()
        extrair_dados()
        mover_service_csv()
        print("RPA finalizado com sucesso!")

    except Exception as e:
        print(f"Erro na execução: {e}")
        # enviar_email(f"Erro na RPA {rpa}", str(e))  # se desejar envio de erro por e-mail
        time.sleep(10)
        exit(1)

if __name__ == '__main__':
    main()
