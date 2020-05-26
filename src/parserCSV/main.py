import glob
import os
import random
import string
import sys
import time
from io import StringIO
from multiprocessing.pool import ThreadPool
from pathlib import Path
from src.parserCSV.api import ParserAPI

import pandas as pd

#
#           PEGANDO ARQUIVOS DE UM DIRETORIO TESTE
#
filepath = Path('C:\\Users\\ianin\\Desktop\\IC\\PARSER\\testeParserCSV')
filesToParse = []

# Preenchendo lista de filesToParse
for file in filepath.iterdir():
    if file.is_file() and file.suffix in ['.csv','.txt','.tsv']:
        print('NOVO ARQUIVO PARA SER PARSEADO: '+file.name)
        filesToParse.append(file.absolute())

api = ParserAPI(filesToParse).run()
