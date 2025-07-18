import os
import sys

# Verifica se o arquivo esta sendo executado de forma compilada ou não e retorna a pasta raiz
def getExecutionPath():
    # Verifica se o script está compilado com PyInstaller
    if hasattr(sys, '_MEIPASS'):
        # Retorna o diretório do executável compilado
        return os.path.dirname(sys.executable)
    else:
        # Retorna o diretório absoluto do script
        return os.path.abspath('.')