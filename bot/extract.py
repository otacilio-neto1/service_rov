from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import time
from datetime import datetime, timedelta
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import os
from .utils import getExecutionPath
import pandas as pd

# Calcular intervalo: últimos 15 dias até hoje
dataFinal = datetime.today().strftime('%d%m%Y')
dataInicial = (datetime.today() - timedelta(days=15)).strftime('%d%m%Y')


def consolidar_txt_em_parquet():
    """Lê todos os arquivos service*.txt e consolida em um único arquivo Parquet"""
    path = os.path.join(getExecutionPath(), "archives")
    # Somente os arquivos que realmente existem (11,12,13,16,17,18,19)
    arquivos = [os.path.join(path, f"service{i}.txt") for i in [11,12,13,16,17,18,19]]
    dfs = []

    for arquivo in arquivos:
        if os.path.isfile(arquivo):
            try:
                df = pd.read_csv(arquivo, sep=';', encoding='utf-8', dtype=str)
                # Remover colunas 'Unnamed' que podem aparecer
                df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
                dfs.append(df)
            except Exception as e:
                print(f"Erro ao ler {arquivo}: {e}")
        else:
            print(f"Arquivo não encontrado: {arquivo}")

    if dfs:
        df_final = pd.concat(dfs, ignore_index=True)
        parquet_path = os.path.join(path, "service.parquet")
        df_final.to_parquet(parquet_path, index=False)
        print(f"Arquivo Parquet gerado com sucesso: {parquet_path}")
    else:
        print("Nenhum arquivo txt encontrado para consolidar.")


def esperar_arquivo(arquivo, timeout=60):
    """Espera até timeout (segundos) o arquivo existir e ter tamanho > 0"""
    tempo_inicial = time.time()
    while True:
        if os.path.isfile(arquivo) and os.path.getsize(arquivo) > 0:
            return True
        if time.time() - tempo_inicial > timeout:
            return False
        time.sleep(1)

def extrair_dados():
    driver = None
    load_dotenv()

    while True:
        try:
            usuario = os.getenv("LOGIN")
            senha = os.getenv("PASSWORD")
            site = os.getenv("SITE")
            os.environ['GH_TOKEN'] = os.getenv("GH_TOKEN")

            path = getExecutionPath()
            local_dir = os.path.join(path, "archives")
            if not os.path.exists(local_dir):
                os.makedirs(local_dir)

            firefox_options = Options()
            firefox_options.headless = True
            firefox_options.set_preference("browser.download.dir", local_dir)
            firefox_options.set_preference("browser.download.folderList", 2)
            firefox_options.set_preference("browser.download.manager.showWhenStarting", False)
            firefox_options.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/plain, text/xml, application/octet-stream")

            service = FirefoxService(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service, options=firefox_options)
            wait = WebDriverWait(driver, 30)

            driver.get(site)
            driver.find_element(By.XPATH,'//*[@id="control_11"]').send_keys(usuario)
            driver.find_element(By.XPATH,'//*[@id="control_15"]').send_keys(senha)
            driver.find_element(By.XPATH,'//*[@id="botaoLogin"]').click()

            # Trocar para nova aba
            handles = driver.window_handles
            driver.switch_to.window(handles[1])

            time.sleep(10)
            driver.find_element(By.XPATH,'//*[@id="a9"]').click()
            driver.find_element(By.XPATH,'//*[@id="m60"]').click()
            driver.find_element(By.XPATH,'//*[@id="g181"]').click()
            driver.find_element(By.XPATH,'/html/body/div[4]/div[4]/table/tbody/tr[2]/td/a').click()

            time.sleep(6)
            driver.switch_to.frame('iframe_19')
            time.sleep(2)

            driver.find_element(By.XPATH, '//*[@id="chkTodos_14"]').click()
            time.sleep(1)
            driver.find_element(By.XPATH, '//*[@id="control1_15"]').send_keys(dataInicial)
            time.sleep(1)
            driver.find_element(By.XPATH, '//*[@id="control2_15"]').send_keys(dataFinal)
            time.sleep(1)
            driver.find_element(By.XPATH, '//*[@id="chkTodos_16"]').click()
            time.sleep(1)
            driver.find_element(By.XPATH, '//*[@id="chkTodos_17"]').click()
            time.sleep(1)

            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btn_19"]')))
            wait.until(EC.invisibility_of_element_located((By.ID, "zenMouseTrap")))
            driver.find_element(By.XPATH, '//*[@id="btn_19"]').click()
            element_combobox = driver.find_element(By.CLASS_NAME, 'comboboxTable')
            element_combobox.find_element(By.XPATH, f"//a[text()='Fechadas']").click()
            time.sleep(1)

            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btn_21"]')))
            wait.until(EC.invisibility_of_element_located((By.ID, "zenMouseTrap")))
            driver.find_element(By.XPATH, '//*[@id="btn_21"]').click()
            element_combobox = driver.find_element(By.CLASS_NAME, 'comboboxTable')
            element_combobox.find_element(By.XPATH, f"//a[text()='Ponto e Vírgula']").click()
            time.sleep(1)

            driver.find_element(By.XPATH, '//*[@id="control_23"]').click()

            while True:
                element = driver.find_element(By.XPATH, '//*[@id="control_26"]')
                if element.text == 'Processamento realizado com sucesso.':
                    time.sleep(5)
                    break

            # Trocar para tela de download
            handles = driver.window_handles
            driver.switch_to.window(handles[2])
            time.sleep(5)

            # Baixar arquivos service11.txt até service19.txt
            for i in range(1, 8):  # 7 arquivos
                xpath_download = f'/html/body/div[4]/table/tbody/tr[2]/td/div/table/tbody/tr/td[1]/div/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td[2]/div/table/tbody/tr[{i}]/td[3]/a'
                driver.find_element(By.XPATH, xpath_download).click()
                time.sleep(2)

            print("Aguardando arquivos serem baixados...")

            arquivos_espera = [os.path.join(local_dir, f"service{i}.txt") for i in [11,12,13,16,17,18,19]]

            todos_baixados = True
            for arquivo in arquivos_espera:
                if not esperar_arquivo(arquivo, timeout=60):
                    print(f"Tempo esgotado esperando o arquivo: {arquivo}")
                    todos_baixados = False

            if todos_baixados:
                print("Todos arquivos baixados com sucesso.")
            else:
                print("Alguns arquivos não foram baixados dentro do tempo esperado.")

            consolidar_txt_em_parquet()

            driver.quit()
            print('Extração concluída com sucesso.')
            break

        except Exception as e:
            print(f"Erro: {e}")
            time.sleep(10)
        finally:
            if driver:
                driver.quit()

if __name__ == "__main__":
    extrair_dados()
