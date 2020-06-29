import glob
import os
import random
import string
import sys
import time
from io import StringIO
from multiprocessing.pool import ThreadPool
from pathlib import Path
from chalicelib.src.parserCSV.api import ParserAPI
from chalicelib.src.utils import ParserConfig,ParserResult
import pandas as pd
from chalicelib.src.loggerConfig import logger
#
#           PEGANDO ARQUIVOS DE UM DIRETORIO TESTE
#
filepath = Path('C://Users//Gabriel Madruga//Documents//ErrosParser//MerdaNow//NewParserCSV')
filesToParse = []

# Preenchendo lista de filesToParse
for file in filepath.iterdir():
    if file.is_file() and file.suffix in ['.csv','.txt','.tsv']:
        logger.debug('NOVO ARQUIVO PARA SER PARSEADO: '+file.name)
        filesToParse.append(file.absolute())

if len(filesToParse)>0:
    parserResults = ParserAPI(filesToParse).runAll()

    logger.debug('Thats all folks')
else:
    logger.error('NÃO HÁ ARQUIVOS A SEREM PARSEADOS!!')
    parserResults = ParserResult(config=None)
logger.fatal


