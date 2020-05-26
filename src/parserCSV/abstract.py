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

class AbstractPaser:
    def __init__(self,file,enc):
        #       INICIALIZANDO OS ATRIBUTOS
        self.file = file
        self.enc = enc
        self.outPutCsvFilePath = None
        self.hash = ''
        self.tipoDocumento = None
        self.final_df = None

    def checkDocumento(self):
        pass

    def finalizeDF(self):
        pass

    def parse(self):
        #           CRIA DIRETORIO E ARQUIVO DE SAIDA
        self.outPutCsvFilePath = Path(str(self.file.parent)+'\\'+str(self.file.stem))
        self.outPutFileName = Path(str(self.file.parent)+'\\'+str(self.file.stem)+'\\'+str(self.file.stem)+'.csv')
        print('Iniciando arquivo no diretorio de saida ' + str(self.outPutCsvFilePath))
        try:
            self.parseDocument()
            if not self.outPutCsvFilePath.exists():
                self.outPutCsvFilePath.mkdir()
            self.final_df.to_csv(self.outPutFileName,index=True, sep=r';')
            self.getTipoDocumento()
            print('Arquivo parseado com sucesso!!')
        except Exception as e:
            print('Erro ao parsear documento: '+e)