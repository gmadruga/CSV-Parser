import glob
import os
import random
import string
import sys
import time
from io import StringIO
from multiprocessing.pool import ThreadPool
from pathlib import Path

import pandas as pd

#
#           PEGANDO ARQUIVOS DE UM DIRETORIO TESTE
#
filepath = Path('C:\\Users\\ianin\\Desktop\\IC\\PARSER\\testeParserCSV')
filesToParse = []
acceptedEncodings = ['utf-8','latin1']

# Preenchendo lista de filesToParse
for file in filepath.iterdir():
    if file.is_file() and file.suffix in ['.csv','.txt','.tsv']:
        print('NOVO ARQUIVO PARA SER PARSEADO: '+file.name)
        filesToParse.append(file.absolute())

# Abrindo os arquivos - Teste
for file in filesToParse:
    try:
        # OBS: O pd.read_csv deve acontecer na classe do parser!!
        df = pd.read_csv(StringIO(file.read_text(encoding='latin1')),sep=r';',engine='python',encoding='latin1',warn_bad_lines=False,
                              error_bad_lines=False,
                              keep_default_na=False,
                              dtype=str,skiprows=15,
                              header=None)
        # Skiprows depende do cabecalho do arquivo a ser aberto (ex: UnimedSeguros DCM = 15)
    except Exception as e:
        print('Nao eh possivel abrir o df: '+e)

